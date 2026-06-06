# Product Requirements Document (PRD)
## Assignment 3: Personal AI Agent — "Research Paper Architect"
**Version**: 1.0 | **Date**: 2026-06-06 | **Deadline**: 2026-06-20

---

## 1. Executive Summary

We are building **ResearchCrew** — a multi-agent AI system built with **CrewAI** that acts as a fully autonomous academic research and LaTeX paper generation assistant. The system accepts a research topic, orchestrates a team of specialized AI agents to gather information, synthesize knowledge, generate visuals, and produce a complete IEEE-formatted LaTeX paper in Hebrew.

This topic was chosen because:
- It is **meta**: the agent itself demonstrates the concepts it writes about (AI agent orchestration)
- It is deep enough to sustain **25–30 pages** of substantive technical content
- It requires multiple tool types (search, code execution, file I/O), satisfying the ≥2 tools requirement
- It aligns perfectly with the course material, making prompt engineering highly targeted

---

## 2. Architecture Decision: CrewAI (Role-Based Multi-Agent)

### Why CrewAI over LangGraph
| Criterion | CrewAI | LangGraph |
|---|---|---|
| Team structure | Native role/task decomposition | Manual graph nodes |
| Alignment with course Ex03 | Direct match | Indirect |
| Memory built-in | Yes (short + long-term) | Requires custom state |
| Paper generation workflow | Sequential/Hierarchical fits perfectly | Overkill for linear doc pipeline |
| Learning curve | Lower | Higher |

**Decision**: **CrewAI** with `Process.sequential` for the paper pipeline and `Process.hierarchical` for the research phase (Manager agent delegates to sub-agents).

---

## 3. Agent Persona & Topic

### Product Name: `ResearchCrew`
### Persona: Academic Research & LaTeX Authoring System
### Research Topic (paper subject): 
**"ארכיטקטורת סוכני בינה מלאכותית ואורקסטרציה של מערכות מרובות-סוכנים בשנת 2026"**
*(AI Agent Architecture and Multi-Agent System Orchestration in 2026)*

This covers: Agent runtimes, CrewAI, LangGraph, MCP, A2A, security (OWASP), deployment models (local vs. cloud), and observability — all course material.

---

## 4. Agent Team Design

### Agent 1: `ResearchDirector` (Manager)
- **Role**: Senior Research Director
- **Goal**: Decompose the research topic into sub-topics, delegate to specialists, and ensure completeness
- **Backstory**: A veteran academic researcher who has led AI survey papers for IEEE journals for 15 years
- **Process**: Hierarchical manager — orchestrates Agent 2 and Agent 3
- **LLM**: `claude-sonnet-4-6` (via Anthropic API)

### Agent 2: `DeepResearcher`
- **Role**: Technical Research Specialist
- **Goal**: Find, read, and summarize authoritative sources on each sub-topic
- **Backstory**: A PhD-level AI systems researcher specializing in multi-agent frameworks
- **Tools**: `SerperSearchTool`, `ArxivSearchTool`, `WebScraperTool`
- **LLM**: `claude-sonnet-4-6`

### Agent 3: `DataVisualizer`
- **Role**: Scientific Data Visualization Engineer
- **Goal**: Generate Python code for charts, tables, and architecture diagrams
- **Backstory**: A data scientist who specializes in academic-quality figures using matplotlib
- **Tools**: `PythonCodeExecutorTool`, `FileWriterTool`
- **LLM**: `claude-sonnet-4-6`

### Agent 4: `LaTeXAuthor`
- **Role**: IEEE LaTeX Technical Writer (Hebrew)
- **Goal**: Transform research summaries and visuals into a complete, compilable LaTeX document in Hebrew
- **Backstory**: A bilingual academic writer fluent in Hebrew and English with IEEE publication experience
- **Tools**: `FileWriterTool`, `FileReaderTool`, `LaTeXValidatorTool`
- **LLM**: `claude-sonnet-4-6`

### Agent 5: `QualityEditor`
- **Role**: Senior Academic Editor
- **Goal**: Review the final paper for completeness, citation accuracy, formatting compliance, and page count
- **Backstory**: An IEEE journal editor who has reviewed hundreds of papers on AI systems
- **Tools**: `FileReaderTool`, `PDFPageCountTool`
- **LLM**: `claude-sonnet-4-6`

---

## 5. Toolbox (Minimum 2 External Tools)

| # | Tool Name | Type | Purpose | Library |
|---|---|---|---|---|
| 1 | `SerperSearchTool` | External API | Web search for research | `crewai_tools` + Serper API |
| 2 | `ArxivSearchTool` | External API | Academic paper lookup | `arxiv` Python lib |
| 3 | `PythonCodeExecutorTool` | Code Execution | Run matplotlib/plotly code to generate PNG graphs | Custom tool using `subprocess` |
| 4 | `FileWriterTool` | File I/O | Write `.tex`, `.bib`, `.py` files | `crewai_tools` |
| 5 | `FileReaderTool` | File I/O | Read research notes and LaTeX sections | `crewai_tools` |
| 6 | `WebScraperTool` | Web | Scrape specific URLs for content | `crewai_tools` |

