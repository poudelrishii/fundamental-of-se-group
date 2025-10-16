# controllers/student_controller.py
from __future__ import annotations

from typing import Optional, Tuple, List, Any

from db.database import Database
from models.student_model import (
    Student,
    students_from_dicts,
    students_to_dicts,
    find_student_by_email,
)
from models.user_model import User


class StudentController:
    """
    Handles student account management and persistence in the Enrollment System.

    Responsibilities:
    - Authenticate (login/logout)
    - Register new students (with validation via model)
    - Load/save the current logged-in student
    - Subject operations (enrol/remove)
    - Password change (validated by model)
    - Expose read-only info (subjects, stats)

    Conventions:
    - Returns (success: bool, payload_or_message: Any) where appropriate.
    - Uses [DEBUG]/[ERROR] print logs for transparency (same as AdminController).
    """

    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    # -------------------------------------------------------------------------
    # Auth
    # -------------------------------------------------------------------------
    def login(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticate a student by email/password. Sets current_student on success.

        Returns:
            (True, "student") on success
            (False, None) on failure
        """
        email_norm = (email or "").strip().lower()
        print(f"[DEBUG][StudentController.login] Attempting login for: {email_norm}")

        try:
            raw = self.db.read_from_file()
        except Exception as ex:
            print(f"[ERROR][StudentController.login] Read DB failed: {ex}")
            return False, None

        students = students_from_dicts(raw)
        student = find_student_by_email(students, email_norm)
        if not student:
            print("[DEBUG][StudentController.login] Student not found.")
            return False, None

        if not student.verify_password(password):
            print("[DEBUG][StudentController.login] Password mismatch.")
            return False, None

        self.current_student = student
        print(f"[DEBUG][StudentController.login] Login successful: {student.email}")
        return True, "student"

    def logout(self) -> None:
        """
        Clears current session.
        """
        if self.current_student:
            print(f"[DEBUG][StudentController.logout] Logging out: {self.current_student.email}")
        self.current_student = None

    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------
    def register(self, name: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Registers a new student after validation.

        Returns:
            (True, "Registered successfully.") on success
            (False, reason) on failure
        """
        email_norm = (email or "").strip().lower()
        print(f"[DEBUG][StudentController.register] Registering: name='{name}', email='{email_norm}'")

        try:
            raw = self.db.read_from_file()
        except Exception as ex:
            msg = f"Failed to read database: {ex}"
            print(f"[ERROR][StudentController.register] {msg}")
            return False, msg

        # Check duplicates
        students = students_from_dicts(raw)
        if find_student_by_email(students, email_norm):
            msg = "A student with this email already exists."
            print(f"[DEBUG][StudentController.register] {msg}")
            return False, msg

        # Validate & create via model
        try:
            new_student = Student.create(name=name, email=email_norm, password=password)
        except Exception as ex:
            msg = f"Validation error: {ex}"
            print(f"[DEBUG][StudentController.register] {msg}")
            return False, msg

        # Persist (preserve non-student records)
        updated_raw = self._upsert_student_raw(raw, new_student)
        try:
            self.db.write_to_file(updated_raw)
            print("[DEBUG][StudentController.register] DB write successful.")
        except Exception as ex:
            msg = f"Failed to write database: {ex}"
            print(f"[ERROR][StudentController.register] {msg}")
            return False, msg

        # Optionally set as current session
        self.current_student = new_student
        return True, "Registered successfully."

    # -------------------------------------------------------------------------
    # Load / Save current
    # -------------------------------------------------------------------------
    def load_current_by_email(self, email: str) -> Tuple[bool, str]:
        """
        Loads a student by email and sets current_student.
        """
        email_norm = (email or "").strip().lower()
        print(f"[DEBUG][StudentController.load_current_by_email] Loading: {email_norm}")

        try:
            raw = self.db.read_from_file()
        except Exception as ex:
            msg = f"Failed to read database: {ex}"
            print(f"[ERROR][StudentController.load_current_by_email] {msg}")
            return False, msg

        students = students_from_dicts(raw)
        student = find_student_by_email(students, email_norm)
        if not student:
            msg = "Student not found."
            print(f"[DEBUG][StudentController.load_current_by_email] {msg}")
            return False, msg

        self.current_student = student
        print(f"[DEBUG][StudentController.load_current_by_email] Loaded: {student.email}")
        return True, "Loaded"

    def save_current(self) -> Tuple[bool, str]:
        """
        Writes the current_student back into the DB record set.
        """
        if not self.current_student:
            return False, "No current student to save."

        print(f"[DEBUG][StudentController.save_current] Saving: {self.current_student.email}")
        try:
            raw = self.db.read_from_file()
        except Exception as ex:
            msg = f"Failed to read database: {ex}"
            print(f"[ERROR][StudentController.save_current] {msg}")
            return False, msg

        updated_raw = self._upsert_student_raw(raw, self.current_student)
        try:
            self.db.write_to_file(updated_raw)
            print("[DEBUG][StudentController.save_current] DB write successful.")
            return True, "Saved"
        except Exception as ex:
            msg = f"Failed to write database: {ex}"
            print(f"[ERROR][StudentController.save_current] {msg}")
            return False, msg

    # -------------------------------------------------------------------------
    # Subject operations (require current_student)
    # -------------------------------------------------------------------------
    def enrol_subject(self, title: str, mark: Optional[int] = None) -> Tuple[bool, str]:
        """
        Enrol the current student in a subject, then persist.
        """
        if not self.current_student:
            return False, "No active session."

        try:
            subject = self.current_student.enrol_subject(title=title, mark=mark)
            print(f"[DEBUG][StudentController.enrol_subject] Enrolled: {subject.title} ({subject.id})")
        except Exception as ex:
            msg = f"Enrol failed: {ex}"
            print(f"[DEBUG][StudentController.enrol_subject] {msg}")
            return False, msg

        ok, msg = self.save_current()
        return (True, "Enrolled and saved.") if ok else (False, msg)

    def remove_subject(self, subject_id: str) -> Tuple[bool, str]:
        """
        Remove a subject by ID for the current student, then persist.
        """
        if not self.current_student:
            return False, "No active session."

        removed = self.current_student.remove_subject(subject_id)
        if not removed:
            msg = "Subject not found."
            print(f"[DEBUG][StudentController.remove_subject] {msg} ({subject_id})")
            return False, msg

        print(f"[DEBUG][StudentController.remove_subject] Removed subject: {subject_id}")
        ok, msg = self.save_current()
        return (True, "Removed and saved.") if ok else (False, msg)

    def change_password(self, new_password: str) -> Tuple[bool, str]:
        """
        Change the current student's password, then persist.
        """
        if not self.current_student:
            return False, "No active session."

        try:
            self.current_student.change_password(new_password)
            print("[DEBUG][StudentController.change_password] Password updated.")
        except Exception as ex:
            msg = f"Password change failed: {ex}"
            print(f"[DEBUG][StudentController.change_password] {msg}")
            return False, msg

        ok, msg = self.save_current()
        return (True, "Password updated and saved.") if ok else (False, msg)

    # -------------------------------------------------------------------------
    # Read-only info for views
    # -------------------------------------------------------------------------
    def list_subjects(self) -> List[Any]:
        """
        Returns a list of Subject objects for the current student (or empty list).
        """
        if not self.current_student:
            return []
        return list(self.current_student.subjects or [])

    def average_mark(self) -> float:
        """
        Computes the current student's average mark.
        """
        if not self.current_student:
            return 0.0
        return float(self.current_student.average_mark())

    def has_passed(self) -> bool:
        """
        PASS if average >= 50.
        """
        if not self.current_student:
            return False
        return bool(self.current_student.has_passed())

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------
    def _upsert_student_raw(self, raw: list, student: Student) -> list:
        """
        Replace (or insert) a student's dict into the raw DB list by email, preserving
        any non-student records (e.g., admins) intact.
        """
        out = []
        email_norm = (student.email or "").lower()
        replaced = False

        for entry in raw or []:
            role = (entry or {}).get("role", "student")
            if role != "student":
                out.append(entry)
                continue

            # Student record — match by email (case-insensitive)
            entry_email = (entry or {}).get("email", "").lower()
            if entry_email == email_norm:
                out.append(student.to_dict())
                replaced = True
            else:
                out.append(entry)

        if not replaced:
            out.append(student.to_dict())

        return out
