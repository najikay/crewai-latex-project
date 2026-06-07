"""
src/tasks/research_tasks.py
===========================
Task definitions for the NavigatorCrew.
"""

from crewai import Task
from src.agents import (
    create_navigation_director,
    create_slam_researcher,
    create_visualization_engineer,
    create_latex_author,
    create_quality_editor
)

def create_outline_task(agent):
    return Task(
        description=(
            "Decompose the topic 'Bat-Inspired Drone Navigation via Bio-Mimetic Multi-Modal Sensor Fusion' "
            "into exactly 7 thematic sub-domains. Define Hebrew titles, page targets, and key equations for each."
        ),
        expected_output="A structured paper outline in Hebrew with mathematical and source requirements for each chapter.",
        agent=agent,
        output_file="outputs/paper_outline.md"
    )

def create_research_task(agent, context):
    return Task(
        description=(
            "For each sub-domain in the outline, find authoritative sources (ArXiv/IEEE). "
            "Extract algorithms, formulas, and benchmarks. Produce structured research briefs in Hebrew."
        ),
        expected_output="Detailed research briefs with LaTeX-ready equations and BibTeX citations.",
        agent=agent,
        context=context
    )

def create_visualization_task(agent, context):
    return Task(
        description=(
            "Generate Python code to create the 9 scientific figures specified in the plan. "
            "Save them as 300 DPI PNGs in latex/figures/."
        ),
        expected_output="9 high-resolution scientific PNG figures.",
        agent=agent,
        context=context
    )

def create_latex_task(agent, context):
    return Task(
        description=(
            "Convert the research briefs and figures into a complete IEEE-formatted LaTeX document in Hebrew. "
            "Ensure the final output is 25-30 pages and compiles with XeLaTeX."
        ),
        expected_output="A set of .tex files in latex/chapters/ and a main.tex ready for compilation.",
        agent=agent,
        context=context
    )

def create_review_task(agent, context):
    return Task(
        description=(
            "Review the generated LaTeX paper for technical accuracy, IEEE standard compliance, "
            "and academic tone. Verify the 8-equation minimum."
        ),
        expected_output="A quality audit report with PASS/WARN/FAIL grades for various axes.",
        agent=agent,
        context=context
    )
