import Pyro4
from common.models import Department

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class DepartmentService:
    def __init__(self):
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self.notify = Pyro4.Proxy("PYRONAME:NotificationService")

    def create_department(self, name: str) -> dict:
        dept_id = self.db.next_department_id()
        dept = Department(id=dept_id, name=name, employees=[]).to_dict()
        self.db.save_department(dept)
        self.notify.send_message(f"[Department] Created {name} (ID={dept_id})")
        return dept

    def list_departments(self):
        return self.db.list_departments()

    def assign_employee(self, emp_id: int, dept_id: int):
        dept = self.db.get_department(dept_id)
        emp = self.db.get_employee(emp_id)
        if not dept: return {"error": "Department not found"}
        if not emp:  return {"error": "Employee not found"}

        if emp_id not in dept["employees"]:
            dept["employees"].append(emp_id)
        self.db.save_department(dept)

        emp["department_id"] = dept_id
        self.db.save_employee(emp)

        self.notify.send_message(f"[Department] Assigned Emp {emp_id} to Dept {dept_id}")
        return {"ok": True, "department": dept, "employee": emp}
    
    def delete_department(self, dept_id: int) -> dict:
        """Delete a department by ID."""
        dept = self.db.get_department(dept_id)
        if not dept:
            return {"error": f"Department {dept_id} not found"}
        self.db.delete_department(dept_id)
        return {"message": f"Department {dept_id} deleted successfully"}


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(DepartmentService)
    ns.register("DepartmentService", uri)
    print("[DepartmentService] Ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
