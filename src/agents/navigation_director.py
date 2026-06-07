"""
src/agents/navigation_director.py
==================================
NavigationResearchDirector -- Hierarchical Manager Agent.
"""

from __future__ import annotations
from typing import Any
from crewai import Agent
from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger

_ROLE = "Senior Research Fellow -- Autonomous Navigation Systems"

_GOAL = (
    "You are the scientific lead of a high-stakes IEEE paper on bat-inspired drone navigation "
    "via bio-mimetic multi-modal sensor fusion.\n\n"
    "Your responsibilities are strictly managerial and architectural:\n\n"
    "1. Decompose the research topic into exactly 7 thematic sub-domains.\n"
    "2. Delegate each sub-domain to the SLAMAndFusionResearcher.\n"
    "3. Synthesize the outline into a master paper structure.\n"
    "4. Accept only high-quality technical deliverables."
)

_BACKSTORY = (
    "Dr. Yael Cohen holds a D.Sc. in Autonomous Robotics from the Technion. "
    "She is a veteran of AI systems research with a focus on bio-inspired navigation."
)

def create_navigation_director(tools: list[Any] | None = None) -> Agent:
    if tools is None:
        tools = []
    logger.debug(f"Creating NavigationResearchDirector | LLM={LLM_IDENTIFIER}")
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
