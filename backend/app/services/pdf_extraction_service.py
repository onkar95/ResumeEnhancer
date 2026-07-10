import fitz
from app.prompts.resume_parser_prompt import (
    RESUME_PARSER_PROMPT
)


class PDFExtractionService:

    def extract_text(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return text
