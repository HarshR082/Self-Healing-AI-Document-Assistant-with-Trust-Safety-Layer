from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL,
    temperature=0.2
)

def generate_summary(text, length="medium"):

    length_map = {
        "short": "Summarize in 3–4 lines.",
        "medium": "Provide a balanced summary.",
        "long": "Provide a detailed summary with explanations."
    }

    prompt = f"""
{length_map[length]}

Document:
{text}
"""

    return llm.invoke(prompt).content
