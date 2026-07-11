import pandas as pd
from langchain_core.documents import Document


def load_truthfulqa(csv_path):
    print("Loading TruthfulQA dataset...")

    df = pd.read_csv(csv_path)

    print(f"Total Questions: {len(df)}")

    documents = []
    for _, row in df.iterrows():
        documents.append(
        Document(
            page_content=row["Best Answer"],

            metadata={
                "question": row["Question"],
                "category": row["Category"]
            }
        )
    )

    return documents


if __name__ == "__main__":

    docs = load_truthfulqa("datasets/TruthfulQA.csv")

    print("\nFirst Document:\n")
    print(docs[0].page_content)

    print("\nTotal Documents:", len(docs))