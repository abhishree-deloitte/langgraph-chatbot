from docx import Document

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract plain text from a .docx file
    """
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)
