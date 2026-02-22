from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL,
    temperature=0
)

def detect_intent(query):

    prompt = f"""
    Classify user request into ONE category:

    question
    summarize
    explain
    compare
    describe
    extract

    Query: {query}

    Only return category name.
    """

    return llm.invoke(prompt).content.strip().lower()
