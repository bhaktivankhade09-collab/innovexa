"""
SubVampire Slayer — FastAPI Backend
Master entry point for all analysis routes.
"""

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd, io
from typing import Optional

from engines.subscription_pattern import detect_recurring_payments
from engines.ghost_risk import score_ghost_risk
from engines.trial_prediction import predict_trials
from engines.analytics import compute_analytics

app = FastAPI(title="SubVampire Slayer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def parse_csv(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.columns = [c.strip().title() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=False, errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df["Type"] = df["Type"].str.strip().str.lower()
    df["Merchant"] = df["Merchant"].str.strip()
    return df

def compute_health_score(subscriptions, analytics, monthly_income):
    if not analytics or monthly_income <= 0:
        return {"health_score": 50, "label": "Unknown", "breakdown": {}}
    total_monthly = analytics.get("total_monthly_cost", 0)
    ghost_count = sum(1 for s in subscriptions if s.get("risk_label") == "High")
    income_ratio = min(total_monthly / monthly_income, 1.0)
    income_penalty = round(income_ratio * 40)
    ghost_penalty  = min(ghost_count * 10, 30)
    count_penalty  = min(len(subscriptions) * 3, 30)
    score = max(0, 100 - income_penalty - ghost_penalty - count_penalty)
    label = ("Excellent " if score >= 75 else
             "Fair "     if score >= 50 else
             "At Risk "  if score >= 25 else "Critical ")
    return {"health_score": score, "label": label,
            "breakdown": {"income_penalty": income_penalty, "ghost_penalty": ghost_penalty, "count_penalty": count_penalty}}

@app.get("/")
def root():
    return {"message": "SubVampire Slayer API is alive "}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), monthly_income: Optional[float] = Form(50000)):
    raw = await file.read()
    try:
        df = parse_csv(raw)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"CSV parse error: {str(e)}"})

    raw_subs   = detect_recurring_payments(df)
    scored_subs = score_ghost_risk(raw_subs)
    trials      = predict_trials(df)
    analytics   = compute_analytics(scored_subs, df)
    health      = compute_health_score(scored_subs, analytics, monthly_income or 50000)

    return {
        "subscriptions": scored_subs,
        "trials": trials,
        "analytics": analytics,
        "health": health,
        "summary": {
            "total_subscriptions": len(scored_subs),
            "ghost_count": sum(1 for s in scored_subs if s["risk_label"] == "High"),
            "trial_count": len(trials),
            "monthly_spend": analytics.get("total_monthly_cost", 0),
            "annual_drain": analytics.get("annual_cost", 0),
        }
    }