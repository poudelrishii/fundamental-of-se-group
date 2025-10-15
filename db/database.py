import os
import pickle
import logging

class Database:
    def __init__(self):
        # Use students.data as required by the assignment
        self.path = "db/students.data"
        self.initialize()

    def initialize(self):
        """Check if the students.data file exists; if not, create it."""
        try:
            if not os.path.exists(self.path):
                with open(self.path, 'wb') as f:
                    pickle.dump([], f)  # start with empty student list
        except Exception as ex:
            logging.error("Error initializing database: %s", ex)

    # --- CRUD OPERATIONS ---

    def read_from_file(self):
        """Read all students from students.data"""
        try:
            with open(self.path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []  # return empty list if file not found or empty
        except Exception as ex:
            logging.error("Error reading file: %s", ex)
            return []

    def write_to_file(self, students):
        """Write all students to students.data"""
        try:
            with open(self.path, 'wb') as f:
                pickle.dump(students, f)
        except Exception as ex:
            logging.error("Error writing to file: %s", ex)

    def clear_all(self):
        """Clear all student data"""
        try:
            with open(self.path, 'wb') as f:
                pickle.dump([], f)
        except Exception as ex:
            logging.error("Error clearing data: %s", ex)
