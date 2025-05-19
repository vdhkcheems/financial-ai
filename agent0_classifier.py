import os
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
configure(api_key=GEMINI_API_KEY)

# Load known companies and sectors
import pandas as pd
def load_entities(csv_path='data/company_fundamentals.csv'):
    df = pd.read_csv(csv_path)
    companies = df['company'].str.lower().unique().tolist()
    sectors = df['sector'].str.lower().unique().tolist()
    return companies, sectors

# Build classification prompt
def build_prompt(query, companies, sectors):
    companies_str = ', '.join(companies)
    sectors_str = ', '.join(sectors)

    prompt = f"""
You are a classification agent for a financial chatbot.

Known companies: [{companies_str}]
Known sectors: [{sectors_str}]

Classify the user query into ONE of the following three categories:

1. "non_financial" - The query is not about financial data, metrics, or numeric performance, it might include the companies and sector from above but the nature of query itself is not financial (e.g. who designed the logo of infosys?, when was HDFC founded?, tell me something interesting about wipro etc,).
2. "financial_known" - The query is financial in nature AND mentions a known company or sector.
3. "financial_unknown" - The query is financial in nature BUT no known company or sector is mentioned.

Just return one of the three strings. Here is the query:
\"{query}\"
"""
    return prompt

# Main classification function
def classify_query(query, csv_path='data/company_fundamentals.csv'):
    companies, sectors = load_entities(csv_path)
    prompt = build_prompt(query.lower(), companies, sectors)

    model = GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    result = response.text.strip().lower()

    # Normalize to expected output
    if "non_financial" in result:
        return "non_financial"
    elif "financial_known" in result:
        return "financial_known"
    elif "financial_unknown" in result:
        return "financial_unknown"
    else:
        return "uncertain"

# Example usage
if __name__ == "__main__":
    financial_known_queries = [
    "Show me the net profit of Infosys in 2020.",
    "Plot the revenue trend of TCS from 2015 to 2024.",
    "What was the ROE for HDFC Bank last year?",
    "I want a table showing Reliance Industries' yearly sales.",
    "Compare the EPS of ICICI and SBI over the last 5 years.",
    "Which pharma company among these has had the best sales growth?",
    "Bar chart of Wipro’s yearly ROE please.",
    "Total sales of all energy companies from 2018–2022?",
    "Give me the stock price average of Dr Reddy’s from 2020-2024."
    ]
    financial_unknown_queries = [
    "What's the revenue of Tesla in 2021?",
    "Show me the profit trend of Amazon from 2015.",
    "Can I get EPS values for Zoom over the last 5 years?",
    "Is Nvidia's ROE better than AMD’s?",
    "How has Apple’s sales grown in the last decade?",
    "Graph the net profit of a US-based AI startup.",
    "Which logistics company had the highest revenue in 2020?",
    "Compare Meta and Alphabet in terms of net profit.",
    "How much did PayPal earn in 2022?",
    "Give me a chart of Bumble’s financial performance."
    ]
    non_financial_queries = [
    "Who is the CEO of Infosys?",
    "Tell me something interesting about Wipro.",
    "How old is TCS as a company?",
    "Who are the founders of HDFC Bank?",
    "What is the company culture like at Dr. Reddy’s?",
    "Where is the headquarters of Reliance?",
    "Why are IT companies laying off employees?",
    "What are the core values of ICICI Bank?",
    "Tell me the mission statement of Sun Pharma."
    ]

    for q in non_financial_queries:
        result = classify_query(q)
        print(f"Classification: {result}")
