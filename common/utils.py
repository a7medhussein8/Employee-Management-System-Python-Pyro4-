import threading
import json
from pathlib import Path
from typing import Dict, Any

class JSONStore:
    """
    Thread-safe JSON file read/write (tiny KV-ish store).
    Structure:
    {
      "employees": { "1": {...}, ... },
      "departments": { "10": {...} },
      "attendance": { "100": {...} },
      "payroll": { "200": {...} },
      "counters": { "employee": 1, "department": 1, "attendance": 1, "payroll": 1 }
    }
    """
    def __init__(self, file_path: str):
        self.fp = Path(file_path)
        self.lock = threading.Lock()
        if not self.fp.exists():
            self._init_file()

    def _init_file(self):
        data = {
            "employees": {},
            "departments": {},
            "attendance": {},
            "payroll": {},
            "counters": {"employee": 1, "department": 1, "attendance": 1, "payroll": 1},
            "notifications": []
        }
        self.fp.parent.mkdir(parents=True, exist_ok=True)
        self.fp.write_text(json.dumps(data, indent=2))

    def read(self) -> Dict[str, Any]:
        with self.lock:
            return json.loads(self.fp.read_text())

    def write(self, data: Dict[str, Any]):
        with self.lock:
            self.fp.write_text(json.dumps(data, indent=2))
