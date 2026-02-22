import json
import os
from difflib import SequenceMatcher

CACHE_FILE = "semantic_cache.json"


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return []

    with open(CACHE_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def find_similar_query(query, doc_id, threshold=0.85):
    """
    Return cached answer only if same document.
    """
    cache = load_cache()

    for item in cache:
        if item["doc_id"] == doc_id:
            if similarity(query.lower(), item["query"].lower()) >= threshold:
                return item["answer"]

    return None


def store_query(query, answer, doc_id):
    """
    Store answer specific to a document.
    """
    cache = load_cache()

    cache.append({
        "doc_id": doc_id,
        "query": query,
        "answer": answer
    })

    save_cache(cache)
