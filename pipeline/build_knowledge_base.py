from scraper.web_scraper import scrape_agrisnet

from vectorstore.faiss_store import (
    build_vectorstore
)


def build_knowledge_base():

    print("\n==============================")
    print("BUILDING AGRICULTURE KNOWLEDGE BASE")
    print("==============================\n")

    print("STEP 1: Scraping Agrisnet")

    scrape_agrisnet()

    print("\nSTEP 2: Creating vector store")

    build_vectorstore()

    print("\n==============================")
    print("KNOWLEDGE BASE READY")
    print("==============================\n")