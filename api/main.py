import joblib
import json
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    FareRequest, FareResponse,
    DemandRequest, DemandResponse,
    TipRequest, TipResponse
)

# ── Load Models ──────────────────────────────────────────
print("⏳ Loading models...")
fare_model   = joblib.load("models/fare_model.pkl")
demand_model = joblib.load("models/demand_model.pkl")
tip_model    = joblib.load("models/tip_model.pkl")

with open("models/feature_config.json") as f:
    feature_config = json.load(f)

FARE_FEATURES   = feature_config["fare_features"]
DEMAND_FEATURES = feature_config["demand_features"]
TIP_FEATURES    = feature_config["tip_features"]

print("✅ All models loaded!")

# ── FastAPI App ───────────────────────────────────────────
app = FastAPI(
    title       = "NYC TLC Taxi ML API",
    description = "ML predictions for NYC Yellow Taxi trips — fare, demand & tip",
    version     = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_methods  = ["*"],
    allow_headers  = ["*"]
)

# ── Health Check ─────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status"    : "✅ NYC TLC ML API is running",
        "models"    : ["fare_prediction", "demand_forecasting", "tip_prediction"],
        "docs"      : "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": 3}

# ── Endpoint 1: Fare Prediction ──────────────────────────
@app.post("/predict/fare", response_model=FareResponse)
def predict_fare(req: FareRequest):
    try:
        input_df = pd.DataFrame([{
            "TRIP_DISTANCE"        : req.trip_distance,
            "PICKUP_LOCATION_ID"   : req.pickup_location_id,
            "DROPOFF_LOCATION_ID"  : req.dropoff_location_id,
            "PICKUP_HOUR"          : req.pickup_hour,
            "PICKUP_DAY"           : req.pickup_day,
            "PICKUP_MONTH"         : req.pickup_month,
            "PASSENGER_COUNT"      : req.passenger_count,
            "IS_WEEKEND"           : req.is_weekend,
            "TRIP_CATEGORY"        : req.trip_category,
            "TIME_OF_DAY"          : req.time_of_day
        }])
        input_df.columns = FARE_FEATURES
        pred = float(fare_model.predict(input_df)[0])
        return FareResponse(
            predicted_fare  = round(pred, 2),
            fare_range_low  = round(pred * 0.85, 2),
            fare_range_high = round(pred * 1.15, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Endpoint 2: Demand Forecasting ───────────────────────
@app.post("/predict/demand", response_model=DemandResponse)
def predict_demand(req: DemandRequest):
    try:
        input_df = pd.DataFrame([{
            "PICKUP_LOCATION_ID" : req.pickup_location_id,
            "PICKUP_HOUR"        : req.pickup_hour,
            "PICKUP_DAY"         : req.pickup_day,
            "PICKUP_MONTH"       : req.pickup_month,
            "IS_WEEKEND"         : req.is_weekend
        }])
        input_df.columns = DEMAND_FEATURES
        pred = max(0, int(demand_model.predict(input_df)[0]))

        if pred < 5:
            level = "Very Low"
        elif pred < 20:
            level = "Low"
        elif pred < 50:
            level = "Medium"
        elif pred < 100:
            level = "High"
        else:
            level = "Very High"

        return DemandResponse(
            predicted_trips = pred,
            demand_level    = level,
            location_id     = req.pickup_location_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Endpoint 3: Tip Prediction ────────────────────────────
@app.post("/predict/tip", response_model=TipResponse)
def predict_tip(req: TipRequest):
    try:
        input_df = pd.DataFrame([{
            "TRIP_DISTANCE"      : req.trip_distance,
            "FARE_AMOUNT"        : req.fare_amount,
            "PICKUP_HOUR"        : req.pickup_hour,
            "PICKUP_DAY"         : req.pickup_day,
            "IS_WEEKEND"         : req.is_weekend,
            "TRIP_CATEGORY"      : req.trip_category,
            "TIME_OF_DAY"        : req.time_of_day,
            "PICKUP_LOCATION_ID" : req.pickup_location_id,
            "TRIP_DURATION_MIN"  : req.trip_duration_min,
            "REVENUE_PER_MILE"   : req.revenue_per_mile
        }])
        input_df.columns = TIP_FEATURES
        prob       = float(tip_model.predict_proba(input_df)[0][1])
        prediction = "High Tip" if prob > 0.5 else "Low Tip"
        recommended_tip = round(req.fare_amount * 0.20, 2) if prob > 0.5 \
                          else round(req.fare_amount * 0.15, 2)

        return TipResponse(
            tip_prediction      = prediction,
            probability         = round(prob, 4),
            recommended_tip_usd = recommended_tip
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
