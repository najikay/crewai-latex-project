"""
src/agents/__init__.py
=======================
Public API for the NavigatorCrew agent team.
"""

from src.agents.navigation_director import create_navigation_director
from src.agents.slam_researcher import create_slam_researcher
from src.agents.visualization_engineer import create_visualization_engineer
from src.agents.latex_author import create_latex_author
from src.agents.quality_editor import create_quality_editor

__all__ = [
    "create_navigation_director",
    "create_slam_researcher",
    "create_visualization_engineer",
    "create_latex_author",
    "create_quality_editor",
]
