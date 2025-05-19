import pandas as pd
import random

sectors_companies = {
    "IT": ["Infosys", "TCS", "Wipro"],
    "Banking": ["HDFC Bank", "ICICI Bank", "SBI"],
    "Energy": ["Reliance Inds", "NHPC"],
    "Pharma": ["Sun Pharma", "Dr. Reddy's"]
}

years = list(range(2015, 2025))

def generate_metrics(sector):
    # Ranges adjusted slightly by sector
    base = {
        "sales": (20000, 150000),
        "net_profit": (2000, 30000),
        "roe": (8, 25),
        "eps": (10, 200),
        "debt_equity": (0.1, 1.5),
        "dividend_yield": (0.5, 3.5),
        "avg_price": (50, 3500)
    }
    # for sector wise trends
    if sector == "Banking":
        base["debt_equity"] = (0.05, 0.9)  
    elif sector == "Energy":
        base["eps"] = (30, 300)  
    elif sector == "Pharma":
        base["dividend_yield"] = (0.2, 1.5)

    return base

rows = []

for sector, companies in sectors_companies.items():
    for company in companies:
        row = {
            "company": company,
            "sector": sector
        }

        ranges = generate_metrics(sector)

        for year in years:
            for metric, (low, high) in ranges.items():
                col = f"{metric}_{year}"
                val = round(random.uniform(low, high), 2)
                row[col] = val

        rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("company_fundamentals.csv", index=False)
print("Dummy data CSV generated as 'company_fundamentals.csv'")
