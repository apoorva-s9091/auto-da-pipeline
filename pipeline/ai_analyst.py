import pandas as pd
import os
import google.generativeai as genai
from utils.logger import logger

CHARTS_DIR = "reports/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def get_schema(df: pd.DataFrame) -> str:
    schema = []
    for col in df.columns:
        schema.append(f"{col} ({df[col].dtype})")
    return ", ".join(schema)

def call_gemini(user_request: str, schema: str) -> str:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are a data analysis expert. 
The dataset has these columns: {schema}

User wants: {user_request}

Write a Python function named `analyze(df)` that:
- Takes a pandas DataFrame as input
- Performs the requested analysis
- Saves any charts to 'reports/charts/' using matplotlib
- Returns a dict with results

Return ONLY the function code, nothing else. No markdown, no backticks.
"""
    response = model.generate_content(prompt)
    return response.text

def ai_analysis(df: pd.DataFrame) -> dict:
    print("\nDescribe what analysis you want:")
    user_request = input("> ").strip()

    logger.info(f"AI analysis requested: {user_request}")

    schema = get_schema(df)
    logger.info("Sending schema to Gemini API (data stays local)")

    code = call_gemini(user_request, schema)
    logger.info("Received analysis function from Gemini")

    try:
        local_vars = {}
        exec(code, {"df": df, "pd": pd, "plt": __import__("matplotlib.pyplot", fromlist=["pyplot"]), "sns": __import__("seaborn")}, local_vars)
        result = local_vars["analyze"](df)
        logger.info("AI analysis executed successfully")
        return result
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        return {"error": str(e)}