import os
from google.genai import Client
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(api_key = GOOGLE_API_KEY)

def query_generator(user_query :str, schema : str, retries: int = 3, delay: int = 5 ) :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are an expert SQL Query Generator.
            Convert this natural language into SQL using schema:
            {schema}
            User: {user_query}
            SQL: 
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
        