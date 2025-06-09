<!-- 
Title ##########
  Description of readme ##########
  ToC ##########
  Project tree ##########
Dataset ##########
  How to download the data ##########
  Dataset Files (optional) ##########
  Sample of the raw data ##########
Calculate the metrics
    How to run the code to calc Quantifiable metrics
      Path to the notebooks
      Sample of the output
      Qmetrics table
      Qmetrics corr fig
    Cacl metrics by LLM
      What models did we prompt (List)
      Prompt
      Sample of the output
Human Annotation
  How did we implement the interface of our annotation tool (flask, address of web app files)
  Screenshot of how the interface looks like
  Sample of the file we are saving (each person's record)
  2 figs that compare human-evaluated vs qmetrics and llms (the blue one and left corr map)
Predicting overall quality of a review
  Task definition
  Explain the traditional models (mlp 2 layer 100 N, rf …, svm …)
  Explain what is the source of the LLM-based overall quality (point to the “Cacl metrics by LLM” setion)
  Explain how did we finetune the LLAMA (You can ask Sonny)
  Fig (colored fig with ML models)
Abstract
  the whole abstract
Citation
  TBA
-->
# RottenReviews: Benchmarking Review Quality with Human and LLM-Based Judgments
This repository contains the code and data for the paper "**RottenReviews** : Benchmarking Review Quality with Human and LLM-Based Judgments". It should be noted that due to the size of the dataset, we are unable to provide the full dataset in this repository. Hence, the repository contains the codes for the sake of reproducibility and the data are available on Google Drive.

By following the instructions below, you can download the dataset and run files to either reproduce the results or use the dataset for your research.

## Table of Contents
- [Title](#title)
  - [Table of Contents](#table-of-content)
  - [Project Tree](#project-tree)
- [Dataset](#dataset)
  - [How to Download the Data](#how-to-download-the-data)
  - [Dataset Files Overview](#dataset-files-overview)
  - [Sample of the Raw Data](#sample-of-the-raw-data)
- [Calculate the Metrics](#calculate-the-metrics)
  - [How to Run the Code to Calculate Quantifiable Metrics](#how-to-run-the-code-to-calculate-quantifiable-metrics)
    - [Path to the Notebooks](#path-to-the-notebooks)
    - [Sample of the Output](#sample-of-the-output)
    - [Qmetrics Table](#qmetrics-table)
    - [Qmetrics Correlation Figure](#qmetrics-correlation-figure)
  - [Calculate Metrics by LLM](#calculate-metrics-by-llm)
    - [What Models Did We Prompt](#what-models-did-we-prompt)
    - [Prompt](#prompt)
    - [Sample of the Output](#sample-of-the-output-llm)
- [Human Annotation](#human-annotation)
  - [Interface Implementation](#interface-implementation)
  - [Screenshot of the Interface](#screenshot-of-the-interface)
  - [Sample Saved File](#sample-saved-file)
  - [Comparison Figures](#comparison-figures)
- [Predicting Overall Quality of a Review](#predicting-overall-quality-of-a-review)
  - [Task Definition](#task-definition)
  - [Traditional Models](#traditional-models)
  - [Source of LLM-Based Overall Quality](#source-of-llm-based-overall-quality)
  - [Finetuning LLAMA](#finetuning-llama)
  - [ML Models Figure](#ml-models-figure)
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
    ...
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

# Reproduce the result

## Feature Extraction and Analysis
To extract the defined features, start by using the notebooks located in the [feature_extraction](feature_extraction/) folder. There are four notebooks, each designed to extract features from the raw data of a specific venue. Within each notebook, you will find a section named `Process Raw Data`. This section processes the raw data, extracts all the defined features, and appends them to create a comprehensive dataframe. The final processed files for each venue can then be saved in the [data/processed](data/processed) folder.

Each notebook also includes two additional sections: `Random Sample 1000` and `LLM`. The `Random Sample 1000` section allows you to randomly sample 1000 papers and their reviews for processing using LLMs. If you wish to process all reviews for all papers using LLMs, you can skip the `Random Sample 1000` section and directly run the `LLM` section. 

Furthermore, you can customize the LLM model used by modifying the `llm_name` variable in the code. For this part, the `ollama` library was utilized.

After executing the notebooks in the [feature_extraction](feature_extraction/) folder, you can further analyze the results by plotting the distribution of each metric, as well as examining correlation maps and relationships between quantifiable metrics, human-annotated data, and LLM evaluations. To perform these analyses, run the notebooks in the [feature_analysis](feature_analysis/) folder. The resulting visualizations will be saved in the [feature_analysis/Figures](feature_analysis/Figures) directory.

You can find some of these results and viusalizations in the following table and figures:
<div align="center">

### Quantifiable Metric Statistics
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

<div align="center">






### Correlation Maps
  <img src="images/corr-human-vs-qmetric.png" alt="Alt text" height="320"/>
  <img src="images/corr-qmetric-vs-qmetric-f1000.png" alt="Alt text" height="320"/>
</div>
<p align="center">
  <em>Left: Kendall’s τ correlation between human-evaluated quality dimensions Y-axis and quantifiable metrics X-axis. Right: Correlation between quantifiable metrics on F1000.</em>
</p>


## Human Annotated Data Analysis


## Machine Learning Model Training and Comparison


<div align="center">
  <img src="images/kendall-tau-llms.png" alt="Alt text" height="320" style="transform: rotate(-90deg);"/>
  <img src="images/model-comparison.png" alt="Alt text" height="320"/>
</div>
<p align="center">
  <em>Left: Kendall’s τ correlation between human-evaluated and LLMs-evaluated quality dimensions. Right: Kendall’s τ correlation between human-evaluated and models-predicted Overall Quality of peer reviews.</em>
</p>


# Abstract
The quality of peer review plays a critical role in scientific publishing, yet remains poorly understood and challenging to evaluate at scale. In this work, we introduce *RottenReviews*, a benchmark designed to facilitate systematic assessment of review quality. *RottenReviews* comprises over 15,000 submissions from four distinct academic venues enriched with over 9,000 reviewer scholarly profiles and paper metadata. We define and compute a diverse set of quantifiable review-dependent and reviewer-dependent metrics, and compare them against structured assessments from large language models (LLMs) and expert human annotations. Our human-annotated subset includes over 700 paper–review pairs labeled across 13 explainable and conceptual dimensions of review quality. Our empirical findings reveal that LLMs, both zero-shot and fine-tuned, exhibit limited alignment with human expert evaluations of peer review quality. Surprisingly, simple interpretable models trained on quantifiable features outperform fine-tuned LLMs in predicting overall review quality.

# Citation
