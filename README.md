# NEET College Predictor

A machine learning powered web application that helps NEET aspirants find suitable medical colleges based on their **NEET rank, category, course, quota, state, and counselling preferences**.

> **Current Data:** NEET 2026 Round 1  
> **Round 2:** Releasing soon 🚀

---

## Overview

The NEET College Predictor processes NEET counselling data and uses a machine learning model to predict college closing ranks.

Users can enter their NEET details and preferences to receive a list of matching medical colleges.

### Current Inputs

- NEET Rank
- Candidate Category
- Quota
- State
- Course
- Allotted Category
- Counselling Phase

### Results

The application provides:

- Matching colleges
- College state
- Course
- Quota
- Allotted category
- Candidate category
- Counselling phase
- Predicted closing rank

---

## Features

### 🎯 Rank-Based College Prediction

Uses the student's NEET rank and selected preferences to find suitable colleges.

### 🔍 Multiple Filters

College predictions can be filtered using:

- State
- Quota
- Course
- Allotted Category
- Candidate Category
- Counselling Phase

### 🤖 Machine Learning

Uses a **Random Forest Regressor** to predict college closing ranks.

### 📊 Counselling Data Processing

The counselling data is processed, cleaned, validated and transformed into a machine-learning-ready dataset.

### 🌐 FastAPI Backend

The prediction system is connected to the frontend through a FastAPI REST API.

### 📱 Responsive Frontend

The application provides a responsive interface for interacting with the prediction system.

---

# How It Works

```text
Student
   │
   ▼
Enter NEET Details
   │
   ▼
Frontend
HTML + CSS + JavaScript
   │
   ▼
FastAPI Backend
   │
   ▼
Filter Counselling Data
   │
   ▼
Random Forest Model
   │
   ▼
Predicted Closing Rank
   │
   ▼
College Results
```

---

# Machine Learning

The machine learning pipeline was developed using **Google Colab**.

## Data Preparation

The NEET counselling dataset was processed through the following steps:

```text
Counselling PDF
      ↓
PDF to CSV
      ↓
CSV Validation
      ↓
Data Cleaning
      ↓
State Mapping
      ↓
Closing Rank Generation
      ↓
Feature Preparation
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Model Export
```

### Data Validation

The raw dataset was checked for:

- CSV structure
- Dataset shape
- Column names
- Missing values
- Duplicate records
- Unique values
- Suspicious records

Pandas was used for dataset inspection and analysis.

---

## PDF to CSV Processing

The counselling PDF was processed using `pdfplumber`.

The project includes:

```text
convert_pdf_to_csv.py
```

The script extracts structured counselling records from the PDF.

The extracted data contains:

```text
Rank
Quota
Institute
Course
Allotted Category
Candidate Category
Phase
```

---

## State Mapping

State information was added to the dataset using:

- State-name matching
- City-to-state mapping
- Institute location identification
- Manual mapping for unresolved institutes

The final dataset contains state information used by the prediction system.

---

## Closing Rank Generation

The counselling records were grouped using:

```python
group_columns = [
    "quota",
    "institute",
    "state",
    "course",
    "allottedCategory",
    "candidateCategory",
    "phase"
]
```

The closing rank was calculated using the maximum rank:

```python
closing_df = (
    df.groupby(
        group_columns,
        as_index=False
    )
    .agg(
        closingRank=("rank", "max")
    )
)
```

The resulting `closingRank` is used as the target variable for the machine learning model.

---

# Machine Learning Model

The final model uses a:

**Random Forest Regressor**

### Configuration

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Number of Trees | 100 |
| Random State | 42 |
| Train/Test Split | 80/20 |
| Parallel Processing | `n_jobs=-1` |

### Model Features

```text
Quota
Institute
State
Course
Allotted Category
Candidate Category
Phase
```

### Target

```text
Closing Rank
```

---

## Feature Encoding

Categorical features are processed using `OneHotEncoder`.

