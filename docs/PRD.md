# Product Requirements Document (PRD)
## Assignment 3: Personal AI Agent — "ResearchCrew"
**Version**: 2.0 | **Date**: 2026-06-06 | **Deadline**: 2026-06-20
**Classification**: Academic Submission — Ultra-Granular Specification

---

## 1. Executive Summary

**ResearchCrew** is a multi-agent AI system built on **CrewAI** that functions as a fully autonomous academic research and LaTeX paper generation pipeline. Given a research topic, it orchestrates a team of specialized AI agents to: gather authoritative sources, synthesize knowledge into structured chapters, produce Python-generated scientific visuals, and emit a complete IEEE-formatted Hebrew LaTeX paper ready for MikTeX compilation.

### Why This Topic?
The paper subject is: **"ארכיטקטורת סוכני בינה מלאכותית ואורקסטרציה של מערכות מרובות-סוכנים בשנת 2026"**
*(AI Agent Architecture and Multi-Agent System Orchestration in 2026)*

This is the optimal choice because:
1. **Meta-demonstration**: The agent that builds the paper *is* the subject of the paper — an executable proof-of-concept.
2. **Depth**: Covers agent runtimes, CrewAI, LangGraph, MCP, A2A, security (OWASP), observability — all course material from Lectures L01–L06.
3. **Tool richness**: Naturally requires search (Serper), academic lookup (ArXiv), code execution (matplotlib), and file I/O — satisfying all ≥2 tools requirements with room for bonus tools.
4. **Documentation density**: 7 substantive technical chapters easily reach 25–30 pages in IEEE format.

---

## 2. Architecture Decision Record (ADR)

### Decision: CrewAI over LangGraph

| Evaluation Axis | CrewAI | LangGraph | Winner |
|---|---|---|---|
| Course alignment | Directly used in Ex03 | Mentioned as alternative | CrewAI |
| Role/team metaphor | Native (Agent → Task → Crew) | Graph nodes (manual) | CrewAI |
| Memory integration | Built-in (short/long/entity) | Requires custom state schema | CrewAI |
| Sequential pipeline fit | Process.sequential is trivial | Requires manual edge wiring | CrewAI |
| Hierarchical delegation | Process.hierarchical + manager | Custom supervisor node | CrewAI |
| Learning overhead | Low — maps to course examples | Higher — graph theory needed | CrewAI |
| Observability | CrewAI+ built-in | LangSmith optional | Tie |

**Verdict**: CrewAI with `Process.sequential` for the writing pipeline; `Process.hierarchical` available as a bonus configuration for the research phase.

### LLM Selection
- **Primary**: `claude-sonnet-4-6` via Anthropic API
- **Rationale**: Best balance of instruction-following, Hebrew language capability, and context window (200K tokens — essential for long paper drafts)
- **Fallback**: `gpt-4o` (OpenAI) if Anthropic API is unavailable
- **Embeddings**: `text-embedding-3-small` (OpenAI) for ChromaDB memory

---

## 3. System Architecture Diagram

```
+-----------------------------------------------------------------+
|                     USER INTERFACE LAYER                        |
|   Streamlit app.py  <->  CLI main.py                           |
+---------------------------+-------------------------------------+
                            | topic: str
                            v
+-----------------------------------------------------------------+
|                      CREW ORCHESTRATION                         |
|                      src/crew.py                                |
|  Process.sequential | memory=True | embedder=ChromaDB          |
+------+--------+--------+--------+--------+---------------------+
       |        |        |        |        |
       v        v        v        v        v
  +--------+ +------+ +------+ +------+ +------+
  |Director| |Rsrch | |Visua-| |LaTeX | |Quali-|
  |Manager | |Agent | |lizer | |Author| |ty Ed |
  +---+----+ +--+---+ +--+---+ +--+---+ +--+---+
      |         |         |        |         |
      v         v         v        v         v
+-----------------------------------------------------------------+
|                         TOOLS LAYER                             |
|  SerperSearch | ArxivSearch | CodeExecutor | FileWriter | FileR |
+-----------------------------------------------------------------+
                            |
                            v
+-----------------------------------------------------------------+
|                        MEMORY LAYER                             |
|  Short-term (session) | Long-term (ChromaDB) | Entity memory   |
+-----------------------------------------------------------------+
                            |
                            v
+-----------------------------------------------------------------+
|                         OUTPUT LAYER                            |
|  latex/main.tex | latex/chapters/*.tex | latex/figures/*.png   |
|  latex/references.bib | outputs/paper.pdf                      |
+-----------------------------------------------------------------+
```

