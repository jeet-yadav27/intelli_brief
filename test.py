import sqlite3

conn = sqlite3.connect("data/briefs.db")
cur = conn.cursor()

for row in cur.execute("SELECT id, company, url, brief, created_at FROM briefs"):
    print(f"\nID: {row[0]}")
    print(f"Company: {row[1]}")
    print(f"URL: {row[2]}")
    print(f"Created: {row[4]}")
    print(f"Brief:\n{row[3][:500]}...")  # preview first 500 chars

conn.close()
