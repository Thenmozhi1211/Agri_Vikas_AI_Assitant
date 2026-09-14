from vectorstore.faiss_store import load_vectorstore
from config.settings import RETRIEVAL_K


def get_retriever():

    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": RETRIEVAL_K
        }
    )

    return retriever