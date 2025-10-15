# controllers/student_controller.py
from typing import Optional
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts, find_student_by_email

class StudentController:
    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    # GUI-friendly login used by ViewModel
    def login(self, email: str, password: str):
        raw = self.db.read_from_file() or []
        students = students_from_dicts(raw)
        student = find_student_by_email(students, email)
        if student and student.verify_password(password):
            print(f"[DEBUG][StudentController] Login success for {email}")
            self.current_student = student
            return True, "student"
        print(f"[DEBUG][StudentController] Login failed for {email}")
        return False, None

    def register(self, name: str, email: str, password: str):
        raw = self.db.read_from_file() or []
        students = students_from_dicts(raw)
        if find_student_by_email(students, email):
            return False, "Student already exists."
        s = Student.create(name, email, password)
        students.append(s)
        self.db.write_to_file(students_to_dicts(students))
        return True, f"Registered {s.name} (ID {s.id})"

    # persistence after mutating current_student
    def save_current(self):
        if not self.current_student: return
        raw = self.db.read_from_file() or []
        students = students_from_dicts(raw)
        for i, s in enumerate(students):
            if s.email == self.current_student.email:
                students[i] = self.current_student
                break
        self.db.write_to_file(students_to_dicts(students))
        print("[DEBUG][StudentController] Saved current student to DB")
