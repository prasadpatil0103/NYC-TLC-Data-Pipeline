from pydantic import BaseModel, Field
from typing import Literal

# ── Fare Prediction ──────────────────────────────────────
class FareRequest(BaseModel):
    trip_distance       : float = Field(..., gt=0, example=3.5)
    pickup_location_id  : int   = Field(..., example=161)
    dropoff_location_id : int   = Field(..., example=237)
    pickup_hour         : int   = Field(..., ge=0, le=23, example=8)
    pickup_day          : int   = Field(..., ge=1, le=7, example=2)
    pickup_month        : int   = Field(..., ge=1, le=12, example=1)
    passenger_count     : int   = Field(1, ge=1, le=6, example=1)
    is_weekend          : int   = Field(..., ge=0, le=1, example=0)
    trip_category       : int   = Field(..., ge=0, le=3, example=1,
                                        description="0=Short, 1=Medium, 2=Long, 3=Very Long")
    time_of_day         : int   = Field(..., ge=0, le=3, example=2,
                                        description="0=Late Night, 1=Off Peak, 2=Morning Rush, 3=Evening Rush")

class FareResponse(BaseModel):
    predicted_fare      : float
    fare_range_low      : float
    fare_range_high     : float
    currency            : str = "USD"

# ── Demand Forecasting ───────────────────────────────────
class DemandRequest(BaseModel):
    pickup_location_id  : int = Field(..., example=161)
    pickup_hour         : int = Field(..., ge=0, le=23, example=9)
    pickup_day          : int = Field(..., ge=1, le=7, example=2)
    pickup_month        : int = Field(..., ge=1, le=12, example=1)
    is_weekend          : int = Field(..., ge=0, le=1, example=0)

class DemandResponse(BaseModel):
    predicted_trips     : int
    demand_level        : Literal["Very Low", "Low", "Medium", "High", "Very High"]
    location_id         : int

# ── Tip Prediction ───────────────────────────────────────
class TipRequest(BaseModel):
    trip_distance       : float = Field(..., gt=0, example=3.5)
    fare_amount         : float = Field(..., gt=0, example=18.5)
    pickup_hour         : int   = Field(..., ge=0, le=23, example=8)
    pickup_day          : int   = Field(..., ge=1, le=7, example=2)
    is_weekend          : int   = Field(..., ge=0, le=1, example=0)
    trip_category       : int   = Field(..., ge=0, le=3, example=1)
    time_of_day         : int   = Field(..., ge=0, le=3, example=2)
    pickup_location_id  : int   = Field(..., example=161)
    trip_duration_min   : float = Field(..., gt=0, example=12.5)
    revenue_per_mile    : float = Field(..., gt=0, example=5.28)

class TipResponse(BaseModel):
    tip_prediction      : Literal["High Tip", "Low Tip"]
    probability         : float
    recommended_tip_usd : float
