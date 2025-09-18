import os
import mysql.connector
import pandas as pd


# def query_executor(sql_query: str, db_path="db/employees.db") :
#     try:
#         conn = mysql.connector.connect(
#             host = "localhost",
#             user = "root",
#             password = "abdullah",
#             database = "employees",
#         )
#         result = pd.read_sql(sql_query, conn)
#         conn.close()
#         return result
#     except Exception as e:
#         return f"❌ Execution error: {str(e)}"


# agents/executor.py
# def query_executor(sql_query: str):
#     try:
#         # clean ```sql fences
#         clean_sql = sql_query.strip().replace("```sql", "").replace("```", "")
#         print("🧹 Clean Query to Execute:", clean_sql)

#         # # connect + execute
#         # import mysql.connector
#         # conn = mysql.connector.connect(
#         #     host="localhost",
#         #     user="root",
#         #     password="your_password",
#         #     database="employees"
#         # )
#         # cursor = conn.cursor(dictionary=True)
#         # cursor.execute(clean_sql)

#         # rows = cursor.fetchall()
#         try:
#             conn = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="abdullah",   # <-- use your real password
#                 database="employees"
#             )
#             print("✅ Connected to DB")
#             cursor = conn.cursor()
#             cursor.execute("SHOW TABLES;")
#             for row in cursor.fetchall():
#                 print("📂", row)
#             cursor.close()
#             conn.close()
#         except Exception as e:
#             print("❌ DB Connection failed:", e)
#             print("📊 Raw Result inside executor:", rows)  # <--- add this

#         cursor.close()
#         conn.close()
#         return rows
#     except Exception as e:
#         print("❌ Executor error:", str(e))
#         raise

import mysql.connector

def query_executor(sql_query: str):
    try:
        # 🧹 Clean query
        clean_sql = sql_query.strip().replace("```sql", "").replace("```", "")
        print("🧹 Clean Query to Execute:", clean_sql)

        # ✅ Connect to DB
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abdullah",   # <-- your real password
            database="employees"
        )
        print("✅ Connected to DB")

        # ▶️ Execute query
        cursor = conn.cursor(dictionary=True)
        cursor.execute(clean_sql)

        # 📊 Fetch results
        rows = cursor.fetchall()
        print("📊 Raw Result inside executor:", rows)

        # 🔒 Cleanup
        cursor.close()
        conn.close()

        return rows

    except Exception as e:
        print("❌ Execution error in query_executor:", e)
        raise   # don’t hide errors anymore!

