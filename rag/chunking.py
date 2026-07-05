from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.dataset_loader import load_truthfulqa


def chunk_documents(documents):
    """
    Split the documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    # Load dataset
    documents = load_truthfulqa("datasets/TruthfulQA.csv")

    # Chunk dataset
    chunks = chunk_documents(documents)

    print(f"\nTotal Documents: {len(documents)}")
    print(f"Total Chunks Created: {len(chunks)}")

    print("\nFirst Chunk:\n")
    print(chunks[0].page_content)

    print("\nMetadata:\n")
    print(chunks[0].metadata)