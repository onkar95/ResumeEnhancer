from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.workflows.state import (
    ResumeTailorState
)

from app.agents.resume_parser_agent import (
    resume_parser_node
)

from app.agents.jd_parser_agent import (
    jd_parser_node
)

from app.agents.gap_analysis_agent import (
    gap_analysis_node
)

from app.agents.resume_tailor_agent import (
    resume_tailor_node
)

from app.agents.validation_agent import (
    validation_node
)

from app.agents.comparison_agent import (
    comparison_node
)
from app.agents.enhancement_plan_agent import (
    enhancement_plan_node
)

from app.agents.inventory_reasoning_agent import (
    inventory_reasoning_node
)

from app.agents.tailoring_context_agent import (
    tailoring_context_node
)

from app.agents.inventory_merge_agent import (
    inventory_merge_node
)

from app.agents.candidate_suggestion_agent import (
    candidate_suggestion_node
)

from app.agents.tailoring_decision_agent import (
    tailoring_decision_node
)

MAX_RETRIES = 3


def validation_router(state):

    result = state["validation_result"]

    if result.is_valid:
        return "comparison"

    if state["retry_count"] >= MAX_RETRIES:
        return END

    return "resume_tailor"




builder = StateGraph(
    ResumeTailorState
)

builder.add_node(
    "resume_parser",
    resume_parser_node
)

builder.add_node(
    "jd_parser",
    jd_parser_node
)

builder.add_node(
    "gap_analysis",
    gap_analysis_node
)
builder.add_node(
    "enhancement_plan",
    enhancement_plan_node
)
builder.add_node(
    "inventory_reasoning",
    inventory_reasoning_node
)
builder.add_node(
    "inventory_merge",
    inventory_merge_node
)

builder.add_node(
    "candidate_suggestions",
    candidate_suggestion_node
)

builder.add_node(
    "tailoring_decision",
    tailoring_decision_node
)

builder.add_node(
    "tailoring_context",
    tailoring_context_node
)
builder.add_node(
    "resume_tailor",
    resume_tailor_node
)

builder.add_node(
    "validation",
    validation_node
)

builder.add_node(
    "comparison",
    comparison_node
)

#edges

builder.add_edge(
    START,
    "resume_parser"
)

builder.add_edge(
    "resume_parser",
    "inventory_merge"
)

builder.add_edge(
    "inventory_merge",
    "jd_parser"
)

builder.add_edge(
    "jd_parser",
    "candidate_suggestions"
)

builder.add_edge(
    "candidate_suggestions",
    "gap_analysis"
)

builder.add_edge(
    "gap_analysis",
    "inventory_reasoning"
)

builder.add_edge(
    "inventory_reasoning",
    "enhancement_plan"
)

builder.add_edge(
    "enhancement_plan",
    "tailoring_context"
)

builder.add_edge(
    "tailoring_context",
    "tailoring_decision"
)

builder.add_edge(
    "tailoring_decision",
    "resume_tailor"
)

builder.add_edge(
    "resume_tailor",
    "validation"
)

builder.add_conditional_edges(
    "validation",
    validation_router
)

builder.add_edge(
    "comparison",
    END
)

resume_tailor_graph = (
    builder.compile()
)
