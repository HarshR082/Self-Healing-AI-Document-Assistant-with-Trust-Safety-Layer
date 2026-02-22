import json
import os

LEARNING_FILE = "learning_log.json"


def load_learning():
    if not os.path.exists(LEARNING_FILE):
        return []

    with open(LEARNING_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_learning(data):
    with open(LEARNING_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log_learning_event(query, intent, risk, quality):
    """
    Stores queries that need improvement.
    """

    data = load_learning()

    # flag weak responses
    needs_improvement = False

    if risk in ["MEDIUM", "HIGH"]:
        needs_improvement = True

    if quality < 50:
        needs_improvement = True

    if needs_improvement:
        data.append({
            "query": query,
            "intent": intent,
            "risk": risk,
            "quality": quality
        })

        save_learning(data)
