from sentence_transformers import SentenceTransformer
from rag.dataset_loader import load_truthfulqa

print("Loading embedding model...")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load TruthfulQA dataset
documents = load_truthfulqa("datasets/TruthfulQA.csv")

print(f"\nTotal Documents: {len(documents)}")

# Extract text
texts = [doc.page_content for doc in documents]

print("\nGenerating embeddings...")

embeddings = model.encode(texts)

print("\nEmbedding generation completed!")

print(f"\nTotal Embeddings: {len(embeddings)}")

print(f"\nEmbedding Dimension: {len(embeddings[0])}")

print("\nFirst Embedding (first 10 values):")

print(embeddings[0][:10])