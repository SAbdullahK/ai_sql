from flask import Flask, request, jsonify
from agents.query_generator import query_generator
from agents.validator import query_validator
from agents.security import security_agent
from agents.optimizer import query_optimizer
from agents.executor import query_executor
from agents.answer_formatter import answer_formatter

app = Flask(__name__)

def multi_agent_system(user_query: str, schema: str, db_path: str = "db/employees.db"):
    sql_query = query_generator(user_query,schema)
    print("📝 Generated SQL: ", sql_query)

    validated_sql = query_validator(sql_query, schema)
    print("✅ Validated SQL: ", validated_sql)

    safe_sql = security_agent(validated_sql)
    if isinstance(safe_sql, str) and "❌" in safe_sql:
        return safe_sql
    print("🔒 Safe SQL: ", safe_sql)

    optimized_sql = query_optimizer(safe_sql)
    print("⚡ Optimized SQL: ", optimized_sql)

    result = query_executor(optimized_sql, db_path)
    print("📊 Raw Result: ", result)

    final_answer = answer_formatter(user_query, optimized_sql, result)
    return final_answer


# Flask API endpoint
@app.route("/ask", methods=["POST"])
def ask_sql():
    data = request.get_json()
    user_query = data.get("query")

    schema ="""
    Tables:
    - employees(EmployeeID, BirthDate, FirstName, LastName, Gender, HireDate)
    - departments(DepartmentID, DeptName)
    - dept_emp(EmployeeID, DepartmentID, FromDate, ToDate)
    - dept_manager(EmployeeID, DepartmentID, FromDate, ToDate)
    - titles(EmployeeID, Title, FromDate, ToDate)
    - salaries(EmployeeID, Salary, FromDate, ToDate)
    """

    answer = multi_agent_system(user_query, schema)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