**Note**: Tools 1 and 3 are the two "external" tools that satisfy the assignment minimum. All others are supporting utilities.

---

## 6. Memory Strategy

CrewAI's built-in memory stack will be fully enabled:

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,           # Enables short-term + long-term + entity memory
    embedder={
        "provider": "openai",   # or "huggingface" for local
        "config": {"model": "text-embedding-3-small"}
    },
    verbose=True
)
```

| Memory Type | Purpose |
|---|---|
| **Short-Term Memory** | Pass research summaries between tasks in the same run |
| **Long-Term Memory** (ChromaDB) | Persist research findings across multiple crew runs |
| **Entity Memory** | Track key entities: frameworks, authors, concepts |

This means: if the crew is re-run, it will remember what it already researched and skip redundant searches.

---

## 7. User Interface: Streamlit Web App

**File**: `app.py`

### UI Components:
1. **Topic Input** — text field for the research subject
2. **Configuration Panel** — select agents to enable, choose LLM, set paper length target
3. **Progress Tracker** — real-time display of which agent/task is running (via CrewAI callbacks)
4. **Output Preview** — syntax-highlighted LaTeX source display
5. **Download Buttons** — download `.tex`, `.bib`, generated `.pdf`, and graph `.png` files
6. **Log Console** — scrollable agent thought/action log

### CLI Alternative:
A `main.py` CLI script that accepts `--topic`, `--output-dir`, and `--model` flags, for terminal-based usage.

---

## 8. Paper Structure (25–30 pages, IEEE, Hebrew)

| Chapter | Title (Hebrew) | Pages |
|---|---|---|
| Cover | דף שער — פרטי הגשה, שמות, תאריך | 1 |
| Abstract | תקציר + Abstract (EN) | 1 |
| 1 | מבוא — רקע ומוטיבציה | 2–3 |
| 2 | ארכיטקטורת סוכן AI — Runtime, Planner, Memory, Tools | 4–5 |
| 3 | מסגרות עבודה — CrewAI, LangGraph, AutoGen השוואה | 4–5 |
| 4 | פרוטוקולי תקשורת — MCP ו-A2A | 3–4 |
| 5 | אבטחה — OWASP Top 10 לסוכני AI | 3–4 |
| 6 | מודלי פריסה — Local vs. Cloud, Observability | 3–4 |
| 7 | המערכת שפיתחנו — ResearchCrew Architecture | 3–4 |
| 8 | תוצאות וניתוח | 2–3 |
| 9 | סיכום ועתיד | 1–2 |
| Refs | ביבליוגרפיה (BibTeX) | 1–2 |

**Total**: 28–34 pages target (trim to 30 in editing phase)

---

## 9. Security & Configuration

```
.env file:
  ANTHROPIC_API_KEY=...
  SERPER_API_KEY=...
  OPENAI_API_KEY=...   (for embeddings only)
```

- All keys loaded via `python-dotenv`
- `.env` added to `.gitignore`
- No credentials in any source file
- API key validation at startup with clear error messages

---

## 10. Repository Structure

```
assignment3/
├── .env                    # API keys (gitignored)
├── .env.example            # Template for keys
├── .gitignore
├── requirements.txt
├── README.md
├── app.py                  # Streamlit web interface
├── main.py                 # CLI entry point
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research_director.py
│   │   ├── deep_researcher.py
│   │   ├── data_visualizer.py
│   │   ├── latex_author.py
│   │   └── quality_editor.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── research_tasks.py
│   │   ├── visualization_tasks.py
│   │   └── writing_tasks.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_tools.py
│   │   ├── code_executor.py
│   │   ├── file_tools.py
│   │   └── arxiv_tool.py
│   ├── crew.py             # Crew assembly
│   └── config.py           # Settings, model names, paths
├── latex/
│   ├── main.tex            # Master LaTeX file
│   ├── chapters/
│   │   ├── ch01_intro.tex
│   │   ├── ch02_architecture.tex
│   │   ├── ch03_frameworks.tex
│   │   ├── ch04_protocols.tex
│   │   ├── ch05_security.tex
│   │   ├── ch06_deployment.tex
│   │   ├── ch07_our_system.tex
│   │   ├── ch08_results.tex
│   │   └── ch09_conclusion.tex
│   ├── figures/            # PNG graphs and screenshots
│   ├── references.bib      # BibTeX file
│   └── ieee_hebrew.sty     # Custom style adjustments
├── outputs/                # Generated files (gitignored for large PDFs)
├── tests/
│   ├── test_tools.py
│   ├── test_agents.py
│   └── test_crew.py
└── docs/
    └── course_summary.md   # 20-page course summary
```

---

## 11. Success Metrics

| Metric | Target |
|---|---|
| Paper page count | 25–30 pages |
| LaTeX compilation | Zero errors, clean PDF |
| Tools used | ≥ 2 external (Serper + ArXiv) |
| Memory active | ChromaDB persistence confirmed |
| Demo video | ≤ 3 minutes, shows full pipeline |
| GitHub repo | All code committed, README complete |
| Course summary | ≥ 20 pages separate document |
