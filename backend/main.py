from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.query_generator import query_generator
from agents.validator import query_validator
from agents.security import security_agent
from agents.executor import query_executor
from agents.answer_formatter import answer_formatter

app = Flask(__name__)
CORS(app)

def multi_agent_system(user_query: str, schema: str):
    # Step 1: Generate SQL
    sql_query = query_generator(user_query, schema)
    print("📝 Generated SQL:", sql_query)

    # Step 2: Validate SQL
    validated_sql = query_validator(sql_query, schema)
    print("✅ Validated SQL:", validated_sql)

    # Step 3: Security check
    safe_sql = security_agent(validated_sql)
    if "❌" in safe_sql:
        return safe_sql
    print("🔒 Safe SQL:", safe_sql)

    # Step 4: Execute SQL
    try:
        result = query_executor(safe_sql)
        print("📊 Raw Result:", result)
    except Exception as e:
        print("❌ Error in query_executor:", str(e))
        return f"Execution failed: {str(e)}"

    # Step 5: Format Answer
    try:
        final_answer = answer_formatter(user_query, safe_sql, result)
        print("🎯 Final Answer:", final_answer)
        return final_answer
    except Exception as e:
        print("❌ Error in answer_formatter:", str(e))
        return f"Formatting failed: {str(e)}"


# Flask API endpoint
@app.route("/ask", methods=["POST"])
def ask_sql():
    data = request.get_json()
    user_query = data.get("query")  # 👈 make sure frontend sends "query"

    schema = """
    Tables:
    - employees(EmployeeID, BirthDate, FirstName, LastName, Gender, HireDate)
    - departments(DepartmentID, DeptName)
    - dept_emp(EmployeeID, DepartmentID, FromDate, ToDate)
    - dept_manager(EmployeeID, DepartmentID, FromDate, ToDate)
    - titles(EmployeeID, Title, FromDate, ToDate)
    - salaries(EmployeeID, Salary, FromDate, ToDate)
    """

    answer = multi_agent_system(user_query, schema)
    print("🎯 Final Answer Sent:", answer)

    return jsonify({
        "answer": str(answer) if answer else "⚠️ No answer generated"
    })


if __name__ == "__main__":
    app.run(debug=True)











#from flask import Flask, request, jsonify
# from flask_cors import CORS
# from agents.query_generator import query_generator
# from agents.validator import query_validator
# from agents.security import security_agent
# from agents.optimizer import query_optimizer
# from agents.executor import query_executor
# from agents.answer_formatter import answer_formatter

# app = Flask(__name__)
# CORS(app)

# def multi_agent_system(user_query : str, schema : str):
#     sql_query = query_generator(user_query,schema)
#     print("📝 Generated SQL: ", sql_query)

#     validated_sql = query_validator(sql_query, schema)
#     print("✅ Validated SQL: ", validated_sql)

#     safe_sql = security_agent(validated_sql)
#     if "❌" in safe_sql:
#         return safe_sql
#     print("🔒 Safe SQL: ", safe_sql)

#     # optimized_sql = query_optimizer(safe_sql)
#     # print("⚡ Optimized SQL: ", optimized_sql)

#     try:
#         result = query_executor(safe_sql)
#         print("📊 Raw Result: ", result)
#     except Exception as e:
#         print("❌ Error in query_executor:", str(e))
#         return f"Execution failed: {str(e)}"

#     try:
#         final_answer = answer_formatter(user_query, optimized_sql, result)
#         print("🎯 Final Answer:", final_answer)
#         return final_answer
#     except Exception as e:
#         print("❌ Error in answer_formatter:", str(e))
#         return f"Formatting failed: {str(e)}"



# # Flask API endopint
# @app.route("/ask", methods=["POST"])
# def ask_sql():
#     data = request.get_json()
#     user_query = data.get("query")

#     schema ="""
#     Tables:
#     - employees(EmployeeID, BirthDate, FirstName, LastName, Gender, HireDate)
#     - departments(DepartmentID, DeptName)
#     - dept_emp(EmployeeID, DepartmentID, FromDate, ToDate)
#     - dept_manager(EmployeeID, DepartmentID, FromDate, ToDate)
#     - titles(EmployeeID, Title, FromDate, ToDate)
#     - salaries(EmployeeID, Salary, FromDate, ToDate)
#     """

#     answer = multi_agent_system(user_query, schema)
#     print("🎯 Final Answer Sent:", answer)

#     # Make sure it's always a string
#     return jsonify({
#         "answer": str(answer) if answer else "⚠️ No answer generated"
#     })



# if __name__ == "__main__" :
#     app.run(debug = True)