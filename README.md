# 💹 Financial Query Understanding System

A modular multi-agent system that interprets natural language queries about financial data and responds with structured insights using tables, charts, and explanations.

---

## 🚀 Features

- 🔍 **Agent 0: Query Classifier**
  - Classifies user queries into:
    - `financial_known`
    - `financial_unknown`
    - `non_financial`

- 🧠 **Agent 1: Query Parser**
  - Extracts structured info:
    - Company, sector, metric (e.g., net profit), time period, and intent (table/graph/RAG)

- 📊 **Agent 2: Data Retriever**
  - Extracts relevant rows/columns from `company_fundamentals.csv`
  - Handles edge cases like:
    - Sector-only queries
    - Missing fundamentals
    - Multi-year/multi-company selection

- 🧾 **Agent 3: Explanation via RAG**
  - Uses Gemini API + company summary text to answer "why", "explain", "conclude"-type queries and also give insights on the fetched data.
  - Context is dynamically constructed using parsed data and `company_description.txt`

---

## How to Setup
1. Install dependencies  in a new virtual environment and set it as source
   ```bash
   pip install -r requirements.txt
   ```
2. Create a .env file with your ```GEMINI_API_KEY```

3. run
    ```bash
    streamlit run app.py
    ```

### [Deployed link](https://vdhkcheems-financial-ai-app-dknrjm.streamlit.app/)

### 🧾 2. Note on My Approach

I approached the problem with a **clean multi-agent architecture** that breaks down complex natural language understanding into modular steps. Each "agent" in the system is responsible for a specific stage of processing — classification, parsing, retrieval, and reasoning — ensuring separation of concerns and easier debugging.

Key highlights:
- **Agent 0** filters queries early, reducing unnecessary computation.
- **Agent 1** uses LLMs to extract structured query info, with fallbacks for missing fields.
- **Agent 2** maps structured inputs to tabular data robustly, handling company/sector ambiguity and non-existent columns gracefully.
- **Agent 3** provides explainability via a lightweight RAG approach, integrating structured company insights with retrieved data.

The overall design is both scalable and practical for real-world financial assistants. It demonstrates strong software engineering principles, clear abstraction, and thoughtful UX handling.
