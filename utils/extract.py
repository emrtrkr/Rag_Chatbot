import pdfplumber
from docx import Document

def extract_text(file) -> str:
    """
    Extracts text from a PDF or DOCX file-like object.
    """
    text = ""
    name = file.name.lower()
    if name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''
    elif name.endswith('.docx'):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + '\n'
    else:
        raise ValueError(f"Unsupported file type: {file.name}")
    return text
