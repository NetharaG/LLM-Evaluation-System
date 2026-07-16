import chromadb
from sentence_transformers import SentenceTransformer

from rag.dataset_loader import load_truthfulqa
from rag.chunking import chunk_documents

print("Loading embedding model...")
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)
print("Loading dataset...")
documents = load_truthfulqa("datasets/TruthfulQA.csv")

print("Chunking...")
chunks = chunk_documents(documents)

print("Creating ChromaDB client...")

client = chromadb.PersistentClient(path="./database/chroma_db")
try:
    client.delete_collection("truthfulqa")
except:
    pass

collection = client.create_collection("truthfulqa")

print("Generating embeddings and storing...")

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk.page_content).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk.page_content],
        metadatas=[chunk.metadata]
    )

print(f"\nStored {collection.count()} documents successfully.")