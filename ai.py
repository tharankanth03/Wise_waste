from models.db import get_db
from models.waste import get_monthly_stats
import os

# Optional: real OpenAI integration
try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    _HAS_OPENAI = bool(os.environ.get("OPENAI_API_KEY"))
except ImportError:
    _HAS_OPENAI = False

# ── Fallback rule-based suggestions ──────────────────────────────────────────

FOOD_TIPS = [
    ("Plan meals before shopping", "You tend to waste food mid-week. Try planning Mon–Thu meals before your weekly shop to use existing fridge stock first."),
    ("First-in, first-out", "Move older items to the front of your fridge when you shop. This simple habit cuts food waste by up to 25%."),
    ("Freeze before it expires", "Bread, cooked rice, and fruit about to turn? Freeze them. Your freezer is your best zero-waste tool."),
    ("Smaller portions, seconds available", "Serving smaller portions and offering seconds reduces plate waste without anyone going hungry."),
]

PLASTIC_TIPS = [
    ("Carry a reusable bag", "Single-use carrier bags account for a large share of your plastic waste. A foldable bag in your pocket fixes this permanently."),
    ("Switch to bar soap & shampoo bars", "Liquid soap and shampoo bottles are 90% of bathroom plastic waste for most users. Bars last longer and produce zero packaging."),
    ("Buy in bulk", "Buying dry goods (rice, lentils, oats) in bulk dramatically reduces packaging waste per kg of food."),
    ("Reuse glass jars", "Instead of buying storage containers, repurpose glass jars from food products — they're airtight and last years."),
]

ENERGY_TIPS = [
    ("Standby is not off", "Devices on standby can account for 10–15% of home energy use. A smart power strip cuts this automatically."),
    ("Wash clothes at 30°C", "90% of a washing machine's energy goes to heating water. Washing at 30°C works just as well for most loads."),
    ("LED bulbs everywhere", "If you haven't replaced all bulbs with LEDs yet, it's the single highest-ROI energy action available."),
    ("Short cold showers", "Cutting shower time by 2 minutes saves around 10 litres of hot water — and the energy to heat it — per shower."),
]

def _rule_based_suggestions(stats, detailed=False):
    suggestions = []

    # Pick suggestions based on which category is highest
    food    = stats.get("food", 0)
    plastic = stats.get("plastic", 0)
    energy  = stats.get("energy", 0)

    ranked = sorted(
        [("food", food, FOOD_TIPS), ("plastic", plastic, PLASTIC_TIPS), ("energy", energy, ENERGY_TIPS)],
        key=lambda x: x[1], reverse=True
    )

    for i, (category, amount, tips) in enumerate(ranked):
        tip = tips[i % len(tips)]
        suggestions.append({
            "category": category,
            "emoji":    {"food": "🥗", "plastic": "🧴", "energy": "⚡"}[category],
            "title":    tip[0],
            "body":     tip[1],
            "amount":   amount,
        })
        if not detailed and i >= 1:
            break

    return suggestions

def _openai_suggestions(user_id, stats, detailed=False):
    prompt = f"""
You are WasteWise, an AI waste-reduction coach. A user has logged the following waste this month:
- Food waste: {stats.get('food', 0)} kg
- Plastic waste: {stats.get('plastic', 0)} kg
- Energy waste: {stats.get('energy', 0)} kWh

Give {'5' if detailed else '2'} specific, encouraging, and actionable suggestions to help them reduce waste.
For each suggestion, return JSON with keys: category (food/plastic/energy), title (short), body (2 sentences max), emoji.
Return only a JSON array, no other text.
"""
    try:
        resp = _client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        import json
        text = resp.choices[0].message.content.strip()
        return json.loads(text)
    except Exception:
        return None

def get_ai_suggestions(user_id, detailed=False):
    stats = get_monthly_stats(user_id)
    if _HAS_OPENAI:
        result = _openai_suggestions(user_id, stats, detailed)
        if result:
            return result
    return _rule_based_suggestions(stats, detailed)
