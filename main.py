# main.py

from pathlib import Path
import uvicorn

from config.config import (
    PROCESSED_DATA_PATH,
    FAISS_INDEX_PATH,
    HOST,
    PORT
)

from data_pipline import DataPipeline

from Data_layer.embeddings.embedding import (
    EmbeddingManager
)


def initialize_system():

    print("=" * 60)
    print("Initializing RAG Chatbot")
    print("=" * 60)

    # ==================================
    # Check Chunks
    # ==================================

    chunk_file = (
        Path(PROCESSED_DATA_PATH)
        / "chunks.json"
    )

    if not chunk_file.exists():

        print(
            "Chunks not found."
        )

        print(
            "Running Data Pipeline..."
        )

        pipeline = DataPipeline()

        pipeline.run()

        print(
            "Preprocessing Completed"
        )

    else:

        print(
            "Chunks Already Exist"
        )

    # ==================================
    # Check FAISS
    # ==================================

    faiss_index = (
        Path(FAISS_INDEX_PATH)
        / "index.faiss"
    )

    embedding_manager = (
        EmbeddingManager()
    )

    if not faiss_index.exists():

        print(
            "FAISS Index Not Found"
        )

        print(
            "Creating FAISS Index..."
        )

        embedding_manager.create_faiss_index()

        print(
            "FAISS Index Created"
        )

    else:

        print(
            "FAISS Index Loaded"
        )

    print("=" * 60)
    print("System Ready")
    print("=" * 60)


if __name__ == "__main__":

    initialize_system()

    uvicorn.run(
        "Backend.api_calls:app",
        host=HOST,
        port=PORT,
        reload=False
    )