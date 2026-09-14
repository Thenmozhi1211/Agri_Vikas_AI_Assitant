from langchain_openai import OpenAIEmbeddings

from config.settings import EMBEDDING_MODEL


def get_embeddings():

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    return embeddings