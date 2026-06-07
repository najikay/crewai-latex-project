"""
src/tasks/research_tasks.py
============================
Factory functions for the 5 NavigatorCrew tasks.

Task pipeline (sequential dependency chain):
  task_outline   → task_research → task_figures
                                      ↓
                               task_latex → task_review

Each factory accepts the pre-built agent objects so that crew.py can
inject the correct instances at assembly time.
"""

from __future__ import annotations

from crewai import Agent, Task

from src.config import logger


# ---------------------------------------------------------------------------
# Task 1 — Research Director: Outline
# ---------------------------------------------------------------------------

def create_task_outline(director: Agent) -> Task:
    """
    Director decomposes the paper topic into 7 sub-domains and writes
    the master outline to outputs/paper_outline.md.
    """
    logger.debug("Creating task_outline")
    return Task(
        description=(
            "You are the scientific lead. Decompose the research topic — "
            "'Bat-Inspired Drone Navigation via Bio-Mimetic Multi-Modal Sensor Fusion' — "
            "into EXACTLY 7 thematic sub-domains.\n\n"
            "For each sub-domain produce:\n"
            "  1. A precise Hebrew chapter title (\\section{} level).\n"
            "  2. A target page count (2–5 pages; total 25–30 pages across all chapters).\n"
            "  3. A list of 3–5 key equations that MUST appear (give their names and "
            "     standard references, e.g. 'EKF predict step — Thrun 2005, p. 58').\n"
            "  4. A list of 3 primary sources to locate (author + topic hint).\n"
            "  5. A delegation brief for the SLAMAndFusionResearcher stating the required "
            "     mathematical depth (no 'general overviews').\n\n"
            "Then synthesise everything into a master paper structure and write it to "
            "outputs/paper_outline.md using the SafeFileWriterTool (if available) or "
            "include it verbatim in your final answer.\n\n"
            "The LaTeXAuthor will use this outline as their sole blueprint — "
            "every chapter must be traceable to a line in this document."
        ),
        expected_output=(
            "A Markdown file (outputs/paper_outline.md) containing:\n"
            "  • Paper title (Hebrew + English)\n"
            "  • 7 numbered chapters with: Hebrew title, page budget, "
            "    required equations (name + citation), primary sources, "
            "    delegation brief for researcher\n"
            "  • A global bibliography strategy (minimum 15 sources total)\n"
            "  • Confirmation line: 'OUTLINE COMPLETE — 7 chapters defined.'"
        ),
        agent=director,
    )


# ---------------------------------------------------------------------------
# Task 2 — SLAM Researcher: Deep Research
# ---------------------------------------------------------------------------

def create_task_research(researcher: Agent, context: list[Task]) -> Task:
    """
    Researcher produces structured research briefs for all 7 sub-domains
    defined by the director's outline.
    """
    logger.debug("Creating task_research")
    return Task(
        description=(
            "Read the master outline from outputs/paper_outline.md. "
            "For EACH of the 7 sub-domains, produce a structured research brief "
            "using the following schema:\n\n"
            "## [Hebrew Chapter Title]\n\n"
            "### 1. Summary (300–500 words)\n"
            "State-of-the-art as of 2024–2026. Dominant algorithms + failure modes.\n\n"
            "### 2. Key Algorithms\n"
            "Pseudocode skeleton or mathematical recurrence for each algorithm.\n\n"
            "### 3. Equations (LaTeX-ready)\n"
            "Every equation as a \\begin{equation}...\\label{eq:name}...\\end{equation} snippet. "
            "Verify against primary sources (Thrun 2005, Kalman 1960, Simmons 1979, etc.).\n\n"
            "### 4. Benchmark Results\n"
            "Numerical data: RMSE [cm], ATE [cm], RPE [cm/m], CPU [%], Power [W]. "
            "Each number must have author + year + table/figure reference.\n\n"
            "### 5. BibTeX Entries\n"
            "@article/@inproceedings/@book entries for every cited source. "
            "Every entry must have author, title, year, and venue.\n\n"
            "### 6. Hebrew Section Titles\n"
            "Proposed \\subsection{} titles for the LaTeXAuthor.\n\n"
            "Use SerperDevSearchTool, ArxivSearchTool, and WebScraperTool to find "
            "and verify sources. Do not invent equations or fabricate citations."
        ),
        expected_output=(
            "7 complete research briefs (one per chapter) in the schema above, "
            "delivered as a single structured Markdown document. "
            "Total: ≥ 21 BibTeX entries, ≥ 14 numbered equations, "
            "≥ 28 benchmark data points with citations. "
            "Confirmation line: 'RESEARCH COMPLETE — 7 briefs delivered.'"
        ),
        agent=researcher,
        context=context,
    )


