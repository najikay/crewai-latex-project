"""
src/crew.py
============
NavigatorCrew assembly — wires agents, tools, tasks, and the TokenAccountant
into a single, runnable CrewAI Crew.

Public API:
    build_crew() -> tuple[Crew, TokenAccountant]

Usage:
    crew, accountant = build_crew()
    result = crew.kickoff()
    accountant.finalize(getattr(crew, "usage_metrics", None))
    accountant.save_report("outputs/token_report.md")
    accountant.uninstall()
"""

from __future__ import annotations

from crewai import Crew, Process

from src.agents import (
    create_navigation_director,
    create_slam_researcher,
    create_visualization_engineer,
    create_latex_author,
    create_quality_editor,
)
from src.config import get_embedder_config, logger, validate_config
from src.tasks import create_all_tasks
from src.tools import (
    ArxivSearchTool,
    FileReaderTool,
    PythonCodeExecutorTool,
    SafeFileWriterTool,
    SerperDevSearchTool,
    WebScraperTool,
)
from src.utils.token_accountant import TokenAccountant


def build_crew() -> tuple[Crew, TokenAccountant]:
    """
    Validate configuration, instantiate all tools and agents, assemble the
    Crew with a hierarchical process, and attach the TokenAccountant.

    Returns:
        crew        — ready-to-kickoff CrewAI Crew
        accountant  — TokenAccountant with LiteLLM callback already installed
    """
    # ------------------------------------------------------------------
    # 0. Validate API keys before spending tokens
    # ------------------------------------------------------------------
    validate_config()

    # ------------------------------------------------------------------
    # 1. Instantiate tools
    # ------------------------------------------------------------------
    serper   = SerperDevSearchTool()
    arxiv    = ArxivSearchTool()
    scraper  = WebScraperTool()
    executor = PythonCodeExecutorTool()
    writer   = SafeFileWriterTool()
    reader   = FileReaderTool()

    logger.info("NavigatorCrew: all 6 tools instantiated.")

    # ------------------------------------------------------------------
    # 2. Instantiate agents with their tool sets
    # ------------------------------------------------------------------
    director    = create_navigation_director(tools=[writer])           # writes paper_outline.md
    researcher  = create_slam_researcher(tools=[serper, arxiv, scraper])
    visualizer  = create_visualization_engineer(tools=[executor, writer])
    author      = create_latex_author(tools=[writer, reader])
    editor      = create_quality_editor(tools=[reader])

    logger.info("NavigatorCrew: 5 agents instantiated.")

    # ------------------------------------------------------------------
    # 3. Build tasks with dependency wiring
    # ------------------------------------------------------------------
    tasks = create_all_tasks(
        director=director,
        researcher=researcher,
        visualizer=visualizer,
        author=author,
        editor=editor,
    )

    logger.info("NavigatorCrew: 5 tasks created.")

    # ------------------------------------------------------------------
    # 4. Token accounting
    # ------------------------------------------------------------------
    accountant = TokenAccountant()
    accountant.install()

    # ------------------------------------------------------------------
    # 5. Assemble crew
    # ------------------------------------------------------------------
    crew = Crew(
        # Worker agents only — director is the hierarchical manager
        agents=[researcher, visualizer, author, editor],
        tasks=tasks,
        process=Process.hierarchical,
        manager_agent=director,
        verbose=True,
        memory=True,
        embedder=get_embedder_config(),
        step_callback=accountant.step_callback,
        task_callback=accountant.task_callback,
    )

    logger.info(
        "NavigatorCrew assembled: "
        f"process=hierarchical | agents=5 | tasks={len(tasks)} | memory=True"
    )
    return crew, accountant
