import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from config import DB_DIR, GROQ_API_KEY, MODEL
from intent_router import detect_intent

# Knowledge & preferences
from knowledge_store import load_knowledge, get_active_doc
from user_preferences import load_preferences
from doc_understanding import generate_summary

# Trust & safety layer
from hallucination_guard import detect_hallucination
from quality_score import quality_score
from metrics_store import log_metrics

# Phase 4 intelligence
from prompt_optimizer import optimize_prompt
from self_healing import heal_response
from semantic_cache import find_similar_query, store_query
from adaptive_learning import log_learning_event


# ------------------------
# Load embedding once
# ------------------------
embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ------------------------
# Retriever Factory
# ------------------------
def get_retriever():
    active_doc = get_active_doc()

    if not active_doc:
        return None

    doc_id = os.path.splitext(active_doc)[0]
    doc_db_path = os.path.join(DB_DIR, doc_id)

    if not os.path.exists(doc_db_path):
        return None

    vectordb = Chroma(
        persist_directory=doc_db_path,
        embedding_function=embedding
    )

    return vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10}
    )

# ------------------------
# LLM Initialization
# ------------------------
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL,
    temperature=0.2
)

# ------------------------
# Prompt Builder
# ------------------------
def build_prompt(intent, context, query, summary_length="medium"):

    base_rules = """
You are a  document-based assistant.
RULES:
- Base the answer primarily on the document excerpts.
- Ensure all factual claims are supported by the document.
- You may add explanations to improve clarity and understanding.
- You may explain concepts to improve clarity and understanding.
- If the document partially answers the question, respond with available information and state limitations.
- Do NOT introduce facts that contradict the document.
- If the question is ambiguous, provide the most relevant interpretation.
- Ask for clarification only when necessary.
- Keep responses concise by default.
- Provide more detail when the user asks for explanation or depth.
- Do not fabricate document-specific facts.
- Provide examples when helpful
- If the document does not contain the answer, say:
  "This information is not available in the uploaded documents."
- Highlight key insights when appropriate.
- Keep responses clear, professional, and helpful.

"""

    if intent in ["summarize", "explain"]:
        length_instruction = {
            "short": "Give summary in 3–4 lines.",
            "medium": "Give a balanced summary.",
            "long": "Give a detailed summary with explanation."
        }

        return f"""
{base_rules}

{length_instruction.get(summary_length, "")}

Context:
{context}
"""
    else:
        return f"""
{base_rules}

Context:
{context}

Question:
{query}

Answer:
"""

# ------------------------
# Main Response Function
# ------------------------
def generate_response(query):

    retriever = get_retriever()
    intent = detect_intent(query)

    knowledge = load_knowledge()
    active_doc = get_active_doc()
    doc_id = active_doc if active_doc else "global"

    # ✅ Semantic Cache Lookup (after doc_id exists)
    cached_answer = find_similar_query(query, doc_id)
    if cached_answer:
        return cached_answer, "cached", "LOW", 100, []

    prefs = load_preferences()
    summary_length = prefs.get("summary_length", "medium")

    # ------------------------
    # Active document knowledge
    # ------------------------
    if not active_doc or active_doc not in knowledge:
        return "No active document available.", "error", "LOW", 0, []

    knowledge_context = knowledge[active_doc]

    # ------------------------
    # Summary / Explanation
    # ------------------------
    if intent in ["summarize", "explain"]:
        summary = generate_summary(knowledge_context, summary_length)

        risk = "LOW"
        score = 100

        log_metrics(intent, risk, score)
        return summary, intent, risk, score, []

    # ------------------------
    # Retrieval
    # ------------------------
    if retriever is None:
        return "Vector store not found.", "error", "LOW", 0, []

    docs = retriever.invoke(query)

    if not docs:
        return (
            "This information is not available in the uploaded documents.",
            "unknown",
            "LOW",
            0,
            []
        )

    retrieved_context = "\n\n".join(
        [
            f"Source: {d.metadata.get('source','unknown')}\n{d.page_content}"
            for d in docs
        ]
    )

    combined_context = f"""
Use the following document information to answer.

DOCUMENT OVERVIEW:
{knowledge_context}

DOCUMENT EXCERPTS:
{retrieved_context}

Answer strictly from the excerpts above.
"""

    prompt = build_prompt(
        intent,
        combined_context,
        query,
        summary_length
    )

    # Prompt safety baseline
    prompt = optimize_prompt(prompt)

    answer = llm.invoke(prompt).content.strip()

    # ------------------------
    # Trust Layer
    # ------------------------
    risk, unsupported = detect_hallucination(
        combined_context,
        answer
    )

    quality = quality_score(combined_context, answer)

    # Adaptive prompt strengthening (learning)
    prompt = optimize_prompt(prompt, risk, quality)

    # Self-healing safety enforcement
    answer = heal_response(answer, risk, quality, unsupported)

    # Log metrics & learning signals
    log_metrics(intent, risk, quality)
    log_learning_event(query, intent, risk, quality)

    print("Retrieved docs:", len(docs))

    # Store high-quality responses in semantic cache
    if risk == "LOW" and quality >= 60:
        store_query(query, answer, doc_id)

    return answer, intent, risk, quality, unsupported
