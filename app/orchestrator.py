# app/orchestrator.py

from typing import Dict

import torch
from transformers import pipeline

from app.rag import RAGPipeline

from langchain_groq import ChatGroq

from config.config import (
    LLM_MODEL,
    GROQ_API_KEY,
    LLM_PROVIDER
)

from app.logger import (
    get_logger
)


class LocalLLM:

    def __init__(self, model_name: str):

        device = 0 if torch.cuda.is_available() else -1

        self.pipeline = pipeline(
            "text2text-generation",
            model=model_name,
            device=device,
            max_new_tokens=256,
            do_sample=False
        )

    def invoke(self, prompt: str):

        result = self.pipeline(
            prompt,
            max_new_tokens=256,
            clean_up_tokenization_spaces=True
        )

        if isinstance(result, list) and result:
            output = result[0]
            if isinstance(output, dict):
                return output.get(
                    "generated_text",
                    output.get("text", str(output))
                )
            return str(output)

        return str(result)


class RAGOrchestrator:

    def __init__(self):

        self.logger = get_logger()

        self.rag = RAGPipeline()

        if LLM_PROVIDER.lower() == "groq" and GROQ_API_KEY:
            self.llm = ChatGroq(
                model=LLM_MODEL,
                api_key=GROQ_API_KEY,
                temperature=0.2
            )
        else:
            self.logger.info(
                "Using local transformer model for generation"
            )
            self.llm = LocalLLM(
                model_name=LLM_MODEL
            )

        self.logger.info(
            "RAG Orchestrator Initialized"
        )

    # ====================================
    # Main Query Flow
    # ====================================

    def ask(
        self,
        question: str
    ) -> Dict:

        try:

            self.logger.info(
                f"Question Received: {question}"
            )

            result = self.rag.ask(

                query=question,

                llm=self.llm
            )

            self.logger.info(
                "Answer Generated Successfully"
            )

            return result

        except Exception as e:

            error_message = str(e)

            if (
                isinstance(self.llm, ChatGroq)
                and "invalid_api_key" in error_message.lower()
            ):
                self.logger.warning(
                    "Invalid Groq API key detected; falling back to local model"
                )
                self.llm = LocalLLM(
                    model_name=LLM_MODEL
                )

                result = self.rag.ask(
                    query=question,
                    llm=self.llm
                )

                self.logger.info(
                    "Answer Generated Successfully with local model"
                )

                return result

            self.logger.error(
                f"RAG Error: {error_message}"
            )

            return {

                "question":
                question,

                "answer":
                "Error while generating answer.",

                "sources":
                [],

                "error":
                error_message
            }

    # ====================================
    # Retrieval Visualization
    # ====================================

    def retrieve_chunks(
        self,
        question: str,
        top_k: int = 5
    ):

        try:

            return (

                self.rag
                .retrieve_matches(

                    query=question,

                    k=top_k
                )
            )

        except Exception as e:

            self.logger.error(
                f"Retrieval Error: {str(e)}"
            )

            return []

    # ====================================
    # System Information
    # ====================================

    def get_system_info(
        self
    ):

        return {

            "project":
            "Hackathon RAG Chatbot",

            "llm_model":
            LLM_MODEL,

            "vector_db":
            "FAISS",

            "embedding":
            "BAAI/bge-small-en-v1.5",

            "supported_documents": [

                "pdf",

                "docx",

                "json"
            ]
        }