from difflib import SequenceMatcher
import re


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def split_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)


def detect_hallucination(context, answer, threshold=0.30):
    """
    Improved hallucination detection using chunk-level similarity.
    """

    context_chunks = [c.strip().lower() for c in context.split("\n") if c.strip()]
    sentences = split_sentences(answer)

    unsupported = []

    for sent in sentences:
        sent_lower = sent.lower()

        best_score = max(
            (similarity(sent_lower, chunk) for chunk in context_chunks),
            default=0
        )

        if best_score < threshold:
            unsupported.append(sent)

    # risk classification
    if len(unsupported) == 0:
        risk = "LOW"
    elif len(unsupported) == 1:
        risk = "LOW"   # ⭐ changed to avoid false alarms
    elif len(unsupported) <= 3:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return risk, unsupported

