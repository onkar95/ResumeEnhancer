from enum import Enum


class SkillOrigin(
    str,
    Enum
):

    RESUME = "resume"

    INVENTORY = "inventory"

    USER_APPROVED = "user_approved"

    INFERRED = "inferred"