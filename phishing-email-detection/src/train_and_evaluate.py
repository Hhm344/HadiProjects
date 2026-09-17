"""
train_and_evaluate.py
---------------------
CMPS354 - Applied Machine Learning for Cybersecurity
Phishing Email Detection in Banking Systems Using Naive Bayes Classifier

This script:
  1. Loads the banking phishing email dataset.
  2. Performs preprocessing (cleaning, vectorization, scaling).
  3. Splits the data into training and testing sets (80/20).
  4. Trains a Multinomial Naive Bayes classifier (proposed model).
  5. Trains baseline models for comparison: Logistic Regression and SVM.
  6. Reports Accuracy, Precision, Recall, F1-score, and confusion matrices.
  7. Saves all figures and a results summary to disk.
"""

import os
import re
import json
import string
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
)
from scipy.sparse import hstack, csr_matrix

# ----------------------- Paths -----------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "phishing_emails.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
RES_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

RANDOM_STATE = 42


# ----------------------- Preprocessing -----------------------
def clean_text(text: str) -> str:
    """Lowercase, strip URLs, punctuation, and extra whitespace."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " URL ", text)
    text = re.sub(r"\d+", " NUM ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["text"] = (df["subject"].fillna("") + " " + df["body"].fillna("")).apply(clean_text)
    return df


# ----------------------- Plot helpers -----------------------
def plot_class_distribution(df: pd.DataFrame, out_path: str) -> None:
    counts = df["label"].value_counts().sort_index()
    labels = ["Legitimate (0)", "Phishing (1)"]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, counts.values, color=["#2C7BB6", "#D7191C"])
    for b, v in zip(bars, counts.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 10, str(v), ha="center", fontweight="bold")
    ax.set_title("Class Distribution in the Banking Email Dataset")
    ax.set_ylabel("Number of Emails")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_confusion_matrix(cm: np.ndarray, classes, title: str, out_path: str) -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.set_title(title)
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"), ha="center",
                    color="white" if cm[i, j] > thresh else "black", fontweight="bold")
    ax.set_ylabel("True label")
    ax.set_xlabel("Predicted label")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_metric_comparison(results: dict, out_path: str) -> None:
    metrics = ["accuracy", "precision", "recall", "f1"]
    models = list(results.keys())
    x = np.arange(len(metrics))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#1B7837", "#5AAE61", "#9970AB", "#D6604D"]
    for i, m in enumerate(models):
        vals = [results[m][k] for k in metrics]
        ax.bar(x + i * width, vals, width, label=m, color=colors[i % len(colors)])
        for j, v in enumerate(vals):
            ax.text(x[j] + i * width, v + 0.01, f"{v:.2f}", ha="center", fontsize=8)
    ax.set_xticks(x + width)
    ax.set_xticklabels([m.capitalize() for m in metrics])
    ax.set_ylim(0, 1.1)
    ax.set_title("Performance Comparison of Models")
    ax.set_ylabel("Score")
    ax.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_roc_curves(roc_data: dict, out_path: str) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    for name, (fpr, tpr, roc_auc) in roc_data.items():
        ax.plot(fpr, tpr, label=f"{name} (AUC = {roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


# ----------------------- Main pipeline -----------------------
def evaluate_model(model, X_test, y_test, name):
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
    }
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n=== {name} ===")
    print(f"Accuracy : {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall   : {metrics['recall']:.4f}")
    print(f"F1-score : {metrics['f1']:.4f}")
    print("Classification report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))
    return y_pred, metrics, cm


def main():
    print("Loading dataset...")
    df = load_data(DATA_PATH)
    print(f"  Records: {len(df)}")
    print(f"  Phishing: {(df['label'] == 1).sum()}")
    print(f"  Legitimate: {(df['label'] == 0).sum()}")

    plot_class_distribution(df, os.path.join(FIG_DIR, "class_distribution.png"))

    # ----------------------- Feature engineering -----------------------
    print("\nVectorizing text...")
    # For Multinomial Naive Bayes we use raw counts (its natural input).
    from sklearn.feature_extraction.text import CountVectorizer
    count_vec = CountVectorizer(max_features=3000, ngram_range=(1, 2), min_df=2)
    X_text_count = count_vec.fit_transform(df["text"])

    # For LR/SVM we use TF-IDF (their natural input).
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), min_df=2)
    X_text_tfidf = vectorizer.fit_transform(df["text"])

    numeric_cols = ["num_links", "has_urgent_words", "has_money_words",
                    "has_suspicious_url", "num_misspellings"]
    X_num = df[numeric_cols].values.astype(float)
    X_num = (X_num - X_num.min(axis=0)) / (X_num.max(axis=0) - X_num.min(axis=0) + 1e-9)

    X_nb = hstack([X_text_count, csr_matrix(X_num)]).tocsr()
    X = hstack([X_text_tfidf, csr_matrix(X_num)]).tocsr()
    y = df["label"].values

    print(f"  NB feature matrix shape:    {X_nb.shape}")
    print(f"  TF-IDF feature matrix shape: {X.shape}")

    # ----------------------- Train / test split -----------------------
    indices = np.arange(len(y))
    idx_train, idx_test, y_train, y_test = train_test_split(
        indices, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    X_train_nb, X_test_nb = X_nb[idx_train], X_nb[idx_test]
    X_train, X_test = X[idx_train], X[idx_test]
    print(f"  Train: {len(idx_train)}  Test: {len(idx_test)}")

    # ----------------------- Proposed model: Multinomial NB -----------------------
    print("\nTraining proposed model: Multinomial Naive Bayes (CountVectorizer features)...")
    nb = MultinomialNB(alpha=0.1)
    nb.fit(X_train_nb, y_train)

    cv_scores = cross_val_score(nb, X_train_nb, y_train, cv=5, scoring="f1")
    print(f"  5-fold CV F1 mean = {cv_scores.mean():.4f}  std = {cv_scores.std():.4f}")

    y_pred_nb, m_nb, cm_nb = evaluate_model(nb, X_test_nb, y_test, "Multinomial Naive Bayes")
    plot_confusion_matrix(
        cm_nb, ["Legitimate", "Phishing"],
        "Confusion Matrix - Naive Bayes",
        os.path.join(FIG_DIR, "cm_naive_bayes.png"),
    )

    # ----------------------- Baseline: Logistic Regression -----------------------
    print("\nTraining baseline: Logistic Regression...")
    lr = LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)
    lr.fit(X_train, y_train)
    y_pred_lr, m_lr, cm_lr = evaluate_model(lr, X_test, y_test, "Logistic Regression")
    plot_confusion_matrix(
        cm_lr, ["Legitimate", "Phishing"],
        "Confusion Matrix - Logistic Regression",
        os.path.join(FIG_DIR, "cm_logistic_regression.png"),
    )

    # ----------------------- Baseline: Linear SVM -----------------------
    print("\nTraining baseline: Linear SVM...")
    svm = LinearSVC(random_state=RANDOM_STATE)
    svm.fit(X_train, y_train)
    y_pred_svm, m_svm, cm_svm = evaluate_model(svm, X_test, y_test, "Linear SVM")
    plot_confusion_matrix(
        cm_svm, ["Legitimate", "Phishing"],
        "Confusion Matrix - Linear SVM",
        os.path.join(FIG_DIR, "cm_linear_svm.png"),
    )

    # ----------------------- Baseline: Decision Tree -----------------------
    print("\nTraining baseline: Decision Tree...")
    dt = DecisionTreeClassifier(max_depth=20, random_state=RANDOM_STATE)
    dt.fit(X_train, y_train)
    y_pred_dt, m_dt, cm_dt = evaluate_model(dt, X_test, y_test, "Decision Tree")
    plot_confusion_matrix(
        cm_dt, ["Legitimate", "Phishing"],
        "Confusion Matrix - Decision Tree",
        os.path.join(FIG_DIR, "cm_decision_tree.png"),
    )

    # ----------------------- Comparison plot -----------------------
    results = {
        "Naive Bayes": m_nb,
        "Logistic Regression": m_lr,
        "Linear SVM": m_svm,
        "Decision Tree": m_dt,
    }
    plot_metric_comparison(results, os.path.join(FIG_DIR, "model_comparison.png"))

    # ----------------------- ROC curves -----------------------
    roc_data = {}
    nb_scores = nb.predict_proba(X_test_nb)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, nb_scores)
    roc_data["Naive Bayes"] = (fpr, tpr, auc(fpr, tpr))
    lr_scores = lr.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, lr_scores)
    roc_data["Logistic Regression"] = (fpr, tpr, auc(fpr, tpr))
    svm_scores = svm.decision_function(X_test)
    fpr, tpr, _ = roc_curve(y_test, svm_scores)
    roc_data["Linear SVM"] = (fpr, tpr, auc(fpr, tpr))
    dt_scores = dt.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, dt_scores)
    roc_data["Decision Tree"] = (fpr, tpr, auc(fpr, tpr))
    plot_roc_curves(roc_data, os.path.join(FIG_DIR, "roc_curves.png"))

    # ----------------------- Save results summary -----------------------
    summary = {
        "dataset_size": len(df),
        "num_features": X.shape[1],
        "train_size": X_train.shape[0],
        "test_size": X_test.shape[0],
        "cv_f1_mean": float(cv_scores.mean()),
        "cv_f1_std": float(cv_scores.std()),
        "results": {name: {k: float(v) for k, v in m.items()} for name, m in results.items()},
        "confusion_matrices": {
            "Naive Bayes": cm_nb.tolist(),
            "Logistic Regression": cm_lr.tolist(),
            "Linear SVM": cm_svm.tolist(),
            "Decision Tree": cm_dt.tolist(),
        },
        "roc_auc": {name: float(roc_data[name][2]) for name in roc_data},
    }
    with open(os.path.join(RES_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\nDone. All figures and metrics saved.")
    print(f"  Figures: {FIG_DIR}")
    print(f"  Summary: {os.path.join(RES_DIR, 'summary.json')}")


if __name__ == "__main__":
    main()
