import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_insight(
    df: pd.DataFrame,
    parsed_query: dict,
    company_info: dict
) -> str:
    """
    Generate RAG-based insight using financial data and company descriptions.
    """

    companies = parsed_query.get("company", [])
    sector = parsed_query.get("sector", [])
    selected_entries = {}

    if companies != None:
        for company in companies:
            if company in company_info:
                selected_entries[company] = company_info[company]
    elif sector != None:
        for company, info in company_info.items():
            if info["sector"] in sector:
                selected_entries[company] = info

    if not selected_entries:
        description_context = "No relevant company descriptions found."
    else:
        description_context = ""
        for company, info in selected_entries.items():
            desc = f"{company} ({info['sector']} Sector)\n"
            desc += f"Summary: {info['summary']}\n"
            desc += "Highlights:\n" + "\n".join(f"- {pt}" for pt in info["highlights"])
            description_context += desc + "\n\n"

    # Convert DataFrame to markdown
    table_context = df.to_markdown(index=False)

    # Final prompt
    prompt = f"""
You are a financial analysis expert.

User query (structured):
{parsed_query}

Financial Data:
{table_context}

Company Background:
{description_context}

Now provide a thoughtful and clear insight, conclusion, or explanation that helps the user understand the financial trends or context. Avoid repeating table values. Summarize, compare, or explain patterns instead.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
