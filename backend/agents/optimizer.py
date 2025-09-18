import os
from google.genai import Client
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(api_key = GOOGLE_API_KEY)


def query_optimizer(sql_query: str, retries: int = 3, delay: int = 5):
    for attempts in range(1, retries + 1):
        try:
            prompt = f"""
            You are an expert SQL Query Optimizer.
            Rewrite the following SQL query in the most optimized form for performance,
            but keep the logic the same.
            Return ONLY the optimized SQL query (no explanation, no comments, no markdown).
            Query:
            {sql_query}
            """
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[prompt],
            )
            optimized_sql = response.text.strip()

            # remove ```sql ... ``` if Gemini adds markdown
            if optimized_sql.startswith("```"):
                optimized_sql = optimized_sql.strip("`").replace("sql\n", "").replace("sql", "").strip()

            return optimized_sql
        except Exception as e:
            if attempts == retries:
                return f"❌ Failed after {attempts} attempts: {str(e)}"
            time.sleep(delay)


# def query_optimizer(sql_query :str, retries: int = 3, delay: int = 5 ) :
#     for attempts in range(1, retries + 1):
#         try:
#             prompt = f"""You are an expert SQL Query Optimizer.
#             Optimize the following query for performance but keep the logic same:
#             {sql_query}
#             Dont give paragraphs of explaination just a single line answer. If the query needs optimization then optimize it and return a one line answer otherwise just give a single line answer that its is already optimized.
#             """
#             response = client.models.generate_content(
#                 model = "gemini-1.5-flash",
#                 contents = [prompt],
#             )
#             return response.text.strip()
#         except Exception as e:
#             if attempts == retries:
#                 return f"❌ Failed after {attempts} attempts: {str(e)}"
#             time.sleep(delay)