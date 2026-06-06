# config/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# Load Environment Variables
# =====================================================

ENV_PATH = BASE_DIR / "config" / ".env"

load_dotenv(ENV_PATH)

# =====================================================
# Application Settings
# =====================================================

APP_NAME = "RAG Chatbot"

APP_VERSION = "1.0.0"

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# =====================================================
# Data Paths
# =====================================================

RAW_DATA_PATH = os.getenv(
    "RAW_DATA_PATH",
    str(BASE_DIR / "Data_layer" / "raw_data")
)

PROCESSED_DATA_PATH = os.getenv(
    "PROCESSED_DATA_PATH",
    str(BASE_DIR / "Data_layer" / "processed_chunks")
)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    str(BASE_DIR / "Data_layer" / "vector_store")
)

FAISS_INDEX_PATH = os.getenv(
    "FAISS_INDEX_PATH",
    str(BASE_DIR / "Data_layer" / "vector_store" / "faiss_index")
)

# =====================================================
# Chunking Configuration
# =====================================================

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", "800")
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", "150")
)

# =====================================================
# Embedding Model
# =====================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)

EMBEDDING_DIMENSION = int(
    os.getenv("EMBEDDING_DIMENSION", "384")
)

# =====================================================
# Retrieval Configuration
# =====================================================

TOP_K = int(
    os.getenv("TOP_K", "5")
)

SIMILARITY_THRESHOLD = float(
    os.getenv("SIMILARITY_THRESHOLD", "0.70")
)

# =====================================================
# Reranker Configuration
# =====================================================

RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "BAAI/bge-reranker-base"
)

# =====================================================
# LLM Configuration
# =====================================================

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "groq"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "google/flan-t5-small"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)

# =====================================================
# API Configuration
# =====================================================

HOST = os.getenv(
    "HOST",
    "0.0.0.0"
)

PORT = int(
    os.getenv("PORT", "8000")
)

# =====================================================
# Logging Configuration
# =====================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    str(BASE_DIR / "logs" / "rag.log")
)

# =====================================================
# Validation
# =====================================================

required_dirs = [
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    VECTOR_DB_PATH
]

for directory in required_dirs:
    os.makedirs(directory, exist_ok=True)

print("Configuration Loaded Successfully")