import logging

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline

from config import MAX_FEATURES, ML_MODEL_PATH, MODEL_DIR, RANDOM_STATE
from data_utils import load_dataset, split_dataset

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")


def main():
    df = load_dataset()

    x_train, x_test, y_train, y_test = split_dataset(df)

    ml_pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=MAX_FEATURES,
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=RANDOM_STATE
            )
        )
    ])

    ml_pipeline.fit(x_train, y_train)

    predictions = ml_pipeline.predict(x_test)

    score = f1_score(y_test, predictions, average="weighted")

    logging.info("ML Weighted F1 Score: %.3f", score)

    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions, zero_division=0))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(ml_pipeline, ML_MODEL_PATH)

    logging.info("ML model saved: %s", ML_MODEL_PATH)


if __name__ == "__main__":
    main()