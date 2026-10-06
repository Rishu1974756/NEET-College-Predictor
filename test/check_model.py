import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "neet_college_predictor_final.pkl"
)

print("Loading model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")
print("Model type:", type(model))
print("Model steps:", model.named_steps)
