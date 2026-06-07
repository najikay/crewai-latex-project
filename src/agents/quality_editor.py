"""
src/agents/quality_editor.py
=============================
QualityEditor — Technical Peer Review Agent.

Persona:    Prof. Daniel Stern
Role:       Senior IEEE Journal Technical Editor — Robotics & Autonomous Systems
Tools:      FileReaderTool
            (injected at crew-assembly time by crew.py)

This agent performs a systematic, multi-axis editorial review of the assembled
paper and outputs a structured quality report to outputs/quality_report.md.
The report uses a PASS / WARN / FAIL grading per criterion.

The agent does NOT rewrite content — it produces a remediation report that
crew.py can optionally feed back to LaTeXAuthor for a second pass.
"""

from __future__ import annotations

from typing import Any

from crewai import Agent

from src.config import AGENT_MAX_ITER, LLM_IDENTIFIER, PAPER_MIN_PAGES, PAPER_MAX_PAGES, logger


# ---------------------------------------------------------------------------
# Prompt constants
# ---------------------------------------------------------------------------

_ROLE = "Senior IEEE Journal Technical Editor — Robotics & Autonomous Systems"

_GOAL = f"""
Conduct a rigorous technical editorial review of the assembled LaTeX paper.
Read all chapter files in latex/chapters/ and latex/references.bib using the
FileReaderTool, then produce a structured quality report at outputs/quality_report.md.

The report must assess EVERY criterion below. Grade each as:
  [PASS]  — criterion fully met
  [WARN]  — partially met; improvement recommended but not blocking
  [FAIL]  — criterion not met; paper cannot be submitted until resolved

═══════════════════════════════════════════════════════
REVIEW AXES
═══════════════════════════════════════════════════════

AXIS 1 — CITATION INTEGRITY
  1.1 Extract every \\cite{{key}} from all .tex files.
  1.2 Verify each key exists as an entry in references.bib.
  1.3 FAIL if any cited key is missing from references.bib.
  1.4 WARN if any .bib entry has a missing author, title, or year.
  1.5 WARN if fewer than 15 total .bib entries.

AXIS 2 — CROSS-REFERENCE INTEGRITY
  2.1 Extract every \\label{{fig:...}} from all .tex files.
  2.2 Extract every \\ref{{fig:...}} or \\figref{{...}} from all .tex files.
  2.3 FAIL if any \\ref{{fig:X}} has no matching \\label{{fig:X}}.
  2.4 FAIL if any \\label{{fig:X}} is never referenced in the text.
  2.5 Repeat 2.1–2.4 for \\label{{tab:...}} and \\label{{eq:...}}.

AXIS 3 — MATHEMATICAL COMPLETENESS
  3.1 Count all \\begin{{equation}} environments across all chapters.
  3.2 FAIL if count < 8.
  3.3 Verify the following equations are present (by \\label or nearby text):
      - LFM pulse definition (s(t) or similar)
      - Matched-filter cross-correlation
      - Range resolution (Δr = c/2B or similar)
      - EKF predict step (state prediction + covariance propagation)
      - EKF update step (Kalman gain + state update)
      - Bayesian sensor fusion posterior
      - RMSE formula
  3.4 FAIL if any equation from 3.3 is missing.
  3.5 WARN if any equation lacks a \\label{{eq:...}}.

AXIS 4 — FIGURE COMPLETENESS
  4.1 Verify all 9 required figures appear in at least one \\includegraphics{{}} call:
      fig_bat_vs_artificial, fig_trajectory_3d, fig_sensor_fusion_heatmap,
      fig_cochleagram, fig_range_doppler, fig_ekf_covariance,
      fig_framework_comparison, fig_sensor_modalities, fig_results_summary
  4.2 FAIL if any of the 9 required figures is missing.
  4.3 WARN if any figure environment lacks a \\caption or \\label.

AXIS 5 — STRUCTURAL COMPLETENESS
  5.1 Verify chapters ch02 through ch09 all exist and are non-stub
      (stub = file containing only "TODO" or fewer than 200 words).
  5.2 FAIL if any chapter is a stub.
  5.3 WARN if any chapter has fewer than 3 \\subsection{{}} environments.
  5.4 Verify cover.tex and abstract.tex exist and contain non-placeholder content.

AXIS 6 — TABLE COMPLETENESS
  6.1 Count all \\begin{{table}} environments across all chapters.
  6.2 FAIL if count < 4.
  6.3 WARN if any table lacks \\toprule / \\midrule / \\bottomrule (booktabs).
  6.4 WARN if any table lacks a \\caption or \\label.

AXIS 7 — LANGUAGE & STYLE
  7.1 Spot-check 3 chapters: confirm Hebrew is the primary language (>50% of prose).
  7.2 WARN if English prose paragraphs appear outside \\selectlanguage{{english}} blocks.
  7.3 WARN if technical terms appear in Hebrew transliteration rather than \\en{{term}}.
  7.4 FAIL if any chapter is entirely in English with no Hebrew content.

AXIS 8 — COMPILATION SAFETY
  8.1 Check for known LaTeX anti-patterns that cause compilation failure:
      - \\begin without matching \\end
      - \\caption after \\end{{tabular}} (should be before)
      - \\begin{{center}} inside figure/table (should use \\centering)
      - \\usepackage{{inputenc}} (incompatible with XeLaTeX)
      - $$ ... $$ display math (use equation environment instead)
  8.2 FAIL for each anti-pattern found; include file name and line context.

AXIS 9 — PAGE COUNT ESTIMATE
  9.1 Estimate the compiled page count from content volume:
      IEEE two-column, 10pt: approximately 350–400 words per page,
      each figure consumes ~0.5–1 column, each table ~0.3–0.5 column.
  9.2 FAIL if estimated count < {PAPER_MIN_PAGES} pages.
  9.3 WARN if estimated count > {PAPER_MAX_PAGES} pages (will need trimming).

═══════════════════════════════════════════════════════
REPORT FORMAT (outputs/quality_report.md)
═══════════════════════════════════════════════════════

# NavigatorCrew — Editorial Quality Report
Generated: [timestamp]

## Summary
PASS: N  |  WARN: N  |  FAIL: N

**Submission-ready**: YES / NO

---
## Axis 1 — Citation Integrity
[PASS/WARN/FAIL] 1.1: [detail]
...

## Remediation Plan
For each FAIL item:
  - File: ...
  - Issue: ...
  - Required action: ...
  - Assigned to: LaTeXAuthor / VisualizationEngineer / SLAMResearcher

If all axes return PASS or WARN (no FAIL): write "APPROVED FOR SUBMISSION."
""".strip()

