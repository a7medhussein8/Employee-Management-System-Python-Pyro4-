import Pyro4
from common.models import PayrollItem
from datetime import datetime

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PayrollService:
    def __init__(self):
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self.notify = Pyro4.Proxy("PYRONAME:NotificationService")
    
    
    def calculate_for_employee(
        self,
        emp_id: int,
        month: str,
        base: float = 3000.0,
        bonus_present: float = 50.0,
        deduction_absent: float = 100.0,
        deduction_late: float = 20.0
    ) -> dict:
        """Calculate payroll for an employee based on attendance data."""

        # --- 1️⃣ Validate Employee ---
        emp = self.db.get_employee(emp_id)
        if not emp:
            return {"error": f"Employee {emp_id} not found"}

        # --- 2️⃣ Load Attendance Records ---
        records = self.db.list_attendance_for_employee(emp_id)
        present = sum(1 for r in records if r["status"] == "present" and r["date"].startswith(month))
        late = sum(1 for r in records if r["status"] == "late" and r["date"].startswith(month))
        absent = sum(1 for r in records if r["status"] == "absent" and r["date"].startswith(month))

        # --- 3️⃣ Compute Components ---
        bonus = present * bonus_present
        deductions = absent * deduction_absent + late * deduction_late
        total = base + bonus - deductions

        # --- 4️⃣ Build Payroll Record ---
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

        # Add timestamp
        item["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- 5️⃣ Save & Notify ---
        self.db.save_payroll(item)
        self.notify.send_message(f"[Payroll] Employee {emp_id} ({month}) total = ${total:.2f}")

        print(f"[DEBUG] Payroll calculated for Emp {emp_id}: {item}")  # ✅ for debug tracking
        return item

    def list_for_employee(self, emp_id: int):
        """List all previous payrolls for a given employee."""
        data = self.db.list_payroll_for_employee(emp_id)
        # Ensure consistent structure
        for rec in data:
            rec.setdefault("date", "-")
            rec.setdefault("month", "-")
            rec.setdefault("base", 0)
            rec.setdefault("bonus", 0)
            rec.setdefault("deductions", 0)
            rec.setdefault("total", 0)
        return data


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(PayrollService)
    ns.register("PayrollService", uri)
    print("[PayrollService] Ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
