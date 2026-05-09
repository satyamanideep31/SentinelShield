import sqlite3

def init_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_text TEXT,
        threat_level TEXT,
        block_hash TEXT
    )
    ''')

    conn.commit()
    conn.close()

def insert_report(report_text, threat_level, block_hash):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO reports(report_text, threat_level, block_hash)
    VALUES (?, ?, ?)
    ''', (report_text, threat_level, block_hash))

    conn.commit()
    conn.close()

def get_reports():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")

    reports = cursor.fetchall()

    conn.close()

    return reports