from fastapi import APIRouter
from fastapi import Body

from app.schemas.jd_requests import (
    ParseJDRequest,
    ParseJDResponse,
)

from app.services.jd_parser_service import JDParserService

router = APIRouter(
    tags=["Job Description"]
)


@router.post(
    "/parse",
    response_model=ParseJDResponse
)
async def parse_job_description(
    request: ParseJDRequest
):

    parser = JDParserService()

    parsed_jd = await parser.parse(
        request.job_description
    )

    return ParseJDResponse(
        success=True,
        data=parsed_jd
    )


# works with plan text does not except the json body type
@router.post(
    "/parse-text",
    response_model=ParseJDResponse
)
async def parse_job_description(
    job_description: str = Body(
        ...,
        media_type="text/plain"
    )
):

    parser = JDParserService()

    parsed_jd = await parser.parse(
        job_description
    )

    return ParseJDResponse(
        success=True,
        data=parsed_jd
    )
