from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "dataset.csv"
MODEL_DIR = BASE_DIR / "model"

ML_MODEL_PATH = MODEL_DIR / "ml.pkl"
DL_MODEL_PATH = MODEL_DIR / "dl.keras"
DL_METADATA_PATH = MODEL_DIR / "dl_metadata.json"

RANDOM_STATE = 42
TEST_SIZE = 0.20
MAX_FEATURES = 5000
MAX_SEQUENCE_LENGTH = 40