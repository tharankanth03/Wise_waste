# 🌿 WasteWise

**Your AI-Powered Waste Reduction Companion**

> *Track. Reduce. Leave something behind.*

WasteWise is a web application built for the **ORIGIN Hackathon 2026**. It helps individuals and small businesses track and reduce food, plastic, and energy waste — using AI to deliver personalised, actionable recommendations based on your actual habits.

---

## ✨ Features

- **📊 Dashboard** — Visual overview of your monthly waste with trend charts and goal progress
- **📝 Waste Logging** — Log food, plastic, and energy waste in seconds
- **✨ AI Insights** — Personalised reduction tips powered by GPT-3.5 (or rule-based fallback)
- **🗺️ Waste Map** — Interactive map showing anonymised regional waste data (Leaflet.js)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + Flask |
| Templating | Jinja2 |
| Database | SQLite |
| AI Engine | OpenAI GPT-3.5 (optional) |
| Charts | Chart.js |
| Map | Leaflet.js |
| UI | Bootstrap-free custom CSS |
| Deployment | Render |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/wastewise.git
cd wastewise
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and add your SECRET_KEY
# Optionally add your OPENAI_API_KEY for AI-powered suggestions
```

### 5. Run the app

```bash
flask run
```

Visit [http://localhost:5000](http://localhost:5000) — enter any username to start.

---

## 🌍 Deploying to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `gunicorn app:app`
6. Add environment variables: `SECRET_KEY`, `OPENAI_API_KEY` (optional)

Add `gunicorn` to your requirements if deploying:
```
gunicorn>=21.0.0
```

---

## 📁 Project Structure

```
wastewise/
├── app.py                  # Flask app and routes
├── requirements.txt
├── .env.example
├── models/
│   ├── db.py               # SQLite init and connection
│   ├── waste.py            # Waste CRUD and stats
│   └── ai.py               # AI suggestion engine
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── log.html
│   ├── map.html
│   └── insights.html
└── static/
    └── css/
        └── style.css
```

---

## 🏆 ORIGIN Hackathon

This project was built for the **ORIGIN Hackathon 2026** under the theme of **Environmental Responsibility**.

> *ORIGIN — Build what will remain.*

---

## 📄 License

MIT License. Feel free to use, modify, and share.
