# app/rag.py

from typing import Dict, List

from Data_layer.embeddings.embedding import (
    EmbeddingManager
)

from config.config import (
    TOP_K
)


class RAGPipeline:

    def __init__(self):

        self.embedding_manager = (
            EmbeddingManager()
        )

        # Load FAISS Index
        self.vectorstore = (
            self.embedding_manager
            .load_faiss_index()
        )

    # ====================================
    # Retrieve Relevant Documents
    # ====================================

    def retrieve_chunks(
        self,
        query: str,
        k: int = TOP_K
    ):

        documents = (
            self.vectorstore
            .similarity_search(
                query,
                k=k
            )
        )

        return documents

    # ====================================
    # Retrieval Visualization
    # ====================================

    def retrieve_matches(
        self,
        query: str,
        k: int = TOP_K
    ) -> List[Dict]:

        documents = (
            self.retrieve_chunks(
                query=query,
                k=k
            )
        )

        results = []

        for rank, doc in enumerate(
            documents,
            start=1
        ):

            results.append({

                "rank":
                rank,

                "file_name":
                doc.metadata.get(
                    "file_name"
                ),

                "page_number":
                doc.metadata.get(
                    "page_number"
                ),

                "document_type":
                doc.metadata.get(
                    "document_type"
                ),

                "chunk_number":
                doc.metadata.get(
                    "chunk_number"
                ),

                "content":
                doc.page_content[:500]
            })

        return results

    # ====================================
    # Build Context
    # ====================================

    def build_context(
        self,
        query: str
    ):

        documents = (
            self.retrieve_chunks(
                query
            )
        )

        context_parts = []

        sources = []

        for doc in documents:

            context_parts.append(
                doc.page_content
            )

            sources.append({

                "file_name":
                doc.metadata.get(
                    "file_name"
                ),

                "page_number":
                doc.metadata.get(
                    "page_number"
                ),

                "document_type":
                doc.metadata.get(
                    "document_type"
                ),

                "chunk_number":
                doc.metadata.get(
                    "chunk_number"
                )
            })

        context = "\n\n".join(
            context_parts
        )

        return context, sources

    # ====================================
    # Generate Answer
    # ====================================

    def generate_answer(
        self,
        query: str,
        llm
    ) -> Dict:

        context, sources = (
            self.build_context(
                query
            )
        )

        prompt = f"""
You are an enterprise document assistant.

Instructions:
1. Answer ONLY from the provided context.
2. Do not hallucinate.
3. If information is unavailable,
   reply:
   'Information not found in documents.'
4. Provide concise answers.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

        response = llm.invoke(
            prompt
        )

        return {

            "question":
            query,

            "answer":
            str(response),

            "sources":
            sources
        }

    # ====================================
    # Full Query Pipeline
    # ====================================

    def ask(
        self,
        query: str,
        llm
    ) -> Dict:

        return self.generate_answer(
            query=query,
            llm=llm
        )