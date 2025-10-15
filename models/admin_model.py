# models/admin_model.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
from models.user_model import User
from models.student_model import Student, students_from_dicts, students_to_dicts
from models.subject_model import grade_from_mark

def overall_grade_for(student: Student) -> str:
    avg = int(round(student.average_mark()))
    return grade_from_mark(avg)

@dataclass
class Admin(User):
    @staticmethod
    def create(name: str, email: str, password: str) -> "Admin":
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        return Admin(id="000000", name=name.strip(), email=email.strip(),
                     password=(password or "").strip(), role="admin")

    def list_students(self, raw: List[Dict]) -> List[Dict]:
        out=[]
        for s in students_from_dicts(raw):
            out.append({
                "id": s.id, "name": s.name, "email": s.email,
                "subjects_count": len(s.subjects),
                "avg": round(s.average_mark(),2),
                "grade": overall_grade_for(s),
            })
        return out

    def group_by_grade(self, raw: List[Dict]) -> Dict[str, List[Dict]]:
        buckets={"HD":[], "D":[], "C":[], "P":[], "Z":[]}
        for s in students_from_dicts(raw):
            buckets[overall_grade_for(s)].append(s.to_dict())
        return buckets

    def partition_pass_fail(self, raw: List[Dict]) -> Dict[str, List[Dict]]:
        res={"PASS":[], "FAIL":[]}
        for s in students_from_dicts(raw):
            (res["PASS"] if s.has_passed() else res["FAIL"]).append(s.to_dict())
        return res

    def remove_student_by_id(self, raw: List[Dict], student_id: str) -> Tuple[List[Dict], bool]:
        sid=(student_id or "").strip()
        students = [s for s in students_from_dicts(raw) if s.id != sid]
        removed = len(students) != len(students_from_dicts(raw))
        return students_to_dicts(students), removed

    def clear_all_students(self, raw: List[Dict]) -> List[Dict]:
        return [d for d in (raw or []) if str(d.get("role","student")).lower()!="student"]