```python
categorical_columns = [
    "quota",
    "institute",
    "state",
    "course",
    "allottedCategory",
    "candidateCategory",
    "phase"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_columns
        )
    ]
)
```

The preprocessing and model are combined into a Scikit-learn Pipeline:

```python
model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "random_forest",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    )
])
```

---

# Model Training

The dataset was divided into training and testing sets using an 80/20 split.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

y_pred = model.predict(
    X_test
)
```

---

# Model Evaluation

The model was evaluated using:

- **MAE**
- **RMSE**
- **R² Score**

```python
mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)
```

---

# Model Validation

The trained model was saved using Joblib:

```python
joblib.dump(
    model,
    "neet_college_predictor_final.pkl",
    compress=3
)
```

The saved model was then loaded again and tested against the original model to verify that it produced the same prediction.

### Model

```text
model/
└── neet_college_predictor_final.pkl
```

### Dataset

```text
data/
└── neet_2026_phase1_with_state.csv
```

---

# Backend API

The backend is built using **Python and FastAPI**.

## `GET /`

Checks whether the API is running.

```json
{
    "message": "NEET College Predictor API is running"
}
```

## `GET /options`

Returns the available options used by the frontend:

```text
Quota
State
Course
Allotted Category
Candidate Category
Phase
```

## `POST /predict`

Receives student preferences and returns college predictions.

Example request:

```json
{
    "rank": 1000,
    "candidateCategory": "General",
    "quota": "All India",
    "state": "Andhra Pradesh",
    "course": "MBBS",
    "allottedCategory": "Open",
    "phase": 1
}
```

---

# Technology Stack

| Technology | Used For |
|---|---|
| HTML5 | Frontend structure |
| CSS3 | UI design and responsive layout |
| JavaScript | Frontend functionality and API communication |
| Python | Backend, data processing and machine learning |
| FastAPI | REST API |
| Pydantic | Request validation |
| Uvicorn | API server |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning |
| Random Forest | Closing-rank prediction |
| OneHotEncoder | Categorical encoding |
| ColumnTransformer | Data preprocessing |
| Joblib | Model saving and loading |
| pdfplumber | PDF data extraction |
| Git | Version control |
| GitHub | Source code management |
| Vercel | Deployment |

---

# Project Structure

```text
NEET-College-Predictor/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── ceiq-logo.png
│   └── landing.png
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── predictor.py
│
├── test/
│   ├── check_model.py
│   ├── predict.py
│   ├── predict_api.py
│   └── test_predictor.py
│
├── model/
│   └── neet_college_predictor_final.pkl
│
├── data/
│   ├── 2026_round1.pdf
│   └── neet_2026_phase1_with_state.csv
│
├── convert_pdf_to_csv.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Testing

A dedicated `test/` directory is included to validate the application.

### `check_model.py`

Checks whether the trained machine learning model loads correctly.

### `predict.py`

Tests the college prediction functionality.

### `predict_api.py`

Tests the API prediction workflow.

### `test_predictor.py`

Tests the prediction pipeline.

---

# Current Status

| Component | Status |
|---|---|
| NEET 2026 Round 1 Data | ✅ Completed |
| PDF Processing | ✅ Completed |
| CSV Validation | ✅ Completed |
| Data Cleaning | ✅ Completed |
| State Mapping | ✅ Completed |
| Closing Rank Generation | ✅ Completed |
| ML Model Training | ✅ Completed |
| Model Evaluation | ✅ Completed |
| Model Save/Reload Testing | ✅ Completed |
| FastAPI Backend | ✅ Completed |
| Frontend | ✅ Completed |
| College Prediction | ✅ Available |
| NEET 2026 Round 2 | 🚀 Releasing Soon |

---

# Disclaimer

The predicted closing ranks are generated using available counselling data and a machine learning model.

These predictions are intended for guidance only and **do not guarantee admission**.

Students should verify the latest official counselling information before making admission decisions.

---

# Author

**Rishu Kumar**
