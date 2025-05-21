import pandas as pd

df = pd.read_csv("data/company_fundamentals.csv")

def retrieve_data(parsed: dict) -> pd.DataFrame:
    fundamentals = parsed.get("fundamental")
    # Convert to list if single string is provided
    if isinstance(fundamentals, str):
        fundamentals = [fundamentals]
    
    # Check if fundamentals is valid
    if not fundamentals:
        return pd.DataFrame({})
    
    # Replace spaces with underscores in each fundamental
    fundamentals = [fund.replace(" ", "_") for fund in fundamentals]
    
    companies = parsed.get("company")
    sector = parsed.get("sector")
    time_range = parsed.get("time_period")
    
    if not time_range:
        return pd.DataFrame({})
    
    # Parse years
    try:
        start_year, end_year = map(int, time_range.split("-"))
        
        # Ensure start_year is less than or equal to end_year
        if end_year < start_year:
            start_year, end_year = end_year, start_year
        
        years = list(range(start_year, end_year + 1))
    except:
        raise ValueError("Invalid time period format.")

    if start_year < 2015 or end_year > 2024:
        return pd.DataFrame({})
    
    # Build required column names for all fundamentals
    required_columns = []
    for fundamental in fundamentals:
        for year in years:
            required_columns.append(f"{fundamental.lower()}_{year}")
    
    # Filter companies based on company name or sector
    if companies:
        filtered_df = df[df["company"].str.lower().isin([c.lower() for c in companies])]
        if filtered_df.empty:
            return pd.DataFrame({})
    elif sector:
        filtered_df = df[df["sector"].str.lower().isin([s.lower() for s in sector])]
        if filtered_df.empty:
            return pd.DataFrame({})
    else:
        return pd.DataFrame({})
    
    # Check which required columns exist
    available_columns = [col for col in required_columns if col in df.columns]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if not available_columns:
        return pd.DataFrame({})
    
    # Return only relevant columns plus identifiers
    result_df = filtered_df[["company"] + available_columns].copy()
    
    # Rename columns to include fundamental name and year
    new_column_names = ["Company"]
    for col in available_columns:
        # Split by underscore and get all parts except the last one (which is the year)
        fundamental_parts = col.split('_')
        year = fundamental_parts[-1]
        # Rejoin the fundamental name parts with spaces
        fundamental_name = ' '.join(fundamental_parts[:-1])
        # Format the column name
        new_column_names.append(f"{fundamental_name.title()} {year}")
    
    result_df.columns = new_column_names
    result_df = result_df.reset_index(drop=True)
    
    return result_df
if __name__ == "__main__":
    parsed = {'company': ['HDFC Bank'], 'sector': ['Banking'], 'fundamental': 'net_profit', 'time_period': '2024-2020', 'graph_needed': False, 'table_needed': True, 'rag_needed': False}

    try:
        table = retrieve_data(parsed)
        print(table)
    except Exception as e:
        print("Error:", e)
