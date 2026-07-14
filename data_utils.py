import re

import pandas as pd
from sklearn.model_selection import train_test_split

from config import DATA_PATH, RANDOM_STATE, TEST_SIZE


def normalize_question(value: str) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def load_dataset(path=DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Create data/dataset.csv with question,label columns."
        )

    df = pd.read_csv(path)

    required_columns = {"question", "label"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}. Required: question,label"
        )

    df = df[["question", "label"]].dropna().copy()

    df["question"] = df["question"].apply(normalize_question)
    df["label"] = df["label"].astype(str).str.strip()

    df = df[
        (df["question"] != "") &
        (df["label"] != "")
    ].drop_duplicates()

    if len(df) < 10:
        raise ValueError("Dataset must contain at least 10 valid rows.")

    if df["label"].nunique() < 2:
        raise ValueError("Dataset must contain at least 2 subject labels.")

    if df["label"].value_counts().min() < 2:
        raise ValueError("Every label needs at least 2 examples.")

    return df


def split_dataset(df: pd.DataFrame):
    return train_test_split(
        df["question"],
        df["label"],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df["label"]
    )