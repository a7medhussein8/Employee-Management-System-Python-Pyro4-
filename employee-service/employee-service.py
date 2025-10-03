import Pyro4

@Pyro4.expose
class EmployeeService:
    def __init__(self):
        # Instead of storing locally, we'll use Database + Notification
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self.notify = Pyro4.Proxy("PYRONAME:NotificationService")

    def create_employee(self, name, department=None):
        emp_id = self.db.get_next_employee_id()
        employee = {"id": emp_id, "name": name, "department": department}
        
        # Save in database
        self.db.save_employee(employee)
        
        # Notify
        self.notify.send_message(f"Employee {name} created with ID {emp_id}")
        
        return f"Employee {name} created successfully (ID={emp_id})"

    def get_employee(self, emp_id):
        return self.db.load_employee(emp_id)

    def update_department(self, emp_id, department):
        emp = self.db.load_employee(emp_id)
        if emp == "Employee not found":
            return emp
        emp["department"] = department
        self.db.save_employee(emp)
        self.notify.send_message(f"Employee {emp_id} moved to {department} department")
        return f"Employee {emp_id} updated to department {department}"

# Run service
daemon = Pyro4.Daemon()
uri = daemon.register(EmployeeService)
print("EmployeeService is ready. URI:", uri)
daemon.requestLoop()
