import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def answer_formatter(user_query :str,sql_query : str, result, retries: int = 3, delay: int = 5 ) -> str :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are a helpful assistant.
            The user asked: {user_query}
            SQL executed : {sql_query}
            Raw result : {result}

            Format the result into a human understandable, humorous, or friendly answer.
            """
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                # Fallback basic formatter
                return f"Query: {sql_query}\nRows: {getattr(result, 'shape', ('?', '?'))[0]}"
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return (getattr(response, "text", "") or "").strip()
        except Exception as e:
            if attempts == retries:
                return f"❌ Failed after {attempts} attempts: {str(e)}"
            time.sleep(delay)
            