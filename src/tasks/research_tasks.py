"""
src/tasks/research_tasks.py
============================
Factory functions for the 5 NavigatorCrew tasks.
Architecture: Robust Sequential Pipeline v4.0.
"""

from __future__ import annotations
from crewai import Agent, Task
from src.config import logger

def create_task_outline(director: Agent, topic: str) -> Task:
    return Task(
        description=f"Decompose the topic '{topic}' into 7 sub-domains and create outputs/paper_outline.md.",
        expected_output="Detailed paper outline in Markdown format. Confirmation: 'OUTLINE COMPLETE'.",
        agent=director,
        output_file="outputs/paper_outline.md"
    )

def create_task_research(researcher: Agent, context: list[Task]) -> Task:
    return Task(
        description="Produce 7 technical research briefs (summary, algorithms, equations, bibtex) based on outputs/paper_outline.md.",
        expected_output="Structured research briefs in outputs/research_briefs.md. Confirmation: 'RESEARCH COMPLETE'.",
        agent=researcher,
        context=context,
        output_file="outputs/research_briefs.md"
    )

def create_task_figures(visualizer: Agent, context: list[Task]) -> Task:
    return Task(
        description="Generate 9 IEEE-standard figures and save to latex/figures/. Write manifest to outputs/figures_manifest.md.",
        expected_output="9 PNG files and a manifest in outputs/figures_manifest.md.",
        agent=visualizer,
        context=context,
        output_file="outputs/figures_manifest.md"
    )

def create_task_latex(author: Agent, context: list[Task]) -> Task:
    return Task(
        description="Write 11 LaTeX files (chapters + bib) based on briefs and figures. Ensure XeLaTeX compatibility.",
        expected_output="All .tex and .bib files in latex/ folder.",
        agent=author,
        context=context,
        output_file="latex/references.bib" # Using references.bib as the completion sentinel
    )

def create_task_review(editor: Agent, context: list[Task]) -> Task:
    return Task(
        description="""
Conduct a peer review of all LaTeX files and output a report to outputs/quality_report.md.

**MANDATORY**: Your report MUST end with a machine-readable JSON verdict block:

```json
{
  "verdict": "PASS" or "FAIL",
  "score": <integer 0-100>,
  "failed_sections": ["section_name", ...]
}
```

Score below 75 = FAIL. Failed sections must use these exact names if applicable:
methodology, algorithms, related_work, equations, introduction, conclusion, references, figures.
""",
        expected_output="Quality report in outputs/quality_report.md ending with a JSON verdict block.",
        agent=editor,
        context=context,
        output_file="outputs/quality_report.md"
    )

def create_remediation_task(
    agent: Agent,
    failed_sections: list[str],
    quality_report_path: str,
    output_file: str,
) -> Task:
    """
    Targeted fix task. The agent reads the quality report and the existing
    output files, then patches ONLY the sections listed in failed_sections.
    """
    sections_str = ", ".join(failed_sections)
    return Task(
        description=f"""
REMEDIATION TASK. You are fixing specific quality failures identified by the QualityEditor.

1. Read the quality report at {quality_report_path} to understand each specific issue.
2. Read the existing output files to understand what currently exists.
3. Fix ONLY the following failed sections: [{sections_str}]
4. Do NOT modify sections that passed — this minimises unnecessary rewrites.
5. Overwrite only the files that contain the failing sections.
6. Produce the same output files as the original task, but with issues resolved.
""",
        expected_output=f"Fixed output file(s) addressing failures in: {sections_str}. Confirmation: 'REMEDIATION COMPLETE'.",
        agent=agent,
        output_file=output_file,
    )

def create_all_tasks(director, researcher, visualizer, author, editor, topic) -> list[Task]:
    t_outline  = create_task_outline(director, topic)
    t_research = create_task_research(researcher, [t_outline])
    t_figures  = create_task_figures(visualizer, [t_research])
    t_latex    = create_task_latex(author, [t_research, t_figures])
    t_review   = create_task_review(editor, [t_latex])
    return [t_outline, t_research, t_figures, t_latex, t_review]
