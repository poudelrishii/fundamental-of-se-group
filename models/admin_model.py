# admin_model.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple
from user_model import User
from student_model import Student, students_from_dicts, students_to_dicts
from subject_model import grade_from_mark  # moved here

def average_mark_for(student: Student) -> float:
    return student.average_mark()

def overall_grade_for(student: Student) -> str:
    avg = int(round(average_mark_for(student)))
    return grade_from_mark(avg)

def has_passed(student: Student) -> bool:
    return student.has_passed()

@dataclass
class Admin(User):
    @staticmethod
    def create(name: str, email: str, password: str) -> "Admin":
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        return Admin(
            id="000000",
            name=name.strip(),
            email=email.strip(),
            password=(password or "").strip(),
            role="admin",
        )

    def list_students(self, raw: List[Dict]) -> List[Dict]:
        students = students_from_dicts(raw)
        out: List[Dict] = []
        for s in students:
            avg = round(average_mark_for(s), 2)
            out.append({
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "subjects_count": len(s.subjects),
                "avg": avg,
                "grade": overall_grade_for(s),
            })
        return out

    def group_by_grade(self, raw: List[Dict]) -> Dict[str, List[Dict]]:
        buckets: Dict[str, List[Dict]] = {"HD": [], "D": [], "C": [], "P": [], "Z": []}
        for s in students_from_dicts(raw):
            buckets[overall_grade_for(s)].append(s.to_dict())
        return buckets

    def partition_pass_fail(self, raw: List[Dict]) -> Dict[str, List[Dict]]:
        res = {"PASS": [], "FAIL": []}
        for s in students_from_dicts(raw):
            (res["PASS"] if has_passed(s) else res["FAIL"]).append(s.to_dict())
        return res

    def remove_student_by_id(self, raw: List[Dict], student_id: str) -> Tuple[List[Dict], bool]:
        sid = (student_id or "").strip()
        students = [s for s in students_from_dicts(raw) if s.id != sid]
        removed = len(students) != len(students_from_dicts(raw))
        return students_to_dicts(students), removed

    def clear_all_students(self, raw: List[Dict]) -> List[Dict]:
        # keep non-student entries if any (e.g., admins) by checking role
        return [d for d in (raw or []) if str(d.get("role", "student")).lower() != "student"]
