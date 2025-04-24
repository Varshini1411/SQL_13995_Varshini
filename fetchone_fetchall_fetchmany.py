import sqlite3

# Connect to the database
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

# Create and populate the employees table
cursor.execute('CREATE TABLE employees (employee_id INTEGER, name TEXT, department TEXT, salary INTEGER)')
cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?)', [
    (1, 'John', 'HR', 5000),
    (2, 'Alice', 'IT', 6000),
    (3, 'Bob', 'Marketing', 7000)
])
connection.commit()

###---fetchone, fetchall, fetchmany---###

# # Use fetchall()
# cursor.execute('SELECT * FROM employees')
# rows = cursor.fetchall()
# # Output
# print(rows)

# Use fetchone()
cursor.execute('SELECT * FROM employees')
row = cursor.fetchone()
print(row)

#############In the example, fetchone was called in a loop, so each row was retrieved one at a time until no rows were left.
# If no rows remain, fetchone returns None.

# Use fetchmany(size=2)
# cursor.execute('SELECT * FROM employees')
# rows = cursor.fetchmany(size=2)
# print(rows)

# Close the connection
connection.close()

