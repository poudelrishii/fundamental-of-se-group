# view_models/login_view_model.py
import re
from models.user_model import EMAIL_RE, PWD_RE
from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController

class LoginViewModel:
    def __init__(self, db):
        self.username = ""
        self.password = ""
        # compose controllers (no UI here)
        self.student_controller = StudentController(db)
        self.admin_controller = AdminController(db)

    def set_credentials(self, username, password):
        self.username = (username or "").strip()
        self.password = (password or "").strip()

    def validate_credentials(self):
        if not self.username or not self.password:
            return False, "Email and password cannot be empty."
        if not re.match(EMAIL_RE, self.username):
            return False, "Email must end with @university.com."
        if not re.match(PWD_RE, self.password):
            return False, "Password must start with an uppercase, have ≥5 letters, then ≥3 digits."
        return True, "OK"

    def login(self):
        # try admin first (predefined), then students
        ok, role = self.admin_controller.login(self.username, self.password)
        if ok:
            return True, {"message": "Welcome Admin!", "role": role}

        ok, role = self.student_controller.login(self.username, self.password)
        if ok:
            return True, {"message": "Welcome!", "role": role}

        return False, {"message": "Invalid email or password.", "role": None}
