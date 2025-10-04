from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

@dataclass
class Employee:
    id: int
    name: str
    department_id: Optional[int] = None

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Department:
    id: int
    name: str
    employees: List[int]

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class AttendanceRecord:
    id: int
    emp_id: int
    date: str          # YYYY-MM-DD
    status: str        # "present" | "absent" | "late"

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class PayrollItem:
    id: int
    emp_id: int
    month: str         # "2025-10"
    base: float
    bonus: float
    deductions: float
    total: float

    def to_dict(self) -> Dict:
        return asdict(self)
