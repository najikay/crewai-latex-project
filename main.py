"""
main.py
=======
CLI Entry point for NavigatorCrew.
Architecture: LangGraph + CrewAI Sequential Pipeline v5.0.
"""

import argparse
import os
import shutil
import subprocess
from pathlib import Path
from src.config import logger, PROJECT_ROOT


def compile_pdf() -> Path | None:
    """
    Run the full XeLaTeX → BibTeX → XeLaTeX → XeLaTeX sequence.
    Returns path to the compiled PDF, or None on failure.
    Copies the result to outputs/NavigatorCrew_paper.pdf.
    """
    latex_dir = PROJECT_ROOT / "latex"
    pdf_src   = latex_dir / "main.pdf"
    pdf_dst   = PROJECT_ROOT / "outputs" / "NavigatorCrew_paper.pdf"

    def run(cmd: list[str]) -> bool:
        result = subprocess.run(
            cmd, cwd=latex_dir,
            capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.warning(f"[LaTeX] {cmd[0]} returned non-zero: {result.stdout[-500:]}")
        return result.returncode == 0

    logger.info("[LaTeX] Compiling PDF (xelatex → bibtex → xelatex × 2)...")
    run(["xelatex", "-interaction=nonstopmode", "main.tex"])
    run(["bibtex", "main"])
    run(["xelatex", "-interaction=nonstopmode", "main.tex"])
    run(["xelatex", "-interaction=nonstopmode", "main.tex"])

    if pdf_src.exists():
        shutil.copy2(pdf_src, pdf_dst)
        size_mb = pdf_src.stat().st_size / 1_048_576
        logger.success(f"[LaTeX] PDF compiled: {pdf_dst} ({size_mb:.1f} MB)")
        return pdf_dst
    else:
        logger.error("[LaTeX] PDF compilation failed — check latex/main.log")
        return None


def main():
    _DEFAULT_TOPIC = "Bat-Inspired Drone Navigation via Bio-Mimetic Multi-Modal Sensor Fusion"

    parser = argparse.ArgumentParser(description="NavigatorCrew v5.0")
    parser.add_argument(
        "--topic",
        default=_DEFAULT_TOPIC,
        help=f'Research topic (default: "{_DEFAULT_TOPIC}")',
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last checkpoint (skips tasks with existing output files)",
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF compilation after content generation",
    )
    args = parser.parse_args()

    logger.info(f"Topic: {args.topic}")
    logger.info(f"Resume Mode: {args.resume}")

    from src.graph.navigator_graph import build_navigator_graph
    from src.graph.state import PipelineState

    logger.info("Building NavigatorCrew LangGraph pipeline...")
    graph = build_navigator_graph()

    initial_state: PipelineState = {
        "topic": args.topic,
        "remediation_count": 0,
        "failed_sections": [],
        "quality_verdict": "PENDING",
        "quality_score": 0,
    }

    try:
        final_state = graph.invoke(initial_state)
    except Exception as e:
        logger.error(f"Graph execution failed: {e}")
        raise

    # ------------------------------------------------------------------
    # PDF Compilation
    # ------------------------------------------------------------------
    pdf_path = None
    if not args.no_pdf:
        pdf_path = compile_pdf()

    print("\n" + "=" * 52)
    print("  NAVIGATORCREW — EXECUTION COMPLETE")
    print("=" * 52)
    print(f"  Quality Score    : {final_state['quality_score']}/100")
    print(f"  Verdict          : {final_state['quality_verdict']}")
    print(f"  Remediation Runs : {final_state['remediation_count']}")
    if pdf_path:
        print(f"  Final PDF        : {pdf_path}")
    print("=" * 52)


if __name__ == "__main__":
    main()
