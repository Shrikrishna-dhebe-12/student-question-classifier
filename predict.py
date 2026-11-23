import json
from functools import lru_cache

import joblib
import numpy as np
import tensorflow as tf

from config import (
    ML_MODEL_PATH,
    DL_MODEL_PATH,
    DL_METADATA_PATH
)
from data_utils import normalize_question


@lru_cache(maxsize=1)
def load_artifacts():
    model_files = (
        ML_MODEL_PATH,
        DL_MODEL_PATH,
        DL_METADATA_PATH
    )

    missing = [
        str(path)
        for path in model_files
        if not path.is_file()
    ]

    if missing:
        raise FileNotFoundError(
            "Models are missing. Run train_ml.py and train_dl.py first.\n"
            + "\n".join(missing)
        )

    ml_model = joblib.load(ML_MODEL_PATH)

    dl_model = tf.keras.models.load_model(
        DL_MODEL_PATH,
        compile=False
    )

    with open(
        DL_METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        classes = json.load(file)["classes"]

    return ml_model, dl_model, np.array(classes)


def predict_subject(question: str) -> dict:
    question = normalize_question(question)

    ml_model, dl_model, dl_classes = load_artifacts()

    ml_probs = ml_model.predict_proba([question])[0]
    ml_idx = int(np.argmax(ml_probs))

    dl_probs = dl_model(
        tf.constant([[question]], dtype=tf.string),
        training=False
    ).numpy()[0]

    dl_idx = int(np.argmax(dl_probs))

    ml_subject = ml_model.classes_[ml_idx]
    dl_subject = dl_classes[dl_idx]

    ml_conf = float(ml_probs[ml_idx])
    dl_conf = float(dl_probs[dl_idx])

    final_subject = (
        ml_subject
        if ml_conf >= dl_conf
        else dl_subject
    )

    final_confidence = max(
        ml_conf,
        dl_conf
    )

    return {
        "subject": str(final_subject),
        "confidence": round(final_confidence, 4),
        "dl_subject": str(dl_subject),
        "dl_confidence": round(dl_conf, 4),
        "models_agree": ml_subject == dl_subject
    }
