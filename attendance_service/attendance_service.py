import Pyro4
from common.models import AttendanceRecord

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class AttendanceService:
    def __init__(self):
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self.notify = Pyro4.Proxy("PYRONAME:NotificationService")

    def mark(self, emp_id: int, date: str, status: str) -> dict:
        if status not in ("present", "absent", "late"):
            return {"error": "Invalid status"}
        if not self.db.get_employee(emp_id):
            return {"error": "Employee not found"}

        rec_id = self.db.next_attendance_id()
        rec = AttendanceRecord(id=rec_id, emp_id=emp_id, date=date, status=status).to_dict()
        self.db.save_attendance(rec)
        self.notify.send_message(f"[Attendance] Emp {emp_id} marked {status} on {date}")
        return rec

    # def report_for_employee(self, emp_id: int):
    #     return self.db.list_attendance_for_employee(emp_id)
    
    def list_records(self, emp_id: int):
        return self.db.list_attendance_for_employee(emp_id)


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(AttendanceService)
    ns.register("AttendanceService", uri)
    print("[AttendanceService] Ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
