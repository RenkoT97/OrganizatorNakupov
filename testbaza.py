import sqlite3

    # Create a SQL connection to our SQLite database
con = sqlite3.connect('organizator_nakupov.db')

cur = con.cursor()

cur.execute("PRAGMA foreign_key = ON;")
