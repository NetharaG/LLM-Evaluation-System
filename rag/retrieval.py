import chromadb
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)
print("Connecting to ChromaDB...")
client = chromadb.PersistentClient(path="./database/chroma_db")

collection = client.get_collection("truthfulqa")
def retrieve(query, k=1):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return {
        "reference_answer": results["documents"][0][0],
        "question": results["metadatas"][0][0]["question"],
        "category": results["metadatas"][0][0]["category"]
    }
if __name__ == "__main__":

    question = input("Enter your question: ")

    result = retrieve(question)

    print("\nRetrieved Data:\n")

    print(result)

