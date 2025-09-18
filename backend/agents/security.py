import os
import time

def _strip_code_fences(sql_text: str) -> str:
    text = sql_text.strip()
    if text.startswith("```"):
        # Remove leading ```lang
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        # Remove trailing ``` if present
        if text.endswith("```"):
            text = text[:-3]
    return text.strip()


def _first_statement(sql_text: str) -> str:
    # Return only the first statement up to the first semicolon; if none, return as is
    semi_index = sql_text.find(";")
    if semi_index != -1:
        return sql_text[:semi_index]
    return sql_text


def security_agent(sql_query: str) -> str:
    # Normalize and sanitize formatting noise from LLMs
    sanitized = _strip_code_fences(sql_query)
    lowered = sanitized.lower()

    # Block comment injection markers
    if "--" in lowered or "/*" in lowered or "*/" in lowered:
        return "❌ Blocked: SQL comments detected!"

    # Extract only the first statement to prevent multiple statements
    single_stmt = _first_statement(sanitized).strip()
    lowered_single = single_stmt.lower()

    # Block destructive DML/DDL
    dangerous_keywords = [" drop ", " delete ", " update ", " insert ", " alter ", " truncate "]
    padded = f" {lowered_single} "
    if any(keyword in padded for keyword in dangerous_keywords):
        return "❌ Blocked: Unsafe SQL detected!"

    return single_stmt
