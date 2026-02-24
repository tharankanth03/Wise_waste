import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "wastewise.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS waste_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT    NOT NULL,
            category    TEXT    NOT NULL,   -- food | plastic | energy
            amount      REAL    NOT NULL,
            unit        TEXT    NOT NULL,   -- kg | kWh | items
            note        TEXT,
            logged_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Seed some demo map data if empty
    cursor.execute("SELECT COUNT(*) as c FROM waste_logs")
    if cursor.fetchone()["c"] == 0:
        demo = [
            ("demo_rspuram",        "food",    4.8, "kg",  ""),
            ("demo_rspuram",        "plastic", 2.1, "kg",  ""),
            ("demo_rspuram",        "energy",  18,  "kWh", ""),
            ("demo_gandhipuram",    "food",    3.1, "kg",  ""),
            ("demo_gandhipuram",    "plastic", 1.4, "kg",  ""),
            ("demo_gandhipuram",    "energy",  12,  "kWh", ""),
            ("demo_saravanampatti", "food",    1.9, "kg",  ""),
            ("demo_saravanampatti", "plastic", 0.6, "kg",  ""),
            ("demo_saravanampatti", "energy",  9,   "kWh", ""),
            ("demo_peelamedu",      "food",    2.3, "kg",  ""),
            ("demo_peelamedu",      "plastic", 0.9, "kg",  ""),
            ("demo_peelamedu",      "energy",  11,  "kWh", ""),
        ]
        cursor.executemany(
            "INSERT INTO waste_logs (user_id, category, amount, unit, note) VALUES (?,?,?,?,?)",
            demo
        )

    conn.commit()
    conn.close()
