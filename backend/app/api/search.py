"""Semantic search endpoints using FAISS."""

from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()


@router.post("/semantic", summary="Semantic search for similar resumes")
async def semantic_search(query: str, limit: int = 10) -> Dict[str, Any]:
    """Find similar resumes using semantic search."""
    return {
        "query": query,
        "results": [],
        "total_found": 0
    }


@router.get("/similar/{resume_id}", summary="Find similar resumes")
async def find_similar(resume_id: str, limit: int = 5) -> Dict[str, Any]:
    """Find resumes similar to a given resume."""
    return {
        "base_resume_id": resume_id,
        "similar_resumes": [],
        "total_found": 0
    }
