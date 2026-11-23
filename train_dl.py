import json
import logging

import numpy as np
import tensorflow as tf
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder

from config import (
    DL_METADATA_PATH,
    DL_MODEL_PATH,
    MAX_FEATURES,
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

    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.transform(y_test)

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=MAX_FEATURES,
        output_mode="int",
        output_sequence_length=MAX_SEQUENCE_LENGTH
    )

    train_texts = x_train.astype(str).to_numpy()

    vectorizer.adapt(
        tf.data.Dataset.from_tensor_slices(train_texts).batch(256)
    )

    vocab_size = len(vectorizer.get_vocabulary())
    num_classes = len(label_encoder.classes_)

    model = tf.keras.Sequential([
        tf.keras.Input(shape=(1,), dtype=tf.string),

        vectorizer,

        tf.keras.layers.Embedding(
            input_dim=vocab_size,
            output_dim=128,
            mask_zero=True
        ),

        tf.keras.layers.GlobalAveragePooling1D(),

        tf.keras.layers.Dense(
            128,
            activation="relu"
        ),

        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(
            64,
            activation="relu"
        ),

        tf.keras.layers.Dense(
            num_classes,
            activation="softmax"
        )
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    train_ds = (
        tf.data.Dataset
        .from_tensor_slices(
            (
                tf.constant(
                    train_texts.reshape(-1, 1),
                    dtype=tf.string
                ),
                y_train
            )
        )
        .shuffle(
            len(train_texts),
            seed=RANDOM_STATE
        )
        .batch(32)
        .prefetch(tf.data.AUTOTUNE)
    )

    test_texts = x_test.astype(str).to_numpy()

    test_ds = (
        tf.data.Dataset
        .from_tensor_slices(
            (
                tf.constant(
                    test_texts.reshape(-1, 1),
                    dtype=tf.string
                ),
                y_test
            )
        )
        .batch(32)
        .prefetch(tf.data.AUTOTUNE)
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True
        )
    ]

    model.fit(
        train_ds,
        validation_data=test_ds,
        epochs=20,
        callbacks=callbacks,
        verbose=2
    )

    probabilities = model.predict(
        test_ds,
        verbose=0
    )

    predictions = np.argmax(
        probabilities,
        axis=1
    )

    score = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    logging.info(
        "DL Weighted F1 Score: %.4f",
        score
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    model.save(
        DL_MODEL_PATH,
        save_format="keras"
    )

    metadata = {
        "classes": label_encoder.classes_.tolist(),
        "vocab_size": vocab_size,
        "max_sequence_length": MAX_SEQUENCE_LENGTH
    }

    with open(
        DL_METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            metadata,
            file,
            indent=2
        )

    logging.info(
        "DL model saved: %s",
        DL_MODEL_PATH
    )

    logging.info(
        "DL metadata saved: %s",
        DL_METADATA_PATH
    )


if __name__ == "__main__":
    main()
