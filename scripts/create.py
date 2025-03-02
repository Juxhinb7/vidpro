import sqlite3

with sqlite3.connect("../storage/vidpro.db") as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(254) UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL
    )
    """)
    conn.commit()