import fitz


class PDFExtractionService:

    def extract_text(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def extract_hyperlinks(self, pdf_path: str) -> dict:
        """
        PyMuPDF's get_links() reads actual link annotations (the real
        target URL), which get_text() cannot see -- it only sees the
        visible caption ("GitHub", "LinkedIn"). Classify by domain.
        """
        doc = fitz.open(pdf_path)

        urls = []
        for page in doc:
            for link in page.get_links():
                uri = link.get("uri")
                if uri:
                    urls.append(uri)
        doc.close()

        result = {
            "github_url": None,
            "linkedin_url": None,
            "portfolio_url": None,
            "website_url": None,
        }

        for url in urls:
            lower = url.lower()
            if "github.com" in lower and not result["github_url"]:
                result["github_url"] = url
            elif "linkedin.com" in lower and not result["linkedin_url"]:
                result["linkedin_url"] = url
            elif not result["website_url"]:
                result["website_url"] = url

        return result