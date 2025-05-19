import pandas as pd

df = pd.read_csv("data/company_fundamentals.csv")

def retrieve_data(parsed: dict) -> pd.DataFrame:
    fundamental = parsed.get("fundamental")
    if fundamental:
        fundamental = fundamental.replace(" ", "_")
    companies = parsed.get("company")
    sector = parsed.get("sector")
    time_range = parsed.get("time_period")

    if not fundamental:
        raise ValueError("No fundamental specified.")
    if not time_range:
        raise ValueError("No time period specified.")

    # Parse years
    try:
        start_year, end_year = map(int, time_range.split("-"))

        # Ensure start_year is less than or equal to end_year
        if end_year < start_year:
            start_year, end_year = end_year, start_year

        years = list(range(start_year, end_year + 1))
        print(start_year, end_year)
    except:
        raise ValueError("Invalid time period format.")

    # Build required column names
    required_columns = [f"{fundamental.lower()}_{year}" for year in years]

    # Filter companies based on company name or sector
    if companies:
        filtered_df = df[df["company"].str.lower().isin([c.lower() for c in companies])]
        if filtered_df.empty:
            raise ValueError("No matching companies found.")
    elif sector:
        filtered_df = df[df["sector"].str.lower().isin([s.lower() for s in sector])]
        if filtered_df.empty:
            raise ValueError("No companies found in the specified sector(s).")
    else:
        raise ValueError("Neither company nor sector specified.")

    # Check which required columns exist
    available_columns = [col for col in required_columns if col in df.columns]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if not available_columns:
        raise ValueError(f"No data available for fundamental '{fundamental}' in the given time range.")

    # Return only relevant columns plus identifiers
    result_df = filtered_df[["company"] + available_columns].copy()
    result_df.columns = ["Company"] + [col.split("_")[-1] for col in available_columns]

    return result_df
if __name__ == "__main__":
    parsed = {'company': ['HDFC Bank'], 'sector': ['Banking'], 'fundamental': 'net_profit', 'time_period': '2024-2020', 'graph_needed': False, 'table_needed': True, 'rag_needed': False}

    try:
        table = retrieve_data(parsed)
        print(table)
    except Exception as e:
        print("Error:", e)
