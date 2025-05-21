import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  
companies = ['Infosys', 'Wipro', 'TCS', 'HDFC Bank', 'ICICI Bank', 'Axis Bank', 'Reliance Industries', 'NTPC', 'Sun Pharma', 'Dr. Reddy\'s']
sectors = ['IT', 'Banking', 'Energy', 'Pharma']
fundamentals = ['sales', 'net profit', 'roe', 'debt equity', 'dividend yield', 'avg price']

def parse_query(query: str) -> dict:
    prompt = f"""
You are a financial query parser. Your job is to extract structured information from user queries related to companies in our dataset.

Return the following fields as a JSON object:
1. "company": List of company names (e.g., ["Infosys", "Dr. Reddy's", "NTPC"]). Use null if not mentioned. if one of these {companies}, then write like this only as given in the list.
2. "sector": List of sectors (e.g., ["IT", "Banking", "Energy", "Pharma"]). Use null if not mentioned. If one of these {sectors}, then write like this only i.e. write Banking and not Banks or something else.
3. "fundamental": The financial metric requested (e.g., "sales", "net profit", "roe", "stock price", "eps", "debt equity" etc.). Use null if not mentioned. If one of these {fundamentals}, then write like this only, 'avg price' is stock price do if the query asks for stock price return avg price in this.
4. "time_period": Time period string (e.g., "2019", "2020-2024", "2015-2024"). Put "2015-2024" if not mentioned. The current year is 2024. If the query asks for "last 5 years", use "2020-2024", and so on. If the query has only one year then do like this '2021-2021' repeat the year.
5. "graph_needed": true if the query implies or requests a graph; false otherwise.
6. "table_needed": true if the query implies or requests a table; false otherwise.
7. "rag_needed": true if the query seeks explanation, reasoning, or analysis beyond raw data; false otherwise.

Strictly return a **valid JSON object** and nothing else. Do not explain your answer. Use double quotes for keys and string values.
Query: "{query}"
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    cleaned = response.text.strip().strip('```json').strip('```').strip()

    try:
        parsed = json.loads(cleaned)
        return parsed
    except Exception as e:
        print("JSON parsing failed:", e)
        print("Raw response:", cleaned)
        return {}

if __name__ == "__main__":
    queries = [
    # Typical queries
    "Show me the sales of Infosys from 2018 to 2022 in a graph.",
    "Can I get a table of ROE for HDFC Bank for the last 5 years?",
    "What is the net profit trend of Reliance Industries between 2020 and 2024?",
    "Display the yearly revenue of Sun Pharma in a chart.",
    "Plot the sales of all IT companies over the last 3 years.",

    # Missing company, fundamental
    "Give me data on the banking sector from 2015 to 2024.",
    "Which company in the energy sector has shown the best performance recently?",
    
    # No financial metric (should go to RAG)
    "Tell me more about the background and leadership of Wipro.",
    "What is the market reputation of ICICI Bank?",
    
    # Combined case (RAG + chart)
    "How has Infosys been performing in terms of profitability, and can you show me a chart as well?"
    ]
    for q in queries:
        dicti = extract_query_details(q)
        print(dicti)