"""
src/crew.py
===========
Wiring agents, tools, and tasks into a CrewAI Crew.
"""

from crewai import Crew, Process
from src.config import validate_config, LLM_IDENTIFIER
from src.agents import (
    create_navigation_director,
    create_slam_researcher,
    create_visualization_engineer,
    create_latex_author,
    create_quality_editor
)
from src.tasks.research_tasks import (
    create_outline_task,
    create_research_task,
    create_visualization_task,
    create_latex_task,
    create_review_task
)
from src.tools import (
    PythonCodeExecutorTool,
    SerperDevSearchTool,
    ArxivSearchTool,
    SafeFileWriterTool,
    FileReaderTool,
    WebScraperTool
)
from src.utils.token_accountant import TokenAccountant

def build_crew():
    validate_config()
    
    accountant = TokenAccountant()
    accountant.install()
    
    # 1. Tools
    writer = SafeFileWriterTool()
    reader = FileReaderTool()
    search = SerperDevSearchTool()
    arxiv = ArxivSearchTool()
    scraper = WebScraperTool()
    executor = PythonCodeExecutorTool()
    
    # 2. Agents
    director = create_navigation_director(tools=[writer])
    researcher = create_slam_researcher(tools=[search, arxiv, scraper])
    visualizer = create_visualization_engineer(tools=[executor, writer])
    author = create_latex_author(tools=[writer, reader])
    editor = create_quality_editor(tools=[reader])
    
    # 3. Tasks
    task1 = create_outline_task(director)
    task_research = create_research_task(researcher, [task1])
    task_viz = create_visualization_task(visualizer, [task_research])
    task_latex = create_latex_task(author, [task_research, task_viz])
    task_review = create_review_task(editor, [task_latex])
    
    crew = Crew(
        agents=[director, researcher, visualizer, author, editor],
        tasks=[task1, task_research, task_viz, task_latex, task_review],
        process=Process.hierarchical,
        manager_agent=director,
        step_callback=accountant.step_callback,
        task_callback=accountant.task_callback,
        verbose=True
    )
    
    return crew, accountant
