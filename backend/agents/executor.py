import os
import sqlite3
import pandas as pd
from typing import Optional, Union


def _connect_sqlite(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def _ensure_sqlite_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            EmployeeID INTEGER PRIMARY KEY,
            BirthDate TEXT,
            FirstName TEXT,
            LastName TEXT,
            Gender TEXT,
            HireDate TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS departments (
            DepartmentID INTEGER PRIMARY KEY,
            DeptName TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dept_emp (
            EmployeeID INTEGER,
            DepartmentID INTEGER,
            FromDate TEXT,
            ToDate TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dept_manager (
            EmployeeID INTEGER,
            DepartmentID INTEGER,
            FromDate TEXT,
            ToDate TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS titles (
            EmployeeID INTEGER,
            Title TEXT,
            FromDate TEXT,
            ToDate TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS salaries (
            EmployeeID INTEGER,
            Salary REAL,
            FromDate TEXT,
            ToDate TEXT
        );
        """
    )
    conn.commit()


def query_executor(sql_query: str, db_path: str = "db/employees.db") -> Union[pd.DataFrame, str]:
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_db = os.getenv("MYSQL_DB")

    try:
        if all([mysql_host, mysql_user, mysql_password, mysql_db]):
            import mysql.connector  # optional dependency
            conn = mysql.connector.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                database=mysql_db,
            )
            try:
                result = pd.read_sql(sql_query, conn)
                return result
            finally:
                conn.close()
        else:
            conn = _connect_sqlite(db_path)
            try:
                _ensure_sqlite_schema(conn)
                result = pd.read_sql_query(sql_query, conn)
                return result
            finally:
                conn.close()
    except Exception as e:
        return f"❌ Execution error: {str(e)}"
