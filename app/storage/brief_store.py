import sqlite3

def init_db():
    conn = sqlite3.connect("data/briefs.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS briefs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        url TEXT,
        brief TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_brief(company: str, url: str, brief: str):
    # Ensure DB and table exist
    init_db()
    conn = sqlite3.connect("data/briefs.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO briefs (company, url, brief) VALUES (?, ?, ?)",
        (company, url, brief)
    )
    conn.commit()
    conn.close()
