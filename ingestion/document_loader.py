from pathlib import Path

from langchain_core.documents import Document

from config.settings import CLEANED_DIR


def load_documents():

    documents = []

    files = list(CLEANED_DIR.glob("*.txt"))

    if not files:
        raise FileNotFoundError(
            "No cleaned documents found. Run the scraper first."
        )

    for file_path in files:

        text = file_path.read_text(
            encoding="utf-8"
        )

        document = Document(
            page_content=text,
            metadata={
                "source": str(file_path),
                "source_type": "Agrisnet",
            }
        )

        documents.append(document)

    print(f"Loaded {len(documents)} document(s).")

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print("\nFirst document preview:\n")
    print(docs[0].page_content[:1000])