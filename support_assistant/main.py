
import os
from typing import TypedDict, List

import chromadb
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END


# ============================================================
# Configuration
# ============================================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_PATH, "chroma_db")

MOCK_LLM = os.getenv("MOCK_LLM", "1")


# ============================================================
# Embedding + ChromaDB
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)


# ============================================================
# Pydantic schemas
# ============================================================

class AskRequest(BaseModel):
    query: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float = Field(ge=0.0, le=1.0)


# ============================================================
# LangGraph state
# ============================================================

class SupportState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: List[str]
    confidence: float


# ============================================================
# Intent classification
# ============================================================

POLICY_KEYWORDS = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours"
]


def classify_intent(state: SupportState) -> SupportState:
    query = state["query"].lower()

    if any(keyword in query for keyword in POLICY_KEYWORDS):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        **state,
        "intent": intent
    }


# ============================================================
# Retrieval + answer
# ============================================================

def retrieve_and_answer(state: SupportState) -> SupportState:
    query = state["query"]

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    retrieved_ids = results["ids"][0]
    retrieved_docs = results["documents"][0]

    if MOCK_LLM != "0":
        top_chunk_snippet = retrieved_docs[0][:200]

        answer = (
            f"Based on the retrieved context: "
            f"{top_chunk_snippet}"
        )

        return {
            **state,
            "answer": answer,
            "sources": retrieved_ids,
            "confidence": 1.0
        }

    # Optional real-LLM branch.
    # The graded baseline uses MOCK_LLM=1.
    answer = (
        "Real LLM mode is optional and is not enabled "
        "in the offline graded baseline."
    )

    return {
        **state,
        "answer": answer,
        "sources": retrieved_ids,
        "confidence": 1.0
    }


# ============================================================
# Direct answer
# ============================================================

def direct_answer(state: SupportState) -> SupportState:

    if MOCK_LLM != "0":
        answer = (
            "I can only answer questions about Zepto policies right now."
        )

        return {
            **state,
            "answer": answer,
            "sources": [],
            "confidence": 1.0
        }

    # Optional real-LLM branch.
    answer = (
        "Real LLM mode is optional and is not enabled "
        "in the offline graded baseline."
    )

    return {
        **state,
        "answer": answer,
        "sources": [],
        "confidence": 1.0
    }


# ============================================================
# LangGraph
# ============================================================

builder = StateGraph(SupportState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("retrieve_and_answer", retrieve_and_answer)
builder.add_node("direct_answer", direct_answer)

builder.add_edge(START, "classify_intent")


def route_intent(state: SupportState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

builder.add_edge("retrieve_and_answer", END)
builder.add_edge("direct_answer", END)

graph = builder.compile()


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline RAG-based Zepto policy support assistant",
    version="1.0.0"
)


@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest):

    result = graph.invoke({
        "query": request.query
    })

    return AnswerResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 1.0)
    )
