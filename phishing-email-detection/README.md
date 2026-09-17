# Phishing Email Detection in Banking Systems Using Naive Bayes Classifier

**CMPS354 - Applied Machine Learning for Cybersecurity**

This repository contains the source code, dataset, and results for the project on
phishing email detection in banking systems using a Multinomial Naive Bayes classifier.

## Directory layout

```
project/
├── data/
│   └── phishing_emails.csv       # Generated banking phishing dataset (2600 emails)
├── figures/                      # All plots used in the report and presentation
├── results/
│   └── summary.json              # Final metrics for all four models
├── src/
│   ├── generate_dataset.py       # Reproduces the dataset
│   ├── train_and_evaluate.py     # Full training and evaluation pipeline
│   └── make_workflow_diagram.py  # Generates the system workflow diagram
├── requirements.txt
└── README.md
```

## How to run

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. (Re)generate the dataset:

   ```
   python src/generate_dataset.py
   ```

3. Train all models and produce the figures and metrics summary:

   ```
   python src/train_and_evaluate.py
   ```

4. Regenerate the workflow diagram (optional):

   ```
   python src/make_workflow_diagram.py
   ```

## Models trained

| Model                     | Role                  |
|---------------------------|-----------------------|
| Multinomial Naive Bayes   | Proposed model        |
| Logistic Regression       | Baseline comparison   |
| Linear Support Vector Machine | Baseline comparison |
| Decision Tree             | Baseline comparison   |

## Key results

| Metric    | NB     | LR     | SVM    | DT     |
|-----------|--------|--------|--------|--------|
| Accuracy  | 0.9712 | 0.9712 | 0.9712 | 0.9538 |
| Precision | 0.9780 | 0.9780 | 0.9780 | 0.9483 |
| Recall    | 0.9569 | 0.9569 | 0.9569 | 0.9483 |
| F1-score  | 0.9673 | 0.9673 | 0.9673 | 0.9483 |
| ROC AUC   | 0.9701 | 0.9667 | 0.9672 | 0.9409 |

Naive Bayes achieves the highest ROC AUC and matches the more complex linear
baselines on all classification metrics, at a fraction of the training cost.

## Dataset

The dataset combines hand-crafted phishing and legitimate banking email
templates with realistic variation in senders, URLs, urgency cues, and
annotation noise. The class distribution is approximately 55% legitimate
and 45% phishing, mirroring corpora used in published phishing research.
