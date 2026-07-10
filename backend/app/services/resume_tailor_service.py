import json

from app.core.logger import logger

from app.prompts.resume_tailor_prompt import (
    build_resume_tailor_prompt,
)

from app.schemas.job_description import (
    JobDescription,
)

from app.schemas.resume import (
    ResumeDocument,
)


from app.services.groq_service import GroqService as LLMService



from app.utils.json_utils import (
    extract_json,
)

from app.utils.resume_normalizer import (
    normalize_resume,
)


class ResumeTailorService:

    def __init__(self):

        # self.llm_service = GroqService()
        self.llm_service = LLMService()
    async def tailor(
        self,
        resume: ResumeDocument,
        job_description: JobDescription,
    ) -> ResumeDocument:

        logger.info(
            "Starting resume tailoring process"
        )

        try:

            resume_json = json.dumps(
                resume.model_dump(),
                indent=2,
                ensure_ascii=False,
            )

            jd_json = json.dumps(
                job_description.model_dump(),
                indent=2,
                ensure_ascii=False,
            )

            prompt = build_resume_tailor_prompt(
                resume_json=resume_json,
                job_description_json=jd_json,
            )

            logger.info(
                "Resume tailoring prompt generated"
            )

            response = await self.llm_service.generate(
                prompt
            )

            logger.info(
                "Tailoring response received from LLM"
            )

            parsed_json = extract_json(
                response
            )

            logger.info(
                "Tailored resume JSON extracted"
            )

            normalized_resume = normalize_resume(
                parsed_json
            )

            logger.info(
                "Tailored resume normalized"
            )

            tailored_resume = ResumeDocument.model_validate(
                normalized_resume
            )

            logger.info(
                "Resume tailoring completed successfully"
            )

            return tailored_resume

        except Exception:

            logger.exception(
                "Resume tailoring failed"
            )

            raise