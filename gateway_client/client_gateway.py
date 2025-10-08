import Pyro4

def main():
    # Proxies
    db   = Pyro4.Proxy("PYRONAME:DatabaseService")
    emp  = Pyro4.Proxy("PYRONAME:EmployeeService")
    dept = Pyro4.Proxy("PYRONAME:DepartmentService")
    att  = Pyro4.Proxy("PYRONAME:AttendanceService")
    pay  = Pyro4.Proxy("PYRONAME:PayrollService")
    note = Pyro4.Proxy("PYRONAME:NotificationService")

    # Demo flow
    print("== Create Department ==")
    d = dept.create_department("Engineering")
    print(d)

    print("== Create Employee ==")
    e = emp.create_employee("Amro", department_id=d["id"])
    print(e)

    print("== Assign Employee (again, idempotent) ==")
    print(dept.assign_employee(e["id"], d["id"]))

    print("== Mark Attendance ==")
    print(att.mark(e["id"], "2025-10-03", "present"))
    print(att.mark(e["id"], "2025-10-04", "late"))
    print(att.mark(e["id"], "2025-10-05", "absent"))

    print("== Payroll Calc (month=2025-10) ==")
    print(pay.calculate_for_employee(e["id"], "2025-10"))

    print("== Notifications (recent) ==")
    print(note.recent())

if __name__ == "__main__":
    main()
