from app.services import ResumeParserService, PDFExtractionService
from app.core.logger import logger

async def resume_parser_node(state):

    pdf_service = PDFExtractionService()
    parser = ResumeParserService()
    
    logger.info("Starting Resume parsing-agent")
    
    text = pdf_service.extract_text(
        state["resume_pdf_path"]
    )
    
    parsed_resume = await parser.parse_resume(
        text
    )

    logger.info("Completed Resume parsing-agent")
    return {
        "parsed_resume": parsed_resume
    }