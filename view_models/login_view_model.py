from db.database import Database

class LoginViewModel:
    def __init__(self, db):
        """
        ViewModel responsible for validating and authenticating login attempts.
        It interacts directly with the Database to check user credentials.
        """
        self.username = ""
        self.password = ""
        self.db = db

    def set_credentials(self, username: str, password: str):
        self.username = username.strip()
        self.password = password.strip()

    def validate_credentials(self):
        if not self.username or not self.password:
            return False, "Username and password cannot be empty."
        return True, "Valid credentials."

    def login(self):
        if self.db is None:
            return False, "Database not initialised (db is None)."

        users = self.db.read_from_file() or []
        for s in users:
            if s.get("email") == self.username and s.get("password") == self.password:
                return True, f"Welcome {s.get('name','')}!"
        return False, "Invalid email or password."

        return False, "Incorrect username or password."

    def load_users(self, user_dict):
        """
        Injects user data from any source.
        Expected format: { "username1": "password1", "username2": "password2", ... }
        """
        if isinstance(user_dict, dict):
            self._user_store = {
                str(k).strip(): str(v).strip()
                for k, v in user_dict.items()
                if k and v
            }
