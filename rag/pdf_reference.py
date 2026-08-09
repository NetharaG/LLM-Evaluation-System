import fitz
from sentence_transformers import SentenceTransformer
import chromadb
import os


# ============================================
# EMBEDDING MODEL
# ============================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================
# CHROMA DATABASE
# ============================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHROMA_PATH = os.path.join(BASE_DIR, "database", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)


# ============================================
# CREATE PDF REFERENCE
# ============================================

def create_pdf_reference(pdf_path):

    # ----------------------------------------
    # Read PDF
    # ----------------------------------------

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    # ----------------------------------------
    # Check PDF
    # ----------------------------------------

    if not text.strip():
        raise ValueError("No readable text found in PDF.")

    # ----------------------------------------
    # Split text into chunks
    # ----------------------------------------

    chunk_size = 500
    overlap = 100

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    # ----------------------------------------
    # Create unique collection
    # ----------------------------------------

    collection_name = "uploaded_pdf_reference"

    try:
        client.delete_collection(collection_name)
    except:
        pass

    collection = client.create_collection(
        name=collection_name
    )

    # ----------------------------------------
    # Create embeddings
    # ----------------------------------------

    embeddings = model.encode(chunks).tolist()

    # ----------------------------------------
    # Store in ChromaDB
    # ----------------------------------------

    ids = [
        f"pdf_chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return {
        "collection": collection_name,
        "chunks": len(chunks)
    }


# ============================================
# RETRIEVE FROM PDF
# ============================================

def retrieve_from_pdf(question):

    collection = client.get_collection(
        "uploaded_pdf_reference"
    )

    question_embedding = model.encode(
        [question]
    ).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=1
    )

    if not results["documents"]:
        return "No relevant reference found."

    return results["documents"][0][0]