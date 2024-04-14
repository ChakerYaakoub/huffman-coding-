import sqlite3

# Connect to the database
conn = sqlite3.connect('../files_database.db')
cursor = conn.cursor()

# Execute a query to select all rows from the table
cursor.execute('SELECT * FROM Fichiers')

# Fetch all rows and display them
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
