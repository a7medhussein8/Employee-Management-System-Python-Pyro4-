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

@app.route("/employee/delete/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    try:
        with Pyro4.Proxy("PYRONAME:EmployeeService") as emp:
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

    
@app.route("/department/delete/<int:dept_id>", methods=["DELETE"])
def delete_department(dept_id):
    try:
        with Pyro4.Proxy("PYRONAME:DepartmentService") as dept:
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


@app.route("/payroll/calc", methods=["POST"])
def calc_payroll():
    """Calculate payroll for a given employee and month."""
    try:
        data = request.get_json()
        emp_id = int(data.get("emp_id"))
        month = data.get("month", "")
        base = float(data.get("salary", 0))
        bonus = float(data.get("bonus", 0))

        with Pyro4.Proxy("PYRONAME:PayrollService") as payroll:
            result = payroll.calculate_for_employee(emp_id, month, base, bonus)
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/payroll/history/<int:emp_id>", methods=["GET"])
def get_payroll_history(emp_id):
    try:
        with Pyro4.Proxy("PYRONAME:PayrollService") as payroll:
            result = payroll.list_for_employee(emp_id)
            
            # Normalize field names for frontend
            normalized = []
            for r in result:
                normalized.append({
                    "date": r.get("date") or r.get("created_at") or "-",
                    "month": r.get("month"),
                    "base": r.get("base"),
                    "bonus": r.get("bonus"),
                    "total": r.get("total")
                })
            return jsonify(normalized)
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
