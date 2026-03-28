"""Resume extraction endpoints."""

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import List, Dict, Any
import logging

from app.services.nlp_extractor import get_nlp_extractor
from app.services.pdf_extractor import extract_text_from_pdf

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/extract", summary="Extract entities from resume")
async def extract_entities(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extract entities from an uploaded resume file.
    
    **Returns:**
    - Name, email, phone
    - Skills, experience, education
    - Projects, certifications
    - AI-generated insights
    """
    try:
        # Read file
        content = await file.read()
        
        # Extract text from PDF/DOC
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith(('.doc', '.docx')):
            text = extract_text_from_docx(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Extract entities using NLP
        extractor = get_nlp_extractor()
        extracted_data = extractor.extract_entities(text)
        
        logger.info(f"✅ Successfully extracted entities from: {file.filename}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "extracted_data": extracted_data,
            "raw_text_length": len(text),
            "confidence": 0.85,  # Could be calculated based on extraction quality
        }
    
    except Exception as e:
        logger.error(f"❌ Error extracting entities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.get("/extract/{resume_id}", summary="Get extracted data by resume ID")
async def get_extracted_data(resume_id: str) -> Dict[str, Any]:
    """Get previously extracted data for a resume."""
    # This would fetch from database
    # Placeholder implementation
    return {
        "resume_id": resume_id,
        "extracted_data": {},
        "extracted_at": "2024-01-01T00:00:00Z"
    }


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX file."""
    from docx import Document
    from io import BytesIO
    
    doc = Document(BytesIO(content))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
