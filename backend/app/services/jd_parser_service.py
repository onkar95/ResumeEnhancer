from app.utils.jd_normalizer import normalize_jd
from app.core.logger import logger

from app.prompts.job_description_prompt import (
    build_job_description_prompt,
)

from app.schemas.job_description import (
    JobDescription,
)


from app.services.groq_service import GroqService as LLMService


from app.utils.json_utils import (
    extract_json,
)


class JDParserService:

    def __init__(self):
        # self.groq_service = GroqService()
       self.llm_service = LLMService()
    async def parse(self, job_description_text: str) -> JobDescription:

        logger.info("Starting job description parsing")

        try:

            prompt = build_job_description_prompt(job_description_text)
            logger.info("JD parsing prompt generated")

            response = self.llm_service.generate(prompt)
            logger.info("Response received from LLM")

            parsed_json = extract_json(response)
            logger.info("JSON extracted successfully")

            normalised_json = normalize_jd(parsed_json)

            jd = JobDescription.model_validate(normalised_json)
            logger.info("Job description validated successfully")

            return jd

        except Exception as e:

            logger.exception(
                "Failed to parse Job Description"
            )

            raise e
