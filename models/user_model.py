# models/user_model.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Literal
import re, random

Role = Literal["student", "admin"]
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@university\.com$")
PWD_RE   = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")

def gen_student_id() -> str:
    return f"{random.randint(1, 999_999):06d}"

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    role: Role = "student"

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(EMAIL_RE.match((email or "").strip()))

    @staticmethod
    def validate_password(password: str) -> bool:
        return bool(PWD_RE.match((password or "").strip()))

    def verify_password(self, password: str) -> bool:
        return self.password == (password or "").strip()

    @staticmethod
    def create_student(name: str, email: str, password: str) -> "User":
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        if not User.validate_password(password):
            raise ValueError("Password must start with an uppercase, have ≥5 letters, then ≥3 digits.")
        return User(id=gen_student_id(), name=name.strip(), email=email.strip(),
                    password=password.strip(), role="student")

    @staticmethod
    def create_admin(name: str, email: str, password: str) -> "User":
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        return User(id="000000", name=name.strip(), email=email.strip(),
                    password=(password or "").strip(), role="admin")

    def to_dict(self) -> Dict: return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "User":
        return User(
            id=str(data.get("id","")), name=str(data.get("name","")),
            email=str(data.get("email","")), password=str(data.get("password","")),
            role=str(data.get("role","student"))
        )

    @property
    def is_admin(self) -> bool: return self.role == "admin"
    @property
    def is_student(self) -> bool: return self.role == "student"
