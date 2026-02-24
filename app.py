from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models.db import init_db, get_db
from models.waste import log_waste, get_user_logs, get_monthly_stats, get_map_data
from models.ai import get_ai_suggestions
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

init_db()

# ── Auth (simple demo) ────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username:
            session["user_id"] = username
            session["username"] = username
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    stats = get_monthly_stats(session["user_id"])
    suggestions = get_ai_suggestions(session["user_id"])
    return render_template("dashboard.html", stats=stats, suggestions=suggestions,
                           username=session["username"])

# ── Log Waste ─────────────────────────────────────────────────────────────────

@app.route("/log", methods=["GET", "POST"])
def log():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        category = request.form.get("category")
        amount   = float(request.form.get("amount", 0))
        unit     = request.form.get("unit", "kg")
        note     = request.form.get("note", "")
        log_waste(session["user_id"], category, amount, unit, note)
        return redirect(url_for("dashboard"))
    logs = get_user_logs(session["user_id"], limit=20)
    return render_template("log.html", logs=logs, username=session["username"])

# ── Map ───────────────────────────────────────────────────────────────────────

@app.route("/map")
def waste_map():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("map.html", username=session["username"])

@app.route("/api/map-data")
def api_map_data():
    data = get_map_data()
    return jsonify(data)

# ── AI Insights ───────────────────────────────────────────────────────────────

@app.route("/insights")
def insights():
    if "user_id" not in session:
        return redirect(url_for("login"))
    suggestions = get_ai_suggestions(session["user_id"], detailed=True)
    return render_template("insights.html", suggestions=suggestions,
                           username=session["username"])

# ── API: chart data ───────────────────────────────────────────────────────────

@app.route("/api/chart-data")
def api_chart_data():
    if "user_id" not in session:
        return jsonify({"error": "unauthorized"}), 401
    from models.waste import get_weekly_trend
    data = get_weekly_trend(session["user_id"])
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
