# Backend/api_calls.py

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from app.rag import RAGPipeline

from app.orchestrator import (
    RAGOrchestrator
)

from app.logger import get_logger


# ====================================
# App Initialization
# ====================================

app = FastAPI(

    title="RAG Chatbot API",

    description=
    "PDF Knowledge Base Chatbot",

    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

logger = get_logger()

orchestrator = (
    RAGOrchestrator()
)

# ====================================
# Request Models
# ====================================

class QueryRequest(
    BaseModel
):

    question: str


class RetrievalRequest(
    BaseModel
):

    question: str

    top_k: int = 5


# ====================================
# Response Models
# ====================================

class Source(
    BaseModel
):

    file_name: str

    page_number: int | None = None

    document_type: str

    chunk_number: int


class QueryResponse(
    BaseModel
):

    question: str

    answer: str

    sources: list[Source]


class RetrievalResult(
    BaseModel
):

    rank: int

    file_name: str

    page_number: int | None

    document_type: str

    chunk_number: int

    content: str


class RetrievalResponse(
    BaseModel
):

    question: str

    matches: list[
        RetrievalResult
    ]


# ====================================
# Health Check
# ====================================

@app.get("/health")
def health_check():

    return {

        "status":
        "running",

        "service":
        "RAG Chatbot"
    }


# ====================================
# Ask Question
# ====================================

@app.post(

    "/query",

    response_model=
    QueryResponse
)
def query_documents(
    request: QueryRequest
):

    try:

        if not request.question.strip():

            raise HTTPException(

                status_code=400,

                detail=
                "Question is required"
            )

        result = (
            orchestrator.ask(
                request.question
            )
        )

        return QueryResponse(

            question=
            request.question,

            answer=
            result["answer"],

            sources=
            result["sources"]
        )

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# ====================================
# Retrieval Visualization
# ====================================

@app.post(

    "/retrieve",

    response_model=
    RetrievalResponse
)
def retrieve_chunks(
    request:
    RetrievalRequest
):

    try:

        if not request.question.strip():

            raise HTTPException(

                status_code=400,

                detail=
                "Question is required"
            )

        matches = (

            orchestrator.rag
            .retrieve_matches(

                query=
                request.question,

                k=
                request.top_k
            )
        )

        return RetrievalResponse(

            question=
            request.question,

            matches=[
                RetrievalResult(
                    **m
                )
                for m in matches
            ]
        )

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# ====================================
# Show System Info
# ====================================

@app.get("/info")
def system_info():

    return {

        "project":
        "Hackathon RAG Chatbot",

        "vector_db":
        "FAISS",

        "embedding_model":
        "BAAI/bge-small-en-v1.5",

        "supported_files": [

            "pdf",

            "docx",

            "json"
        ]
    }
@app.get("/")
def root():
    return {
        "message": "RAG Chatbot API Running"
    }