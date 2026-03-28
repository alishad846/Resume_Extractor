"""Resume Scoring and Ranking Engine."""

from typing import Dict, List, Any
import re
from collections import Counter

logger_module = "scorer"


class ResumeScorer:
    """Advanced resume scoring system with multi-dimensional scoring."""
    
    def __init__(self):
        """Initialize scoring weights."""
        self.weights = {
            'skills_match': 0.40,           # 40% - Technical skills match
            'experience_match': 0.25,       # 25% - Years and relevance
            'education_match': 0.15,        # 15% - Degree and institution
            'project_quality': 0.10,        # 10% - Project complexity
            'completeness': 0.10,           # 10% - Resume completeness
        }
    
    def score_resume(self, extracted_data: Dict[str, Any], jd_text: str = None) -> Dict[str, Any]:
        """Calculate overall resume score with multiple dimensions."""
        scores = {
            'skills_match': self._score_skills(extracted_data.get('skills', []), jd_text),
            'experience_match': self._score_experience(extracted_data.get('experience', []), jd_text),
            'education_match': self._score_education(extracted_data.get('education', [])),
            'project_quality': self._score_projects(extracted_data.get('projects', [])),
            'completeness': self._score_completeness(extracted_data),
        }
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[key] * self.weights[key] for key in scores.keys()
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'dimension_scores': scores,
            'feedback': self._generate_feedback(scores, extracted_data),
            'grade': self._get_grade(overall_score),
        }
    
    def _score_skills(self, resume_skills: List[str], jd_text: str = None) -> float:
        """Score technical skills match."""
        base_score = min(len(resume_skills) / 10 * 100, 100)  # Presence score
        
        if jd_text and resume_skills:
            jd_lower = jd_text.lower()
            matched_skills = sum(1 for skill in resume_skills if skill.lower() in jd_lower)
            match_ratio = matched_skills / len(resume_skills) if resume_skills else 0
            base_score = (base_score * 0.5) + (match_ratio * 100 * 0.5)
        
        return min(base_score, 100)
    
    def _score_experience(self, experience: List[Dict], jd_text: str = None) -> float:
        """Score work experience relevance and years."""
        if not experience:
            return 20.0
        
        # Years of experience
        years_score = min(len(experience) * 10, 100)
        
        # Experience description quality
        avg_description_length = sum(
            len(exp.get('description', '').split()) for exp in experience
        ) / len(experience) if experience else 0
        
        description_score = min(avg_description_length / 50 * 100, 100)
        
        # JD relevance
        relevance_score = 60.0  # Default
        if jd_text and experience:
            jd_lower = jd_text.lower()
            relevant_exp = sum(
                1 for exp in experience 
                if any(keyword in jd_lower for keyword in exp.get('position', '').split())
            )
            relevance_score = (relevant_exp / len(experience) * 100) if experience else 40
        
        return (years_score * 0.4 + description_score * 0.3 + relevance_score * 0.3)
    
    def _score_education(self, education: List[Dict]) -> float:
        """Score educational background."""
        if not education:
            return 30.0
        
        # Presence score
        base_score = 60.0
        
        # Degree level bonus
        degree_bonuses = {
            'phd': 20,
            'master': 15,
            'bachelor': 10,
            'diploma': 5,
        }
        
        degree_score = 0
        for edu in education:
            degree_text = str(edu.get('degree', '')).lower()
            for degree_type, bonus in degree_bonuses.items():
                if degree_type in degree_text:
                    degree_score = max(degree_score, bonus)
        
        return min(base_score + degree_score, 100)
    
    def _score_projects(self, projects: List[Dict]) -> float:
        """Score project portfolio quality."""
        if not projects:
            return 40.0
        
        # Presence score
        base_score = 50.0 + min(len(projects) * 5, 30)
        
        # Project description quality
        avg_description = sum(
            len(p.get('description', '').split()) for p in projects
        ) / len(projects) if projects else 0
        
        description_score = min(avg_description / 50 * 20, 20)
        
        return min(base_score + description_score, 100)
    
    def _score_completeness(self, extracted_data: Dict[str, Any]) -> float:
        """Score resume completeness."""
        required_fields = [
            'name', 'email', 'phone', 'experience', 'education', 'skills'
        ]
        
        completed_fields = sum(
            1 for field in required_fields 
            if extracted_data.get(field) and 
            (isinstance(extracted_data[field], list) and len(extracted_data[field]) > 0 or
             isinstance(extracted_data[field], str) and len(extracted_data[field]) > 0)
        )
        
        completeness_score = (completed_fields / len(required_fields)) * 100
        return completeness_score
    
    def _generate_feedback(self, scores: Dict[str, float], extracted_data: Dict[str, Any]) -> List[str]:
        """Generate actionable feedback based on scores."""
        feedback = []
        
        # Skills feedback
        if scores['skills_match'] < 60:
            skills_count = len(extracted_data.get('skills', []))
            feedback.append(
                f"⚠️ Skills section needs improvement. Currently listing {skills_count} skills. "
                "Consider adding more relevant technical skills."
            )
        
        # Experience feedback
        if scores['experience_match'] < 50:
            feedback.append(
                "⚠️ Work experience descriptions lack detail. Add metrics, achievements, "
                "and impact statements to each position."
            )
        
        # Education feedback
        if scores['education_match'] < 40:
            feedback.append(
                "💡 Consider adding your educational qualifications to strengthen your profile."
            )
        
        # Projects feedback
        if scores['project_quality'] < 60:
            feedback.append(
                "💡 Add more project details with technologies used and your contributions."
            )
        
        # Completeness feedback
        if scores['completeness'] < 80:
            feedback.append(
                "✏️ Your resume is incomplete. Add missing sections like contact info or experience."
            )
        
        # Positive feedback
        if all(v >= 70 for v in scores.values()):
            feedback.append("✅ Excellent resume! Well-structured with strong technical background.")
        
        return feedback
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def rank_resumes(self, resumes_data: List[Dict[str, Any]], 
                    jd_text: str = None) -> List[Dict[str, Any]]:
        """Rank multiple resumes by score."""
        scored_resumes = []
        
        for resume in resumes_data:
            score_result = self.score_resume(resume.get('extracted_data', {}), jd_text)
            scored_resumes.append({
                'resume_id': resume.get('id'),
                'candidate_name': resume['extracted_data'].get('name'),
                'score_result': score_result,
                'match_percentage': round(score_result['overall_score']),
            })
        
        # Sort by score descending
        scored_resumes.sort(
            key=lambda x: x['score_result']['overall_score'], 
            reverse=True
        )
        
        return scored_resumes


def score_resume_with_jd(extracted_data: Dict[str, Any], 
                        jd_requirements: Dict[str, List[str]]) -> Dict[str, Any]:
    """Score resume against specific job description requirements."""
    scorer = ResumeScorer()
    
    # Build JD text from requirements
    jd_text = " ".join([
        " ".join(reqs) for reqs in jd_requirements.values()
    ])
    
    return scorer.score_resume(extracted_data, jd_text)


def get_resume_scorer() -> ResumeScorer:
    """Get resume scorer instance."""
    return ResumeScorer()
