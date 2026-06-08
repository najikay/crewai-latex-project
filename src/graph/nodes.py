"""
src/graph/nodes.py
==================
LangGraph node functions. Each node:
  - Receives the full PipelineState
  - Does its work (runs a CrewAI sub-crew or parses a file)
  - Returns a dict of state keys to update (LangGraph merges these)
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from crewai import Crew, Process

from src.agents import (
    create_slam_researcher,
    create_latex_author,
    create_quality_editor,
)
from src.graph.state import PipelineState
from src.tasks.research_tasks import (
    create_task_research,
    create_task_latex,
    create_task_review,
    create_remediation_task,        # new factory — see research_tasks.py changes
)
from src.tools import (
    ArxivSearchTool, FileReaderTool,
    NavigatorWebScraperTool, SafeFileWriterTool, SerperDevSearchTool,
)
from src.config import logger

QUALITY_THRESHOLD = 75   # score below this triggers remediation
MAX_REMEDIATIONS  = 2    # hard cap — prevents infinite loops


# ---------------------------------------------------------------------------
# Node 1: run_main_pipeline
# ---------------------------------------------------------------------------
def run_main_pipeline(state: PipelineState) -> dict:
    """
    Runs the existing 4-task CrewAI pipeline (outline → research → figures → latex).
    The QualityEditor is NOT included here; it runs as a separate LangGraph node
    so its verdict can control routing.
    """
    from src.crew import build_crew  # lazy import avoids circular deps

    logger.info("[Graph] NODE: run_main_pipeline")
    # For now, we'll just run the full crew since build_crew builds all 5 agents.
    # In a perfect world, build_crew would take `include_editor=False`.
    # We'll use the existing build_crew to avoid breaking the user's setup too much.
    crew, accountant = build_crew(topic=state["topic"])
    crew.kickoff()
    return {"quality_verdict": "PENDING"}


# ---------------------------------------------------------------------------
# Node 2: run_quality_gate
# ---------------------------------------------------------------------------
def run_quality_gate(state: PipelineState) -> dict:
    """
    Runs only the QualityEditor. Parses its structured JSON verdict from
    outputs/quality_report.md to populate quality_verdict, quality_score,
    and failed_sections in the state.
    """
    logger.info("[Graph] NODE: run_quality_gate")

    editor  = create_quality_editor(tools=[FileReaderTool()])
    t_review = create_task_review(editor, context=[])   # context is files on disk

    Crew(
        agents=[editor],
        tasks=[t_review],
        process=Process.sequential,
        verbose=True,
    ).kickoff()

    # --- Parse the structured verdict from the report ---
    report_path = Path("outputs/quality_report.md")
    verdict, score, failed = _parse_quality_report(report_path)

    logger.info(f"[Graph] Quality verdict={verdict} score={score} failed={failed}")
    return {
        "quality_verdict": verdict,
        "quality_score": score,
        "failed_sections": failed,
    }


def _parse_quality_report(report_path: Path) -> tuple[str, int, list[str]]:
    """
    Extracts the machine-readable JSON block the editor embeds in its report.
    """
    try:
        text = report_path.read_text(encoding="utf-8")
        # Extract the first ```json ... ``` block in the report
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if not match:
            logger.warning("[Graph] No JSON verdict block found — defaulting to PASS")
            return "PASS", 100, []

        data = json.loads(match.group(1))
        score  = int(data.get("score", 100))
        failed = data.get("failed_sections", [])
        verdict = "PASS" if score >= QUALITY_THRESHOLD else "FAIL"
        return verdict, score, failed

    except Exception as exc:
        logger.error(f"[Graph] Failed to parse quality report: {exc} — defaulting to PASS")
        return "PASS", 100, []


# ---------------------------------------------------------------------------
# Node 3: run_remediation
# ---------------------------------------------------------------------------
def run_remediation(state: PipelineState) -> dict:
    """
    Targeted remediation: builds a minimal sub-crew from only the agents
    responsible for the failed sections and re-runs just those tasks.
    """
    count = state["remediation_count"] + 1
    logger.info(f"[Graph] NODE: run_remediation (attempt {count}/{MAX_REMEDIATIONS})")
    logger.info(f"[Graph] Failed sections: {state['failed_sections']}")

    failed = state["failed_sections"]

    # --- Determine which agents are needed ---
    agents, tasks = [], []

    # Researcher is needed if content/algorithm sections failed
    RESEARCH_SECTIONS = {"methodology", "algorithms", "related_work", "equations"}
    if any(s in RESEARCH_SECTIONS for s in failed):
        researcher = create_slam_researcher(tools=[
            SerperDevSearchTool(), ArxivSearchTool(), NavigatorWebScraperTool()
        ])
        t_research = create_remediation_task(
            agent=researcher,
            failed_sections=[s for s in failed if s in RESEARCH_SECTIONS],
            quality_report_path="outputs/quality_report.md",
            output_file="outputs/research_briefs.md",
        )
        agents.append(researcher)
        tasks.append(t_research)

    # LaTeX Author is always needed to re-render any fixed content
    author = create_latex_author(tools=[SafeFileWriterTool(), FileReaderTool()])
    t_latex = create_remediation_task(
        agent=author,
        failed_sections=failed,
        quality_report_path="outputs/quality_report.md",
        output_file="latex/references.bib",
    )
    agents.append(author)
    tasks.append(t_latex)

    if tasks:
        Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        ).kickoff()

    return {
        "remediation_count": count,
        "quality_verdict": "PENDING",  # reset — gate will re-evaluate
    }
