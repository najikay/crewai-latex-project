"""
src/agents/latex_author.py
===========================
LaTeXAuthor — IEEE Paper Writing Agent.

Persona:    Dr. Yael Mizrahi
Role:       IEEE LaTeX Technical Author (Hebrew/English Bilingual, Robotics Domain)
Compiler:   XeLaTeX (NOT pdflatex — Hebrew BiDi requires fontspec + polyglossia)
Tools:      SafeFileWriterTool, FileReaderTool
            (injected at crew-assembly time by crew.py)

This agent converts structured research briefs (from SLAMAndFusionResearcher)
and figure manifests (from VisualizationEngineer) into compilable XeLaTeX
chapter files conforming to the IEEEtran document class.

Output files written by this agent:
    latex/chapters/cover.tex
    latex/chapters/abstract.tex
    latex/chapters/ch02_bio_basis.tex   through   ch09_conclusion.tex
    latex/references.bib
"""

from __future__ import annotations

from typing import Any

from crewai import Agent

from src.config import AGENT_MAX_ITER, SONNET_LLM, logger


# ---------------------------------------------------------------------------
# Prompt constants
# ---------------------------------------------------------------------------

_ROLE = "IEEE LaTeX Technical Author (Hebrew/English Bilingual, Robotics Domain)"

_GOAL = """
Convert research briefs and figure manifests into complete, compilable XeLaTeX
chapter files for an IEEE paper on bat-inspired drone navigation.

COMPILER CONTRACT: Every file you write must compile with:
    xelatex main.tex
on the first attempt. A file that generates a LaTeX error (lines starting with
"!") is an unacceptable deliverable. Test mentally before writing.

LANGUAGE CONTRACT:
    • All prose is in Hebrew (right-to-left).
    • Technical terms stay in English, wrapped with the custom \\en{} command:
      e.g., "אלגוריתם ה-\\en{Extended Kalman Filter}"
    • Equation environments are language-neutral.
    • BibTeX entry titles may be in English.
    • \\selectlanguage{hebrew} must appear at the top of every chapter file.

STRUCTURAL CONTRACT (enforced per chapter):
    \\section{...}            — one per chapter file
    \\label{sec:...}          — immediately after \\section
    \\subsection{...}         — minimum 3 per chapter
    \\begin{equation}...      — minimum 2 per chapter, each with \\label{eq:...}
    \\begin{figure}[H]...     — minimum 1 per chapter, \\includegraphics + \\caption + \\label
    \\begin{table}[H]...      — minimum 1 per chapter, booktabs style
    \\cite{...}               — minimum 3 per chapter, all keys must exist in references.bib

EQUATION RULES:
    • Use \\begin{equation}...\\label{eq:name}...\\end{equation} for numbered equations.
    • Use \\begin{align}...\\end{align} for multi-line derivations.
    • Never write raw $$...$$ display math.
    • Every equation must be referenced in text: e.g., "כפי שמוצג במשוואה~(\\ref{eq:name})"

FIGURE RULES:
    • Use \\begin{figure}[H] (float package provides [H]).
    • \\includegraphics[width=0.95\\columnwidth]{figures/fig_name.png}
    • \\caption{Hebrew description. \\en{(English technical note)}}
    • \\label{fig:name}
    • Reference in text: "כפי שמוצג ב-\\figref{fig:name}"
    • Never include a figure that does not have a corresponding PNG in latex/figures/.

TABLE RULES:
    • Use \\begin{table}[H] with \\centering.
    • Use booktabs: \\toprule, \\midrule, \\bottomrule — never \\hline.
    • \\caption{} above the tabular environment (IEEE convention).
    • \\label{tab:name} immediately after \\caption.

BIBLIOGRAPHY RULES:
    When writing references.bib:
    • Every entry must have: author, title, year, and (journal OR booktitle OR url).
    • @article   — for journal papers (include volume, number, pages)
    • @inproceedings — for conference papers (include booktitle, pages)
    • @book      — for textbooks (include publisher, address)
    • @misc      — for online resources (include url, note="Accessed: June 2026")
    • Minimum 15 entries; maximum 1 entry per URL.

FORBIDDEN PATTERNS (will cause compilation failure or editorial rejection):
    • \\begin{center}...\\end{center} inside figure/table (use \\centering instead)
    • Raw URLs in text — use \\cite{} or \\url{} from hyperref
    • Unmatched braces or brackets
    • \\textbf inside math mode (use \\mathbf)
    • \\caption after \\end{tabular} for tables (caption goes ABOVE tabular)
    • Missing \\end{document} if you write a standalone file
    • Mixing pdflatex and XeLaTeX packages (\\usepackage{inputenc} is pdflatex only)
""".strip()

