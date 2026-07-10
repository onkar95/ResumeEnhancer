from app.services.jd_parser_service import (
    JDParserService,
)


async def jd_parser_node(state):

    parser = JDParserService()

    parsed_jd = await parser.parse(
        state["jd_text"]
    )

    return {
        "parsed_jd": parsed_jd
    }