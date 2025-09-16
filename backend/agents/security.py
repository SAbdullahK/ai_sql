import os
import time

def security_agent(sql_query :str) -> str :
    dangerous = ["drop","delete","update","insert","alter"]
    if any(word in sql_query.lower() for word in dangerous):
        return "❌ Blocked: Unsafe SQL detected!"
    return sql_query
