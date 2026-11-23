from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"

DATA_PATH = DATA_DIR / "dataset.csv"

ML_MODEL_PATH = MODEL_DIR / "ml.pkl"
DL_MODEL_PATH = MODEL_DIR / "dl.keras"
DL_METADATA_PATH = MODEL_DIR / "dl_metadata.json"

RANDOM_STATE = 42
TEST_SIZE = 0.2

MAX_FEATURES = 5000
MAX_SEQUENCE_LENGTH = 40

MODEL_PATHS = {
    "ml": ML_MODEL_PATH,
    "dl": DL_MODEL_PATH,
    "metadata": DL_METADATA_PATH,
}

TRAINING_CONFIG = {
    "random_state": RANDOM_STATE,
    "test_size": TEST_SIZE,
    "max_features": MAX_FEATURES,
    "max_sequence_length": MAX_SEQUENCE_LENGTH,
}
