# app.py
import streamlit as st
from agent0_classifier import classify_query
from agent1_parser import parse_query
from agent2_retriever import retrieve_data
from agent3_rag import generate_insight, generate_normal
from utils.load_company_descriptions import load_company_descriptions
import os
import pandas as pd
import altair as alt
from dotenv import load_dotenv

load_dotenv()

company_descriptions = load_company_descriptions("data/company_descriptions.txt")
st.set_page_config(page_title="Financial Insight Assistant", layout="wide")
st.title("📊 Financial Insight Assistant")

description = """Hello! I am a financial analysis assistant who will help you with providing data, plotting it and doing analysis on it.
The data I currently have access to are of these companies and sectors:
- Infosys, Wipro, TCS (IT Sector)
- HDFC Bank, ICIC Bank, Axis Bank (Banking Sector)
- Reliance Inds, NTPC (Energy Sector)
- Sun Pharma, Dr. Reddy's (Pharma Sector)

And I have access to fundamentals like sales, net profit, debt equity ratio, avg stock price, roe, etc. for every year in 2015-2024.
"""

st.write(description)

user_query = st.text_input("Ask your financial question:")

if st.button("Submit") and user_query:
    with st.spinner("Processing..."):
        query_class = classify_query(user_query)

        if query_class == "non_financial":
            st.warning("⚠️ This is a general/non-financial query. Try asking about a company or sector's finance.")
        
        elif query_class == "financial_unknown":
            st.info("ℹ️ Sorry, I don't have data for the given company or sector")
        
        else:  # financial_known
            parsed = parse_query(user_query)
            if (parsed['company'] or parsed['sector']) and not parsed['fundamental']:
                res = generate_normal(user_query)
                st.write(res)
            else:
                df = retrieve_data(parsed)
                if df.empty:
                    st.error("❌ No data found for this query. Make sure your time range is 2024-2015 or between it. ALso make sure you have the mentioned the given companies/sectors or the fundamentals above only.")
                else:
                    st.subheader("📊 Retrieved Data")
                    st.dataframe(df)
                    if parsed['graph_needed'] == True:
                        x_columns = df.columns[1:]

                        # Plot each row
                        for idx, row in df.iterrows():
                            title = row[0] 
                            y_values = row[1:]  

                            
                            temp_df = pd.DataFrame({
                                'X': x_columns,
                                'Y': y_values.values
                            })

                            
                            st.markdown(f"### 📈 {title}")
                            chart = alt.Chart(temp_df).mark_line(point=True).encode(
                                x='X',
                                y='Y'
                            ).properties(
                                width=600,
                                height=300
                            )
                            st.altair_chart(chart, use_container_width=True)

                    # Generate Gemini-based insight
                    insight = generate_insight(df, parsed, company_descriptions, user_query)
                    st.subheader("🧠 Insight")
                    st.write(insight)
