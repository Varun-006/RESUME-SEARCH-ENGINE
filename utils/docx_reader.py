from docx import Document


def read_docx(file_path):
    """
    Extract text from a .docx file.
    """
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()
