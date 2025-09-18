import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def query_optimizer(sql_query :str, retries: int = 3, delay: int = 5 ) :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are an expert SQL Query Optimizer.
            Optimize the following query for performance but keep the logic same:
            {sql_query}
            """
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                # Fallback: return the query unchanged
                return sql_query
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return (getattr(response, "text", "") or "").strip()
        except Exception as e:
            if attempts == retries:
                return f"❌ Failed after {attempts} attempts: {str(e)}"
            time.sleep(delay)