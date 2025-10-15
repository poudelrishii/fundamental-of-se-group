# models/student_model.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random

from models.user_model import User, gen_student_id
from models.subject_model import Subject, gen_subject_id, grade_from_mark

MAX_SUBJECTS = 4

@dataclass
class Student(User):
    subjects: List[Subject] = field(default_factory=list)

    @staticmethod
    def create(name: str, email: str, password: str) -> "Student":
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        if not User.validate_password(password):
            raise ValueError("Password must start with an uppercase, have ≥5 letters, then ≥3 digits.")
        return Student(
            id=gen_student_id(), name=name.strip(), email=email.strip(),
            password=password.strip(), role="student", subjects=[]
        )

    def enrol_subject(self, title: str) -> Subject:
        if len(self.subjects) >= MAX_SUBJECTS:
            raise ValueError("Cannot enrol in more than four (4) subjects.")
        norm_title = (title or "").strip()
        if not norm_title: raise ValueError("Subject title cannot be empty.")
        if any(s.title.lower()==norm_title.lower() for s in self.subjects):
            raise ValueError("Subject already enrolled.")
        mark = random.randint(25, 100)
        sub = Subject(id=gen_subject_id(), title=norm_title, mark=mark, grade=grade_from_mark(mark))
        self.subjects.append(sub)
        return sub

    def remove_subject(self, subject_id: str) -> bool:
        sid = (subject_id or "").strip()
        for i, s in enumerate(self.subjects):
            if s.id == sid:
                del self.subjects[i]
                return True
        return False

    def change_password(self, new_password: str) -> None:
        if not User.validate_password(new_password):
            raise ValueError("Password must start with an uppercase, have ≥5 letters, then ≥3 digits.")
        self.password = new_password.strip()

    def average_mark(self) -> float:
        if not self.subjects: return 0.0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def has_passed(self) -> bool:
        return self.average_mark() >= 50.0

    def to_dict(self) -> Dict:
        base = super().to_dict()
        base["subjects"] = [s.to_dict() for s in self.subjects]
        base["role"] = "student"
        return base

    @staticmethod
    def from_dict(data: Dict) -> "Student":
        from models.subject_model import Subject  # local import to avoid circular
        return Student(
            id=str(data.get("id","")), name=str(data.get("name","")),
            email=str(data.get("email","")), password=str(data.get("password","")),
            role="student",
            subjects=[Subject.from_dict(d) for d in data.get("subjects", [])]
        )

# DB helpers
def students_from_dicts(raw: List[Dict]) -> List[Student]:
    return [Student.from_dict(d) for d in (raw or []) if str(d.get("role","student")).lower()=="student"]

def students_to_dicts(students: List[Student]) -> List[Dict]:
    return [s.to_dict() for s in students]

def find_student_by_email(students: List[Student], email: str) -> Optional[Student]:
    e = (email or "").strip().lower()
    for s in students:
        if s.email.lower()==e:
            return s
    return None
