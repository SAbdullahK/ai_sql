import os
import mysql.connector
import pandas as pd


def query_executor(sql_query: str, db_path="db/employees.db") :
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "abdullah",
            database = "employees",
        )
        result = pd.read_sql(sql_query, conn)
        conn.close()
        return result
    except Exception as e:
        return f"❌ Execution error: {str(e)}"
