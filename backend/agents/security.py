import os
import time

def security_agent(sql_query: str) -> str:
    dangerous = [" drop ", " delete ", " update ", " insert ", " alter ", " truncate ", ";", "--", "/*", "*/"]
    lower_sql = f" {sql_query.lower()} "
    if any(word in lower_sql for word in dangerous):
        return "❌ Blocked: Unsafe SQL detected!"
    return sql_query