---

## 4. Agent Specifications

### Agent 1: ResearchDirector (Manager Agent)
```
Role:       Senior Research Director & Paper Architect
Goal:       Decompose the research topic '{topic}' into 7-9 thematic sub-topics,
            assign each to DeepResearcher, and ensure the resulting paper structure
            is coherent, complete, and meets IEEE 25-30 page requirements.
Backstory:  You are Dr. Sarah Chen, a 20-year veteran of AI systems research who
            has published 40+ IEEE papers. You are obsessive about structure,
            completeness, and citation quality. You never accept vague deliverables.
LLM:        claude-sonnet-4-6
Tools:      None (manager delegates; does not execute tools directly)
Delegation: allow_delegation=True
Process:    Acts as hierarchical manager in Phase 1 (research)
Max iter:   5
```

### Agent 2: DeepResearcher
```
Role:       Technical AI Systems Research Specialist
Goal:       For each assigned sub-topic, find 5+ authoritative sources, extract
            key technical claims, summarize with academic rigor, and provide
            structured Hebrew-compatible notes for the LaTeX author.
Backstory:  You are Prof. Amit Levi, a computational researcher with a PhD in
            distributed AI systems. You write obsessively detailed research notes
            and never cite a source you have not verified.
LLM:        claude-sonnet-4-6
Tools:      [SerperSearchTool, ArxivSearchTool, WebScraperTool]
Max iter:   10
Memory:     Reads from long-term memory to avoid re-researching known facts
```

### Agent 3: DataVisualizer
```
Role:       Scientific Data Visualization & Graph Engineering Specialist
Goal:       Generate publication-quality Python code using matplotlib/plotly to
            produce 4+ graphs: framework comparison, architecture flowchart,
            security heatmap, deployment radar. Save all as 300 DPI PNG files.
Backstory:  You are Noa Golan, a data scientist and visualization expert who has
            produced figures for 15 peer-reviewed publications. You believe a
            well-crafted figure is worth 500 words of text.
LLM:        claude-sonnet-4-6
Tools:      [PythonCodeExecutorTool, SafeFileWriterTool]
Max iter:   8
Constraint: All generated code must use only whitelisted libraries
```

### Agent 4: LaTeXAuthor
```
Role:       IEEE LaTeX Technical Author (Hebrew/English Bilingual)
Goal:       Convert research summaries and figure references into complete,
            compilable LaTeX chapters in Hebrew. Follow IEEE IEEEtran class
            conventions exactly. Integrate all figures, tables, equations,
            and code listings.
Backstory:  You are Yael Mizrahi, a bilingual academic writer with 10 years
            of experience writing IEEE papers in Hebrew. You know LaTeX syntax
            perfectly and never produce code that does not compile.
LLM:        claude-sonnet-4-6
Tools:      [SafeFileWriterTool, FileReaderTool]
Max iter:   15
Output:     Writes directly to latex/chapters/*.tex and latex/references.bib
```

### Agent 5: QualityEditor
```
Role:       Senior Academic Paper Quality Editor
Goal:       Perform a comprehensive review of the assembled paper: verify page
            count, check every citation exists in .bib, confirm each figure is
            referenced in text, validate Hebrew directionality, and produce a
            detailed remediation report.
Backstory:  You are Prof. Daniel Amir, a meticulous IEEE journal editor who has
            rejected 60% of submissions he has reviewed. Nothing escapes your
            attention. You provide specific line-level feedback.
LLM:        claude-sonnet-4-6
Tools:      [FileReaderTool]
Max iter:   5
Output:     Quality report saved to outputs/quality_report.md
```

---

## 5. Tool Specifications

