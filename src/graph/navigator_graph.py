"""
src/graph/navigator_graph.py
=============================
Builds and returns the compiled LangGraph state machine that orchestrates
the NavigatorCrew pipeline with a feedback loop.

Graph topology:

  [run_main_pipeline]
          |
          v
  [run_quality_gate]  ──PASS──>  [END]
          |
         FAIL
          |
          v
  [run_remediation]
          |
          v
  [run_quality_gate]  ──PASS──>  [END]
          |
         FAIL (if remediation_count >= MAX_REMEDIATIONS)
          |
          v
         [END]  (graceful degradation with whatever we have)
"""
from __future__ import annotations
from langgraph.graph import StateGraph, END

from src.graph.state import PipelineState
from src.graph.nodes import (
    run_main_pipeline,
    run_quality_gate,
    run_remediation,
    QUALITY_THRESHOLD,
    MAX_REMEDIATIONS,
)
from src.config import logger


def _route_after_quality_gate(state: PipelineState) -> str:
    """
    Conditional edge: decides what happens after the quality gate runs.
    This is the heart of the feedback loop.
    """
    if state["quality_verdict"] == "PASS":
        logger.info("[Graph] ROUTE: Quality PASSED → END")
        return "end"

    if state["remediation_count"] >= MAX_REMEDIATIONS:
        logger.warning(
            f"[Graph] ROUTE: Quality FAILED after {MAX_REMEDIATIONS} remediations "
            f"(score={state['quality_score']}) — accepting current output → END"
        )
        return "end"

    logger.info(
        f"[Graph] ROUTE: Quality FAILED (score={state['quality_score']} < {QUALITY_THRESHOLD}) "
        f"→ remediation #{state['remediation_count'] + 1}"
    )
    return "remediate"


def build_navigator_graph():
    """
    Compile and return the NavigatorCrew LangGraph state machine.
    """
    graph = StateGraph(PipelineState)

    # Register nodes
    graph.add_node("run_main_pipeline", run_main_pipeline)
    graph.add_node("run_quality_gate",  run_quality_gate)
    graph.add_node("run_remediation",   run_remediation)

    # Linear edges
    graph.set_entry_point("run_main_pipeline")
    graph.add_edge("run_main_pipeline", "run_quality_gate")
    graph.add_edge("run_remediation",   "run_quality_gate")

    # THE KEY: conditional edge from the quality gate
    graph.add_conditional_edges(
        "run_quality_gate",
        _route_after_quality_gate,
        {
            "end":       END,
            "remediate": "run_remediation",
        },
    )

    return graph.compile()
