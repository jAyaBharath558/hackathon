# Data_layer/embeddings/embedding.py

import json
from pathlib import Path

from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_chroma import Chroma

from config.config import (
    PROCESSED_DATA_PATH,
    FAISS_INDEX_PATH,
    EMBEDDING_MODEL
)


class EmbeddingManager:

    def __init__(self):

        self.embedding_model = (
            HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL
            )
        )

        self.chunk_file = (
            Path(PROCESSED_DATA_PATH)
            / "chunks.json"
        )

    # ==========================
    # Load Chunks
    # ==========================

    def load_chunks(self):

        with open(
            self.chunk_file,
            "r",
            encoding="utf-8"
        ) as f:

            chunks = json.load(f)

        documents = []

        for chunk in chunks:

            documents.append(

                Document(

                    page_content=
                    chunk["chunk_text"],

                    metadata={

                        "chunk_id":
                        chunk["chunk_id"],

                        "file_name":
                        chunk["file_name"],

                        "page_number":
                        chunk["page_number"],

                        "document_type":
                        chunk["document_type"],

                        "chunk_number":
                        chunk["chunk_number"]
                    }
                )
            )

        return documents

    # ==========================
    # Create FAISS
    # ==========================

    def create_faiss_index(self):

        docs = self.load_chunks()

        vectorstore = (
            FAISS.from_documents(
                docs,
                self.embedding_model
            )
        )

        Path(
            FAISS_INDEX_PATH
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        vectorstore.save_local(
            FAISS_INDEX_PATH
        )

        print(
            "FAISS Index Created"
        )

        return vectorstore

    # ==========================
    # Load FAISS
    # ==========================

    def load_faiss_index(self):

        return FAISS.load_local(
            FAISS_INDEX_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

    # ==========================
    # Create ChromaDB
    # ==========================

    def create_chroma_db(self):

        docs = self.load_chunks()

        chroma_path = (
            Path(FAISS_INDEX_PATH)
            .parent
            / "chroma_db"
        )

        db = Chroma.from_documents(

            documents=docs,

            embedding=
            self.embedding_model,

            persist_directory=
            str(chroma_path)
        )

        print(
            "Chroma DB Created"
        )

        return db

    # ==========================
    # Query Embedding
    # ==========================

    def embed_query(
        self,
        query
    ):

        return self.embedding_model.embed_query(
            query
        )

    # ==========================
    # Document Embedding
    # ==========================

    def embed_document(
        self,
        text
    ):

        return self.embedding_model.embed_documents(
            [text]
        )[0]