### Tool 1: SerperSearchTool (External API)
```
Source:    crewai_tools.SerperDevTool
API:       Serper.dev (Google Search API)
Key:       SERPER_API_KEY from .env
Input:     search query string
Output:    List of {title, url, snippet} as formatted string
Errors:
  - Missing key  -> EnvironmentError with setup instructions
  - Rate limit   -> Exponential backoff, 3 retries
  - Timeout      -> TimeoutError with fallback suggestion
  - Empty result -> "No results found" string (no crash)
Validation:
  - Query: non-empty string, max 500 chars
```

### Tool 2: ArxivSearchTool (External API)
```
Source:    Custom BaseTool using arxiv Python library
Input:     query: str, max_results: int (default=5)
Output:    "Title | Authors | Year | Abstract | PDF URL" per result
Errors:
  - Network error  -> retry once, then error message
  - No results     -> empty result message
  - Bad response   -> log warning, return partial results
Validation:
  - query: non-empty string
  - max_results: integer 1-20
```

### Tool 3: PythonCodeExecutorTool
```
Source:    Custom BaseTool
Input:     {code: str, filename: str}
Output:    {status: str, png_path: str, stdout: str, stderr: str}
Security:
  - WHITELIST: matplotlib, plotly, numpy, pandas, scipy
  - BLACKLIST: os, sys, subprocess, shutil, socket, requests
  - AST-based import scanning (not string match)
  - Execution timeout: 30 seconds
  - Output path locked to latex/figures/
Errors:
  - Blocked import     -> SecurityError message
  - Timeout            -> kill process, return timeout error
  - No PNG produced    -> error prompting agent to add savefig()
```

### Tool 4: SafeFileWriterTool
```
Source:    Custom BaseTool
Input:     {path: str, content: str}
Output:    {status: str, path: str}
Security:
  - Validate path within PROJECT_ROOT
  - Block writes to: .env, .gitignore, requirements.txt
  - Allowed dirs: latex/, outputs/, docs/
  - Encoding: UTF-8 always
Errors:
  - Path traversal  -> SecurityError + log
  - Disk full       -> IOError with message
  - Permission      -> PermissionError with path
```

### Tool 5: FileReaderTool
```
Source:    Custom BaseTool
Input:     {path: str}
Output:    UTF-8 string content
Security:
  - Path must be within PROJECT_ROOT
  - Max file size: 1MB
Errors:
  - Not found      -> helpful error with expected path
  - Encoding error -> try latin-1 fallback
  - Too large      -> first 1MB with truncation note
```

### Tool 6: WebScraperTool
```
Source:    crewai_tools.ScrapeWebsiteTool
Input:     URL string
Output:    Extracted text content
Errors:
  - 404       -> "Page not found" message
  - Timeout   -> timeout error message
  - Blocked   -> appropriate message, no crash
```

---

## 6. Memory Architecture

```python
crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    }
)
```

| Memory Type | Storage | Scope | Purpose |
|---|---|---|---|
| Short-Term | In-process RAM | Session only | Pass research to writing within one run |
| Long-Term | ChromaDB (local) | Persistent | Avoid re-searching same topics across runs |
| Entity Memory | ChromaDB | Persistent | Track framework names, authors, concepts |

**Security**: Long-term memory is read-only during writing phase to prevent memory poisoning.

---

## 7. Paper Structure (25-30 pages, IEEE format, Hebrew-primary)

| # | Chapter Title (Hebrew) | Est. Pages | Key Visuals |
|---|---|---|---|
| Cover | det shaer | 1 | Institution name, title, date |
| Abstract | tiktzur | 1 | None |
| 1 | mavo - reka u-motivatzia | 2-3 | Timeline figure |
| 2 | arkhitektura shel sochen AI | 4-5 | Architecture flowchart |
| 3 | misgrotot avoda: CrewAI, LangGraph, AutoGen | 4-5 | Comparison bar chart + table |
| 4 | protokolei tikshoret: MCP ve-A2A | 3-4 | Sequence diagram |
| 5 | bitakhon sokhanim: OWASP Top 10 | 3-4 | Risk heatmap |
| 6 | modelei prisah: Local, Cloud, Hybrid | 3-4 | Radar comparison chart |
| 7 | ha-maarekhet shelanu: ResearchCrew | 3-4 | System diagram, code listings |
| 8 | totzaot ve-nituakh | 2-3 | Results table, performance chart |
| 9 | sikum, migbalot ve-atid | 1-2 | None |
| Refs | bibliographia | 1-2 | None |

