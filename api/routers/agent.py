from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from api.solr_client import search_resources, semantic_search_resources
from langchain.llms import HuggingFacePipeline
from transformers import pipeline

# Initialize the router
target = APIRouter(prefix="/agents", tags=["agents"])


# --------------------------------------------------
# Local LLM setup using a lightweight FLAN-T5 model
# --------------------------------------------------
gen_pipeline = pipeline(
    task="text2text-generation",
    model="google/flan-t5-small",
    tokenizer="google/flan-t5-small",
    max_length=512,
    do_sample=False,
)
llm = HuggingFacePipeline(pipeline=gen_pipeline)


# --------------------------
# Request & Response Models
# --------------------------
class SummaryRequest(BaseModel):
    document_ids: List[str] = Field(..., description="List of resource IDs to summarize")
    max_tokens: Optional[int] = Field(200, ge=50, le=1000, description="Max tokens for summary")


class SummaryResponse(BaseModel):
    summary: str


class QARequest(BaseModel):
    question: str = Field(..., description="Natural language question to answer")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of context passages to retrieve")


class QAResponse(BaseModel):
    answer: str


# --------------------------
# Summary Endpoint
# --------------------------
@target.post("/summary", response_model=SummaryResponse)
def summarize_docs(req: SummaryRequest):
    """
    Retrieve specified documents, extract text, and generate a combined summary.
    """
    # Fetch docs by ID
    id_filter = " OR ".join(req.document_ids)
    q = f"id:({id_filter})"
    solr_res = search_resources(q=q, page=1, page_size=len(req.document_ids), facet_fields=[])
    docs = solr_res.get("response", {}).get("docs", [])
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found for provided IDs.")

    # Aggregate abstracts or fulltext for context
    contexts = [doc.get("abstract", "") for doc in docs]
    prompt = (
        "Summarize the following documents in an academic tone:\n\n"
        + "\n\n".join(contexts)
    )

    # Generate summary
    summary = llm(prompt)
    return SummaryResponse(summary=summary)


# --------------------------
# Q&A Endpoint
# --------------------------
@target.post("/qa", response_model=QAResponse)
def answer_question(req: QARequest):
    """
    Perform semantic retrieval to gather context and answer the user question.
    """
    # Retrieve top-K semantically similar passages
    solr_res = semantic_search_resources(
        query=req.question,
        top_k=req.top_k,
        filters=None,
        page=1,
        page_size=req.top_k,
    )
    docs = solr_res.get("response", {}).get("docs", [])
    if not docs:
        raise HTTPException(status_code=404, detail="No context found for question.")

    # Build context string
    contexts = [doc.get("abstract", "") for doc in docs]
    prompt = (
        "Use the following contexts to answer the question:\n\n"
        + "\n\n".join(contexts)
        + f"\n\nQuestion: {req.question}\nAnswer:"
    )

    # Generate answer
    answer = llm(prompt)
    return QAResponse(answer=answer)
