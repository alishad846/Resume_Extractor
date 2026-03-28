"""Resume scoring and ranking endpoints."""

from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
import logging

from app.services.scorer import get_resume_scorer, score_resume_with_jd

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/score-resume", summary="Score a single resume")
async def score_single_resume(
    extracted_data: Dict[str, Any] = Body(...),
    jd_text: str = None
) -> Dict[str, Any]:
    """
    Score a resume based on multiple criteria.
    
    **Scoring Dimensions:**
    - Skills match (40%)
    - Experience relevance (25%)
    - Education quality (15%)
    - Project portfolio (10%)
    - Resume completeness (10%)
    
    **Returns:**
    - Overall score (0-100)
    - Dimension-wise scores
    - Letter grade (A-F)
    - Actionable feedback
    """
    try:
        scorer = get_resume_scorer()
        score_result = scorer.score_resume(extracted_data, jd_text)
        
        logger.info(f"✅ Resume scored: {score_result['overall_score']}")
        
        return {
            "status": "success",
            "score_result": score_result,
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    except Exception as e:
        logger.error(f"❌ Scoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@router.post("/batch-score", summary="Score multiple resumes")
async def batch_score_resumes(
    resumes: List[Dict[str, Any]] = Body(...)
) -> Dict[str, Any]:
    """Score multiple resumes in batch."""
    try:
        scorer = get_resume_scorer()
        ranked_resumes = scorer.rank_resumes(resumes)
        
        logger.info(f"✅ Batch scored {len(resumes)} resumes")
        
        return {
            "status": "success",
            "total_resumes": len(resumes),
            "ranked_resumes": ranked_resumes,
            "top_candidates": ranked_resumes[:5]
        }
    
    except Exception as e:
        logger.error(f"❌ Batch scoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch scoring failed: {str(e)}")


@router.post("/score-with-jd", summary="Score resume against job description")
async def score_resume_vs_jd(
    extracted_data: Dict[str, Any] = Body(...),
    jd_requirements: Dict[str, List[str]] = Body(...)
) -> Dict[str, Any]:
    """
    Score resume specifically against job description requirements.
    
    **JD Requirements Structure:**
    ```json
    {
        "required_skills": ["Python", "AWS", "Docker"],
        "nice_to_have": ["Kubernetes", "Go"],
        "years_experience": 5,
        "educational_background": ["Bachelor's", "Master's"]
    }
    ```
    """
    try:
        score_result = score_resume_with_jd(extracted_data, jd_requirements)
        
        logger.info(f"✅ JD matching score: {score_result['overall_score']}")
        
        return {
            "status": "success",
            "jd_match_score": score_result['overall_score'],
            "dimension_scores": score_result['dimension_scores'],
            "match_percentage": round(score_result['overall_score']),
            "feedback": score_result['feedback'],
            "recommendations": generate_recommendations(score_result)
        }
    
    except Exception as e:
        logger.error(f"❌ JD matching error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"JD matching failed: {str(e)}")


def generate_recommendations(score_result: Dict[str, Any]) -> List[str]:
    """Generate personalized recommendations based on score."""
    recommendations = []
    
    scores = score_result.get('dimension_scores', {})
    
    if scores.get('skills_match', 0) < 60:
        recommendations.append(
            "📚 Learn additional technical skills mentioned in the job description"
        )
    
    if scores.get('experience_match', 0) < 50:
        recommendations.append(
            "🎯 Gain more hands-on experience with the tech stack required"
        )
    
    if scores.get('education_match', 0) < 60:
        recommendations.append(
            "🎓 Consider relevant certifications to strengthen your credentials"
        )
    
    if len(recommendations) == 0:
        recommendations.append("🌟 Excellent fit! Apply with confidence!")
    
    return recommendations


@router.get("/score/{resume_id}", summary="Get score for a specific resume")
async def get_resume_score(resume_id: str) -> Dict[str, Any]:
    """Retrieve previously calculated score for a resume."""
    # Would fetch from database
    return {
        "resume_id": resume_id,
        "overall_score": 85.5,
        "grade": "B",
        "calculated_at": "2024-01-01T00:00:00Z"
    }
