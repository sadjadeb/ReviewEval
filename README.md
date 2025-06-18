# RottenReviews: Benchmarking Review Quality with Human and LLM-Based Judgments
This repository contains the code and data for the paper "**RottenReviews** : Benchmarking Review Quality with Human and LLM-Based Judgments". It should be noted that due to the size of the dataset, we are unable to provide the full dataset in this repository. Hence, the repository contains the codes for the sake of reproducibility and the data are available on Google Drive.

By following the instructions below, you can download the dataset and run files to either reproduce the results or use the dataset for your research.

## Table of Contents
- [Title](#title)
  - [Table of Contents](#table-of-contents)
  - [Project Tree](#project-tree)
- [Dataset](#dataset)
  - [How to Download the Data](#how-to-download-the-data)
  - [Dataset Files Overview](#dataset-files-overview)
  - [Sample of the Raw Data](#sample-of-the-raw-data)
- [Calculate the Metrics](#calculate-the-metrics)
  - [Run notebooks](#run-notebooks)
  - [Quantifiable metrics](#quantifiable-metrics)
    - [Sample of the output](#sample-of-the-output)
    - [Quantifiable metrics table](#quantifiable-metrics-table)
    - [Quantifiable metrics correlation figure](#quantifiable-metrics-correlation-figure)
  - [Calculate metrics by LLM](#calculate-metrics-by-llm)
    - [Models](#models)
    - [Prompt](#prompt)
    - [Sample of the output](#sample-of-the-output)
- [Human Annotation](#human-annotation)
  - [Interface Implementation](#interface-implementation)
  - [Interface UI](#interface-ui)
  - [Record Sample](#record-sample)
  - [Comparison Figures](#comparison-figures)
- [Predicting Overall Quality of a Review](#predicting-overall-quality-of-a-review)
  - [Traditional Models](#traditional-models)
  - [LLM-Based Overall Quality](#llm-based-overall-quality)
  - [Fine-tuning LLaMA](#fine-tuning-llama)
- [Abstract](#abstract)
- [Citation](#citation)

## Project Tree
```
RottenReviews
├─ data
│  ├─ dataset-overview.txt
│  ├─ human-annotation-data/ (all the human annotated data would appear here)
│  ├─ processed/ (all the processed and cleaned data would appear here)
│  └─ raw/ (all the raw data crawled from different venues would appear here)
├─ feature_analysis
│  ├─ Figure/ (all the figures and visualizations would appear here)
│  ├─ stats-qmetrics-distributions-f1000-swj.ipynb
│  └─ stats-qmetrics-distributions-iclr-neurips-HA.ipynb
├─ feature_extraction
│  └─ process-neurips2023.ipynb
├─ human_annotation
│  ├─ HA-decision-vs-overall-quality.ipynb
│  ├─ interface/ (web application for gathering human annotation data)
│  ├─ llm-process-human-annotation-data.ipynb
│  ├─ llm-self-correlation-map.ipynb
│  └─ llm-vs-human-kendaltau.ipynb
├─ images/ (all the figures presented in README.md)
├─ predict_review_quality_score
│  ├─ Folds/ (train and test splitted data with 5 folds)
│  ├─ all_folds_data.csv
│  ├─ classical-ml-vs-llms.ipynb
│  ├─ human_llms_qmetrics.csv
│  ├─ human_vs_llm.csv
│  └─ llama3-finetune/
├─ requirements.txt
├─ README.md
└─ .gitignore
```

# Dataset
In this section, we provide detailed instructions on how to download the dataset, an overview of the dataset file organization, and a sample of the raw data.

## How to Download the Data
Note: You need to install the gdown package to download the dataset.
```bash
pip install gdown
```

If you already have the gdown package installed, you can use the following commands to download the dataset:
```bash
cd RottenReviews/
gdown --folder https://drive.google.com/drive/folders/1Uqfyl5uBKBdZem9kQHkhNSPMPnwqJrYV?usp=sharing
```

## Dataset Files Overview
| Folder Name   | File Name               | File Size | Record Type | Number of Records | Format  |
|---------------|-------------------------|-----------|-------------|-------------------|---------|
| raw           | f1000research          | 497 MB    | Submission  | 4,509  | JSON    |
| raw           | semantic-web-journal   | 12.7 MB   | Submission  | 796    | JSON    |
| raw           | iclr-2024              | 148 MB    | Submission  | 7,262  | PKL     |
| raw           | neurips-2023           | 81.6 MB   | Submission  | 3,395  | PKL     |
| processed     | f1000research          | 41.2 MB   | Review      | 9,482      | CSV     |
| processed     | semantic-web-journal   | 14.6 MB   | Review      | 2,337      | CSV     |
| processed     | iclr-2024              | 147 MB    | Review      | 28,028     | JSON    |
| processed     | neurips-2023           | 80.6 MB   | Review      | 15,175     | JSON    |
| processed     | merged-200-papers      | 3.3 MB    | Submission  | 200    | JSON    |

## Sample of the Raw Data
Here's a sample of raw data from Semantic Web Journal.
```json
{
  "id": "3654-4868",
  "date": "02/29/2024",
  "type": "Full Paper",
  "abstract": "Relation prediction in Knowledge...",
  "pdf_link": "https://www.semantic-web-journal...",
  "authors": [
    "Jiangtao Ma",
    "Yuke Ma",
    "Fan Zhang1",
    "..."
  ],
  "editor": "Guest Editors KG Gen from Text 2023",
  "status": [
    "Reviewed"
  ],
  "decision": "Major Revision",
  "reviews": [
    {
      "reviewer": "Anonymous",
      "date": "27/Aug/2024",
      "suggestion": "Minor Revision",
      "comment": "The paper proposed a new approach..."
    },
    {
      "reviewer": "Anonymous",
      "date": "03/Sep/2024",
      "suggestion": "Major Revision",
      "comment": "The subject on which the proposal..."
    }
  ],
  "version_prev": null,
  "version_next": null,
  "title": "HiHo: A Hierarchical and Homogenous Subgraph...",
  "rev_link": "https://www.semantic-web-journal..."
}
```


# Calculate the Metrics
In this work, we calculated two categories of metrics: (1) quantifiable metrics derived using off-the-shelf text processing methods, and (2) metrics obtained by prompting various LLM models to quantify specific aspects of review quality. Below, you will find instructions to reproduce the results, along with sample outputs and visualizations generated from these metrics.

## Run notebooks
To extract features, start by running the notebooks in the [feature_extraction](feature_extraction/) folder. Each notebook processes raw data from a specific venue, extracts defined features, and saves the processed files in the [data/processed](data/processed) folder. Both quantifiable metrics and LLM-based metrics are calculated within the same notebook. Each notebook includes a dedicated section named "LLM" that separates the code for these two categories of metrics.

#### Sample Run for Feature Extraction
```bash
cd feature_extraction/
jupyter nbconvert --to notebook --execute process-iclr2024.ipynb
```

After extracting features, analyze the results by running notebooks in the [feature_analysis](feature_analysis/) folder. These notebooks plot metric distributions, correlation maps, and relationships between quantifiable metrics, human annotations, and LLM evaluations. Visualizations are saved in the [feature_analysis/Figure](feature_analysis/Figure) directory.

#### Sample Run for Feature Analysis
```bash
cd feature_analysis/
jupyter nbconvert --to notebook --execute stats-qmetrics-distributions-iclr-neurips-HA.ipynb
```

## Quantifiable metrics
Quantifiable metrics derived using off-the-shelf text processing methods are measurable attributes extracted directly from the text of reviews and submissions. These metrics include features such as review length, lexical diversity, sentiment polarity, and readability, among others. By leveraging established natural language processing (NLP) techniques and tools, these metrics provide objective insights into various aspects of review quality, enabling systematic analysis and comparison across datasets.

### Sample of the output
```json
{
  "paper_id": "11-565",
  "reviewer": "Daniel A Nation",
  "review_date": "19 Jan 2023",
  "review_suggestion": "Approved",
  "length_words": 278,
  "title": "Assessing the role of...",
  "abstract": "Although observational studies...",
  "days_to_submit": 240,
  "review_text": "This is a meta-analysis of...",
  "mattr": 0.7832,
  "question_count": 1,
  "citation_count": 0,
  "sentiment_polarity": 0.1869,
  "politeness_score": 0.8376,
  "similarity_score": 0.9741,
  "reading_ease": 19.97,
  "hedgeing": 14.8,
  "explicit_reference": 1,
  "...": "...",
}
```

### Quantifiable metrics table
The table below summarizes the statistics of quantifiable metrics across four venues: NeurIPs, ICLR, F1000, and SWJ. Metrics such as review length, readability, sentiment polarity, and politeness vary significantly across venues, reflecting differences in review styles and submission characteristics. For instance, SWJ reviews are notably longer and more detailed, while NeurIPs and ICLR reviews exhibit higher lexical diversity and politeness scores. These variations highlight the diverse nature of peer review practices across academic venues.
<div align="center">

| Metric                         | Dependency | NeurIPs | ICLR   | F1000  | SWJ     |
|-------------------------------|------------|--------:|-------:|-------:|--------:|
| Review Length                 | Review     | 439.4   | 424.5  | 398.17 | 782.09  |
| # References                  | Review     | 1.25    | 1.42   | 0.29   | 2.29    |
| # Section-specific Comments   | Review     | 1.43    | 1.73   | 1.78   | 7.27    |
| Semantic Alignment            | Review     | 0.90    | 0.90   | 0.88   | 0.90    |
| Timeliness                    | Review     | 59.13   | 39.81  | 142.36 | 89.46   |
| Politeness                    | Review     | 0.84    | 0.81   | 0.83   | 0.75    |
| Readability                   | Review     | 38.02   | 37.65  | 36.60  | 43.86   |
| Lexical Diversity             | Review     | 0.77    | 0.77   | 0.76   | 0.76    |
| # Raised Questions            | Review     | 3.76    | 4.02   | 1.72   | 2.88    |
| Sentiment Polarity            | Review     | 0.11    | 0.11   | 0.15   | 0.10    |
| Hedging                       | Review     | 0.005   | 0.009  | 0.013  | 0.007   |
| General Topic Alignment       | Reviewer   | N/A     | N/A    | 0.74   | 0.76    |
| Recency-Based Topic Alignment | Reviewer   | N/A     | N/A    | 0.65   | 0.64    |
| In-depth Topical Alignment    | Reviewer   | N/A     | N/A    | 0.87   | 0.88    |
| Reviewer’s Citation           | Reviewer   | N/A     | N/A    | 4683.0 | 2476.08 |
| Reviewer’s Academic Tenure    | Reviewer   | N/A     | N/A    | 29.16  | 25.68   |
</div>


### Quantifiable metrics correlation figure
The figure below shows correlations between metrics like review length, sentiment polarity, readability, and politeness for the F1000 dataset.
<div align="center">
  <img src="images/corr-qmetric-vs-qmetric-f1000.png" alt="Alt text" height="600"/>
</div>
<p align="center">
  <em>Correlation between quantifiable metrics on F1000.</em>
</p>

## Calculate metrics by LLM
As mentioned in [Run notebooks](#run-notebooks), by running the notebooks, you can reproduce the results and prompt LLMs to evaluate the review in each aspect defined in the prompt. A sample of the prompt and the list of models used are available in the following subsections.

### Models
- **Qwen-3**: A state-of-the-art model optimized for natural language understanding and generation tasks.
- **Phi-4**: Known for its advanced reasoning capabilities and contextual comprehension.
- **GPT-4o**: OpenAI's latest iteration of the GPT series, designed for high-quality text generation.


### Prompt
We prompted all the models mentioned above with the same prompt to evaluate review quality. Below is the exact prompt used:

```markdown
# REVIEW-QUALITY JUDGE

## 0 — ROLE

You are **ReviewInspector-LLM**, a rigorous, impartial meta-reviewer.
Your goal is to assess the quality of a single peer-review against a predefined set of criteria and to provide precise, structured evaluations.

## 1 — INPUTS

Title: {title}  
Abstract: {abstract}  
Review: {review_text}  

## 2 — EVALUATION CRITERIA

Return **only** the scale value or label at right (no rationale text).

| #  | Criterion                    | Allowed scale / label                       | Description                                                                |
| -- | ---------------------------- | ------------------------------------------- | -------------------------------------------------------------------------- |
| 1  | **Comprehensiveness**        | integer **0-5**                             | Extent to which the review covers all key aspects of the paper.            |
| 2  | **Usage of Technical Terms** | integer **0-5**                             | Appropriateness and frequency of domain-specific vocabulary.               |
| 3  | **Factuality**               | **factual / partially factual / unfactual** | Accuracy of the statements made in the review.                             |
| 4  | **Sentiment Polarity**       | **negative / neutral / positive**           | Overall sentiment conveyed by the reviewer.                                |
| 5  | **Politeness**               | **polite / neutral / impolite**             | Tone and manner of the review language.                                    |
| 6  | **Vagueness**                | **none / low / moderate / high / extreme**  | Degree of ambiguity or lack of specificity in the review.                  |
| 7  | **Objectivity**              | integer **0-5**                             | Presence of unbiased, evidence-based commentary.                           |
| 8  | **Fairness**                 | integer **0-5**                             | Perceived impartiality and balance in judgments.                           |
| 9  | **Actionability**            | integer **0-5**                             | Helpfulness of the review in suggesting clear next steps.                  |
| 10 | **Constructiveness**         | integer **0-5**                             | Degree to which the review offers improvements rather than just criticism. |
| 11 | **Relevance Alignment**      | integer **0-5**                             | How well the review relates to the content and scope of the paper.         |
| 12 | **Clarity and Readability**  | integer **0-5**                             | Ease of understanding the review, including grammar and structure.         |
| 13 | **Overall Quality**          | integer **0-100**                           | Holistic evaluation of the review's usefulness and professionalism.        |

## 3 — SCORING GUIDELINES

For 0-5 scales:

* 5 = Outstanding  
* 4 = Strong  
* 3 = Adequate  
* 2 = Weak  
* 1 = Very weak  
* 0 = Absent/irrelevant  

## 4 — ANALYSIS & COMPUTATION (silent)

1. Read and understand the review in the context of the paper title and abstract.  
2. Extract quantitative and qualitative signals (e.g., term usage, factual consistency, tone, clarity).  
3. Map observations to the corresponding scoring scales.  

## 5 — OUTPUT FORMAT (strict)  
Return **exactly one** JSON block wrapped in the tag below — **no comments or extra text**.

```json
<review_assessment>
{{
  "paper_title": "{title}",
  "criteria": {{
    "Comprehensiveness":       ...,
    "Usage of Technical Terms":   ...,
    "Factuality":    ...,
    "Sentiment Polarity":      ...,
    "Politeness":  ...,
    "Vagueness":          ...,
    "Objectivity":             ...,
    "Fairness":         ...,
    "Actionability":        ...,
    "Constructiveness":    ...,
    "Relevance Alignment":    ...,
    "Clarity and Readability":    ...,
    "Relevance Alignment":    ...,
    "Overall Quality":     ...
  }},
}}
</review_assessment>
```

### Sample of the output
```json
{
  "paper_id": "123",
  "reviewer": "Reviewer_EGJf",
  "Comprehensiveness": 2,
  "Vagueness": "moderate",
  "Objectivity": 2,
  "Fairness": 3,
  "Actionability": 1,
  "Constructiveness": 2,
  "Relevance Alignment": 2,
  "Clarity and Readability": 3,
  "Usage of Technical Terms": 2,
  "Factuality": "partially factual",
  "Sentiment Polarity": "neutral",
  "Politeness": "polite",
  "Overall Quality": 40
}
```

# Human Annotation
In this study, we conducted a human evaluation of reviews from four academic venues. We randomly selected 50 papers from each venue, resulting in a dataset of 200 papers along with their associated reviews. This dataset comprises 661 reviews and 200 papers, providing a comprehensive basis for analyzing review quality. The processed dataset is available in `data/processed/merged-200-papers.json`.

## Interface Implementation
We implemented the interface to gather human annotation data using Flask and built a web application for this purpose. The source code for the web application is available in the `human_annotation/interface` directory, which contains all necessary files to deploy and run the annotation tool.

## Interface UI
Here's a screenshot of the user interface of the human data gathering web app:
<div align="center">
  <img src="images/UI-1.png" alt="User Interface Example" height="400"/>
</div>

<div align="center">
  <img src="images/UI-2.png" alt="User Interface Example" height="400"/>
</div>


## Record Sample
The recorded data from participants are stored in the `data/human-annotation-data` folder. Each file in this directory represents a single record, containing annotations provided by individual participants. These records include detailed evaluations of review quality across multiple dimensions, such as comprehensiveness, clarity, and fairness. Below is a sample of one record:

```json
{
    "paper_id": "170",
    "submitted_at": "2025-05-15T18:57:57.054760",
    "metrics": {
        "review_Sangeeta-Saha_Comprehensiveness": 3,
        "review_Sangeeta-Saha_Usage_of_Technical_Terms": 3,
        "review_Sangeeta-Saha_Factuality": "partially factual",
        "review_Sangeeta-Saha_Sentiment_Polarity": "negative",
        "review_Sangeeta-Saha_Politeness": "neutral",
        "review_Sangeeta-Saha_Vagueness": "moderate",
        "review_Sangeeta-Saha_Objectivity": 4,
        "review_Sangeeta-Saha_Fairness": 4,
        "review_Sangeeta-Saha_Actionability": 2,
        "review_Sangeeta-Saha_Constructiveness": 3,
        "review_Sangeeta-Saha_Relevance_Alignment": 4,
        "review_Sangeeta-Saha_Clarity_and_Readability": 1,
        "review_Sangeeta-Saha_Overall_Quality": 60,
        "review_J-H-Arias-Castro_Comprehensiveness": 3,
        "review_J-H-Arias-Castro_Usage_of_Technical_Terms": 3,
        "...": "..."
    }
}
```

## Comparison Figures
<div align="center">
  <img src="images/kendall-tau-llms.png" alt="Kendall’s τ correlation between human-evaluated and LLMs-evaluated quality dimensions" height="320" style="transform: rotate(-90deg);"/>
  <img src="images/corr-human-vs-qmetric.png" alt="Kendall’s τ correlation between human-evaluated quality dimensions Y-axis and quantifiable metrics X-axis" height="320"/>
</div>
<p align="center">
  <em>Left: Kendall’s τ correlation between human-evaluated and LLMs-evaluated quality dimensions. Right: Kendall’s τ correlation between human-evaluated quality dimensions Y-axis and quantifiable metrics X-axis.</em>
</p>

# Predicting Overall Quality of a Review
We aimed to predict the overall quality of a review using quantifiable metrics extracted in the previous steps, with labels for overall quality derived from human annotation data. All relevant codes for this section are available in the `predict_review_quality_score` directory.

## Traditional Models
Below is a list of traditional models used for predicting overall review quality, along with a brief explanation of their setup using `sklearn` library:

1. **Random Forest**:  
  A robust ensemble learning method that combines multiple decision trees to improve prediction accuracy.  
    - **Key Parameters**:  
      - `random_state=42`: Ensures reproducibility.  
      - `n_estimators=100`: Specifies the number of trees in the forest.

2. **Linear Regression**:  
  A simple and interpretable model that fits a linear relationship between input features and the target variable.  
    - **Key Parameters**:  
      - Default settings used for simplicity.

3. **Neural Network**:  
  A multi-layer perceptron (MLP) designed to capture complex non-linear relationships in the data.  
    - **Key Parameters**:  
      - `random_state=42`: Ensures reproducibility.  
      - `hidden_layer_sizes=(54, 108, 108, 54)`: Specifies the architecture with four layers and varying neuron counts.

## LLM-Based Overall Quality
Each LLM quantifies the overall quality of a review on a 0–100 scale, as defined in the [Prompt](#prompt) section. This score reflects the review's overall usefulness and professionalism across dimensions like comprehensiveness, clarity, and fairness. Using three base models and one fine-tuned model (as detailed in [Models](#models)), we compared LLM-generated scores with human annotations to evaluate alignment and reliability in assessing review quality.

## Fine-tuning LLAMA
All the necessary code to fine-tune LLaMA is available in the `predict_review_quality_score/llama3-finetune` directory. You can fine-tune the model using the following command:

```bash
cd /home/ali/RottenReviews/predict_review_quality_score/llama3-finetune/

python llm_eval.py --train_data_path /path/to/train_data.csv \
           --val_data_path /path/to/val_data.csv \
           --model_name_or_path llama-base \
           --output_dir /path/to/output_dir \
           --batch_size 16 \
           --learning_rate 5e-5 \
           --num_train_epochs 3 \
           --logging_dir /path/to/logging_dir
```

<div align="center">
  <img src="images/model-comparison.png" alt="Alt text" height="400"/>
</div>
<p align="center">
  <em>Kendall’s τ correlation between human-evaluated and models-predicted Overall Quality of peer reviews.</em>
</p>

# Abstract
The quality of peer review plays a critical role in scientific publishing, yet remains poorly understood and challenging to evaluate at scale. In this work, we introduce *RottenReviews*, a benchmark designed to facilitate systematic assessment of review quality. *RottenReviews* comprises over 15,000 submissions from four distinct academic venues enriched with over 9,000 reviewer scholarly profiles and paper metadata. We define and compute a diverse set of quantifiable review-dependent and reviewer-dependent metrics, and compare them against structured assessments from large language models (LLMs) and expert human annotations. Our human-annotated subset includes over 700 paper–review pairs labeled across 13 explainable and conceptual dimensions of review quality. Our empirical findings reveal that LLMs, both zero-shot and fine-tuned, exhibit limited alignment with human expert evaluations of peer review quality. Surprisingly, simple interpretable models trained on quantifiable features outperform fine-tuned LLMs in predicting overall review quality.

# Citation
TBA
