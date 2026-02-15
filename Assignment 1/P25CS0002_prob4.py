"""
Problem 4: Sports vs Politics Classifier
P25CS0002 - Ashutosh

Simple implementation using libraries (scikit-learn).
- Feature representations: Bag of Words, TF-IDF, N-grams
- ML techniques compared: Naive Bayes, Logistic Regression, Linear SVM
"""

import csv
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


def load_dataset(csv_path: str):
    texts, labels = [], []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (row.get("text") or "").strip()
            label = (row.get("label") or "").strip().lower()
            if text and label in {"sport", "politics"}:
                texts.append(text)
                labels.append(label)
    return texts, labels


def build_experiments():
    # At least 3 ML techniques + requested feature types
    return [
        (
            "BoW + Naive Bayes",
            Pipeline([
                ("vec", CountVectorizer(stop_words="english", max_features=10000)),
                ("clf", MultinomialNB()),
            ]),
        ),
        (
            "TF-IDF + Logistic Regression",
            Pipeline([
                ("vec", TfidfVectorizer(stop_words="english", max_features=10000)),
                ("clf", LogisticRegression(max_iter=1200, random_state=42)),
            ]),
        ),
        (
            "N-grams(1,2) + Linear SVM",
            Pipeline([
                ("vec", TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=15000)),
                ("clf", LinearSVC(random_state=42)),
            ]),
        ),
    ]


def main():
    data_file = "sport_politics_balanced.csv"
    if not Path(data_file).exists():
        data_file = "sport_politics.csv"

    if not Path(data_file).exists():
        print("Dataset not found. Run: python extract_sport_politics.py --balanced")
        return

    texts, labels = load_dataset(data_file)
    if not texts:
        print("Dataset is empty or invalid.")
        return

    print(f"Loaded {len(texts)} documents from {data_file}")

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        stratify=labels,
        random_state=42,
    )

    experiments = build_experiments()
    results = []

    print("\nTraining and evaluating models...\n")
    for name, model in experiments:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        results.append((name, acc, model))
        print(f"{name:<35} accuracy = {acc:.4f}")

    results.sort(key=lambda x: x[1], reverse=True)
    best_name, best_acc, best_model = results[0]

    print("\n" + "=" * 60)
    print("Best model:", best_name)
    print(f"Best accuracy: {best_acc:.4f}")
    print("=" * 60)

    final_preds = best_model.predict(X_test)
    print("\nClassification report (best model):")
    print(classification_report(y_test, final_preds, digits=4))

    print("\nInteractive mode (press Enter on empty line to quit)")
    while True:
        user_text = input("Enter news text: ").strip()
        if not user_text:
            print("Exiting.")
            break
        pred = best_model.predict([user_text])[0]
        print("Prediction:", pred.upper())


if __name__ == "__main__":
    main()
