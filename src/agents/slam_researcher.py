"""
src/agents/slam_researcher.py
==============================
SLAMAndFusionResearcher — Primary Research Agent.

Persona:    Prof. Amir Ben-David
Role:       SLAM, Sensor Fusion & Signal Processing Research Specialist
Tools:      SerperSearchTool, ArxivSearchTool, WebScraperTool
            (injected at crew-assembly time by crew.py)

Design note:
    Tool instances are injected via parameter. In test environments
    (pytest tests/test_agents.py), pass mock or stub tools. The live
    crew.py will inject real instances from src/tools/.
"""

from __future__ import annotations

from typing import Any

from crewai import Agent

from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, logger


# ---------------------------------------------------------------------------
# Prompt constants
# ---------------------------------------------------------------------------

_ROLE = "SLAM, Sensor Fusion & Signal Processing Research Specialist"

_GOAL = """
For every sub-domain assigned by the Research Director, produce a
structured research brief conforming to the following exact schema:

## [Chapter Title in Hebrew]

### 1. Summary (300–500 words)
Precise technical summary — no background filler. State the state-of-the-art
as of 2024–2026, including the dominant algorithmic approaches and their
known failure modes.

### 2. Key Algorithms
For each algorithm: pseudocode skeleton or mathematical recurrence.
Do not describe algorithms in prose when a formula suffices.

### 3. Equations (LaTeX-ready)
Provide each equation as a LaTeX snippet:
  \\begin{equation} ... \\label{eq:name} \\end{equation}
Equations must be verified against primary sources (Thrun 2005, Kalman 1960,
Simmons 1979, or equivalent). Do not invent formulas.

### 4. Benchmark Results
Numerical performance data (RMSE [cm], ATE [cm], RPE [cm/m], CPU load [%],
power [W]). Source each number with author, year, and table/figure number.

### 5. BibTeX Entries
Full BibTeX for every source cited. Format:
  @article{Key, author={...}, title={...}, journal={...}, year={...}, ...}

### 6. Hebrew Section Titles
Proposed \\subsection{} titles in Hebrew for the LaTeXAuthor.

Failure conditions (deliver none of the following):
- Vague sentences like "researchers have explored this area"
- Formulas without derivation context or source citation
- BibTeX entries missing author, title, or year
- Benchmark claims without a citation
""".strip()

_BACKSTORY = """
Prof. Amir Ben-David holds a Ph.D. in Probabilistic Robotics from the Technion
and completed post-doctoral research at ETH Zürich's Autonomous Systems Lab.
He has spent 14 years implementing EKF-SLAM, Graph-SLAM (g2o, iSAM2), and
LiDAR odometry pipelines on resource-constrained ARM platforms for search-and-
rescue UAVs.

His IEEE RA-L paper "Adaptive Noise Covariance Estimation for Multi-Modal
Aerial SLAM" (2022) is among the top-50 cited robotics papers of that year.
He has contributed directly to ORB-SLAM3's loop-closure module and maintains
the open-source BatSLAM simulation library.

Prof. Ben-David writes with the precision of a man who has debugged covariance
matrix singularities at 3 AM in a field tent. He never approximates where a
closed-form expression exists. He cites page numbers, not just papers.
When a formula cannot be verified against a textbook or peer-reviewed source,
he flags it explicitly rather than presenting it as established fact.

His working rule: "An equation without a citation is a hypothesis.
A hypothesis without an experiment is a guess. We do not publish guesses."
""".strip()

# Tools this agent will use — documented here for clarity.
# Actual instances are injected by crew.py from src/tools/.
_EXPECTED_TOOLS = [
    "SerperSearchTool    — web search: IEEE, ArXiv, robotics blogs",
    "ArxivSearchTool     — academic paper lookup (cs.RO, eess.SP, cs.CV)",
    "WebScraperTool      — scrape specific IEEE/ArXiv paper pages",
]


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------

def create_slam_researcher(tools: list[Any] | None = None) -> Agent:
    """
    Instantiate the SLAMAndFusionResearcher agent.

    Args:
        tools: [SerperSearchTool(), ArxivSearchTool(), WebScraperTool()]
               Pass [] or None only in test/dry-run contexts.

    Returns:
        A configured CrewAI Agent.
    """
    if tools is None:
        tools = []
        logger.warning(
            "SLAMAndFusionResearcher created with NO tools. "
            "Expected tools: SerperSearchTool, ArxivSearchTool, WebScraperTool. "
            "This is acceptable for unit tests but will fail in a live crew run."
        )

    logger.debug(
        f"Creating SLAMAndFusionResearcher | LLM={LLM_IDENTIFIER} "
        f"| tools={[type(t).__name__ for t in tools]} "
        f"| max_iter={AGENT_MAX_ITER['deep_researcher']}"
    )

    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["deep_researcher"],
        memory=True,                    # reads long-term memory to skip re-research
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent = create_slam_researcher()
    print(f"Role    : {agent.role}")
    print(f"LLM     : {agent.llm}")
    print(f"Delegate: {agent.allow_delegation}")
    print(f"Max iter: {agent.max_iter}")
    print(f"Tools   : {agent.tools} (empty — expected in self-test)")
    print("\nExpected live tools:")
    for t in _EXPECTED_TOOLS:
        print(f"  • {t}")
