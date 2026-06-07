"""
src/agents/latex_author.py
==========================
IEEE LaTeX Technical Author (Hebrew/English Bilingual).

Persona:    Yael Mizrahi
Role:       IEEE LaTeX Technical Author (Hebrew/English Bilingual)
"""

from __future__ import annotations
from typing import Any
from crewai import Agent
from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger

_ROLE = "IEEE LaTeX Technical Author (Hebrew/English Bilingual)"

_GOAL = (
    "Convert research summaries and figure references into complete, compilable LaTeX chapters in Hebrew. "
    "Follow IEEE IEEEtran class conventions exactly. Integrate all figures, tables, and equations. "
    "Ensure the document structure supports 25-30 pages."
)

_BACKSTORY = (
    "Yael Mizrahi is a bilingual academic writer with 10 years of experience writing IEEE papers in Hebrew. "
    "She knows LaTeX syntax perfectly and never produces code that does not compile under XeLaTeX."
)

def create_latex_author(tools: list[Any] | None = None) -> Agent:
    if tools is None:
        tools = []
    logger.debug(f"Creating LaTeXAuthor | LLM={LLM_IDENTIFIER}")
    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["latex_author"],
        memory=True,
    )
