
import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "neet_college_predictor_final.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "neet_2026_phase1_with_state.csv"
)

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

df["phase"] = pd.to_numeric(df["phase"], errors="coerce")


def get_options():
    return {
        "quota": sorted(
            df["quota"].dropna().unique().tolist()
        ),
        "state": sorted(
            df["state"].dropna().unique().tolist()
        ),
        "course": sorted(
            df["course"].dropna().unique().tolist()
        ),
        "allottedCategory": sorted(
            df["allottedCategory"].dropna().unique().tolist()
        ),
        "candidateCategory": sorted(
            df["candidateCategory"].dropna().unique().tolist()
        ),
        "phase": sorted(
            df["phase"].dropna().unique().astype(int).tolist()
        )
    }


def predict_colleges(
    rank,
    quota=None,
    state=None,
    course=None,
    allottedCategory=None,
    candidateCategory=None,
    phase=1,
    top_n=10
):
    filtered = df.copy()

    if state:
        filtered = filtered[
            filtered["state"].astype(str).str.lower()
            == state.lower()
        ]

    if quota:
        filtered = filtered[
            filtered["quota"].astype(str).str.lower()
            == quota.lower()
        ]

    if course:
        filtered = filtered[
            filtered["course"].astype(str).str.lower()
            == course.lower()
        ]

    if allottedCategory:
        filtered = filtered[
            filtered["allottedCategory"].astype(str).str.lower()
            == allottedCategory.lower()
        ]

    if candidateCategory:
        filtered = filtered[
            filtered["candidateCategory"].astype(str).str.lower()
            == candidateCategory.lower()
        ]

    filtered = filtered[
        filtered["phase"] == phase
    ]

    if filtered.empty:
        return []

    feature_columns = [
        "quota",
        "institute",
        "state",
        "course",
        "allottedCategory",
        "candidateCategory",
        "phase"
    ]

    colleges = (
        filtered[feature_columns]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    colleges["predictedClosingRank"] = model.predict(
        colleges[feature_columns]
    )

    colleges = colleges[
        colleges["predictedClosingRank"] >= rank
    ]

    colleges = colleges.sort_values(
        "predictedClosingRank",
        ascending=True
    )

    colleges = colleges.head(top_n)

    return colleges[
        [
            "institute",
            "state",
            "course",
            "quota",
            "allottedCategory",
            "candidateCategory",
            "phase",
            "predictedClosingRank"
        ]
    ].round(0).to_dict(orient="records")