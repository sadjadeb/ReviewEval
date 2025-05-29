# RottenReviews : Benchmarking Review Quality with Human and LLM-Based Judgments

This repository contains the code and data for the paper "**RottenReviews** : Benchmarking Review Quality with Human and LLM-Based Judgments". It should be noted that due to the size of the dataset, we are unable to provide the full dataset in this repository. Hence, the repository contains the codes for the sake of reproducibility and the data are available on Google Drive.

By following the instructions below, you can download the dataset and run files to either reproduce the results or use the dataset for your research.

# Dataset
TBD

## Download the Dataset
TBD

## Dataset Files
TBD


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
