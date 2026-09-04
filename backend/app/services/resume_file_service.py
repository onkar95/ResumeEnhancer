# services/resume_file_service.py
from pathlib import Path
from app.services.pdf_extraction_service import PDFExtractionService
from app.services.docx_extraction_service import DocxExtractionService


class ResumeFileService:
    """Dispatches text/hyperlink extraction based on file extension."""

    def __init__(self):
        self._pdf = PDFExtractionService()
        self._docx = DocxExtractionService()

    def _service_for(self, path: str):
        ext = Path(path).suffix.lower()
        if ext == ".docx":
            return self._docx
        return self._pdf  # default / .pdf

    def extract_text(self, path: str) -> str:
        return self._service_for(path).extract_text(path)

    def extract_hyperlinks(self, path: str) -> dict:
        return self._service_for(path).extract_hyperlinks(path)