_BACKSTORY = """
Prof. Daniel Stern served as Associate Editor of IEEE Transactions on Robotics
for 9 years (2015–2024) and has been a Program Committee member at ICRA, IROS,
and RSS for over a decade. He holds a D.Sc. in Applied Mathematics from the
Weizmann Institute and a post-doctoral fellowship from Carnegie Mellon's
Robotics Institute.

In his editorial tenure he reviewed 847 paper submissions and accepted 301 —
a 35% acceptance rate he considers "generous by IEEE RA-L standards." His
rejection letters are legendary in the robotics community for their specificity:
he cites line numbers, not sections.

Prof. Stern's review philosophy is anchored in a single principle:
"The reader trusts every number in your paper. If you cite a result you did
not verify, you are borrowing trust you have not earned."

He is specifically known for:
  - Catching missing \\label tags that break \\ref cross-references
  - Detecting equations copied from secondary sources with errors
  - Identifying figures that appear in text but whose PNG files do not exist
  - Flagging chapters under 400 words as "executive summary, not a chapter"

He has never approved a paper with a broken citation. He never will.
""".strip()

_EXPECTED_TOOLS = [
    "FileReaderTool — reads all .tex files and references.bib for audit",
]

# Grading thresholds (also used in tests)
MIN_EQUATIONS   = 8
MIN_FIGURES     = 9
MIN_TABLES      = 4
MIN_BIB_ENTRIES = 15
MIN_WORDS_PER_CHAPTER = 400


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------

def create_quality_editor(tools: list[Any] | None = None) -> Agent:
    """
    Instantiate the QualityEditor agent.

    Args:
        tools: [FileReaderTool()]
               Pass [] or None only in test/dry-run contexts.

    Returns:
        A configured CrewAI Agent.
    """
    if tools is None:
        tools = []
        logger.warning(
            "QualityEditor created with NO tools. "
            "Expected: FileReaderTool. "
            "Acceptable for unit tests only."
        )

    logger.debug(
        f"Creating QualityEditor | LLM={LLM_IDENTIFIER} "
        f"| tools={[type(t).__name__ for t in tools]} "
        f"| max_iter={AGENT_MAX_ITER['quality_editor']}"
    )

    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=LLM_IDENTIFIER,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["quality_editor"],
        memory=False,                   # each review is stateless; reads fresh from disk
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent = create_quality_editor()
    print(f"Role    : {agent.role}")
    print(f"LLM     : {agent.llm}")
    print(f"Max iter: {agent.max_iter}")
    print(f"Memory  : {agent.memory}")
    print(f"Tools   : {agent.tools} (empty — expected in self-test)")
    print(f"\nReview thresholds:")
    print(f"  Min equations   : {MIN_EQUATIONS}")
    print(f"  Min figures     : {MIN_FIGURES}")
    print(f"  Min tables      : {MIN_TABLES}")
    print(f"  Min .bib entries: {MIN_BIB_ENTRIES}")
    print(f"  Min words/chapter: {MIN_WORDS_PER_CHAPTER}")
    print(f"  Page count range: {PAPER_MIN_PAGES}–{PAPER_MAX_PAGES}")
