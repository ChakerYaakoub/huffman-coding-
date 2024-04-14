import os
import sqlite3

def create_database_if_not_exists():
    # Check if the database file exists
    if not os.path.exists('files_database.db'):
        # If the database file does not exist, create it
        conn = sqlite3.connect('files_database.db')
        cursor = conn.cursor()
        
        # Create the necessary tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS Fichiers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            original_filename TEXT,

                            path TEXT,
                            reverse_mapping blob
                        )''')
        
        # Commit changes and close connection
        conn.commit()
        conn.close()



