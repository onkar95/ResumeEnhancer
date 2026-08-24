"""
Resume Parser Service

Responsibilities

1. Build parser prompt
2. Call Groq
3. Parse JSON
4. Normalize response
5. Validate ResumeDocument
6. Return ResumeDocument
"""

from app.prompts.resume_parser_prompt import (
    RESUME_PARSER_PROMPT,
)

from app.schemas.resume import (
    ResumeDocument,
)


# from app.services.models.groq_service import GroqService as LLMService
from app.services.models.gemini_service import GeminiService as LLMService


from app.utils.json_utils import (
    parse_llm_json,
)

from app.utils.resume_normalizer import (
    normalize_resume,
)
from string import Template
from app.core.logger import logger


class ResumeParserService:
    """
    Converts extracted resume text into ResumeDocument.
    """

    def __init__(self):

        self.llm_service = LLMService()

    async def parse_resume(
        self,
        resume_text: str,
    ) -> ResumeDocument:
        """
        Parse resume text into ResumeDocument.

        Args
        ----
        resume_text : str

        Returns
        -------
        ResumeDocument
        """
        try:

            template = Template(RESUME_PARSER_PROMPT)

            prompt = template.substitute(
                resume_text=resume_text
            )
            logger.info("Resume parsing prompt generated")


            llm_response = await self.llm_service.generate_json(
                prompt
            )

            logger.info("LLM call-1 Resume parsing LLMResponse Received")
            parsed_json = parse_llm_json(
                llm_response
            )
            
            print("RAW:", repr(llm_response))

            parsed_json = parse_llm_json(llm_response)
            print("PARSED:", repr(parsed_json))

            normalized_json = normalize_resume(parsed_json)
            print("NORMALIZED:", repr(normalized_json))

            # print("llm response for resume parsing into json ", "=" * 100)
            # print("", parsed_json)  # Print the last 3000 characters
            # print("=" * 100)

            normalized_json = normalize_resume(
                parsed_json
            )

            resume = ResumeDocument.model_validate(
                normalized_json
            )

            logger.info("Resume validated successfully")
            return resume
        except Exception as e:

            logger.exception(
                "Failed to parse Resume"
            )

            raise e


# import json
# from app.services.groq_service import GroqService
# from app.prompts.resume_parser_prompt import (
#     RESUME_PARSER_PROMPT
# )
# from app.utils.json_utils import (
#     parse_llm_json
# )


# class ResumeParserService:

#     def __init__(self):
#         self.groq_service = GroqService()

#     async def parse_resume(
#         self,
#         resume_text: str
#     ):

#         prompt = RESUME_PARSER_PROMPT.format(
#             resume_text=resume_text
#         )


#         response = await self.groq_service.generate(
#             prompt
#         )

#         return parse_llm_json(response)
