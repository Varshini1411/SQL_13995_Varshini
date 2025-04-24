import sqlite3

# Step 1: Connect to the database
connection = sqlite3.connect(":memory:")  # In-memory database
cursor = connection.cursor()

# Step 2: Create a table
cursor.execute("""
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary INTEGER NOT NULL
)
""")

# Step 3: Insert multiple rows using executemany
data = [
    (1, "John", "HR", 5000),
    (2, "Alice", "IT", 6000),
    (3, "Bob", "Marketing", 7000),
    (4, "Eve", "Finance", 8000)
]

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", data)

# Step 4: Query the table to verify the data
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()
print(rows)
# # Step 5: Print the output
# for row in rows:
#     print(row)

# Step 6: Close the connection
connection.close()