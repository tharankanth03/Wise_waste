from models.db import get_db
from datetime import datetime, timedelta

def log_waste(user_id, category, amount, unit, note=""):
    conn = get_db()
    conn.execute(
        "INSERT INTO waste_logs (user_id, category, amount, unit, note) VALUES (?,?,?,?,?)",
        (user_id, category, amount, unit, note)
    )
    conn.commit()
    conn.close()

def get_user_logs(user_id, limit=20):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM waste_logs WHERE user_id=? ORDER BY logged_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_monthly_stats(user_id):
    conn = get_db()
    since = (datetime.now() - timedelta(days=30)).isoformat()

    rows = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM waste_logs
        WHERE user_id=? AND logged_at >= ?
        GROUP BY category
    """, (user_id, since)).fetchall()
    conn.close()

    stats = {"food": 0.0, "plastic": 0.0, "energy": 0.0}
    for row in rows:
        if row["category"] in stats:
            stats[row["category"]] = round(row["total"], 2)

    # CO2 equivalent estimates
    stats["co2_saved"] = round(
        stats["food"] * 0.5 +
        stats["plastic"] * 1.8 +
        stats["energy"] * 0.23,
        2
    )

    # Goal progress (example targets)
    stats["goals"] = {
        "food":    {"target": 2.0,  "current": stats["food"],    "pct": min(100, round(stats["food"]    / 2.0  * 100))},
        "plastic": {"target": 0.5,  "current": stats["plastic"], "pct": min(100, round(stats["plastic"] / 0.5  * 100))},
        "energy":  {"target": 10.0, "current": stats["energy"],  "pct": min(100, round(stats["energy"]  / 10.0 * 100))},
    }

    return stats

def get_weekly_trend(user_id):
    conn = get_db()
    weeks = []
    for i in range(5, -1, -1):
        start = (datetime.now() - timedelta(weeks=i+1)).isoformat()
        end   = (datetime.now() - timedelta(weeks=i)).isoformat()
        row = conn.execute("""
            SELECT
                SUM(CASE WHEN category='food'    THEN amount ELSE 0 END) as food,
                SUM(CASE WHEN category='plastic' THEN amount ELSE 0 END) as plastic,
                SUM(CASE WHEN category='energy'  THEN amount ELSE 0 END) as energy
            FROM waste_logs
            WHERE user_id=? AND logged_at BETWEEN ? AND ?
        """, (user_id, start, end)).fetchone()
        weeks.append({
            "label": f"Wk {6-i}",
            "food":    round(row["food"]    or 0, 2),
            "plastic": round(row["plastic"] or 0, 2),
            "energy":  round(row["energy"]  or 0, 2),
        })
    conn.close()
    return weeks

def get_map_data():
    """Aggregated, anonymised regional data for the map."""
    regions = [
        {"name": "RS Puram",        "lat": 11.0020, "lng": 76.9500, "level": "high"},
        {"name": "Gandhipuram",     "lat": 11.0168, "lng": 76.9558, "level": "medium"},
        {"name": "Saravanampatti",  "lat": 11.0600, "lng": 77.0300, "level": "low"},
        {"name": "Peelamedu",       "lat": 11.0220, "lng": 77.0270, "level": "low"},
    ]

    conn = get_db()
    result = []
    for r in regions:
        prefix = "demo_" + r["name"].lower().replace(" ", "")
        row = conn.execute("""
            SELECT
                SUM(CASE WHEN category='food'    THEN amount ELSE 0 END) as food,
                SUM(CASE WHEN category='plastic' THEN amount ELSE 0 END) as plastic,
                SUM(CASE WHEN category='energy'  THEN amount ELSE 0 END) as energy
            FROM waste_logs WHERE user_id=?
        """, (prefix,)).fetchone()
        result.append({**r, "food": round(row["food"] or 0, 1),
                       "plastic": round(row["plastic"] or 0, 1),
                       "energy":  round(row["energy"]  or 0, 1)})
    conn.close()
    return result
