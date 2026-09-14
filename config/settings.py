from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env", override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. Please add it to the .env file."
    )

AGRI_URL = "https://www.tnagrisnet.tn.gov.in"

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

RAW_DIR = PROJECT_ROOT / "data" / "schemes" / "raw"
CLEANED_DIR = PROJECT_ROOT / "data" / "schemes" / "cleaned"
CHUNKS_DIR = PROJECT_ROOT / "data" / "schemes" / "chunks"
VECTORSTORE_DIR = PROJECT_ROOT / "data" / "schemes" / "vectorstore"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 5

for directory in [
    RAW_DIR,
    CLEANED_DIR,
    CHUNKS_DIR,
    VECTORSTORE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)