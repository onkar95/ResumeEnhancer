from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.inventory_reasoning import (
    InventoryReasoning,
    RelatedSkill
)


RELATED_SKILL_MAP = {

    "microservices": [
        "docker",
        "rabbitmq",
        "grpc"
    ],

    "event driven architecture": [
        "rabbitmq",
        "kafka"
    ],

    "cloud native": [
        "docker",
        "kubernetes"
    ],

    "distributed systems": [
        "rabbitmq",
        "grpc",
        "docker"
    ]
}


def inventory_reasoning_node(
    state: ResumeTailorState
):

    inventory = state[
        "resume_inventory"
    ]

    jd = state[
        "parsed_jd"
    ]

    inventory_skills = {

        skill.name.lower()

        for skill in inventory.skills
    }

    reasoning = InventoryReasoning()

    jd_terms = (
        jd.required_skills
        + jd.preferred_skills
        + jd.keywords
    )

    for term in jd_terms:

        normalized = (
            term.strip()
            .lower()
        )

        if (
            normalized
            not in RELATED_SKILL_MAP
        ):
            continue

        related = (
            RELATED_SKILL_MAP[
                normalized
            ]
        )

        for skill in related:

            if (
                skill
                in inventory_skills
            ):

                reasoning.related_skills.append(
                    RelatedSkill(
                        skill=skill,
                        reason=(
                            f"{skill} supports {term}"
                        ),
                        confidence=0.90
                    )
                )

    return {
        "inventory_reasoning":
            reasoning
    }