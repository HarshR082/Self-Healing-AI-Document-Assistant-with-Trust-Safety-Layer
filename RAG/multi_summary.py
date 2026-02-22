from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL,
    temperature=0.2
)

def summarize_multiple(docs_summary):

    combined = "\n\n".join(docs_summary)

    prompt = f"""
Combine and summarize the following document summaries.

Summaries:
{combined}
"""

    return llm.invoke(prompt).content
