from pathlib import Path

from langchain_community.vectorstores import FAISS

from ingestion.embeddings import get_embeddings
from ingestion.text_splitter import split_documents
from config.settings import VECTORSTORE_DIR


INDEX_NAME = "agriculture_index"


def build_vectorstore():

    print("Creating documents and chunks...")

    chunks = split_documents()

    print("Creating embeddings...")

    embeddings = get_embeddings()

    print("Building FAISS vector store...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(
        str(VECTORSTORE_DIR),
        index_name=INDEX_NAME
    )

    print("FAISS vector store created.")

    return vectorstore


def load_vectorstore():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        index_name=INDEX_NAME,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def vectorstore_exists():

    index_file = (
        VECTORSTORE_DIR /
        f"{INDEX_NAME}.faiss"
    )

    metadata_file = (
        VECTORSTORE_DIR /
        f"{INDEX_NAME}.pkl"
    )

    return (
        index_file.exists()
        and metadata_file.exists()
    )