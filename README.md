# RottenReviews: Benchmarking Review Quality with Human and LLM-Based Judgments

This repository contains the code and data for the paper "**RottenReviews** : Benchmarking Review Quality with Human and LLM-Based Judgments". It should be noted that due to the size of the dataset, we are unable to provide the full dataset in this repository. Hence, the repository contains the codes for the sake of reproducibility and the data are available on Google Drive.

By following the instructions below, you can download the dataset and run files to either reproduce the results or use the dataset for your research.

# Dataset

### Download the Dataset
To download the dataset from Google Drive, you can use the following commands:

Note: You need to install the gdown package to download the dataset.
```bash
pip install gdown
```

If you already have the gdown package installed, you can use the following commands to download the dataset:
```bash
cd RottenReviews/
gdown --folder https://drive.google.com/drive/folders/1Uqfyl5uBKBdZem9kQHkhNSPMPnwqJrYV?usp=sharing
```
### Dataset Files Overview
| Folder Name   | File Name               | File Size | Record Type | Number of Records | Format  |
|---------------|-------------------------|-----------|-------------|-------------------|---------|
| raw           | f1000research          | 497 MB    | Submission  | 4,509 Submission  | JSON    |
| raw           | semantic-web-journal   | 12.7 MB   | Submission  | 796 Submission    | JSON    |
| raw           | iclr-2024              | 148 MB    | Submission  | 7,262 Submission  | PKL     |
| raw           | neurips-2023           | 81.6 MB   | Submission  | 3,395 Submission  | PKL     |
|---------------|-------------------------|-----------|-------------|-------------------|---------|
| processed     | f1000research          | 41.2 MB   | Review      | 9,482 Review      | CSV     |
| processed     | semantic-web-journal   | 14.6 MB   | Review      | 2,337 Review      | CSV     |
| processed     | iclr-2024              | 147 MB    | Review      | 28,028 Review     | JSON    |
| processed     | neurips-2023           | 80.6 MB   | Review      | 15,175 Review     | JSON    |
| processed     | merged-200-papers      | 3.3 MB    | Submission  | 200 Submission    | JSON    |
| processed     | HA_ALL_qmetrics        | 3.3 MB    | Review      | 661 Review        | JSON    |
| processed     | HA_ALL_qwen            | 3.5 MB    | Review      | 661 Review        | JSON    |
| processed     | HA_ALL_llama           | 3.3 MB    | Review      | 661 Review        | JSON    |
| processed     | HA_ALL_phi4            | 46 KB     | Review      | 661 Review        | CSV     |
| processed     | HA_ALL_gpt             | 45 KB     | Review      | 661 Review        | CSV     |





# Statistics

<!-- <div align="center">

### Statistics of the `RottenReviews` Dataset

| Feature                  | NeurIPs | ICLR   | F1000 | SWJ  |
|--------------------------|--------:|-------:|------:|-----:|
| # Papers                 | 3,395   | 7,262  | 4,509 | 796  |
| # Reviews                | 15,175  | 28,028 | 9,482 | 2,337|
| Avg # Reviews per paper  | 4.47    | 3.86   | 2.10  | 2.93 |
| # Identified Reviewers   | N/A     | N/A    | 8,831 | 701  |

</div> -->

<div align="center">

### Statistics of Review-dependent (above) and Reviewer-dependent (below) Quantifiable Metrics

| Metric                         | NeurIPs | ICLR   | F1000  | SWJ     |
|-------------------------------|--------:|-------:|-------:|--------:|
| Review Length                 | 439.4   | 424.5  | 398.17 | 782.09  |
| # References                  | 1.25    | 1.42   | 0.29   | 2.29    |
| # Section-specific Comments   | 1.43    | 1.73   | 1.78   | 7.27    |
| Semantic Alignment            | 0.90    | 0.90   | 0.88   | 0.90    |
| Timeliness                    | 59.13   | 39.81  | 142.36 | 89.46   |
| Politeness                    | 0.84    | 0.81   | 0.83   | 0.75    |
| Readability                   | 38.02   | 37.65  | 36.60  | 43.86   |
| Lexical Diversity             | 0.77    | 0.77   | 0.76   | 0.76    |
| # Raised Questions            | 3.76    | 4.02   | 1.72   | 2.88    |
| Sentiment Polarity            | 0.11    | 0.11   | 0.15   | 0.10    |
| Hedging                       | 0.005   | 0.009  | 0.013  | 0.007   |
| **General Topic Alignment**   | N/A     | N/A    | 0.74   | 0.76    |
| **Recency-Based Topic Align.**| N/A     | N/A    | 0.65   | 0.64    |
| **In-depth Topical Alignment**| N/A     | N/A    | 0.87   | 0.88    |
| **Reviewer’s Citation**       | N/A     | N/A    | 4683.0 | 2476.08 |
| **Reviewer’s Academic Tenure**| N/A     | N/A    | 29.16  | 25.68   |

</div>



# Results Analysis
Kendall’s $\tau$ correlation between human-evaluated quality dimensions ($Y$-axis) and quantifiable metrics ($X$-axis).
<p align="center">
  <img src="images/corr-human-vs-qmetric.png" alt="Alt text" width="600"/>
</p>


Correlation between quantifiable metrics on F1000.
<p align="center">
  <img src="images/corr-qmetric-vs-qmetric-f1000.png" alt="Alt text" width="600"/>
</p>


Kendall’s $\tau$ correlation between human-evaluated  and LLMs-evaluated quality dimensions
<p align="center">
  <img src="images/kendall-tau-llms.png" alt="Alt text" width="600"/>
</p>


Kendall’s $\tau$ correlation between human-evaluated and models-predicted Overall Quality of peer reviews.
<p align="center">
  <img src="images/model-comparison.png" alt="Alt text" width="600"/>
</p>


# Abstract
The quality of peer review plays a critical role in scientific publishing, yet remains poorly understood and challenging to evaluate at scale. In this work, we introduce *RottenReviews*, a benchmark designed to facilitate systematic assessment of review quality. *RottenReviews* comprises over 15,000 submissions from four distinct academic venues enriched with over 9,000 reviewer scholarly profiles and paper metadata. We define and compute a diverse set of quantifiable review-dependent and reviewer-dependent metrics, and compare them against structured assessments from large language models (LLMs) and expert human annotations. Our human-annotated subset includes over 700 paper–review pairs labeled across 13 explainable and conceptual dimensions of review quality. Our empirical findings reveal that LLMs, both zero-shot and fine-tuned, exhibit limited alignment with human expert evaluations of peer review quality. Surprisingly, simple interpretable models trained on quantifiable features outperform fine-tuned LLMs in predicting overall review quality.


# Citation
TBD
