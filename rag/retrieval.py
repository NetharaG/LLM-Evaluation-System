# import chromadb
# from sentence_transformers import SentenceTransformer

# print("Loading embedding model...")
# model = SentenceTransformer(
#     "all-MiniLM-L6-v2",
#     local_files_only=True
# )
# print("Connecting to ChromaDB...")
# client = chromadb.PersistentClient(path="./database/chroma_db")

# collection = client.get_collection("truthfulqa")
# def retrieve(query, k=5):

#     query_embedding = model.encode(query).tolist()

#     results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=k,
#     include=["documents", "metadatas", "distances"]
# )

#     print("\n========== TOP RETRIEVED RESULTS ==========\n")
#     for i in range(len(results["documents"][0])):
#         print(f"Result {i + 1}")
        
#         print("Distance :", results["distances"][0][i])
        
#         print(
#                 "Question :",
#                 results["metadatas"][0][i]["question"]
#             )
        
#         print(
#                 "Category :",
#                 results["metadatas"][0][i]["category"]
#             )
        
#         print(
#                 "Reference:",
#                 results["documents"][0][i]
#             )
        
#         print("-" * 60)



#     return {
#         "reference_answer": results["documents"][0][0],
#         "question": results["metadatas"][0][0]["question"],
#         "category": results["metadatas"][0][0]["category"]
#     }
# if __name__ == "__main__":

#     question = input("Enter your question: ")

#     result = retrieve(question)

#     print("\nRetrieved Data:\n")

#     print(result)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# LOAD TRUTHFULQA DATASET
# ============================================================

DATASET_PATH = "datasets/TruthfulQA.csv"

print("Loading TruthfulQA dataset...")

df = pd.read_csv(DATASET_PATH)

# Remove rows with missing questions/answers
df = df.dropna(subset=["Question", "Best Answer"]).reset_index(drop=True)

print(f"Loaded {len(df)} TruthfulQA questions.")


# ============================================================
# CREATE TF-IDF INDEX
# ============================================================

print("Creating TF-IDF index...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

question_vectors = vectorizer.fit_transform(
    df["Question"].astype(str)
)

print("TF-IDF index ready.")


# ============================================================
# RETRIEVE SIMILAR QUESTIONS
# ============================================================

def retrieve(query, k=5):

    query = str(query)

    # Convert user question into TF-IDF vector
    query_vector = vectorizer.transform([query])

    # Calculate similarity with every dataset question
    similarities = cosine_similarity(
        query_vector,
        question_vectors
    )[0]

    # Get top k matching questions
    top_indices = similarities.argsort()[-k:][::-1]

    print("\n========== TOP RETRIEVED RESULTS ==========\n")

    for rank, index in enumerate(top_indices, start=1):

        row = df.iloc[index]

        print(f"Result {rank}")

        print("Similarity :", round(float(similarities[index]), 4))

        print("Question :", row["Question"])

        print("Category :", row["Category"])

        print("Reference :", row["Best Answer"])

        print("-" * 60)


    # Best matching result
    best_index = top_indices[0]

    best_row = df.iloc[best_index]


    return {
        "reference_answer": str(best_row["Best Answer"]),
        "question": str(best_row["Question"]),
        "category": str(best_row["Category"])
    }


# ============================================================
# TEST RETRIEVAL
# ============================================================

if __name__ == "__main__":

    question = input("Enter your question: ")

    result = retrieve(question)

    print("\nRetrieved Data:\n")

    print(result)

