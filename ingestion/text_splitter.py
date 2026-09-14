from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHUNKS_DIR
)

from ingestion.document_loader import load_documents


def split_documents():

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Save chunks for inspection
    output_file = CHUNKS_DIR / "chunks.txt"

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        for index, chunk in enumerate(chunks):

            file.write(
                f"\n\n===== CHUNK {index + 1} =====\n\n"
            )

            file.write(
                chunk.page_content
            )

    print(f"Chunks saved to: {output_file}")

    return chunks


if __name__ == "__main__":
    chunks = split_documents()

    print("\nFirst chunk:\n")
    print(chunks[0].page_content)