from app.core.logger import logger

from app.services.jd_parser_service import (
    JDParserService,
)


def jd_parser_node(state):
    logger.info("started JD parsing-agent")

    parser = JDParserService()

    parsed_jd = parser.parse(
        state["jd_text"]
    )
    logger.info("completed JD parsing-agent")
    return {
        "parsed_jd": parsed_jd
    }
