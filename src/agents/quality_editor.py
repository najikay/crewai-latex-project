"""
src/agents/quality_editor.py
============================
Technical Peer Reviewer & Quality Editor.

Persona:    Prof. Daniel Stern
Role:       Technical Peer Reviewer & Quality Editor
"""

from __future__ import annotations
from typing import Any
from crewai import Agent
from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger

_ROLE = "Technical Peer Reviewer & Quality Editor"

_GOAL = (
    "Critique the draft paper for technical accuracy, citation completeness, and adherence to IEEE standards. "
    "Verify that the 8-equation minimum is met and that the tone remains formal and academic. "
    "Export quality audit axes (PASS/WARN/FAIL)."
)

_BACKSTORY = (
    "Prof. Daniel Stern is a veteran academic editor who has reviewed hundreds of submissions for IEEE journals. "
    "He has a sharp eye for detail and a zero-tolerance policy for generic AI-generated content."
)

def create_quality_editor(tools: list[Any] | None = None) -> Agent:
    if tools is None:
        tools = []
    logger.debug(f"Creating QualityEditor | LLM={LLM_IDENTIFIER}")
    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["quality_editor"],
        memory=False,
    )