# ---------------------------------------------------------------------------
# Task 3 — Visualization Engineer: All 9 Figures
# ---------------------------------------------------------------------------

def create_task_figures(visualizer: Agent, context: list[Task]) -> Task:
    """
    VisualizationEngineer generates all 9 required publication-quality figures
    and writes the figures manifest to outputs/figures_manifest.md.
    """
    logger.debug("Creating task_figures")
    return Task(
        description=(
            "Generate ALL 9 required publication-quality figures for the IEEE paper. "
            "For each figure, write and execute a complete Python script via "
            "PythonCodeExecutorTool, then confirm the PNG was saved to latex/figures/.\n\n"
            "Required figures (in order):\n"
            "  1. fig_bat_vs_artificial.png  — two-column flowchart (bat vs drone pipeline)\n"
            "  2. fig_trajectory_3d.png      — 3D helix trajectory (GT vs SLAM vs LiDAR cloud)\n"
            "  3. fig_sensor_fusion_heatmap.png — 10×10m occupancy + confidence overlay\n"
            "  4. fig_cochleagram.png         — LFM spectrogram (f0=20kHz, B=80kHz)\n"
            "  5. fig_range_doppler.png       — Range-Doppler map (3 synthetic targets)\n"
            "  6. fig_ekf_covariance.png      — EKF trajectory with 2σ ellipses\n"
            "  7. fig_framework_comparison.png — grouped bar chart (4 algorithms × 4 metrics)\n"
            "  8. fig_sensor_modalities.png   — block diagram (3 inputs → fusion → SLAM map)\n"
            "  9. fig_results_summary.png     — 3-panel (RMSE line, ATE bar, RPE boxplot)\n\n"
            "All figures: dpi=300, bbox_inches='tight', plt.close('all') after saving.\n"
            "After all 9 figures are confirmed, write outputs/figures_manifest.md "
            "listing: filename, title_en, caption_he, latex_label for each figure."
        ),
        expected_output=(
            "9 PNG files confirmed in latex/figures/ (each ≥ 10 KB at 300 DPI). "
            "outputs/figures_manifest.md listing all 9 figures with Hebrew captions "
            "and \\label{fig:...} keys. "
            "Confirmation line: 'FIGURES COMPLETE — 9/9 PNG files generated.'"
        ),
        agent=visualizer,
        context=context,
    )


# ---------------------------------------------------------------------------
# Task 4 — LaTeX Author: Write all chapters
# ---------------------------------------------------------------------------

def create_task_latex(author: Agent, context: list[Task]) -> Task:
    """
    LaTeXAuthor converts research briefs and figure manifests into
    compilable XeLaTeX chapter files.
    """
    logger.debug("Creating task_latex")
    return Task(
        description=(
            "Using the research briefs and figures manifest, write ALL LaTeX source files "
            "for the IEEE paper. Use SafeFileWriterTool for every write.\n\n"
            "Files to write (in order):\n"
            "  latex/chapters/cover.tex          — title page (Hebrew)\n"
            "  latex/chapters/abstract.tex        — Hebrew abstract (200–300 words)\n"
            "  latex/chapters/ch02_bio_basis.tex  — through ch09_conclusion.tex\n"
            "  latex/references.bib               — ≥ 15 BibTeX entries\n\n"
            "Per-chapter structural requirements (enforced):\n"
            "  • \\selectlanguage{hebrew} at top\n"
            "  • \\section{Hebrew Title}\\label{sec:...}\n"
            "  • ≥ 3 \\subsection{} environments\n"
            "  • ≥ 2 \\begin{equation}...\\label{eq:...}...\\end{equation} blocks\n"
            "  • ≥ 1 \\begin{figure}[H] with \\includegraphics + \\caption + \\label\n"
            "  • ≥ 1 \\begin{table}[H] in booktabs style\n"
            "  • ≥ 3 \\cite{} calls (all keys must exist in references.bib)\n\n"
            "FORBIDDEN: \\usepackage{inputenc}, $$ math, \\begin{center} in floats.\n"
            "REQUIRED compiler: xelatex (not pdflatex)."
        ),
        expected_output=(
            "11 files written to latex/: cover.tex, abstract.tex, ch02–ch09 (.tex), "
            "references.bib. Every chapter passes the structural contract above. "
            "references.bib has ≥ 15 entries, no missing author/title/year. "
            "Confirmation line: 'LATEX COMPLETE — 11 files written.'"
        ),
        agent=author,
        context=context,
    )


