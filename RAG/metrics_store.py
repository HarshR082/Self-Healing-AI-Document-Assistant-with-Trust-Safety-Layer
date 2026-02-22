import json
import os

METRICS_FILE = "metrics.json"


def log_metrics(intent, risk, score):

    data = []

    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append({
        "intent": intent,
        "risk": risk,
        "score": score
    })

    with open(METRICS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return []
    with open(METRICS_FILE, "r") as f:
        return json.load(f)
