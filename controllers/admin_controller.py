# controllers/admin_controller.py
from db.database import Database
from models.admin_model import Admin

class AdminController:
    def __init__(self, db: Database):
        self.db = db
        # preload a default admin identity for controller usage
        self.admin = Admin.create("System Admin", "admin@university.com", "AdminPass123")

    def login(self, email: str, password: str):
        if email.strip().lower()=="admin@university.com" and self.admin.verify_password(password):
            print("[DEBUG][AdminController] Admin login success")
            return True, "admin"
        print("[DEBUG][AdminController] Admin login failed")
        return False, None

    def list_students(self):
        return self.admin.list_students(self.db.read_from_file() or [])

    def group_by_grade(self):
        return self.admin.group_by_grade(self.db.read_from_file() or [])

    def partition_pass_fail(self):
        return self.admin.partition_pass_fail(self.db.read_from_file() or [])

    def remove_student_by_id(self, student_id: str):
        raw = self.db.read_from_file() or []
        new_raw, removed = self.admin.remove_student_by_id(raw, student_id)
        if removed: self.db.write_to_file(new_raw)
        return removed

    def clear_all_students(self):
        cleared = self.admin.clear_all_students(self.db.read_from_file() or [])
        self.db.write_to_file(cleared)
        return True
