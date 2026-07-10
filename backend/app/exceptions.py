"""
Application Exceptions
"""


class ResumeTailorException(Exception):
    """Base application exception."""


class PDFExtractionException(ResumeTailorException):
    """Raised when PDF extraction fails."""


class ResumeParserException(ResumeTailorException):
    """Raised when resume parsing fails."""


class GroqServiceException(ResumeTailorException):
    """Raised when Groq request fails."""


class JSONParsingException(ResumeTailorException):
    """Raised when JSON parsing fails."""