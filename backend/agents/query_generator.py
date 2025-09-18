import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def query_generator(user_query :str, schema : str, retries: int = 3, delay: int = 5 ) :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are an expert SQL Query Generator.
            Convert this natural language into SQL using schema:
            {schema}
            User: {user_query}
            SQL: 
            """
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                # Fallback heuristic if no API key is configured
                return "SELECT * FROM employees LIMIT 5;"
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return (getattr(response, "text", "") or "").strip()
        except Exception as e:
            if attempts == retries:
                return f"❌ Failed after {attempts} attempts: {str(e)}"
            time.sleep(delay)
        