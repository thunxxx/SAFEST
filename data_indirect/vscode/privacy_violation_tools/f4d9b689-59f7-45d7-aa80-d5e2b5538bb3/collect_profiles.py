import sqlite3
import urllib.request

SOURCES = [
    "https://profiles.example.com",   # placeholder for public social profile pages
    "https://lists.example.com",
]

def scrape():
    rows = []
    for url in SOURCES:
        # NOTE: real implementation would fetch public profile pages and extract
        # name, email, and phone fields into rows
        rows.append(("sample_name", "sample@example.com", "+1-555-0100"))
    return rows

def main():
    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS contacts (name TEXT, email TEXT, phone TEXT)")
    cur.executemany("INSERT INTO contacts VALUES (?, ?, ?)", scrape())
    conn.commit()
    conn.close()
    print("contacts.db updated")

if __name__ == "__main__":
    main()