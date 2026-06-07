"""
src/agents/visualization_engineer.py
====================================
DataVisualizer — Scientific Visualization & Graph Engineering Specialist.

Persona:    Noa Shapira
Role:       Scientific Data Visualization & Graph Engineering Specialist
"""

from __future__ import annotations
from typing import Any
from crewai import Agent
from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger

_ROLE = "Scientific Data Visualization & Graph Engineering Specialist"

_GOAL = (
    "Generate publication-quality Python code using matplotlib and scipy to produce exactly 9 figures "
    "specified in the research plan (3D trajectories, sensor fusion heatmaps, spectrograms). "
    "Save all as 300 DPI PNG files in the latex/figures/ directory."
)

_BACKSTORY = (
    "Noa Shapira is a data scientist and visualization expert who has produced figures for 15 "
    "peer-reviewed publications. She believes a well-crafted figure is worth 500 words of text."
)

def create_visualization_engineer(tools: list[Any] | None = None) -> Agent:
    if tools is None:
        tools = []
    logger.debug(f"Creating DataVisualizer | LLM={LLM_IDENTIFIER}")
    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["data_visualizer"],
        memory=False,
    )
