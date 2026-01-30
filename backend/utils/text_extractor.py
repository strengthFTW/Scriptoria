import pdfplumber
from docx import Document
import io

def extract_text_from_pdf(file_stream):
    """Extract text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_stream):
    """Extract text from DOCX using python-docx."""
    doc = Document(file_stream)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text).strip()

def clean_text(text):
    """Basic text cleaning."""
    if not text:
        return ""
    # Remove excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
