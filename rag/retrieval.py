import chromadb
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to ChromaDB...")
client = chromadb.PersistentClient(path="./database/chroma_db")

collection = client.get_collection("truthfulqa")


def retrieve(query, k=3):

    print("\nSearching...\n")

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0][0]


if __name__ == "__main__":

    question = input("Enter your question: ")

    reference = retrieve(question)

    print("\nRetrieved Reference Answer:\n")
    print(reference)