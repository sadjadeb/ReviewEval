from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import random
from datetime import datetime
from collections import defaultdict


app = Flask(__name__)

INPUT_FILE = '../data/merged_200_papers.json'
OUTPUT_DIR = '../assessments_output/'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

LABEL_TO_INT_MAP = {
    "Outstanding": 5,
    "Strong": 4,
    "Adequate": 3,
    "Weak": 2,
    "Very weak": 1,
    "Absent/irrelevant": 0
}

# Load all review data
def load_reviews():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        review_lines = [json.loads(line.strip()) for line in f]

    papers = defaultdict(list)
    for entry in review_lines:
        papers[entry['paper_id']].append(entry)

    return papers  # dict: paper_id -> list of reviews

# Serve one paper randomly but ensuring balance
def get_balanced_paper(papers):
    # Count how many times each paper has been assessed
    paper_counts = {pid: 0 for pid in papers}

    for fname in os.listdir(OUTPUT_DIR):
        if not fname.endswith('.json'):
            continue
        try:
            with open(os.path.join(OUTPUT_DIR, fname), 'r') as f:
                entry = json.load(f)
                pid = entry.get('paper_id')
                pid = int(pid)
                if pid in paper_counts:
                    paper_counts[pid] += 1
        except Exception:
            continue  # skip corrupted files

    # Find paper_ids with the minimum count
    min_count = min(paper_counts.values())
    least_reviewed_papers = [pid for pid, count in paper_counts.items() if count == min_count]

    selected_pid = random.choice(least_reviewed_papers)
    return selected_pid, papers[selected_pid]


@app.route('/', methods=['GET'])
def index():
    all_papers = load_reviews()
    paper_id, reviews = get_balanced_paper(all_papers)

    paper_info = {
        "paper_id": paper_id,
        "title": reviews[0]["title"],
        "abstract": reviews[0]["abstract"],
        "authors": reviews[0]["authors"],
        "reviews": reviews
    }
    return render_template('index.html', paper=paper_info)


@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    from collections import Counter

    submissions = []
    total_assessments = 0

    for fname in os.listdir(OUTPUT_DIR):
        if not fname.endswith('.json'):
            continue
        try:
            with open(os.path.join(OUTPUT_DIR, fname), 'r') as f:
                entry = json.load(f)
                assessor = entry.get('assessor', 'unknown')
                submissions.append(assessor)
                total_assessments += 1
        except Exception:
            continue

    assessor_counts = Counter(submissions)
    sorted_leaderboard = sorted(assessor_counts.items(), key=lambda x: (-x[1], x[0]))

    return render_template('leaderboard.html', leaderboard=sorted_leaderboard, total_assessments=total_assessments)


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    assessor = form_data.get("assessor")
    paper_id = form_data.get("paper_id")

    if not assessor:
        return "Assessor name is required.", 400
    assessor = assessor.replace(' ', '-')  # sanitize assessor name

    # Get grouped reviews
    all_papers = load_reviews()
    reviews = all_papers[int(paper_id)]

    output = {
        "assessor": assessor,
        "paper_id": paper_id,
        "submitted_at": datetime.now().isoformat(),
        "metrics": {}
    }

    metric_names = [
        "Comprehensiveness", "Usage_of_Technical_Terms", "Factuality", "Sentiment_Polarity",
        "Politeness", "Vagueness", "Objectivity", "Fairness",
        "Actionability", "Constructiveness", "Relevance_Alignment", "Clarity_and_Readability", "Overall_Quality"
    ]

    for i, review in enumerate(reviews):
        reviewer_name = review['reviewer'].replace(' ', '-').replace('_', '-')  # sanitize reviewer name
        for j, metric in enumerate(metric_names):
            field_name = f"review_{i}_{j}"
            value = form_data.get(field_name)
            if value is None or value == "":
                return f"Missing value for review {i}, metric {metric}", 400
            
            # Convert descriptive label to numeric value if applicable
            if value in LABEL_TO_INT_MAP:
                value = LABEL_TO_INT_MAP[value]
            elif value.isdigit():
                value = int(value)
            
            output["metrics"][f"review_{reviewer_name}_{metric}"] = value
            
    # Save file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"{assessor}_{paper_id}_{timestamp}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
