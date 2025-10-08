from flask import Flask, jsonify, request
from flask_cors import CORS
import Pyro4

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Connect to Pyro4 services
emp = Pyro4.Proxy("PYRONAME:EmployeeService")
dept = Pyro4.Proxy("PYRONAME:DepartmentService")
att = Pyro4.Proxy("PYRONAME:AttendanceService")
pay = Pyro4.Proxy("PYRONAME:PayrollService")
note = Pyro4.Proxy("PYRONAME:NotificationService")

# ---------------------------------------------------------------------
# EMPLOYEE ROUTES
# ---------------------------------------------------------------------

@app.route("/employees", methods=["GET"])
def list_employees():
    """List all employees"""
    try:
        return jsonify(emp.list_employees())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/employees", methods=["POST"])
def create_employee():
    """Create a new employee"""
    try:
        data = request.json
        name = data.get("name")
        department_id = data.get("department_id")
        result = emp.create_employee(name, department_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    """Delete an employee"""
    try:
        result = emp.delete_employee(emp_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------
# DEPARTMENT ROUTES
# ---------------------------------------------------------------------

@app.route("/departments", methods=["GET"])
def list_departments():
    """List all departments"""
    try:
        return jsonify(dept.list_departments())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/departments", methods=["POST"])
def create_department():
    """Create a new department"""
    try:
        data = request.json
        name = data.get("name")
        result = dept.create_department(name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/departments/<int:dept_id>", methods=["DELETE"])
def delete_department(dept_id):
    """Delete a department"""
    try:
        result = dept.delete_department(dept_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------
# ATTENDANCE ROUTES
# ---------------------------------------------------------------------

@app.route("/attendance", methods=["POST"])
def mark_attendance():
    """Mark attendance for an employee"""
    try:
        data = request.json
        emp_id = data.get("emp_id")
        date = data.get("date")
        status = data.get("status")
        result = att.mark(emp_id, date, status)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/attendance/<int:emp_id>", methods=["GET"])
def get_attendance(emp_id):
    """Retrieve attendance records for an employee"""
    try:
        result = att.list_records(emp_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------
# PAYROLL ROUTES
# ---------------------------------------------------------------------


@app.route("/payroll/history/<int:emp_id>", methods=["GET"])
def list_payroll(emp_id):
    """Return all previous payrolls for a specific employee"""
    try:
        result = pay.list_for_employee(emp_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/payroll/<int:emp_id>/<month>", methods=["GET"])
def calc_payroll(emp_id, month):
    """Calculate payroll for a given employee and month"""
    try:
        result = pay.calculate_for_employee(emp_id, month)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------
# NOTIFICATION ROUTES
# ---------------------------------------------------------------------

@app.route("/notifications", methods=["GET"])
def list_notifications():
    """List recent notifications"""
    try:
        return jsonify(note.recent())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------
# GLOBAL ERROR HANDLER
# ---------------------------------------------------------------------

@app.errorhandler(Exception)
def handle_exception(e):
    """Catch-all for unhandled errors"""
    return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------

if __name__ == "__main__":
    print("🚀 Flask Gateway running on http://localhost:5000")
    app.run(port=5000, debug=True)
