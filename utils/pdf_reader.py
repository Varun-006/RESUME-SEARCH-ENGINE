import os
from pypdf import PdfReader


class PDFReader:
    """
    Reads PDF resumes from a folder and extracts text.
    """

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a single PDF file.
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return ""

    def load_resumes(self):
        """
        Read every PDF inside the folder and return list of dicts.
        """
        resumes = []

        if not os.path.exists(self.folder_path):
            print(f"Folder not found: {self.folder_path}")
            return resumes

        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(self.folder_path, filename)
                text = self.extract_text_from_pdf(full_path)
                if text:
                    resumes.append({
                        "filename": filename,
                        "text": text
                    })

        return resumes
