import requests
import json
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util
import argparse
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27021/")
db = client.openalex_ds
authors_col = db.authors_w_works
works_col = db.works


def search_openalex_by_name(name):
    """
    Searches for authors in the OpenAlex database by their name.

    Args:
        name (str): The name of the author to search for.

    Returns:
        list: A list of dictionaries containing authors details if matches are found.
        None: If no matches are found or if an error occurs.
    """
    url = f"https://api.openalex.org/authors?filter=display_name.search:{name.replace(' ', '%20')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["meta"]["count"] > 0:
            return data["results"]
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def get_most_similar_openalex_id(submission_embedding, openalex_results, similarity_model):
    """
    Finds the most similar OpenAlex ID based on the submission embedding.

    Args:
        submission_embedding (Tensor): The embedding of the submission.
        openalex_results (list): A list of dictionaries containing authors details.
        similarity_model: A pre-trained similarity model (e.g., SentenceTransformer)
                          used to compute embeddings and measure similarity.

    Returns:
        dict: The most similar OpenAlex author information.
    """
    best_score = -1
    best_match = None

    for person in openalex_results:
        try:
            topic_text = ' '.join([topic['display_name'] for topic in person['topics']])
            person_embedding = similarity_model.encode(topic_text, convert_to_tensor=True)
            similarity = util.cos_sim(submission_embedding, person_embedding).item()
            if similarity > best_score:
                best_score = similarity
                best_match = person
        except KeyError:
            continue

    return best_match


def find_openalex_id_of_reviewers(dataset, dataset_name, similarity_model):
    reviewers_info = {}
    for submission in tqdm(dataset):
        if dataset_name == 'sw':
            submission_text = submission['title'] + ' ' + submission['abstract']
        elif dataset_name == 'f1000':
            submission = submission[0]
            submission_text = submission['paper']['title'] + ' ' + submission['paper']['abstract']
        submission_embedding = similarity_model.encode(submission_text, convert_to_tensor=True)

        for reviewer in submission['reviews']:
            reviewer_name_field = 'reviewer' if dataset_name == 'sw' else 'name'
            reviewer_name = reviewer[reviewer_name_field]
            
            # Skip if the reviewer is anonymous or already processed
            if reviewer_name == 'Anonymous' or reviewer_name in reviewers_info:
                continue
            
            # remove the Dr. prefix from the reviewer name
            if reviewer_name.startswith('Dr. '):
                reviewer_name = reviewer_name[4:]
            
            # Search for the reviewer in OpenAlex
            openalex_results = search_openalex_by_name(reviewer_name)
            if openalex_results:
                if len(openalex_results) == 1:
                    reviewers_info[reviewer_name] = openalex_results[0]
                else:
                    best_match = get_most_similar_openalex_id(submission_embedding, openalex_results, similarity_model)
                    reviewers_info[reviewer_name] = best_match
            else:
                print(f"No OpenAlex match found for {reviewer_name}")
                reviewers_info[reviewer_name] = None

    return reviewers_info


def append_works_to_reviewers(reviewers_info : dict):
    author_ids = []
    ids_to_names = {}
    for reviewer_name, reviewer_info in reviewers_info.items():
        if reviewer_info is not None:
            author_ids.append(reviewer_info["id"])
            ids_to_names[reviewer_info["id"]] = reviewer_name
    
    print(f"Number of authors to process: {len(author_ids)}")

    # Fetch all author documents for the given IDs
    authors = authors_col.find({"_id": {"$in": author_ids}}, {"_id": 1, "known_works": 1})

    for author in tqdm(authors, desc="Processing authors", total=len(author_ids)):
        author_id = author["_id"]
        known_works_ids = [work['id'] for work in author["known_works"]]
        recent_works_ids = [work['id'] for work in author["known_works"] if work['year'] >= 2023]
        first_publication_year = min([work['year'] for work in author["known_works"]])
        
        # Fetch all works by ID in a single query
        works = works_col.find({"_id": {"$in": known_works_ids}}, {"title": 1, "abstract": 1})
        recent_works = works_col.find({"_id": {"$in": recent_works_ids}}, {"title": 1, "abstract": 1})

        # Extract title and abstract
        works_list = [{"title": work.get("title", ""), "abstract": work.get("abstract", "")} for work in works]
        recent_works_list = [{"title": work.get("title", ""), "abstract": work.get("abstract", "")} for work in recent_works]

        reviewers_info[ids_to_names[author_id]]["works"] = works_list
        reviewers_info[ids_to_names[author_id]]["recent_works"] = recent_works_list
        reviewers_info[ids_to_names[author_id]]["first_publication_year"] = first_publication_year

    return reviewers_info


