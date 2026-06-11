import pandas as pd
import numpy as np
import os
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error


DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/raw/features.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "pts_model.joblib")

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

TARGET = "PTS"


def load_and_prepare(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["GAME_DATE"])
    df = df.sort_values("GAME_DATE").reset_index(drop=True)
    df["opponent_encoded"] = df["opponent"].astype("category").cat.codes
    df = df.dropna(subset=FEATURES + [TARGET])
    return df


def time_split(df: pd.DataFrame, test_fraction: float = 0.2):
    cutoff = int(len(df) * (1 - test_fraction))
    return df.iloc[:cutoff], df.iloc[cutoff:]


def train(df_train: pd.DataFrame) -> XGBRegressor:
    X = df_train[FEATURES]
    y = df_train[TARGET]

    model = XGBRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X, y)
    return model


def evaluate(model: XGBRegressor, df_test: pd.DataFrame) -> float:
    X = df_test[FEATURES]
    y = df_test[TARGET]
    preds = model.predict(X)
    return mean_absolute_error(y, preds)


if __name__ == "__main__":
    print("Loading data...")
    df = load_and_prepare(DATA_PATH)
    print(f"  {len(df)} rows after dropping nulls")

    df_train, df_test = time_split(df)
    print(f"  Train: {len(df_train)} rows | Test: {len(df_test)} rows")

    print("Training XGBoost...")
    model = train(df_train)

    mae = evaluate(model, df_test)
    print(f"  Test MAE: {mae:.2f} pts")

    joblib.dump(model, MODEL_PATH)
    print(f"  Model saved → {MODEL_PATH}")
