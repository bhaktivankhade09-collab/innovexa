"""
SubscriptionPatternEngine
Detects recurring payment patterns from transaction data.
"""

import pandas as pd
from typing import List, Dict


def detect_recurring_payments(df: pd.DataFrame) -> List[Dict]:
    """
    Detects recurring transactions by grouping on Merchant + Amount,
    then checking time gaps for monthly (~28-31 days) or weekly (~7 days) patterns.
    """
    debits = df[df["Type"].str.lower() == "debit"].copy()
    debits = debits.sort_values("Date")
    subscriptions = []

    for (merchant, amount), group in debits.groupby(["Merchant", "Amount"]):
        group = group.sort_values("Date")
        occurrences = len(group)
        if occurrences < 2:
            continue

        dates = group["Date"].tolist()
        gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates) - 1)]
        median_gap = sorted(gaps)[len(gaps) // 2]

        if 28 <= median_gap <= 31:
            frequency = "monthly"
            monthly_amount = float(amount)
        elif 6 <= median_gap <= 8:
            frequency = "weekly"
            monthly_amount = float(amount) * 4.33
        else:
            continue

        subscriptions.append({
            "merchant": merchant,
            "frequency": frequency,
            "monthly_amount": round(monthly_amount, 2),
            "occurrence_count": occurrences,
            "last_charge_date": dates[-1].strftime("%Y-%m-%d"),
            "avg_gap_days": round(sum(gaps) / len(gaps), 1)
        })

    return subscriptions
