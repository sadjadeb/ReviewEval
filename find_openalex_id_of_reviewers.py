import requests
import json
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util
import argparse


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


def find_openalex_id_of_sw_reviewers(dataset_path, output_path, similarity_model):
    """
    Finds and maps OpenAlex IDs for reviewers in a Semantic Web dataset.
    
    Args:
        dataset_path (str): Path to the JSON file containing the Semantic Web dataset.
                            The dataset should include submission titles, abstracts, 
                            and reviews with reviewer names.
        output_path (str): Path to save the output pickle file containing the mapping
                           of reviewer names to their OpenAlex IDs.
        similarity_model: A pre-trained similarity model (e.g., SentenceTransformer)
                          used to compute embeddings and measure similarity between
                          submission content and OpenAlex profiles.
    Returns:
        None: The function saves the processed data to the specified output file.
    """
    # Load the Semantic Web data from JSON file
    with open(dataset_path, 'r') as f:
        sw_data = json.load(f)

    # Process the data to find OpenAlex IDs for reviewers
    sw_reviewers_info = {}
    for submission in tqdm(sw_data):
        submission_text = submission['title'] + ' ' + submission['abstract']
        submission_embedding = similarity_model.encode(submission_text, convert_to_tensor=True)

        for reviewer in submission['reviews']:
            reviewer_name = reviewer['reviewer']
            
            # Skip if the reviewer is anonymous or already processed
            if reviewer_name == 'Anonymous' or reviewer_name in sw_reviewers_info:
                continue
            
            # Search for the reviewer in OpenAlex
            openalex_results = search_openalex_by_name(reviewer_name)
            if openalex_results:
                if len(openalex_results) == 1:
                    sw_reviewers_info[reviewer_name] = openalex_results[0]
                else:
                    best_score = -1
                    best_match = None

                    for person in openalex_results:
                        topic_text = ' '.join([topic['display_name'] for topic in person['topics']])
                        person_embedding = similarity_model.encode(topic_text, convert_to_tensor=True)
                        similarity = util.cos_sim(submission_embedding, person_embedding).item()
                        if similarity > best_score:
                            best_score = similarity
                            best_match = person

                    sw_reviewers_info[reviewer_name] = best_match
            else:
                print(f"No OpenAlex match found for {reviewer_name}")
                sw_reviewers_info[reviewer_name] = None

    # Save the processed data to a pickle file
    with open(output_path, 'wb') as f:
        pickle.dump(sw_reviewers_info, f)


def find_openalex_id_of_f1000_reviewers(dataset_path, output_path, similarity_model):
    """
    Finds and maps OpenAlex IDs for reviewers in a F1000 dataset.
    
    Args:
        dataset_path (str): Path to the JSON file containing the Semantic Web dataset.
                            The dataset should include submission titles, abstracts, 
                            and reviews with reviewer names.
        output_path (str): Path to save the output pickle file containing the mapping
                           of reviewer names to their OpenAlex IDs.
        similarity_model: A pre-trained similarity model (e.g., SentenceTransformer)
                          used to compute embeddings and measure similarity between
                          submission content and OpenAlex profiles.
    Returns:
        None: The function saves the processed data to the specified output file.
    """
    # Load the F1000 data from JSON file
    with open(dataset_path, 'r') as f:
        f1000_data = json.load(f)

    # Process the data to find OpenAlex IDs for reviewers
    f1000_reviewers_info = {}
    for submission in tqdm(f1000_data):
        submission = submission[0]
        submission_text = submission['paper']['title'] + ' ' + submission['paper']['abstract']
        submission_embedding = similarity_model.encode(submission_text, convert_to_tensor=True)

        for reviewer in submission['reviews']:
            reviewer_name = reviewer['name']
            
            # remove the Dr. prefix from the reviewer name
            if reviewer_name.startswith('Dr. '):
                reviewer_name = reviewer_name[4:]
            
            # Skip if the reviewer is anonymous or already processed
            if reviewer_name == 'Anonymous' or reviewer_name in f1000_reviewers_info:
                continue
            
            # Search for the reviewer in OpenAlex
            openalex_results = search_openalex_by_name(reviewer_name)
            if openalex_results:
                if len(openalex_results) == 1:
                    f1000_reviewers_info[reviewer_name] = openalex_results[0]
                else:
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
                            f1000_reviewers_info[reviewer_name] = openalex_results[0]

                    f1000_reviewers_info[reviewer_name] = best_match
            else:
                print(f"No OpenAlex match found for {reviewer_name}")
                f1000_reviewers_info[reviewer_name] = None

    # Save the processed data to a pickle file
    with open(output_path, 'wb') as f:
        pickle.dump(f1000_reviewers_info, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find OpenAlex IDs for reviewers.")
    parser.add_argument('--dataset', type=str, choices=['sw', 'f1000'], required=True,
                        help="Source of reviewers: 'sw' for Semantic Web, 'f1000' for F1000Research.")
    args = parser.parse_args()
    
    # Load the SPECTER model to compute embeddings for similarity
    specter_model = SentenceTransformer('allenai/specter').to('cuda')

    if args.dataset == 'sw':
        dataset_path = 'data/raw/semantic-web-journal.json'
        output_path = 'data/processed/sw_reviewers_info.pkl'
        find_openalex_id_of_sw_reviewers(dataset_path, output_path, specter_model)
    elif args.dataset == 'f1000':
        dataset_path = 'data/raw/f1000research.json'
        output_path = 'data/processed/f1000_reviewers_info.pkl'
        find_openalex_id_of_f1000_reviewers(dataset_path, output_path, specter_model)