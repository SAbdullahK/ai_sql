import os
from google.genai import Client
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(api_key = GOOGLE_API_KEY)

def query_validator(sql_query :str, schema : str, retries: int = 3, delay: int = 5 ) :
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""You are an expert SQL Query Validator.
            Check this SQL query against schema:
            {schema}
            SQL: {sql_query}
            if valid, return SQL. If invaid, fix table/column names.
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