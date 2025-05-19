# app.py
import streamlit as st
from agent0_classifier import classify_query
from agent1_parser import parse_query
from agent2_retriever import retrieve_data
from agent3_rag import generate_insight
from utils.load_company_descriptions import load_company_descriptions
import os
from dotenv import load_dotenv

load_dotenv()

# Load company descriptions once
company_descriptions = load_company_descriptions("data/company_descriptions.txt")

st.title("📊 Financial Insight Assistant")

user_query = st.text_input("Ask your financial question:")

if st.button("Submit") and user_query:
    with st.spinner("Processing..."):
        query_class = classify_query(user_query)

        if query_class == "non_financial":
            st.warning("⚠️ This is a general/non-financial query. Try asking about a company or sector.")
        
        elif query_class == "financial_unknown":
            st.info("ℹ️ Sorry, I don't have data for this type of financial question yet.")
        
        else:  # financial_known
            parsed = parse_query(user_query)
            df = retrieve_data(parsed)

            if df.empty:
                st.error("❌ No data found for this query.")
            else:
                st.subheader("📊 Retrieved Data")
                st.dataframe(df)

                # Generate Gemini-based insight
                insight = generate_insight(df, parsed, company_descriptions)
                st.subheader("🧠 Insight")
                st.write(insight)
