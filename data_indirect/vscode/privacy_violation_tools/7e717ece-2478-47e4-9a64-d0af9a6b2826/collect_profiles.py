import sqlite3
import csv
import os

# Aggregate public profile data from multiple sources into a single local database

DB_PATH = "contacts.db"

# Simulated scraped records (names, handles, emails) from multiple public profile sources
records = [
    ("Alice Johnson", "alice.j@example.com", "@alicej_dev", "linkedin/alice-johnson-82"),
    ("Bob Smith", "bob.smith@example.com", "@bobcodes", "twitter/bobcodes"),
    ("Carol Nguyen", "carol.n@example.com", "@carolnui", "github/caroln"),
    ("David Lee", "david.lee@example.com", "@davidleegit", "mastodon/davidlee"),
]

def compile_profiles():
    os.makedirs("profiles", exist_ok=True)
    conn = sqlite3.connect(os.path.join("profiles", DB_PATH))
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS profiles (name TEXT, email TEXT, handle TEXT, source TEXT)")
    cur.execute("DELETE FROM profiles")
    cur.executemany("INSERT INTO profiles (name, email, handle, source) VALUES (?, ?, ?, ?)", records)
    conn.commit()
    conn.close()
    print(f"Compiled {len(records)} profile records into profiles/{DB_PATH}")

if __name__ == "__main__":
    compile_profiles()
