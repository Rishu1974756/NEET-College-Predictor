from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .predictor import predict_colleges, get_options

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


class PredictionRequest(BaseModel):
    rank: int
    candidateCategory: str
    quota: str | None = None
    state: str | None = None
    course: str | None = None
    allottedCategory: str | None = None
    phase: int = 1


@app.get("/")
def home():
    return {
        "message": "NEET College Predictor API is running"
    }


@app.get("/options")
def options():
    return get_options()


@app.post("/predict")
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