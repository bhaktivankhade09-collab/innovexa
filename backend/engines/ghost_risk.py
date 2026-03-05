"""
GhostRiskEngine
Scores each subscription for ghost subscription risk (0-100).
"""

from typing import List, Dict

ENTERTAINMENT_KEYWORDS = ["netflix", "spotify", "hotstar", "prime", "zee", "sony", "youtube", "crunchyroll", "hulu"]
PRODUCTIVITY_KEYWORDS  = ["notion", "zoom", "slack", "figma", "canva", "adobe", "dropbox", "monday"]
FITNESS_KEYWORDS       = ["gym", "fitness", "fitzone", "cult", "healthify", "strava"]


def _categorise(merchant: str) -> str:
    m = merchant.lower()
    if any(k in m for k in ENTERTAINMENT_KEYWORDS):
        return "Entertainment"
    if any(k in m for k in PRODUCTIVITY_KEYWORDS):
        return "Productivity"
    if any(k in m for k in FITNESS_KEYWORDS):
        return "Fitness"
    return "Other"


def score_ghost_risk(subscriptions: List[Dict]) -> List[Dict]:
    """
    Adds ghost_risk_score (0-100) and risk_label to each subscription.
    Scoring factors:
      - Low amount < 300  → +25
      - Long running (>4 occurrences) → +20
      - Entertainment category → +25
      - High frequency (weekly) → +15
      - Unknown category → +15
    """
    scored = []
    for sub in subscriptions:
        score = 0
        category = _categorise(sub["merchant"])

        if sub["monthly_amount"] < 300:
            score += 25
        if sub["occurrence_count"] > 4:
            score += 20
        if category == "Entertainment":
            score += 25
        if sub["frequency"] == "weekly":
            score += 15
        if category == "Other":
            score += 15

        score = min(score, 100)

        if score >= 70:
            label = "High"
        elif score >= 40:
            label = "Medium"
        else:
            label = "Low"

        scored.append({
            **sub,
            "category": category,
            "ghost_risk_score": score,
            "risk_label": label
        })

    return scored