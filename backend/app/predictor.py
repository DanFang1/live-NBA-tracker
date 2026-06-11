import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/pts_model.joblib")

model = joblib.load(MODEL_PATH)

FEATURES = [
    "last5_avg_pts",
    "last5_avg_ast",
    "last5_avg_reb",
    "last5_avg_min",
    "days_rest",
    "is_home",
    "avg_pts_vs_opponent",
    "opponent_encoded",
]

def predict_pts(features: dict) -> float:
    df = pd.DataFrame([features])[FEATURES]
    return float(model.predict(df)[0])