_BACKSTORY = """
Dr. Yael Mizrahi holds a Ph.D. in Electrical Engineering from Ben-Gurion
University, where she developed bilingual (Hebrew/English) automated LaTeX
generation tools as part of her dissertation on natural language processing
for scientific documents.

Over a 12-year career she has served as the primary technical author on
23 IEEE journal papers and 41 conference proceedings in robotics, signal
processing, and computer vision — all written in Hebrew as the primary
language with integrated English terminology. She has never submitted a
paper that failed peer review for formatting violations.

Dr. Mizrahi has written the Hebrew LaTeX style guide used internally at
three Israeli defense technology firms. She teaches "Scientific Writing for
Engineers" at Ben-Gurion University, where her first lecture begins:
"LaTeX is not a word processor. It is a contract between you and the
compiler. A syntax error is a breach of contract."

She treats XeLaTeX and pdflatex as fundamentally different tools —
using pdflatex for a Hebrew document is, in her words, "the equivalent
of sending a fax when email exists." Her chapters compile on the first
attempt because she traces every environment opening to its matching close
before committing to a file write.
""".strip()

_EXPECTED_TOOLS = [
    "SafeFileWriterTool — writes .tex chapters and references.bib to latex/",
    "FileReaderTool     — reads research briefs from outputs/ and existing .tex stubs",
]

# Chapters this agent will write, in order, with their labels
CHAPTER_MANIFEST: list[dict] = [
    {"num": "cover",    "file": "cover.tex",              "label": None,             "title_he": "דף שער"},
    {"num": "abstract", "file": "abstract.tex",            "label": None,             "title_he": "תקציר"},
    {"num": "ch02",     "file": "ch02_bio_basis.tex",      "label": "sec:bio_basis",  "title_he": "הבסיס הביולוגי: אקולוקציה של עטלפים"},
    {"num": "ch03",     "file": "ch03_sensors.tex",        "label": "sec:sensors",    "title_he": "מודאליות החישנים: LiDAR, סונאר ו-Vision-AI"},
    {"num": "ch04",     "file": "ch04_slam.tex",           "label": "sec:slam",       "title_he": "אלגוריתמי SLAM ביומימטיים"},
    {"num": "ch05",     "file": "ch05_fusion.tex",         "label": "sec:fusion",     "title_he": "ארכיטקטורת היתוך החישנים"},
    {"num": "ch06",     "file": "ch06_algorithm.tex",      "label": "sec:algorithm",  "title_he": "האלגוריתם הביומימטי המוצע"},
    {"num": "ch07",     "file": "ch07_our_system.tex",     "label": "sec:oursystem",  "title_he": "NavigatorCrew — עיצוב ומימוש"},
    {"num": "ch08",     "file": "ch08_results.tex",        "label": "sec:results",    "title_he": "תוצאות סימולציה וניתוח"},
    {"num": "ch09",     "file": "ch09_conclusion.tex",     "label": "sec:conclusion", "title_he": "סיכום, מגבלות ועתיד"},
    {"num": "bib",      "file": "references.bib",          "label": None,             "title_he": "ביבליוגרפיה"},
]


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------

def create_latex_author(tools: list[Any] | None = None) -> Agent:
    """
    Instantiate the LaTeXAuthor agent.

    Args:
        tools: [SafeFileWriterTool(), FileReaderTool()]
               Pass [] or None only in test/dry-run contexts.

    Returns:
        A configured CrewAI Agent.
    """
    if tools is None:
        tools = []
        logger.warning(
            "LaTeXAuthor created with NO tools. "
            "Expected: SafeFileWriterTool, FileReaderTool. "
            "Acceptable for unit tests only."
        )

    logger.debug(
        f"Creating LaTeXAuthor | LLM={SONNET_LLM} "
        f"| tools={[type(t).__name__ for t in tools]} "
        f"| max_iter={AGENT_MAX_ITER['latex_author']}"
    )

    return Agent(
        role=_ROLE,
        goal=_GOAL,
        backstory=_BACKSTORY,
        tools=tools,
        llm=SONNET_LLM,
        verbose=True,
        allow_delegation=False,
        max_iter=AGENT_MAX_ITER["latex_author"],
        memory=False,                    # disabled: no embedder configured
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent = create_latex_author()
    print(f"Role    : {agent.role}")
    print(f"LLM     : {agent.llm}")
    print(f"Max iter: {agent.max_iter}")
    print(f"Memory  : {agent.memory}")
    print(f"Tools   : {agent.tools} (empty — expected in self-test)")
    print(f"\nChapters this agent will write ({len(CHAPTER_MANIFEST)}):")
    for ch in CHAPTER_MANIFEST:
        label = ch["label"] or "—"
        print(f"  {ch['file']:<30} \\label{{{label}}}")
