"""
SubscriptionAnalyticsEngine
Computes aggregated financial analytics and chart-ready data.
"""

from typing import List, Dict
import pandas as pd
from collections import defaultdict


def compute_analytics(subscriptions: List[Dict], df: pd.DataFrame) -> Dict:
    """
    Returns comprehensive analytics:
      - total_monthly_cost
      - annual_cost
      - five_year_projection
      - monthly_trend (for line chart)
      - category_breakdown (for pie chart)
      - subscription_amounts (for bar chart)
    """
    if not subscriptions:
        return {}

    total_monthly = sum(s["monthly_amount"] for s in subscriptions)
    annual_cost = round(total_monthly * 12, 2)
    five_year = round(total_monthly * 12 * 5, 2)

    # Monthly trend from raw debit transactions
    debits = df[df["Type"].str.lower() == "debit"].copy()
    debits["month"] = debits["Date"].dt.to_period("M").astype(str)
    monthly_trend = (
        debits.groupby("month")["Amount"]
        .sum()
        .reset_index()
        .rename(columns={"month": "month", "Amount": "total"})
        .sort_values("month")
        .to_dict(orient="records")
    )

    # Category breakdown
    category_totals: Dict[str, float] = defaultdict(float)
    for s in subscriptions:
        category_totals[s.get("category", "Other")] += s["monthly_amount"]
    category_breakdown = [
        {"category": cat, "amount": round(amt, 2)}
        for cat, amt in category_totals.items()
    ]

    # Per-subscription bar data
    subscription_amounts = [
        {"merchant": s["merchant"], "monthly_amount": s["monthly_amount"]}
        for s in subscriptions
    ]

    return {
        "total_monthly_cost": round(total_monthly, 2),
        "annual_cost": annual_cost,
        "five_year_projection": five_year,
        "monthly_trend": monthly_trend,
        "category_breakdown": category_breakdown,
        "subscription_amounts": subscription_amounts,
    }