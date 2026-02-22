import json
import os

# ⭐ Always store in project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_FILE = os.path.join(BASE_DIR, "knowledge_db.json")
ACTIVE_FILE = os.path.join(BASE_DIR, "active_doc.json")


def save_knowledge(doc_name, summary):

    data = {}

    if os.path.exists(KNOWLEDGE_FILE):
        try:
            with open(KNOWLEDGE_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}

    data[doc_name] = summary

    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    set_active_doc(doc_name)


def load_knowledge():

    if not os.path.exists(KNOWLEDGE_FILE):
        return {}

    try:
        with open(KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def set_active_doc(doc_name):

    with open(ACTIVE_FILE, "w") as f:
        json.dump({"active": doc_name}, f)


def get_active_doc():

    if not os.path.exists(ACTIVE_FILE):
        return None

    try:
        with open(ACTIVE_FILE, "r") as f:
            return json.load(f).get("active")
    except:
        return None