def get_similarity_metrics_for_reviewers(dataset, dataset_name, reviewers_info, similarity_model):
    similarity_info = {}
    for submission in tqdm(dataset):
        if dataset_name == 'sw':
            submission_text = submission['title'] + ' ' + submission['abstract']
        elif dataset_name == 'f1000':
            submission = submission[0]
            submission_text = submission['paper']['title'] + ' ' + submission['paper']['abstract']
        submission_embedding = similarity_model.encode(submission_text, convert_to_tensor=True)
        
        for reviewer in submission['reviews']:
            reviewer_name_field = 'reviewer' if dataset_name == 'sw' else 'name'
            reviewer_name = reviewer[reviewer_name_field]
            # Skip if the reviewer is anonymous or not in the reviewers_info or has no works
            if (
                reviewer_name == 'Anonymous' or 
                reviewer_name not in reviewers_info or 
                reviewers_info[reviewer_name] is None or 
                'works' not in reviewers_info[reviewer_name]
            ):
                continue
            
            # remove the Dr. prefix from the reviewer name
            if reviewer_name.startswith('Dr. '):
                reviewer_name = reviewer_name[4:]
            
            max_similarity = 0
            avg_similarity = 0
            avg_recent_similarity = 0
            
            author_works = reviewers_info[reviewer_name]['works']
            author_works_embeddings = similarity_model.encode(
                [(work.get('title', '') or '') + ' ' + (work.get('abstract', '') or '') for work in author_works], convert_to_tensor=True
            )
            # Compute cosine similarity between submission and author's works
            similarities = util.cos_sim(submission_embedding, author_works_embeddings)
            max_similarity = similarities.max().item()
            avg_similarity = similarities.mean().item()
            
            author_recent_works = reviewers_info[reviewer_name]['recent_works']
            if len(author_recent_works) > 0:
                author_recent_works_embeddings = similarity_model.encode(
                    [(work.get('title', '') or '') + ' ' + (work.get('abstract', '') or '') for work in author_recent_works], convert_to_tensor=True
                )
                recent_similarities = util.cos_sim(submission_embedding, author_recent_works_embeddings)
                avg_recent_similarity = recent_similarities.mean().item()
            
            submission_id_field = 'id' if dataset_name == 'sw' else 'main'
            if submission[submission_id_field] not in similarity_info:
                similarity_info[submission[submission_id_field]] = {}
            similarity_info[submission[submission_id_field]][reviewer_name] = {
                "max_similarity": max_similarity,
                "avg_similarity": avg_similarity,
                "avg_recent_similarity": avg_recent_similarity
            }
    
    return similarity_info
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find OpenAlex IDs for reviewers.")
    parser.add_argument('--dataset', type=str, choices=['sw', 'f1000'], required=True,
                        help="Source of reviewers: 'sw' for Semantic Web, 'f1000' for F1000Research.")
    args = parser.parse_args()
    
    # Load the SPECTER model to compute embeddings for similarity
    specter_model = SentenceTransformer('allenai/specter').to('cuda')

    if args.dataset == 'sw':
        dataset_path = 'data/raw/semantic-web-journal.json'
        reviewers_info_path = 'data/processed/sw_reviewers_info.pkl'
        output_path = 'data/processed/sw_reviewers_similarity_info.pkl'
    elif args.dataset == 'f1000':
        dataset_path = 'data/raw/f1000research.json'
        reviewers_info_path = 'data/processed/f1000_reviewers_info.pkl'
        output_path = 'data/processed/f1000_reviewers_similarity_info.pkl'
        
    # Load the Semantic Web data from JSON file
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    
    reviewers_info = find_openalex_id_of_reviewers(dataset, args.dataset, specter_model)
    reviewers_info_with_works = append_works_to_reviewers(reviewers_info)
    
    # Save the reviewers info with works to a pickle file
    with open(reviewers_info_path, 'wb') as f:
        pickle.dump(reviewers_info_with_works, f)
    
    similarity_info = get_similarity_metrics_for_reviewers(dataset, args.dataset, reviewers_info_with_works, specter_model)
    
    # Save the processed data to a pickle file
    with open(output_path, 'wb') as f:
        pickle.dump(similarity_info, f)
        