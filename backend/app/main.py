from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.predictor import predict_pts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest):
    predicted_pts = predict_pts(request.model_dump())
    return {"predicted_pts": round(predicted_pts, 1)}