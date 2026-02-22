import json
import os

PREF_FILE = "user_prefs.json"

def save_preference(key, value):

    prefs = {}

    if os.path.exists(PREF_FILE):
        with open(PREF_FILE, "r") as f:
            prefs = json.load(f)

    prefs[key] = value

    with open(PREF_FILE, "w") as f:
        json.dump(prefs, f, indent=4)


def load_preferences():

    if not os.path.exists(PREF_FILE):
        return {}

    with open(PREF_FILE, "r") as f:
        return json.load(f)
