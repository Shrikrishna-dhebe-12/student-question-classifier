import json
from functools import lru_cache

import joblib
import numpy as np
import tensorflow as tf

from config import DL_METADATA_PATH, DL_MODEL_PATH, ML_MODEL_PATH
from data_utils import normalize_question


@lru_cache(maxsize=1)
def load_artifacts():
    required_files = [
        ML_MODEL_PATH,
        DL_MODEL_PATH,
        DL_METADATA_PATH
    ]

    missing_files = [
        str(file)
        for file in required_files
        if not file.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Models are missing. Run train_ml.py and train_dl.py first.\n"
            + "\n".join(missing_files)
        )

    ml_model = joblib.load(ML_MODEL_PATH)

    dl_model = tf.keras.models.load_model(DL_MODEL_PATH)

    metadata = json.loads(
        DL_METADATA_PATH.read_text(encoding="utf-8")
    )

    return ml_model, dl_model, metadata["classes"]


def predict_subject(question: str) -> dict:
    clean_question = normalize_question(question)

    ml_model, dl_model, dl_classes = load_artifacts()

    ml_probabilities = ml_model.predict_proba([clean_question])[0]
    ml_index = int(np.argmax(ml_probabilities))

    # TensorFlow-compatible text input
    question_tensor = tf.constant(
        [[clean_question]],
        dtype=tf.string
    )

    dl_probabilities = dl_model.predict(
        question_tensor,
        verbose=0
    )[0]

    dl_index = int(np.argmax(dl_probabilities))

    ml_subject = str(ml_model.classes_[ml_index])
    dl_subject = str(dl_classes[dl_index])

    return {
        "subject": ml_subject,
        "confidence": round(float(ml_probabilities[ml_index]), 4),
        "dl_subject": dl_subject,
        "dl_confidence": round(float(dl_probabilities[dl_index]), 4),
        "models_agree": ml_subject == dl_subject
    }