from app.services import ResumeParserService, PDFExtractionService
from app.core.logger import logger

async def resume_parser_node(state):

    pdf_service = PDFExtractionService()
    parser = ResumeParserService()

    logger.info("Starting Resume parsing-agent")

    text = pdf_service.extract_text(state["resume_pdf_path"])
    links = pdf_service.extract_hyperlinks(state["resume_pdf_path"])

    parsed_resume = await parser.parse_resume(text)

    # Reattach the real URLs -- the LLM never sees these, pure text
    # extraction can't recover a link target.
    parsed_resume.contact_info.github_url = links.get("github_url")
    parsed_resume.contact_info.linkedin_url = links.get("linkedin_url")
    parsed_resume.contact_info.portfolio_url = links.get("portfolio_url")
    parsed_resume.contact_info.website_url = links.get("website_url")

    logger.info("Completed Resume parsing-agent")
    return {"parsed_resume": parsed_resume}