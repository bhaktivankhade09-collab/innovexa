#DEMO CSV file genrator
import csv 
from datetime import datetime ,timedelta
import random 
#generating Demo transactions csv file
def generate_demo_csv(output_path='demo_transactions.csv'):
    rows=[]
    today=datetime.today()

    def add_monthly(merchant,amount,months=6,start_offset=0):
        for i in range(months):
            date=today-timedelta(days=30*(months-i)+start_offset)
            rows.append({
                'Date':date.strftime('%Y-%m-%d'),
                'Merchant':merchant,
                'Amount':amount,
                'Type':'debit'
            })
    #add weekly transactions 
    def add_weekly(merchant, amount, weeks=12):
        for i in range(weeks):
            date = today - timedelta(weeks=(weeks - i))
            rows.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Merchant": merchant,
                "Amount": amount,
                "Type": "debit"
            })

    # Netflix — monthly, increasing trend simulation
    netflix_amounts = [199, 199, 199, 249, 249, 249]
    for i, amt in enumerate(netflix_amounts):
        date = today - timedelta(days=30 * (6 - i))
        rows.append({"Date": date.strftime("%Y-%m-%d"), "Merchant": "Netflix", "Amount": amt, "Type": "debit"})

    # Spotify — monthly
    add_monthly("Spotify", 119, months=6)

    # Canva ₹1 trial — single occurrence (trial detection)
    rows.append({
        "Date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
        "Merchant": "Canva Pro Trial",
        "Amount": 1,
        "Type": "debit"
    })

    # ₹99 mystery micro subscription
    add_monthly("QuickRead Premium", 99, months=5)

    # Gym membership — monthly
    add_monthly("FitZone Gym Membership", 799, months=6)

    # Hotstar — monthly
    add_monthly("Disney+ Hotstar", 299, months=4)

    # Notion — monthly
    add_monthly("Notion Pro", 160, months=3)

    # Zoom — monthly ghost subscription (low use)
    add_monthly("Zoom Subscription", 149, months=6)

    # Some random credits/debits (non-subscription noise)
    merchants_noise = ["Zomato", "Swiggy", "Amazon", "Flipkart", "Uber", "Ola"]
    for _ in range(30):
        date = today - timedelta(days=random.randint(1, 180))
        rows.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Merchant": random.choice(merchants_noise),
            "Amount": round(random.uniform(50, 2000), 2),
            "Type": random.choice(["debit", "debit", "credit"])
        })

    # Sort by date
    rows.sort(key=lambda x: x["Date"])

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Merchant", "Amount", "Type"])
        writer.writeheader()
        writer.writerows(rows)

    print(f" Demo CSV generated: {output_path} ({len(rows)} rows)")

if __name__ == "__main__":
    generate_demo_csv()