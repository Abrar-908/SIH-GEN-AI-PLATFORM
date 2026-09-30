from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag.vector_store import vector_store

router = APIRouter(prefix="/rag", tags=["rag"])

class IndexRequest(BaseModel):
    document_id: int
    chunks: List[Dict[str, Any]]

class SearchRequest(BaseModel):
    document_id: int
    query: str
    top_k: int = 5

@router.post("/index")
def index_document_chunks(data: IndexRequest):
    count = vector_store.index_document(data.document_id, data.chunks)
    return {
        "status": "success",
        "document_id": data.document_id,
        "indexed_chunks": count
    }

@router.post("/search")
def search_rag(data: SearchRequest):
    results = vector_store.search(data.document_id, data.query, data.top_k)
    return {
        "document_id": data.document_id,
        "query": data.query,
        "top_k": data.top_k,
        "results": results
    }
