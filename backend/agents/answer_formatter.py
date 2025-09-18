import os
from google.genai import Client
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(api_key = GOOGLE_API_KEY)

# def answer_formatter(user_query :str,sql_query : str, result, retries: int = 3, delay: int = 5 ) -> str :
#     for attempts in range(1, retries + 1):
#         try:
#             prompt = f"""You are a helpful assistant.
#             The user asked: {user_query}
#             SQL executed : {sql_query}
#             Raw result : {result}

#             Format the result into a human understandable, humorous, or friendly answer.
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

def answer_formatter(user_query: str, sql_query: str, result, retries: int = 3, delay: int = 5):
    """
    Format the SQL query result into a human-friendly answer.
    Returns a dictionary with keys: 'query', 'rows', 'friendly_answer', 'error'.
    """
    answer_package = {
        "query": sql_query,
        "rows": result if isinstance(result, list) else [],
        "friendly_answer": None,
        "error": None
    }

    # Handle empty results
    if not result or (isinstance(result, list) and len(result) == 0):
        answer_package["friendly_answer"] = "⚠️ No records found for your query."
        return answer_package

    # If AI client is not available, return basic friendly answer
    if client is None:
        try:
            # Simple summary
            if len(result) == 1 and len(result[0]) == 1:
                key = list(result[0].keys())[0]
                answer_package["friendly_answer"] = f"The result of your query: {result[0][key]}"
            else:
                # Show first 5 rows
                rows_text = []
                for i, row in enumerate(result[:5]):
                    row_str = ", ".join([f"{k}: {v}" for k, v in row.items()])
                    rows_text.append(f"{i+1}. {row_str}")
                more_rows = f"\n...and {len(result)-5} more rows." if len(result) > 5 else ""
                answer_package["friendly_answer"] = "Here are the first few results:\n" + "\n".join(rows_text) + more_rows
            return answer_package
        except Exception as e:
            answer_package["friendly_answer"] = f"⚠️ Could not format results: {str(e)}"
            return answer_package

    # If AI client is available, use it
    for attempt in range(1, retries + 1):
        try:
            prompt = f"""You are a helpful assistant.
The user asked: {user_query}
SQL executed: {sql_query}
Raw result: {result}

Format the result into a human understandable, humorous, or friendly answer.
"""
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[prompt],
            )
            answer_package["friendly_answer"] = response.text.strip()
            return answer_package
        except Exception as e:
            if attempt == retries:
                answer_package["error"] = f"❌ Failed after {attempt} attempts: {str(e)}"
                answer_package["friendly_answer"] = f"⚠️ Could not generate AI answer: {str(e)}"
                return answer_package
            time.sleep(delay)