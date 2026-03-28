"""Advanced NLP service for entity extraction from resumes."""

import spacy
import re
from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class NLPExtractor:
    """Advanced NLP-based entity extraction using SpaCy and BERT."""
    
    def __init__(self, spacy_model: str = "en_core_web_lg", embedding_model: str = "sentence-transformers/all-mpnet-base-v2"):
        """Initialize NLP models."""
        try:
            self.nlp = spacy.load(spacy_model)
            logger.info(f"✅ Loaded SpaCy model: {spacy_model}")
        except OSError:
            logger.warning(f"SpaCy model {spacy_model} not found. Installing...")
            import os
            os.system(f"python -m spacy download {spacy_model}")
            self.nlp = spacy.load(spacy_model)
        
        self.embedding_model = SentenceTransformer(embedding_model)
        logger.info(f"✅ Loaded embedding model: {embedding_model}")
        
        # Pattern definitions
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(?:\+?1[-.\s]?)?\(?(?:\d{3})\)?[-.\s]?(?:\d{3})[-.\s]?(?:\d{4})',
            'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+',
            'github': r'(?:https?://)?(?:www\.)?github\.com/[\w-]+',
            'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract all entities from resume text."""
        doc = self.nlp(text)
        
        extracted = {
            'name': self._extract_name(doc, text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'linkedin': self._extract_linkedin(text),
            'github': self._extract_github(text),
            'location': self._extract_location(doc),
            'summary': self._extract_summary(text),
            'skills': self._extract_skills(doc, text),
            'education': self._extract_education(doc),
            'experience': self._extract_experience(doc, text),
            'projects': self._extract_projects(doc, text),
            'certifications': self._extract_certifications(doc),
            'languages': self._extract_languages(doc, text),
        }
        
        return extracted
    
    def _extract_name(self, doc, text: str) -> str:
        """Extract person name using NER."""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # Return the first person entity (likely the name)
                return ent.text
        
        # Fallback: Extract capitalized words at the beginning
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            words = line.split()
            if len(words) >= 2 and all(w[0].isupper() for w in words[:2]):
                return ' '.join(words[:2])
        
        return ""
    
    def _extract_email(self, text: str) -> List[str]:
        """Extract email addresses."""
        matches = re.findall(self.patterns['email'], text)
        return list(set(matches))
    
    def _extract_phone(self, text: str) -> List[str]:
        """Extract phone numbers."""
        matches = re.findall(self.patterns['phone'], text)
        return list(set(matches))
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn profile."""
        match = re.search(self.patterns['linkedin'], text)
        return match.group(0) if match else ""
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub profile."""
        match = re.search(self.patterns['github'], text)
        return match.group(0) if match else ""
    
    def _extract_location(self, doc) -> str:
        """Extract location from GPE (Geopolitical Entity)."""
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return ent.text
        return ""
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary."""
        summary_keywords = ['summary', 'objective', 'profile', 'about']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                # Get lines after the summary header
                summary_text = '\n'.join(lines[i+1:i+4])
                return summary_text.strip()
        
        return ""
    
    def _extract_skills(self, doc, text: str) -> List[str]:
        """Extract technical and soft skills."""
        skills = []
        
        # Common skill keywords
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
            'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
            'react', 'vue', 'angular', 'node.js', 'django', 'flask', 'fastapi', 'spring',
            'html', 'css', 'sass', 'webpack', 'git', 'rest', 'graphql', 'grpc',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
            'pytorch', 'scikit-learn', 'pandas', 'numpy', 'spark', 'hadoop',
            'leadership', 'communication', 'project management', 'agile', 'scrum',
        ]
        
        text_lower = text.lower()
        for skill in skill_keywords:
            if skill in text_lower:
                skills.append(skill.title())
        
        return list(set(skills))
    
    def _extract_education(self, doc) -> List[Dict[str, str]]:
        """Extract education information."""
        education = []
        
        degree_types = ['bachelor', 'master', 'phd', 'diploma', 'associate', 'b.s.', 'm.s.']
        
        for ent in doc.ents:
            if ent.label_ == "ORG":  # Organizations are often universities
                education.append({
                    "institution": ent.text,
                    "degree": "",
                    "field": ""
                })
        
        return education[:5]  # Limit to 5 entries
    
    def _extract_experience(self, doc, text: str) -> List[Dict[str, str]]:
        """Extract work experience."""
        experience = []
        
        # Look for job titles and company names
        for ent in doc.ents:
            if ent.label_ == "ORG":
                experience.append({
                    "company": ent.text,
                    "position": "",
                    "duration": "",
                    "description": ""
                })
        
        return experience[:10]  # Limit to 10 entries
    
    def _extract_projects(self, doc, text: str) -> List[Dict[str, str]]:
        """Extract projects."""
        projects = []
        
        project_keywords = ['project', 'developed', 'built', 'created', 'deployed']
        lines = text.split('\n')
        
        current_project = None
        for line in lines:
            if any(keyword in line.lower() for keyword in project_keywords):
                if current_project:
                    projects.append(current_project)
                current_project = {
                    "name": line.strip(),
                    "description": "",
                    "technologies": []
                }
        
        if current_project:
            projects.append(current_project)
        
        return projects[:5]  # Limit to 5 projects
    
    def _extract_certifications(self, doc) -> List[str]:
        """Extract certifications."""
        certifications = []
        
        cert_keywords = ['certification', 'certified', 'credential', 'license']
        
        # Look for these in the text (would need full text access)
        # This is a simplified version
        
        return certifications
    
    def _extract_languages(self, doc, text: str) -> List[str]:
        """Extract languages spoken."""
        languages = []
        
        language_list = ['english', 'spanish', 'french', 'german', 'mandarin', 
                        'japanese', 'hindi', 'portuguese', 'russian', 'arabic',
                        'italian', 'korean', 'polish', 'dutch', 'turkish']
        
        text_lower = text.lower()
        for lang in language_list:
            if lang in text_lower:
                languages.append(lang.title())
        
        return languages
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate sentence embeddings for semantic search."""
        embedding = self.embedding_model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts."""
        from sklearn.metrics.pairwise import cosine_similarity
        
        emb1 = self.embedding_model.encode(text1)
        emb2 = self.embedding_model.encode(text2)
        
        similarity = cosine_similarity([emb1], [emb2])[0][0]
        return float(similarity)


# Initialize singleton extractor
_extractor = None


def get_nlp_extractor() -> NLPExtractor:
    """Get NLP extractor instance (singleton pattern)."""
    global _extractor
    if _extractor is None:
        _extractor = NLPExtractor()
    return _extractor
