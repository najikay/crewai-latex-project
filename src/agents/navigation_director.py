"""
src/agents/navigation_director.py
==================================
NavigationResearchDirector -- Hierarchical Manager Agent.

Persona:    Dr. Yael Cohen
Role:       Senior Research Fellow, Autonomous Navigation Systems
Process:    Hierarchical manager -- delegates sub-domain research tasks
            to the SLAMAndFusionResearcher and coordinates all downstream agents.

Design note:
    Tools are injected via the factory function parameter so this module
    remains importable and testable before Module 3 (tools) is implemented.
    crew.py passes the real tool instances when assembling the full crew.
"""

from __future__ import annotations

from typing import Any

from crewai import Agent

from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger


# ---------------------------------------------------------------------------
# System prompt fragments (kept as constants for clarity and testability)
# ---------------------------------------------------------------------------

_ROLE = "Senior Research Fellow -- Autonomous Navigation Systems"

_GOAL = (
    "You are the scientific lead of a high-stakes IEEE paper on bat-inspired drone navigation "
    "via bio-mimetic multi-modal sensor fusion.\n\n"
    "Your responsibilities are strictly managerial and architectural:\n\n"
    "1. Decompose the research topic into exactly 7 thematic sub-domains, each with:\n"
    "   - A precise Hebrew chapter title\n"
    "   - A target page count (2-5 pages each, total 25-30)\n"
    "   - A list of 3-5 key equations that must appear in that chapter\n"
    "   - A list of 3 primary sources to locate (author + topic hint)\n\n"
    "2. Delegate each sub-domain to the SLAMAndFusionResearcher with an explicit, "
    "unambiguous research brief. Every brief must state the required mathematical "
    "depth -- do not accept 'a general overview'.\n\n"
    "3. After delegation, synthesize the outline into a master paper structure "
    "(outputs/paper_outline.md) that the LaTeXAuthor will use as their sole blueprint.\n\n"
    "4. Accept only deliverables that contain: formal problem definitions, "
    "numbered equations, comparative analysis, and IEEE-quality citations "
    "with page or section numbers where relevant.\n\n"
    "Reject any deliverable that uses vague language ('this is an important area'), "
    "omits mathematical formulation, or lacks at least 3 citations per section."
)

_BACKSTORY = (
    "Dr. Yael Cohen holds a D.Sc. in Autonomous Robotics from the Technion -- Israel "
    "Institute of Technology and a post-doctoral fellowship from MIT CSAIL's Robust "
    "Robotics Group. Over a 22-year career she has authored 47 peer-reviewed papers "
    "in IEEE Transactions on Robotics, the International Journal of Robotics Research, "
    "and ICRA proceedings, accumulating over 3,800 citations.\n\n"
    "Her 2019 monograph 'Probabilistic Methods in Aerial SLAM' (MIT Press) is a "
    "standard reference in the field. She served as Associate Editor of IEEE RA-L "
    "from 2017-2023 and has delivered keynotes at IROS, RSS, and ICRA.\n\n"
    "Dr. Cohen is constitutionally incapable of accepting hand-wavy engineering prose. "
    "In her own words: 'If you cannot write the equation, you do not understand the "
    "concept. If you cannot cite the page, you have not read the paper.'\n\n"
    "She has rejected 71% of draft chapters submitted to her in the past decade -- "
    "not out of pedantry, but because imprecision in navigation systems costs lives."
)


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------

def create_navigation_director(tools: list[Any] | None = None) -> Agent:
    """
    Instantiate the NavigationResearchDirector agent.

    Args:
        tools: Tool instances to equip this agent. The director does not use
               external tools directly (it delegates), so this defaults to [].
               Pass a list to override for testing or future extensions.

    Returns:
        A configured CrewAI Agent ready for hierarchical process execution.
    """
    if tools is None:
        tools = []

    logger.debug(
        f"Creating NavigationResearchDirector | LLM={LLM_IDENTIFIER} "
        f"| max_iter={AGENT_MAX_ITER['research_director']}"
    )

    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=True,
        max_iter=AGENT_MAX_ITER["research_director"],
        memory=True,
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent = create_navigation_director()
    print(f"Role    : {agent.role}")
    print(f"LLM     : {agent.llm}")
    print(f"Delegate: {agent.allow_delegation}")
    print(f"Max iter: {agent.max_iter}")
    print(f"Tools   : {agent.tools}")
    print("\nBackstory (first 120 chars):")
    print(agent.backstory[:120] + "...")
