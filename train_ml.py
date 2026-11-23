import logging

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline

from config import (
    MAX_FEATURES,
    ML_MODEL_PATH,
    MODEL_DIR,
    RANDOM_STATE,
)
from data_utils import load_dataset, split_dataset

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)


def build_pipeline():
    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                strip_accents="unicode",
                ngram_range=(1, 3),
                max_features=MAX_FEATURES,
                sublinear_tf=True,
                min_df=1
            )
        ),
        (
            "classifier",
            LogisticRegression(
                solver="lbfgs",
                max_iter=3000,
                class_weight="balanced",
                random_state=RANDOM_STATE,
                n_jobs=-1
            )
        )
    ])


def main():
    df = load_dataset()

    x_train, x_test, y_train, y_test = split_dataset(df)

    model = build_pipeline()

    model.fit(
        x_train,
        y_train
    )

    predictions = model.predict(x_test)

    score = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    logging.info(
        "ML Weighted F1 Score: %.4f",
        score
    )

    print(
        "\nClassification Report:\n"
    )

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        ML_MODEL_PATH,
        compress=3
    )

    logging.info(
        "ML model saved: %s",
        ML_MODEL_PATH
    )


if __name__ == "__main__":
    main()
