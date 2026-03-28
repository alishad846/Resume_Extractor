"""PDF and document text extraction utilities."""

from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF file content."""
    try:
        from io import BytesIO
        pdf_file = BytesIO(pdf_content)
        reader = PdfReader(pdf_file)
        
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"
        
        return extracted_text
    
    except Exception as e:
        logger.error(f"❌ PDF extraction error: {str(e)}")
        raise ValueError(f"Failed to extract PDF text: {str(e)}")


def validate_pdf(pdf_content: bytes) -> bool:
    """Validate if the content is a valid PDF."""
    try:
        from io import BytesIO
        pdf_file = BytesIO(pdf_content)
        PdfReader(pdf_file)
        return True
    except:
        return False
