import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .predictor import predict_colleges, get_options


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


class PredictionRequest(BaseModel):
    rank: int
    candidateCategory: str
    quota: str | None = None
    state: str | None = None
    course: str | None = None
    allottedCategory: str | None = None
    phase: int = 1


@app.get("/api/health")
def health():
    return {
        "message": "NEET College Predictor API is running"
    }


@app.get("/api/options")
def options():
    return get_options()


@app.post("/api/predict")
def predict(data: PredictionRequest):
    results = predict_colleges(
        rank=data.rank,
        quota=data.quota,
        state=data.state,
        course=data.course,
        allottedCategory=data.allottedCategory,
        candidateCategory=data.candidateCategory,
        phase=data.phase,
        top_n=10
    )

    return {
        "success": True,
        "results": results
    }


app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)