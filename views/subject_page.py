# views/subject_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from views.base_page import BasePage
from resources.parameters.app_parameters import PAGE_CONFIG
from models.student_model import (
    students_from_dicts,
    students_to_dicts,   # kept for parity with EnrolmentPage save flow (not used here yet)
    find_student_by_email,
)


class SubjectPage(BasePage):
    """
    SubjectPage
    -----------
    Read-only view that lists the logged-in student's enrolled subjects,
    including Subject ID, Title, Mark, and Grade.

    Assumptions:
    - `controller` provides:
        - `db`: persistence layer with read_from_file() / write_to_file()
        - `navigate(page_name: str)`
        - `current_user_email`: the email of the logged-in student
    - `BasePage` provides:
        - set_title(), add_centered_frame(), set_background_color()
    """

    def __init__(self, master, controller=None, db=None, **kwargs):
        super().__init__(
            master,
            background_color=PAGE_CONFIG.get("background_color"),
            **kwargs
        )
        self.controller = controller
        self.db = db if db is not None else getattr(controller, "db", None)
        self.student = None

        self._build_ui()
        self._load_student()
        self._refresh_table()

    # ----------------------------
    # UI Construction
    # ----------------------------
    def _build_ui(self) -> None:
        # Title
        self.set_title(
            text="Enrolled Subjects",
            style="Title.TLabel",
            pady=PAGE_CONFIG.get("title_pady", 16),
            anchor="center",
        )

        # Center frame for content
        self.content_frame = self.add_centered_frame(width=None, height=None)
        self.content_frame.configure(bg=PAGE_CONFIG.get("background_color"))

        # Info label (student name / email)
        self.info_var = tk.StringVar(value="Loading student...")
        self.info_label = ttk.Label(self.content_frame, textvariable=self.info_var, style="FieldLabel.TLabel")
        self.info_label.pack(anchor="w", pady=(0, 8))

        # Table
        self._build_table(self.content_frame)

        # Footer stats
        footer = tk.Frame(self.content_frame, bg=PAGE_CONFIG.get("background_color"))
        footer.pack(fill="x", pady=(8, 0))

        self.avg_var = tk.StringVar(value="Average: —")
        self.status_var = tk.StringVar(value="Status: —")

        self.avg_label = ttk.Label(footer, textvariable=self.avg_var, style="FieldLabel.TLabel")
        self.avg_label.pack(side="left", padx=(0, 12))

        self.status_label = ttk.Label(footer, textvariable=self.status_var, style="FieldLabel.TLabel")
        self.status_label.pack(side="left")

        # Buttons row
        buttons_row = tk.Frame(self.content_frame, bg=PAGE_CONFIG.get("background_color"))
        buttons_row.pack(fill="x", pady=(12, 0))

        self.back_btn = ttk.Button(buttons_row, text="Back", command=self._on_back, style="Primary.TButton")
        self.back_btn.pack(side="right")

    def _build_table(self, parent: tk.Misc) -> None:
        table_frame = tk.Frame(parent, bg=PAGE_CONFIG.get("background_color"))
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "title", "mark", "grade")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("mark", text="Mark")
        self.tree.heading("grade", text="Grade")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("title", width=260, anchor="w")
        self.tree.column("mark", width=80, anchor="center")
        self.tree.column("grade", width=80, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    # ----------------------------
    # Data Loading / Refresh
    # ----------------------------
    def _load_student(self) -> None:
        """
        Load the current student using controller.current_user_email.
        """
        if self.controller is None or self.db is None:
            self.info_var.set("Error: controller/db not available.")
            return

        email = getattr(self.controller, "current_user_email", None)
        if not email:
            self.info_var.set("No user session. Please log in.")
            return

        try:
            raw = self.db.read_from_file()
        except Exception as ex:
            self.info_var.set("Error reading database.")
            messagebox.showerror("Database Error", f"Failed to read data.\n{ex}")
            return

        students = students_from_dicts(raw)
        student = find_student_by_email(students, email)

        if not student:
            self.info_var.set(f"Student not found for: {email}")
            return

        self.student = student
        self.info_var.set(f"Student: {student.name}  |  {student.email}")

    def _refresh_table(self) -> None:
        """
        Rebuild the table rows from self.student.subjects and update stats.
        """
        # clear rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not self.student:
            self.avg_var.set("Average: —")
            self.status_var.set("Status: —")
            return

        subjects = getattr(self.student, "subjects", []) or []
        if not subjects:
            # still show clean stats
            self.avg_var.set("Average: —")
            self.status_var.set("Status: No subjects")
            return

        # insert rows
        for subj in subjects:
            self.tree.insert(
                "",
                "end",
                values=(getattr(subj, "id", ""),
                        getattr(subj, "title", ""),
                        getattr(subj, "mark", ""),
                        getattr(subj, "grade", "")),
            )

        # stats
        try:
            avg = self.student.average_mark()
            passed = self.student.has_passed()
            self.avg_var.set(f"Average: {avg:.1f}")
            self.status_var.set(f"Status: {'PASS' if passed else 'FAIL'}")
        except Exception:
            self.avg_var.set("Average: —")
            self.status_var.set("Status: —")

    # ----------------------------
    # Actions
    # ----------------------------
    def _on_back(self) -> None:
        """
        Navigate back to the main student page (enrolment) if available,
        otherwise back to login as a safe default.
        """
        if self.controller and hasattr(self.controller, "navigate"):
            # Prefer returning to enrolment page; fall back to login
            target = "enrolment" if "enrolment" in getattr(self.controller, "pages", {}) else "login"
            self.controller.navigate(target)
        else:
            messagebox.showinfo("Navigation", "No router available to navigate back.")
