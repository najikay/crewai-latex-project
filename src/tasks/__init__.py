"""
src/tasks/__init__.py
======================
Public API for NavigatorCrew task definitions.
"""

from src.tasks.research_tasks import (
    create_task_outline,
    create_task_research,
    create_task_figures,
    create_task_latex,
    create_task_review,
    create_all_tasks,
)

__all__ = [
    "create_task_outline",
    "create_task_research",
    "create_task_figures",
    "create_task_latex",
    "create_task_review",
    "create_all_tasks",
]
