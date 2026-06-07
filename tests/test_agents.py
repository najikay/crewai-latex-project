import pytest
from src.agents import (
    create_navigation_director,
    create_slam_researcher,
    create_visualization_engineer,
    create_latex_author,
    create_quality_editor
)
from src.utils.token_accountant import TokenAccountant

def test_navigation_director_creation():
    agent = create_navigation_director()
    assert "Senior Research Fellow" in agent.role
    assert agent.allow_delegation is True
    assert agent.verbose is True

def test_slam_researcher_creation():
    agent = create_slam_researcher()
    assert "SLAM" in agent.role
    assert agent.allow_delegation is False

def test_visualization_engineer_creation():
    agent = create_visualization_engineer()
    assert "Visualization" in agent.role
    # In CrewAI, memory=False might result in None or a disabled object
    assert not agent.memory

def test_latex_author_creation():
    agent = create_latex_author()
    assert "LaTeX" in agent.role
    # In CrewAI, memory=True results in a Memory object
    assert agent.memory is not None

def test_quality_editor_creation():
    agent = create_quality_editor()
    assert "Peer Reviewer" in agent.role

def test_token_accountant_integration():
    acc = TokenAccountant()
    acc.record(100, 50)
    report = acc.report()
    assert report["total"]["total_tokens"] == 150
    assert report["total"]["call_count"] == 1

def test_token_accountant_reset():
    acc = TokenAccountant()
    acc.record(100, 50)
    acc.reset()
    assert acc.total.total_tokens == 0

def test_agent_max_iter_from_config():
    from src.config import AGENT_MAX_ITER
    director = create_navigation_director()
    assert director.max_iter == AGENT_MAX_ITER["research_director"]
    
    researcher = create_slam_researcher()
    assert researcher.max_iter == AGENT_MAX_ITER["deep_researcher"]
