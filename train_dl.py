import json
import logging

import numpy as np
import tensorflow as tf
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder

from config import (
    DL_METADATA_PATH,
    DL_MODEL_PATH,
    MAX_SEQUENCE_LENGTH,
    MODEL_DIR,
    RANDOM_STATE,
)
from data_utils import load_dataset, split_dataset

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)


def main():
    tf.keras.utils.set_random_seed(RANDOM_STATE)

    df = load_dataset()

    x_train, x_test, y_train, y_test = split_dataset(df)

    label_encoder = LabelEncoder()

    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=5000,
        output_mode="int",
        output_sequence_length=MAX_SEQUENCE_LENGTH
    )

    train_text_tensor = tf.constant(
        x_train.astype(str).to_numpy(),
        dtype=tf.string
    )

    vectorizer.adapt(train_text_tensor)

    inputs = tf.keras.Input(
        shape=(1,),
        dtype=tf.string,
        name="question"
    )

    x = vectorizer(inputs)

    x = tf.keras.layers.Embedding(
        input_dim=len(vectorizer.get_vocabulary()),
        output_dim=64,
        mask_zero=True
    )(x)

    x = tf.keras.layers.GlobalAveragePooling1D()(x)

    x = tf.keras.layers.Dense(64, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.25)(x)

    x = tf.keras.layers.Dense(32, activation="relu")(x)

    outputs = tf.keras.layers.Dense(
        len(label_encoder.classes_),
        activation="softmax",
        name="subject"
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="student_question_classifier"
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    x_train_tensor = tf.constant(
        x_train.astype(str).to_numpy().reshape(-1, 1),
        dtype=tf.string
    )

    x_test_tensor = tf.constant(
        x_test.astype(str).to_numpy().reshape(-1, 1),
        dtype=tf.string
    )

    model.fit(
        x_train_tensor,
        y_train_encoded,
        validation_split=0.15,
        epochs=12,
        batch_size=16,
        verbose=2
    )

    probabilities = model.predict(
        x_test_tensor,
        verbose=0
    )

    predictions = probabilities.argmax(axis=1)

    score = f1_score(
        y_test_encoded,
        predictions,
        average="weighted"
    )

    logging.info("DL Weighted F1 Score: %.3f", score)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model.save(DL_MODEL_PATH)

    metadata = {
        "classes": label_encoder.classes_.tolist()
    }

    DL_METADATA_PATH.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    logging.info("DL model saved: %s", DL_MODEL_PATH)
    logging.info("DL metadata saved: %s", DL_METADATA_PATH)


if __name__ == "__main__":
    main()