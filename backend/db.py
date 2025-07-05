import sqlite3
import json
from datetime import datetime

DB_PATH = "urlshortener.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_time TEXT,
        longurl TEXT,
        shorturl TEXT UNIQUE,
        validity INTEGER,
        expiry TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shorturl TEXT,
        clicked_url TEXT,
        clicked_time TEXT,
        source TEXT
    )''')
    conn.commit()
    conn.close()

def insert_url(longurl, shorturl, validity, expiry):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    created_time = datetime.utcnow().isoformat()
    c.execute("INSERT INTO urls (created_time, longurl, shorturl, validity, expiry) VALUES (?, ?, ?, ?, ?)",
              (created_time, longurl, shorturl, validity, expiry))
    conn.commit()
    conn.close()

def get_url(shorturl):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM urls WHERE shorturl=?", (shorturl,))
    row = c.fetchone()
    conn.close()
    return row

def insert_stat(shorturl, clicked_url, source):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    clicked_time = datetime.utcnow().isoformat()
    c.execute("INSERT INTO stats (shorturl, clicked_url, clicked_time, source) VALUES (?, ?, ?, ?)",
              (shorturl, clicked_url, clicked_time, source))
    conn.commit()
    conn.close()

def get_stats(shorturl):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT clicked_url, clicked_time, source FROM stats WHERE shorturl=?", (shorturl,))
    rows = c.fetchall()
    conn.close()
    return [
        {"url": row[0], "time": row[1], "source": row[2]}
        for row in rows
    ]