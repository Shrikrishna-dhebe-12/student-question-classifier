import re

import pandas as pd
from sklearn.model_selection import train_test_split

from config import DATA_PATH, RANDOM_STATE, TEST_SIZE

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_question(value: str) -> str:
    return _WHITESPACE_RE.sub(
        " ",
        str(value).strip().lower()
    )


def load_dataset(path=DATA_PATH) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Create data/dataset.csv with question,label columns."
        )

    df = pd.read_csv(
        path,
        usecols=["question", "label"]
    ).dropna()

    df["question"] = (
        df["question"]
        .astype(str)
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df["label"] = (
        df["label"]
        .astype(str)
        .str.strip()
    )

    df = df.loc[
        (df["question"] != "") &
        (df["label"] != "")
    ].drop_duplicates(ignore_index=True)

    rows = len(df)

    if rows < 10:
        raise ValueError(
            "Dataset must contain at least 10 valid rows."
        )

    label_counts = df["label"].value_counts()

    if len(label_counts) < 2:
        raise ValueError(
            "Dataset must contain at least 2 subject labels."
        )

    if (label_counts < 2).any():
        raise ValueError(
            "Every label needs at least 2 examples."
        )

    return df


def split_dataset(df: pd.DataFrame):
    return train_test_split(
        df["question"],
        df["label"],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df["label"],
        shuffle=True
    )
