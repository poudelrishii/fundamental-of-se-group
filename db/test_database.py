# test_database.py
from database import Database

# Initialize database
db = Database()

# Step 1: Make sure the file exists
print("Database file path:", db.path)

# Step 2: Read current data (should be empty at first)
print("Initial data:", db.read_from_file())

# Step 3: Add a mock student with password
students = db.read_from_file()

students.append({
    "id": "000001",
    "name": "Alice",
    "email": "alice@university.com",
    "password": "Password123"  # ✅ Password for testing login
})
db.write_to_file(students)

# Step 4: Read back the data
print("Data after adding Alice:", db.read_from_file())

# Step 5: Clear all data (optional)
# db.clear_all()
# print("Data after clear_all():", db.read_from_file())
