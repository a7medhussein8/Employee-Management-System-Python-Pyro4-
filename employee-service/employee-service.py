import Pyro4
from common.models import Employee

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class EmployeeService:
    def __init__(self):
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self.notify = Pyro4.Proxy("PYRONAME:NotificationService")

    def create_employee(self, name: str, department_id: int | None = None) -> dict:
        emp_id = self.db.next_employee_id()
        emp = Employee(id=emp_id, name=name, department_id=department_id).to_dict()
        self.db.save_employee(emp)
        self.notify.send_message(f"[Employee] Created {name} (ID={emp_id})")
        return emp

    def get_employee(self, emp_id: int):
        return self.db.get_employee(emp_id) or {"error": "Employee not found"}

    def list_employees(self):
        return self.db.list_employees()

    def update_department(self, emp_id: int, department_id: int):
        emp = self.db.get_employee(emp_id)
        if not emp: return {"error": "Employee not found"}
        emp["department_id"] = department_id
        self.db.save_employee(emp)
        self.notify.send_message(f"[Employee] {emp_id} moved to department {department_id}")
        return emp

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(EmployeeService)
    ns.register("EmployeeService", uri)
    print("[EmployeeService] Ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