---

## 8. Streamlit UI Specification

Components:
- st.text_input: research topic
- st.selectbox: model selection (sonnet / opus)
- st.slider: target page count (25-30)
- st.multiselect: enable/disable individual tools
- st.button: "Generate Paper" trigger
- st.progress: per-agent progress (via CrewAI step callbacks)
- st.expander: agent log (collapsible, scrollable)
- st.download_button: for .tex, .bib, each .png, final .pdf
- st.code: syntax-highlighted LaTeX preview
- st.image: inline graph preview

---

## 9. Security Requirements

- All API keys in .env, loaded via python-dotenv
- .env listed in .gitignore, never committed
- PythonCodeExecutor uses AST-based import whitelist
- All file paths canonicalized and validated against PROJECT_ROOT
- No shell=True in subprocess calls
- LaTeX special characters escaped in all agent outputs
- Input topic HTML-escaped before passing to agents

---

## 10. Repository Structure

```
assignment3/
+-- .env                     (gitignored)
+-- .env.example
+-- .gitignore
+-- requirements.txt
+-- README.md
+-- app.py                   (Streamlit UI)
+-- main.py                  (CLI)
+-- src/
|   +-- __init__.py
|   +-- config.py
|   +-- agents/
|   |   +-- research_director.py
|   |   +-- deep_researcher.py
|   |   +-- data_visualizer.py
|   |   +-- latex_author.py
|   |   +-- quality_editor.py
|   +-- tasks/
|   |   +-- research_tasks.py
|   |   +-- visualization_tasks.py
|   |   +-- writing_tasks.py
|   +-- tools/
|   |   +-- search_tools.py
|   |   +-- code_executor.py
|   |   +-- file_tools.py
|   |   +-- web_scraper.py
|   +-- crew.py
+-- latex/
|   +-- main.tex
|   +-- course_summary_main.tex
|   +-- chapters/
|   |   +-- cover.tex
|   |   +-- abstract.tex
|   |   +-- ch01_intro.tex ... ch09_conclusion.tex
|   +-- figures/
|   +-- references.bib
+-- outputs/                 (gitignored for PDFs)
+-- tests/
|   +-- test_tools.py
|   +-- test_agents.py
|   +-- test_crew.py
+-- docs/
    +-- PRD.md
    +-- TODO.md
    +-- course_summary.md
```

---

## 11. Success Metrics

| Requirement | Acceptance Criterion | Verification |
|---|---|---|
| Agent runs end-to-end | crew.kickoff() completes | pytest tests/test_crew.py |
| 2+ external tools | Serper + ArXiv return results | pytest tests/test_tools.py |
| Memory active | .chroma/ directory exists | os.path.exists check |
| Paper length | 25-30 pages | pdfinfo output.pdf grep Pages |
| LaTeX compiles | Zero critical errors | pdflatex exit code 0 |
| Hebrew RTL | Text flows right-to-left | Visual PDF inspection |
| Bibliography | 15+ entries, all cited | bibtex with zero warnings |
| Figures | 4+ PNG files in latex/figures/ | ls figures/*.png wc -l |
| No hardcoded keys | Zero secrets in src/ | grep -r "sk-" src/ = empty |
| Tests pass | All pytest green | pytest tests/ -v |
| Course summary | 20+ pages | pdfinfo course_summary.pdf |

---

## 12. Edge Cases & Risk Mitigation

| Risk | Probability | Mitigation |
|---|---|---|
| Serper rate limit | Medium | Exponential backoff + result caching |
| Agent generates invalid LaTeX | High | QualityEditor reviews; manual fix fallback |
| Hebrew BiDi rendering broken | Medium | Test compile early; use polyglossia if babel fails |
| Paper under 25 pages | Medium | QualityEditor checks; expand-section task |
| ArXiv returns irrelevant papers | Low | Query refinement in prompt; manual curation |
| MikTeX package missing | Medium | Pre-run package check script |
| ChromaDB corruption | Low | Memory rebuild script; auxiliary only |
| OpenAI key missing for embeddings | Medium | HuggingFace local fallback (all-MiniLM-L6-v2) |
