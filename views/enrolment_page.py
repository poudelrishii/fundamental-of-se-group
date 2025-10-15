# views/enrolment_page.py
import tkinter as tk
from tkinter import ttk, messagebox

from views.base_page import BasePage
from models.student_model import (
    Student,
    students_from_dicts,
    students_to_dicts,
    find_student_by_email,
)
from models.subject_model import Subject

class EnrolmentPage(BasePage):
    """
    Student Enrolment GUI:
      - requires controller.db  (Database)
      - expects controller.current_user_email to be set by LoginPage on success
    """

    def __init__(self, master, controller=None, db=None):
        super().__init__(master, bg="white")
        self.controller = controller
        self.db = db or (controller.db if controller else None)

        self.student: Student | None = None

        self._build_ui()
        self._load_student()
        self._refresh_view()

    # ------------------ UI ------------------
    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        title = tk.Label(self, text="Enrolment", font=("Segoe UI", 16, "bold"), bg="white")
        title.grid(row=0, column=0, columnspan=2, pady=(16, 8))

        # Info / status line
        self.info_var = tk.StringVar(value="")
        info = tk.Label(self, textvariable=self.info_var, bg="white", fg="#333")
        info.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Subjects table
        table_frame = tk.LabelFrame(self, text="Enrolled Subjects", bg="white")
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=12, pady=8)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=("id", "title", "mark", "grade"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("mark", text="Mark")
        self.tree.heading("grade", text="Grade")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("title", width=260, anchor="w")
        self.tree.column("mark", width=80, anchor="center")
        self.tree.column("grade", width=80, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

        # Enrol controls
        enrol_frame = tk.LabelFrame(self, text="Enrol in a Subject", bg="white")
        enrol_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        enrol_frame.columnconfigure(1, weight=1)

        tk.Label(enrol_frame, text="Subject title:", bg="white").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.enrol_title_var = tk.StringVar()
        tk.Entry(enrol_frame, textvariable=self.enrol_title_var).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        tk.Button(enrol_frame, text="Enrol", command=self._on_enrol).grid(row=0, column=2, padx=6, pady=6)

        # Remove controls
        remove_frame = tk.LabelFrame(self, text="Remove a Subject", bg="white")
        remove_frame.grid(row=3, column=1, sticky="ew", padx=12, pady=8)
        remove_frame.columnconfigure(1, weight=1)

        tk.Label(remove_frame, text="Subject ID:", bg="white").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.remove_id_var = tk.StringVar()
        tk.Entry(remove_frame, textvariable=self.remove_id_var).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        tk.Button(remove_frame, text="Remove", command=self._on_remove).grid(row=0, column=2, padx=6, pady=6)

        # Password change
        pw_frame = tk.LabelFrame(self, text="Change Password", bg="white")
        pw_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=12, pady=8)
        pw_frame.columnconfigure(1, weight=1)

        tk.Label(pw_frame, text="New password:", bg="white").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.new_pw_var = tk.StringVar()
        tk.Entry(pw_frame, textvariable=self.new_pw_var, show="*").grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        tk.Button(pw_frame, text="Update Password", command=self._on_change_password).grid(row=0, column=2, padx=6, pady=6)

        # Footer with stats + actions
        footer = tk.Frame(self, bg="white")
        footer.grid(row=5, column=0, columnspan=2, sticky="ew", padx=12, pady=12)
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=1)
        footer.columnconfigure(2, weight=1)

        self.avg_var = tk.StringVar(value="Average: 0.00")
        self.status_var = tk.StringVar(value="Status: -")
        tk.Label(footer, textvariable=self.avg_var, bg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(footer, textvariable=self.status_var, bg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=1)

        tk.Button(footer, text="Logout", command=self._on_logout).grid(row=0, column=2, sticky="e")

    # ------------------ Data load/save ------------------
    def _load_student(self):
        if not self.controller or not hasattr(self.controller, "current_user_email"):
            print("[ERROR][EnrolmentPage] controller.current_user_email is missing.")
            self.info_var.set("Error: No logged-in user.")
            return

        email = (self.controller.current_user_email or "").strip()
        if not email:
            print("[ERROR][EnrolmentPage] Empty current_user_email.")
            self.info_var.set("Error: No logged-in user.")
            return

        raw = self.db.read_from_file() if self.db else []
        students = students_from_dicts(raw)
        s = find_student_by_email(students, email)
        if not s:
            print(f"[ERROR][EnrolmentPage] Student not found for email={email}")
            self.info_var.set("Error: Student not found.")
            return

        self.student = s
        self.info_var.set(f"Logged in as: {self.student.name}  ({self.student.email})")
        print(f"[DEBUG][EnrolmentPage] Loaded student {self.student.email}")

    def _save_student(self):
        """Persist current student back to the DB."""
        if not self.student:
            return
        raw = self.db.read_from_file() or []
        students = students_from_dicts(raw)
        # replace this student
        for i, s in enumerate(students):
            if s.email.lower() == self.student.email.lower():
                students[i] = self.student
                break
        else:
            # if for some reason not present, append
            students.append(self.student)
        # keep any non-student entries (e.g., admin)
        others = [d for d in (raw or []) if str(d.get("role", "student")).lower() != "student"]
        self.db.write_to_file(others + students_to_dicts(students))
        print("[DEBUG][EnrolmentPage] Saved student to DB")

    # ------------------ UI refresh ------------------
    def _refresh_view(self):
        # clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.student:
            return

        # fill table
        for subj in self.student.subjects:
            self.tree.insert("", "end", values=(subj.id, subj.title, subj.mark, subj.grade))

        # update stats
        avg = self.student.average_mark()
        self.avg_var.set(f"Average: {avg:.2f}")
        self.status_var.set(f"Status: {'PASS' if self.student.has_passed() else 'FAIL'}")

    # ------------------ Actions ------------------
    def _on_enrol(self):
        if not self.student:
            return
        title = self.enrol_title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Subject title cannot be empty.")
            return
        try:
            subj: Subject = self.student.enrol_subject(title)
            print(f"[DEBUG][EnrolmentPage] Enrolled '{subj.title}' (ID {subj.id}, Mark {subj.mark}, Grade {subj.grade})")
            self._save_student()
            self.enrol_title_var.set("")
            self._refresh_view()
        except Exception as e:
            print(f"[ERROR][EnrolmentPage] Enrol failed: {e}")
            messagebox.showerror("Enrol Error", str(e))

    def _on_remove(self):
        if not self.student:
            return
        sid = self.remove_id_var.get().strip()
        if not sid:
            messagebox.showerror("Error", "Enter a Subject ID to remove.")
            return
        removed = self.student.remove_subject(sid)
        if removed:
            print(f"[DEBUG][EnrolmentPage] Removed subject ID {sid}")
            self._save_student()
            self.remove_id_var.set("")
            self._refresh_view()
        else:
            print(f"[DEBUG][EnrolmentPage] Subject ID {sid} not found")
            messagebox.showerror("Remove Error", "Subject ID not found.")

    def _on_change_password(self):
        if not self.student:
            return
        new_pw = self.new_pw_var.get().strip()
        if not new_pw:
            messagebox.showerror("Error", "Enter a new password.")
            return
        try:
            self.student.change_password(new_pw)
            self._save_student()
            self.new_pw_var.set("")
            messagebox.showinfo("Success", "Password updated.")
            print("[DEBUG][EnrolmentPage] Password updated")
        except Exception as e:
            print(f"[ERROR][EnrolmentPage] Password change failed: {e}")
            messagebox.showerror("Password Error", str(e))

    def _on_logout(self):
        print("[DEBUG][EnrolmentPage] Logging out")
        try:
            # Optional: clear session info on controller
            if hasattr(self.controller, "current_user_email"):
                self.controller.current_user_email = ""
            if hasattr(self.controller, "navigate"):
                self.controller.navigate("login")
        except Exception as e:
            messagebox.showerror("Navigation Error", str(e))
