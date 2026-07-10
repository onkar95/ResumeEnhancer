from app.services import ResumeParserService, PDFExtractionService


async def resume_parser_node(state):

    pdf_service = PDFExtractionService()
    parser = ResumeParserService()

    text = pdf_service.extract_text(
        state["resume_pdf_path"]
    )

    parsed_resume = await parser.parse_resume(
        text
    )

    return {
        "parsed_resume": parsed_resume
    }