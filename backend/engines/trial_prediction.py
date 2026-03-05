"""
TrialPredictionEngine
Detects trial transactions and predicts upcoming conversion charges.
"""

import pandas as pd
from datetime import timedelta
from typing import List, Dict

TRIAL_KEYWORDS = ["trial", "premium", "pro", "membership", "plus", "elite", "vip"]


def predict_trials(df: pd.DataFrame) -> List[Dict]:
    """
    Identifies potential trial-to-paid conversions.
    Criteria:
      - Amount < 10
      - Only appears ONCE (first occurrence)
      - Merchant name contains a trial keyword
    """
    debits = df[df["Type"].str.lower() == "debit"].copy()
    trials = []

    for merchant, group in debits.groupby("Merchant"):
        if len(group) != 1:
            continue  # Must be first-and-only occurrence

        row = group.iloc[0]
        if float(row["Amount"]) >= 10:
            continue

        merchant_lower = merchant.lower()
        if not any(kw in merchant_lower for kw in TRIAL_KEYWORDS):
            continue

        charge_date = row["Date"] + timedelta(days=7 if "trial" in merchant_lower else 30)
        trials.append({
            "merchant": merchant,
            "trial_amount": float(row["Amount"]),
            "trial_date": row["Date"].strftime("%Y-%m-%d"),
            "predicted_renewal_flag": True,
            "estimated_next_charge_date": charge_date.strftime("%Y-%m-%d"),
            "renewal_window_days": 7 if "trial" in merchant_lower else 30
        })

    return trials
