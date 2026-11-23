import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from predict import load_artifacts, predict_subject
from answer_engine import generate_answer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

ANSWER_TEMPLATES = {
    "OS": (
        "Operating System manages processes, memory, files, CPU scheduling "
        "and hardware resources. FCFS, Round Robin and Priority Scheduling "
        "are common CPU scheduling concepts."
    ),
    "Python": (
        "Python is a high-level programming language. Lists store ordered "
        "mutable values, while dictionaries store data as key-value pairs."
    ),
    "CN": (
        "Computer Networks explains communication between devices. TCP gives "
        "reliable communication, while DNS converts domain names into IP addresses."
    ),
    "Java": (
        "Java is an object-oriented programming language. Inheritance allows "
        "one class to reuse another class, while polymorphism supports multiple behaviors."
    ),
}

FALLBACK_ANSWER = (
    "The subject was identified, but a detailed answer template is not yet "
    "available for this subject."
)


class PredictRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500
    )


class PredictResponse(BaseModel):
    subject: str
    confidence: float
    dl_subject: str
    dl_confidence: float
    models_agree: bool
    answer: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_artifacts()
        logging.info("Models loaded successfully")
    except FileNotFoundError as error:
        logging.warning("Models not found: %s", error)

    yield


app = FastAPI(
    title="AI Student Question Classifier",
    version="2.0.0",
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "StudentAI backend is running"
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    question = payload.question.strip()

    try:
        result = predict_subject(question)

        result["answer"] = generate_answer(
            question=question,
            subject=result["subject"],
            confidence=result["confidence"]
        )

        return result

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    except Exception as error:
        logging.exception("Prediction error")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        ) from error


@app.get("/subjects")
async def subjects():
    return {
        "subjects": tuple(ANSWER_TEMPLATES.keys())
    }
