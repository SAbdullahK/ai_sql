import os
from google.genai import Client
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(api_key = GOOGLE_API_KEY)

def answer_formatter(user_query :str,sql_query : str, result, retries: int = 3, delay: int = 5 ) -> str :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are a helpful assistant.
            The user asked: {user_query}
            SQL executed : {sql_query}
            Raw result : {result}

            Format the result into a human understandable, humorous, or friendly answer.
            """
            response = client.models.generate_content(
                model = "gemini-1.5-flash",
                contents = [prompt],
            )
            return response.text.strip()
        except Exception as e:
            if attempts == retries:
                return f"❌ Failed after {attempts} attempts: {str(e)}"
            time.sleep(delay)
