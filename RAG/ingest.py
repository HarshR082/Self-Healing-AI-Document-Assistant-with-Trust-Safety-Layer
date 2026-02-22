import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import DB_DIR
from doc_understanding import generate_summary
from knowledge_store import save_knowledge
if os.path.exists("semantic_cache.json"):
    os.remove("semantic_cache.json")

# ------------------------
# Load embedding once
# ------------------------
embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def ingest_file(file_path):

    # ------------------------
    # Load document
    # ------------------------
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)

    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")

    else:
        print("Unsupported file type")
        return

    docs = loader.load()

    # ------------------------
    # ⭐ DOCUMENT UNDERSTANDING PHASE
    # ------------------------
    full_text = "\n".join([doc.page_content for doc in docs])

    # ⭐ FIXED FUNCTION NAME
    doc_summary = generate_summary(full_text)

    doc_name = os.path.basename(file_path)

    save_knowledge(doc_name, doc_summary)

    print(f"Knowledge stored for {doc_name}")

    # ------------------------
    # Add metadata
    # ------------------------
    for doc in docs:
        doc.metadata["source"] = doc_name

    # ------------------------
    # Chunking
    # ------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    # ------------------------
    # ⭐ PER DOCUMENT VECTOR STORE
    # ------------------------
    doc_id = os.path.splitext(doc_name)[0]
    doc_db_path = os.path.join(DB_DIR, doc_id)

    vectordb = Chroma(
        persist_directory=doc_db_path,
        embedding_function=embedding
    )

    vectordb.add_documents(chunks)

    print(f"Ingested {len(chunks)} chunks successfully")