# ---------------------------------------------------------------------------
# Task 5 — Quality Editor: Review
# ---------------------------------------------------------------------------

def create_task_review(editor: Agent, context: list[Task]) -> Task:
    """
    QualityEditor audits the assembled paper across 9 axes and writes
    a structured quality report to outputs/quality_report.md.
    """
    logger.debug("Creating task_review")
    return Task(
        description=(
            "Conduct a rigorous technical editorial review of the assembled LaTeX paper. "
            "Use FileReaderTool to read every file in latex/chapters/ and latex/references.bib.\n\n"
            "Audit all 9 axes and grade each criterion [PASS], [WARN], or [FAIL]:\n\n"
            "  Axis 1 — Citation Integrity: all \\cite{} keys exist in references.bib.\n"
            "  Axis 2 — Cross-Reference Integrity: all \\ref{} labels have matching \\label{}.\n"
            "  Axis 3 — Mathematical Completeness: ≥ 8 equations; 7 required equations present.\n"
            "  Axis 4 — Figure Completeness: all 9 required figures in \\includegraphics{}.\n"
            "  Axis 5 — Structural Completeness: ch02–ch09 non-stub (≥ 200 words each).\n"
            "  Axis 6 — Table Completeness: ≥ 4 \\begin{table} environments.\n"
            "  Axis 7 — Language & Style: Hebrew primary language (> 50% prose).\n"
            "  Axis 8 — Compilation Safety: no forbidden anti-patterns (inputenc, $$ math, etc.).\n"
            "  Axis 9 — Page Count Estimate: 25–30 compiled pages.\n\n"
            "Write the structured report to outputs/quality_report.md."
        ),
        expected_output=(
            "outputs/quality_report.md containing:\n"
            "  • Summary table: PASS count, WARN count, FAIL count\n"
            "  • 'Submission-ready: YES / NO'\n"
            "  • Per-axis breakdown with [PASS/WARN/FAIL] + detail for each criterion\n"
            "  • Remediation Plan listing every FAIL with: file, issue, required action, "
            "    assigned agent\n"
            "  • If zero FAILs: 'APPROVED FOR SUBMISSION.'\n"
            "Confirmation line: 'REVIEW COMPLETE — quality_report.md written.'"
        ),
        agent=editor,
        context=context,
    )


# ---------------------------------------------------------------------------
# Convenience: build all 5 tasks in dependency order
# ---------------------------------------------------------------------------

def create_all_tasks(
    director: Agent,
    researcher: Agent,
    visualizer: Agent,
    author: Agent,
    editor: Agent,
) -> list[Task]:
    """
    Build and return all 5 tasks with correct context (dependency) wiring.

    Dependency graph:
        outline ──► research ──► latex ──► review
               ╰──► figures ──────────────╯
    """
    t_outline  = create_task_outline(director)
    t_research = create_task_research(researcher, context=[t_outline])
    t_figures  = create_task_figures(visualizer,  context=[t_outline])
    t_latex    = create_task_latex(author,         context=[t_research, t_figures])
    t_review   = create_task_review(editor,        context=[t_latex])

    logger.debug("All 5 tasks created with dependency wiring.")
    return [t_outline, t_research, t_figures, t_latex, t_review]
