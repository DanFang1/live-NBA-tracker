import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.predictor import predict_pts, predict_with_interval
from app.live import get_live_features, _features_df
from nba_api.stats.static import players as nba_players

app = FastAPI()

_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    last5_avg_pts: float
    last5_avg_ast: float
    last5_avg_reb: float
    last5_avg_min: float
    days_rest: float
    is_home: int
    avg_pts_vs_opponent: float
    opponent_encoded: int


@app.get("/players")
def list_players():
    player_ids = _features_df["PLAYER_ID"].unique().tolist()
    result = []
    for pid in player_ids:
        info = nba_players.find_player_by_id(pid)
        if info:
            result.append({"id": int(pid), "name": info["full_name"]})
    result.sort(key=lambda x: x["name"])
    return result


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest):
    predicted_pts = predict_pts(request.model_dump())
    return {"predicted_pts": round(predicted_pts, 1)}


@app.get("/live/{player_id}")
def live_predict(player_id: int):
    features = get_live_features(player_id)
    if features is None:
        return {"error": "Player not found in any live game today"}
    result = predict_with_interval(features)
    return {"player_id": player_id, **result}