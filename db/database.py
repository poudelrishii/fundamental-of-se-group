# db/database.py
import os
import pickle

class Database:
    def __init__(self):
        # assignment requires students.data in a db/ folder
        os.makedirs("db", exist_ok=True)
        self.path = os.path.join("db", "students.data")
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.path):
            print(f"[DEBUG][DB] Creating new data file at {self.path}")
            with open(self.path, "wb") as f:
                pickle.dump([], f)

    def read_from_file(self):
        try:
            with open(self.path, "rb") as f:
                data = pickle.load(f)
                print(f"[DEBUG][DB] Read {len(data)} records from {self.path}")
                return data
        except Exception as e:
            print(f"[ERROR][DB] Failed reading {self.path}: {e}")
            return []

    # backward-compat alias (some older code called this)
    def read_data(self):
        return self.read_from_file()

    def write_to_file(self, data_list):
        try:
            with open(self.path, "wb") as f:
                pickle.dump(list(data_list or []), f)
            print(f"[DEBUG][DB] Wrote {len(data_list or [])} records to {self.path}")
        except Exception as e:
            print(f"[ERROR][DB] Failed writing {self.path}: {e}")

    def clear_all(self):
        self.write_to_file([])
        print("[DEBUG][DB] Cleared all records")
