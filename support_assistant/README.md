# Zepto Support Assistant

## Module 3

This project implements an offline RAG-based Zepto Support Assistant using
local embeddings, ChromaDB, LangGraph, Pydantic and FastAPI.

## Architecture

Policy Documents
    |
    v
Document Ingestion
    |
    v
all-MiniLM-L6-v2 Embeddings
    |
    v
ChromaDB - zepto_policies
    |
    v
LangGraph Intent Router
    |
    +--> policy_question --> retrieve_and_answer
    |
    +--> general_question --> direct_answer
    |
    v
Pydantic Structured Response
    |
    v
FastAPI /ask

## Documents

Eight Zepto policy documents are stored in the docs directory.

The documents cover:

1. Delivery Policy
2. Returns and Refunds
3. Membership Tiers
4. Order Tracking
5. Order Cancellation
6. Damaged or Missing Items
7. Gift Cards
8. Customer Support Hours

## Embeddings

The documents are embedded locally using:

all-MiniLM-L6-v2

The embeddings are stored in the ChromaDB collection:

zepto_policies

## Retrieval

For policy questions, the retrieve_and_answer node embeds the query and
retrieves the top 3 most similar documents using cosine similarity.

## Intent Classification

The classify_intent node uses the required keyword heuristic in the default
MOCK_LLM mode.

Policy keywords include delivery, return, refund, membership, tracking,
cancel, gift card and support hours.

## Mock LLM Mode

The default mode is MOCK_LLM=1.

No external LLM API call is required.

For policy questions, the system returns an answer based on the top retrieved
document.

For general questions, the system returns:

I can only answer questions about Zepto policies right now.

## Structured Output

The final response is validated using Pydantic.

Example:

{
  "answer": "Based on the retrieved context: ...",
  "sources": ["doc_01", "doc_03", "doc_08"],
  "confidence": 1.0
}

For general questions, sources is an empty list.

## Example 1 - Policy Question

Request:

{
  "query": "How much does Zepto charge for delivery below INR 149?"
}

Response:

{
  "answer": "Based on the retrieved context: ...",
  "sources": ["doc_01", "doc_03", "doc_08"],
  "confidence": 1.0
}

This query is routed to policy_question and then to retrieve_and_answer.

## Example 2 - General Question

Request:

{
  "query": "What is the capital of India?"
}

Response:

{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}

This query is routed to general_question and then to direct_answer.

## FastAPI

Run locally with:

uvicorn main:app --host 0.0.0.0 --port 8000

Endpoint:

POST /ask

## Docker

Build:

docker build -t zepto-support-assistant .

Run:

docker run -p 7860:7860 zepto-support-assistant

The application listens on port 7860 inside the container.

## Project Files

docs/
main.py
prompts.py
requirements.txt
Dockerfile
README.md
chroma_db/

## Conclusion

The system provides a deterministic offline RAG baseline for Zepto policy
questions. Documents are embedded locally, indexed in ChromaDB, routed using
LangGraph and returned through a validated FastAPI response.
