from fastapi import FastAPI, UploadFile, File, Body
import os

from rag_engine import generate_response
from ingest import ingest_file
from user_preferences import save_preference

UPLOAD_DIR = "documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Smart RAG API")

# ------------------------
# Upload Document
# ------------------------
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        ingest_file(file_path)

        return {
            "status": "success",
            "message": "Document uploaded & indexed",
            "file": file.filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ------------------------
# Chat Endpoint
# ------------------------
@app.get("/chat")
def chat(query: str):
    try:
        answer, intent, risk, quality,unsupported = generate_response(query)

        return {
            "response": answer,
            "intent": intent,
            "hallucination_risk": risk,
            "quality_score": quality,
            "unsupported_sentences": unsupported
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "response": "Error processing request",
            "intent": "error",
            "hallucination_risk": "unknown",
            "quality_score": 0,
            "error": str(e)
        }


# ------------------------
# Save User Preferences
# ------------------------
@app.post("/set_preferences")
async def set_preferences(data: dict = Body(...)):
    try:
        summary_length = data.get("summary_length", "medium")

        save_preference("summary_length", summary_length)

        return {
            "status": "success",
            "summary_length": summary_length
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
