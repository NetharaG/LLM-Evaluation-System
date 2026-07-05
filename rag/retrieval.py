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

    return results


if __name__ == "__main__":

    question = input("Enter your question: ")

    results = retrieve(question)

    print("\nTop Results\n")

    for i, doc in enumerate(results["documents"][0]):

        print("=" * 70)
        print(f"Result {i+1}\n")
        print(doc)
        print()