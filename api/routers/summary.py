# routers/summary.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from api.solr_client import semantic_search_resources, search_resources
# from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

router = APIRouter(prefix="/summary", tags=["summary"])


# Initialize a local LLM for summaries
gen_pipeline = pipeline(
    task="text2text-generation",
    model="google/flan-t5-small",
    tokenizer="google/flan-t5-small",
    max_length=512,
    do_sample=False,
)
llm = HuggingFacePipeline(pipeline=gen_pipeline)


# --- Pydantic Schemas ---
class SummaryRequest(BaseModel):
    """
    Request for canned summaries or key takeaways by topic or document IDs.
    """
    topic: Optional[str] = Field(None, description="Free-text topic to summarize")
    document_ids: Optional[List[str]] = Field(None, description="List of resource IDs to summarize")
    summary_type: str = Field("chapter", description="Type: 'chapter' or 'key_takeaways'")
    top_k: int = Field(5, ge=1, le=20, description="Number of context docs to retrieve")


class SummaryResponse(BaseModel):
    summary: str


# --- Helper to build prompt templates ---
def build_prompt(contexts: List[str], summary_type: str) -> str:
    if summary_type == "chapter":
        header = "Provide an academic-style chapter summary for the following contexts:\n\n"
    else:
        header = "Provide key takeaways in bullet points for the following contexts:\n\n"
    return header + "\n\n".join(contexts)


# --- Endpoint ---
@router.post("/", response_model=SummaryResponse)
def generate_summary(req: SummaryRequest):
    # Validate input
    if not req.topic and not req.document_ids:
        raise HTTPException(status_code=400, detail="Provide either 'topic' or 'document_ids'.")

    # Retrieve contexts via semantic search
    if req.document_ids:
        # join IDs for an ID-based query
        q = "id:(" + " OR ".join(req.document_ids) + ")"
        solr_res = search_resources(q=q, page=1, page_size=len(req.document_ids), facet_fields=[])
        docs = solr_res.get("items", [])
        contexts = [d.get("abstract", "") for d in docs]
    else:
        solr_res = semantic_search_resources(query=req.topic, top_k=req.top_k, filters=None, page=1, page_size=req.top_k)
        docs = solr_res.get("items", [])
        contexts = [d.get("abstract", "") for d in docs]

    if not contexts:
        raise HTTPException(status_code=404, detail="No context found for summary.")

    # Build and run prompt
    prompt = build_prompt(contexts, req.summary_type)
    output = llm(prompt)

    return SummaryResponse(summary=output)
