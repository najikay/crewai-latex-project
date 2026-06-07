"""
src/agents/slam_researcher.py
==============================
SLAMAndFusionResearcher — Primary Research Agent.
"""

from __future__ import annotations
from typing import Any
from crewai import Agent
from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger

_ROLE = "SLAM, Sensor Fusion & Signal Processing Research Specialist"

_GOAL = "Produce structured research briefs with algorithms, equations, and benchmarks."

_BACKSTORY = "Prof. Amir Ben-David is a SLAM and sensor fusion expert with a PhD from the Technion."

def create_slam_researcher(tools: list[Any] | None = None) -> Agent:
    if tools is None:
        tools = []
    logger.debug(f"Creating SLAMAndFusionResearcher | LLM={LLM_IDENTIFIER}")
    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["deep_researcher"],
        memory=True,
    )
