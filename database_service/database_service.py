# import Pyro4
# from common.utils import JSONStore

# @Pyro4.expose
# @Pyro4.behavior(instance_mode="single")
# class DatabaseService:
#     # def __init__(self, db_file="data/db.json"):
#     #     self.store = JSONStore(db_file)
        
#     def __init__(self):
#         self.store = JSONStore("database.json")
#         data = self.store.read()
#         for key in ("employees", "departments", "attendance", "payroll"):
#             if key not in data:
#                 data[key] = {}
#         self.store.write(data)


#     # ---------- ID counters ----------
#     def _next(self, key: str) -> int:
#         data = self.store.read()
#         data["counters"][key] += 1
#         self.store.write(data)
#         return data["counters"][key] - 1

#     def next_employee_id(self) -> int:  return self._next("employee")
#     def next_department_id(self) -> int: return self._next("department")
#     def next_attendance_id(self) -> int: return self._next("attendance")
#     def next_payroll_id(self) -> int:    return self._next("payroll")

#     # ---------- Employees ----------
#     def save_employee(self, emp: dict):
#         data = self.store.read()
#         data["employees"][str(emp["id"])] = emp
#         self.store.write(data)

#     def get_employee(self, emp_id: int):
#         return self.store.read()["employees"].get(str(emp_id))

#     def list_employees(self):
#         return list(self.store.read()["employees"].values())

#     # ---------- Departments ----------
#     def save_department(self, dept: dict):
#         data = self.store.read()
#         data["departments"][str(dept["id"])] = dept
#         self.store.write(data)

#     def get_department(self, dept_id: int):
#         return self.store.read()["departments"].get(str(dept_id))

#     def list_departments(self):
#         return list(self.store.read()["departments"].values())

#     # ---------- Attendance ----------
#     # def save_attendance(self, rec: dict):
#     #     data = self.store.read()
#     #     data["attendance"][str(rec["id"])] = rec
#     #     self.store.write(data)

#     # def list_attendance_for_employee(self, emp_id: int):
#     #     all_rec = self.store.read()["attendance"].values()
#     #     return [r for r in all_rec if int(r["emp_id"]) == int(emp_id)]

#     def save_attendance(self, rec: dict):
#         data = self.store.read()
#         # ensure attendance key exists
#         if "attendance" not in data:
#             data["attendance"] = {}
#         data["attendance"][str(rec["id"])] = rec
#         self.store.write(data)

#     def list_attendance_for_employee(self, emp_id: int):
#         data = self.store.read()
#         all_rec = data.get("attendance", {}).values()  # safe access
#         return [r for r in all_rec if int(r["emp_id"]) == int(emp_id)]


#     # ---------- Payroll ----------
#     def save_payroll(self, item: dict):
#         data = self.store.read()
#         data["payroll"][str(item["id"])] = item
#         self.store.write(data)

#     # def list_payroll_for_employee(self, emp_id: int):
#     #     all_items = self.store.read()["payroll"].values()
#     #     return [p for p in all_items if int(p["emp_id"]) == int(emp_id)]
    
#     def list_payroll_for_employee(self, emp_id: int):
#         data = self.store.read()
#         all_items = data.get("payroll", {}).values()  # safer
#         return [p for p in all_items if int(p["emp_id"]) == int(emp_id)]


#     # ---------- Notifications storage (optional central store) ----------
#     def append_notification(self, msg: str):
#         data = self.store.read()
#         data["notifications"].append(msg)
#         self.store.write(data)

#     def list_notifications(self):
#         return self.store.read().get("notifications", [])

# def main():
#     daemon = Pyro4.Daemon()
#     ns = Pyro4.locateNS()
#     uri = daemon.register(DatabaseService)
#     ns.register("DatabaseService", uri)
#     print("[DatabaseService] Ready.")
#     daemon.requestLoop()

# if __name__ == "__main__":
#     main()


import Pyro4
from pymongo import MongoClient

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class DatabaseService:
    def __init__(self):
        # Connect to local MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["emsdb"]  # database name
        print("[DatabaseService] Connected to MongoDB")

    # ---------- ID counters ----------
    def next_employee_id(self) -> int:
        return self._next("employee")

    def next_department_id(self) -> int:
        return self._next("department")

    def next_attendance_id(self) -> int:
        return self._next("attendance")

    def next_payroll_id(self) -> int:
        return self._next("payroll")

    def _next(self, key: str) -> int:
        counters = self.db["counters"]
        result = counters.find_one_and_update(
            {"_id": key}, {"$inc": {"value": 1}}, upsert=True, return_document=True
        )
        return result["value"]

    # ---------- Employees ----------
    def save_employee(self, emp: dict):
        self.db["employees"].replace_one({"id": emp["id"]}, emp, upsert=True)

    def get_employee(self, emp_id: int):
        return self.db["employees"].find_one({"id": emp_id}, {"_id": 0})

    def list_employees(self):
        return list(self.db["employees"].find({}, {"_id": 0}))
    
    def delete_employee(self, emp_id: int):
        self.db["employees"].delete_one({"id": emp_id})


    # ---------- Departments ----------
    def save_department(self, dept: dict):
        self.db["departments"].replace_one({"id": dept["id"]}, dept, upsert=True)

    def get_department(self, dept_id: int):
        return self.db["departments"].find_one({"id": dept_id}, {"_id": 0})

    def list_departments(self):
        return list(self.db["departments"].find({}, {"_id": 0}))
    
    def delete_department(self, dept_id: int):
        self.db["departments"].delete_one({"id": dept_id})


    # ---------- Attendance ----------
    def save_attendance(self, rec: dict):
        self.db["attendance"].replace_one({"id": rec["id"]}, rec, upsert=True)

    def list_attendance_for_employee(self, emp_id: int):
        return list(self.db["attendance"].find({"emp_id": emp_id}, {"_id": 0}))

    # ---------- Payroll ----------
    def save_payroll(self, item: dict):
        self.db["payroll"].replace_one({"id": item["id"]}, item, upsert=True)

    def list_payroll_for_employee(self, emp_id: int):
        return list(self.db["payroll"].find({"emp_id": emp_id}, {"_id": 0}))

    # ---------- Notifications ----------
    def append_notification(self, msg: str):
        self.db["notifications"].insert_one({"msg": msg})

    def list_notifications(self):
        notes = list(self.db["notifications"].find({}, {"_id": 0, "msg": 1}))
        return [n["msg"] for n in notes]

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(DatabaseService)
    ns.register("DatabaseService", uri)
    print("[DatabaseService] Ready with MongoDB backend.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
