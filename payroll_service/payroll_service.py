import Pyro4
from common.models import PayrollItem
from datetime import datetime

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PayrollService:
    def __init__(self):
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self.notify = Pyro4.Proxy("PYRONAME:NotificationService")

    # def calculate_for_employee(self, emp_id: int, month: str,
    #                            base: float = 3000.0,
    #                            bonus_present: float = 50.0,
    #                            deduction_absent: float = 100.0,
    #                            deduction_late: float = 20.0) -> dict:
    #     emp = self.db.get_employee(emp_id)
    #     if not emp:
    #         return {"error": "Employee not found"}

    #     records = self.db.list_attendance_for_employee(emp_id)
    #     present = sum(1 for r in records if r["status"] == "present" and r["date"].startswith(month))
    #     late    = sum(1 for r in records if r["status"] == "late"    and r["date"].startswith(month))
    #     absent  = sum(1 for r in records if r["status"] == "absent"  and r["date"].startswith(month))

    #     bonus = present * bonus_present
    #     deductions = absent * deduction_absent + late * deduction_late
    #     total = base + bonus - deductions

    #     pid = self.db.next_payroll_id()
    #     item = PayrollItem(id=pid, emp_id=emp_id, month=month,
    #                        base=base, bonus=bonus, deductions=deductions, total=total).to_dict()
    #     self.db.save_payroll(item)
    #     self.notify.send_message(f"[Payroll] Emp {emp_id} {month} total=${total:.2f}")
    #     return item
    
    def calculate_for_employee(self, emp_id: int, month: str,
                           base: float = 3000.0,
                           bonus_present: float = 50.0,
                           deduction_absent: float = 100.0,
                           deduction_late: float = 20.0) -> dict:
        emp = self.db.get_employee(emp_id)
        if not emp:
            return {"error": "Employee not found"}

        records = self.db.list_attendance_for_employee(emp_id)
        present = sum(1 for r in records if r["status"] == "present" and r["date"].startswith(month))
        late    = sum(1 for r in records if r["status"] == "late"    and r["date"].startswith(month))
        absent  = sum(1 for r in records if r["status"] == "absent"  and r["date"].startswith(month))

        bonus = present * bonus_present
        deductions = absent * deduction_absent + late * deduction_late
        total = base + bonus - deductions

        pid = self.db.next_payroll_id()
        item = PayrollItem(
            id=pid,
            emp_id=emp_id,
            month=month,
            base=base,
            bonus=bonus,
            deductions=deductions,
            total=total
        ).to_dict()

    #  Add this line
        item["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.db.save_payroll(item)
        self.notify.send_message(f"[Payroll] Emp {emp_id} {month} total=${total:.2f}")
        return item

    def list_for_employee(self, emp_id: int):
        return self.db.list_payroll_for_employee(emp_id)

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(PayrollService)
    ns.register("PayrollService", uri)
    print("[PayrollService] Ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
