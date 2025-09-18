import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def query_validator(sql_query :str, schema : str, retries: int = 3, delay: int = 5 ) :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are an expert SQL Query Validator.
            Check this SQL query against schema:
            {schema}
            SQL: {sql_query}
            if valid, return SQL. If invaid, fix table/column names.
            """
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                # Fallback: return the query as-is
                return sql_query
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return (getattr(response, "text", "") or "").strip()
        except Exception as e:
            if attempts == retries:
                return f"❌ Failed after {attempts} attempts: {str(e)}"
            time.sleep(delay)