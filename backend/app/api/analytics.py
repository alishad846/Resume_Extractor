"""Analytics and reporting endpoints."""

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()


@router.get("/dashboard", summary="Get dashboard metrics")
async def get_dashboard_metrics() -> Dict[str, Any]:
    """Get overall dashboard metrics and KPIs."""
    return {
        "total_resumes": 1250,
        "total_candidates": 1000,
        "avg_score": 72.5,
        "recent_uploads": 12,
        "top_skills": ["Python", "React", "AWS", "Docker"],
        "metrics": {}
    }


@router.get("/skills-distribution", summary="Get skills distribution")
async def get_skills_distribution() -> Dict[str, Any]:
    """Get distribution of skills across candidate pool."""
    return {
        "skills": [
            {"skill": "Python", "count": 450},
            {"skill": "Java", "count": 380},
            {"skill": "JavaScript", "count": 420},
            {"skill": "AWS", "count": 320}
        ],
        "total_candidates": 1000
    }


@router.get("/experience-distribution", summary="Get experience level distribution")
async def get_experience_distribution() -> Dict[str, Any]:
    """Get distribution of experience levels."""
    return {
        "experience_levels": {
            "0-2 years": 250,
            "2-5 years": 400,
            "5-10 years": 250,
            "10+ years": 100
        },
        "total": 1000
    }


@router.get("/hiring-funnel", summary="Get hiring funnel metrics")
async def get_hiring_funnel() -> Dict[str, Any]:
    """Get hiring metrics and funnel analytics."""
    return {
        "applied": 1000,
        "screened": 450,
        "interviewed": 120,
        "offered": 20,
        "accepted": 15
    }
