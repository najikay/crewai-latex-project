# TODO.md — Assignment 3: ResearchCrew
## Complete Build Checklist | Deadline: 2026-06-20

> **How to use**: Work top-to-bottom. Mark `[x]` when done. Never skip a test step.

---

## PHASE 1: Environment & Project Setup

### 1.1 Machine Setup
- [ ] Install Python 3.11+ if not already installed
- [ ] Install MikTeX from https://miktex.org/download (Windows) — choose "Install for all users"
- [ ] Open MikTeX Package Manager → install: `IEEEtran`, `babel-hebrew`, `booktabs`, `biblatex`, `fancyhdr`, `hyperref`, `amsmath`, `graphicx`
- [ ] Install Git if not already installed
- [ ] Create GitHub account (if needed) and create repo: `assignment3-researchcrew`
- [ ] Install VS Code + LaTeX Workshop extension (for live LaTeX preview)

### 1.2 Project Skeleton
- [ ] Create root folder: `assignment3/`
- [ ] Run: `python -m venv venv` inside `assignment3/`
- [ ] Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- [ ] Create `requirements.txt`:
  ```
  crewai==0.80.0
  crewai-tools==0.15.0
  anthropic>=0.40.0
  streamlit>=1.35.0
  python-dotenv>=1.0.0
  arxiv>=2.1.0
  matplotlib>=3.9.0
  plotly>=5.22.0
  chromadb>=0.5.0
  langchain-openai>=0.1.0
  pytest>=8.0.0
  ```
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify install: `python -c "import crewai, anthropic, streamlit; print('All OK')"`
- [ ] Create `.env` file with:
  ```
  ANTHROPIC_API_KEY=your_key_here
  SERPER_API_KEY=your_key_here
  OPENAI_API_KEY=your_key_here
  ```
- [ ] Create `.env.example` (same structure, empty values)
- [ ] Create `.gitignore` containing: `.env`, `venv/`, `__pycache__/`, `outputs/`, `*.pyc`, `*.pdf`
- [ ] Create full directory structure (see PRD Section 10)
- [ ] Initial git commit: `git commit -m "chore: project skeleton"`

---

## PHASE 1: Tools Layer

### 1.3 Search Tools
- [ ] Create `src/tools/search_tools.py`
- [ ] Implement `SerperSearchTool` using `crewai_tools.SerperDevTool`
- [ ] Implement `ArxivSearchTool` as a custom `BaseTool` subclass
  - [ ] `name`: `"arxiv_search"`
  - [ ] `description`: describes when to use it
  - [ ] `_run(query: str)` → calls `arxiv.Search()` → returns formatted string of 5 results
- [ ] Test `SerperSearchTool`: search "CrewAI multi-agent" → assert non-empty result
- [ ] Test `ArxivSearchTool`: search "LangGraph stateful agents" → assert ≥ 3 papers returned

### 1.4 Code Executor Tool
- [ ] Create `src/tools/code_executor.py`
- [ ] Implement `PythonCodeExecutorTool(BaseTool)`:
  - [ ] Validate code only uses allowed imports (whitelist: matplotlib, plotly, numpy, pandas)
  - [ ] Write code to temp `.py` file
  - [ ] Run via `subprocess.run(["python", tmpfile], timeout=30, capture_output=True)`
  - [ ] Auto-inject `plt.savefig("latex/figures/<filename>.png", dpi=300, bbox_inches='tight')`
  - [ ] Return: path to saved PNG + stdout
- [ ] Test: execute a simple `plt.plot([1,2,3,4])` → verify PNG appears in `latex/figures/`
- [ ] Test: attempt to execute `import os; os.remove("file")` → verify it is blocked

### 1.5 File I/O Tools
- [ ] Create `src/tools/file_tools.py`
- [ ] Implement `SafeFileWriterTool(BaseTool)`:
  - [ ] Validate path stays within project directory (no `../` escapes)
  - [ ] Create parent directories if needed
  - [ ] Write UTF-8 content
- [ ] Implement `FileReaderTool(BaseTool)`:
  - [ ] Validate path exists and is within project
  - [ ] Return UTF-8 content
- [ ] Test: write Hebrew text to `outputs/test.txt` → read it back → assert match

---

## PHASE 1: Agents Layer

### 1.6 Config Module
- [ ] Create `src/config.py`:
  - [ ] Load `.env` via `load_dotenv()`
  - [ ] Expose: `MODEL_NAME`, `OUTPUT_DIR`, `LATEX_DIR`, all API keys
  - [ ] Raise `ValueError` with clear message if any required key is missing
- [ ] Test: delete `ANTHROPIC_API_KEY` from `.env` temporarily → verify clear error message appears

### 1.7 Build Each Agent
- [ ] Create `src/agents/research_director.py` → `create_research_director()` function
  - [ ] `allow_delegation=True` (manager agent)
  - [ ] `llm=f"anthropic/{MODEL_NAME}"`
  - [ ] `verbose=True`
- [ ] Create `src/agents/deep_researcher.py` → `create_deep_researcher()` function
  - [ ] Tools: `[SerperSearchTool(), ArxivSearchTool()]`
- [ ] Create `src/agents/data_visualizer.py` → `create_data_visualizer()` function
  - [ ] Tools: `[PythonCodeExecutorTool(), SafeFileWriterTool()]`
- [ ] Create `src/agents/latex_author.py` → `create_latex_author()` function
  - [ ] Tools: `[SafeFileWriterTool(), FileReaderTool()]`
- [ ] Create `src/agents/quality_editor.py` → `create_quality_editor()` function
  - [ ] Tools: `[FileReaderTool()]`
- [ ] Smoke test each agent: instantiate without errors

---

## PHASE 1: Tasks & Crew

### 1.8 Build Tasks
- [ ] Create `src/tasks/research_tasks.py`:
  - [ ] `create_decompose_task(director)` — produce list of 7 sub-topics
  - [ ] `create_research_task(researcher, subtopic)` — research one sub-topic → save to `outputs/research_{slug}.md`
- [ ] Create `src/tasks/visualization_tasks.py`:
  - [ ] `create_graphs_task(visualizer)` — generate 4 graphs → return PNG paths
- [ ] Create `src/tasks/writing_tasks.py`:
  - [ ] `create_chapter_task(author, chapter_num, research_file)` → write `.tex` file
  - [ ] `create_bibliography_task(author)` → compile `references.bib`
  - [ ] `create_review_task(editor)` → review full paper, return quality report
- [ ] Verify every task has a specific, measurable `expected_output`

### 1.9 Crew Assembly
- [ ] Create `src/crew.py` → `build_crew(topic: str) -> Crew`
  - [ ] `memory=True`
  - [ ] `embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}`
  - [ ] `output_log_file="outputs/crew_log.txt"`
  - [ ] `process=Process.sequential`
- [ ] Test with simple topic ("machine learning"): run crew → verify it completes without crash

### 1.10 CLI Interface
- [ ] Create `main.py` with `argparse`
  - [ ] `--topic` (required)
  - [ ] `--output-dir` (optional, default: "outputs")
- [ ] Test: `python main.py --topic "test"` → runs and outputs something

### 1.11 Streamlit Interface
- [ ] Create `app.py` with Streamlit
  - [ ] Sidebar: topic input, run button
  - [ ] Main area: progress spinner, output display
  - [ ] Download buttons for: `.tex`, `.bib`, each `.png` graph
  - [ ] Log console (show `crew_log.txt` content)
- [ ] Test: `streamlit run app.py` → UI loads in browser
- [ ] Test: Click run button → spinner appears → crew runs → results shown

---

## PHASE 1: Tests
- [ ] Create `tests/test_tools.py`:
  - [ ] `test_serper_search_returns_results()`
  - [ ] `test_arxiv_search_returns_papers()`
  - [ ] `test_code_executor_generates_png()`
  - [ ] `test_code_executor_blocks_dangerous_imports()`
  - [ ] `test_file_writer_creates_file()`
  - [ ] `test_file_reader_returns_content()`
- [ ] Create `tests/test_agents.py`:
  - [ ] `test_all_agents_instantiate()`
- [ ] Create `tests/test_crew.py`:
  - [ ] `test_crew_builds_without_error()`
- [ ] Run: `python -m pytest tests/ -v` → all green
- [ ] Take **screenshot** of passing tests for submission evidence

---

## PHASE 2: Content Generation

### 2.1 Research Phase
- [ ] Run full research crew on the real topic: `python main.py --topic "ארכיטקטורת סוכני AI בשנת 2026"`
- [ ] Verify these files exist and are ≥ 800 words each:
  - [ ] `outputs/research_intro.md`
  - [ ] `outputs/research_architecture.md`
  - [ ] `outputs/research_frameworks.md`
  - [ ] `outputs/research_protocols.md`
  - [ ] `outputs/research_security.md`
  - [ ] `outputs/research_deployment.md`
  - [ ] `outputs/research_our_system.md`
- [ ] Review each file for accuracy and completeness
- [ ] Edit/supplement any thin sections manually

### 2.2 Graph Generation
- [ ] Verify these PNG files exist in `latex/figures/`:
  - [ ] `fig_framework_comparison.png` (bar chart: CrewAI vs LangGraph vs AutoGen)
  - [ ] `fig_agent_architecture.png` (flowchart: Planner→Memory→Tools→RAG)
  - [ ] `fig_security_heatmap.png` (OWASP risk matrix)
  - [ ] `fig_deployment_radar.png` (radar chart: Local vs Cloud vs Hybrid)
- [ ] Verify each PNG is ≥ 300 DPI
- [ ] Verify each PNG has Hebrew labels where appropriate
- [ ] Take **screenshots** of graph generation code running for submission

### 2.3 Course Summary Document
- [ ] Create `docs/course_summary.md`
- [ ] Write section for each of the 5 previous tasks (Tasks 1–5)
  - [ ] Task 1: description, what you built, screenshot/link
  - [ ] Task 2: description, what you built, screenshot/link
  - [ ] Task 3: description, what you built, screenshot/link
  - [ ] Task 4: description, what you built, screenshot/link
  - [ ] Task 5: description, what you built, screenshot/link
- [ ] Add course overview section (2–3 pages)
- [ ] Add reflection section (1–2 pages)
- [ ] Verify total: ≥ 20 pages when rendered

---

## PHASE 3: LaTeX/IEEE Integration

### 3.1 LaTeX Structure
- [ ] Create `latex/main.tex` (master file — see IMPLEMENTATION_PLAN Step 3.1)
- [ ] Set `\documentclass[10pt, a4paper, journal]{IEEEtran}`
- [ ] Add all required `\usepackage{}` declarations
- [ ] Configure `fancyhdr` for headers/footers on every page
- [ ] Set up `\bibliography{references}` + `\bibliographystyle{IEEEtran}`
- [ ] Test compile (empty chapters): `pdflatex main.tex` → no fatal errors

### 3.2 Cover Sheet
- [ ] Create `latex/chapters/cover.tex`
  - [ ] Course name in Hebrew
  - [ ] Assignment number (3)
  - [ ] Paper title in Hebrew
  - [ ] Student name(s)
  - [ ] Submission date: 20 יוני 2026
  - [ ] Institution/department
- [ ] Verify cover compiles and looks correct in PDF

### 3.3 Abstract
- [ ] Create `latex/chapters/abstract.tex`
  - [ ] Hebrew abstract (150–250 words)
  - [ ] English abstract (same content, 150–250 words)
  - [ ] 5–7 keywords

### 3.4 Write All Chapters (Hebrew LaTeX)
For each chapter, create the `.tex` file and verify:
- [ ] `ch01_intro.tex` — includes `\section{}`, references at least 2 sources
- [ ] `ch02_architecture.tex` — includes architecture diagram figure, 1 table
- [ ] `ch03_frameworks.tex` — includes framework comparison table and bar chart figure
- [ ] `ch04_protocols.tex` — includes MCP/A2A diagram, code listing
- [ ] `ch05_security.tex` — includes security heatmap figure, OWASP table
- [ ] `ch06_deployment.tex` — includes radar chart figure, comparison table
- [ ] `ch07_our_system.tex` — includes screenshot of running code, architecture figure
- [ ] `ch08_results.tex` — includes metrics table, results figure
- [ ] `ch09_conclusion.tex` — summarizes findings, future work

Each chapter must contain:
- [ ] At least one `\subsection{}`
- [ ] At least one `\begin{figure}...\end{figure}` with caption
- [ ] At least one `\begin{table}...\end{table}` with caption
- [ ] At least one `\cite{}` citation
- [ ] All prose in Hebrew (technical terms in English inline)

### 3.5 Math Formulas ("Fancy Formulas")
- [ ] Add at least 2 mathematical formulas in `\begin{equation}` environments
  - [ ] Example: Transformer attention formula
  - [ ] Example: Agent utility/reward function
- [ ] Verify formulas render correctly in PDF

### 3.6 Code Listings
- [ ] Add `\usepackage{listings}` to main.tex
- [ ] Include at least 2 Python code listings (key agent code snippets)
- [ ] Listings must have syntax highlighting and line numbers

### 3.7 Bibliography
- [ ] Create `latex/references.bib` with ≥ 15 entries
  - [ ] At least 5 `@article{}` entries from ArXiv/IEEE
  - [ ] At least 3 `@misc{}` entries for framework documentation
  - [ ] At least 2 `@inproceedings{}` entries
  - [ ] Course material cited as `@unpublished{}`
- [ ] Verify every `\cite{}` in text has a matching entry in `.bib`

### 3.8 Full Compilation
- [ ] Run compilation sequence:
  ```
  pdflatex main.tex
  bibtex main
  pdflatex main.tex
  pdflatex main.tex
  ```
- [ ] Verify: zero errors (warnings are OK)
- [ ] Verify: PDF page count is 25–30 pages
- [ ] Verify: Table of Contents is correct
- [ ] Verify: All figures appear
- [ ] Verify: Bibliography section appears with all references
- [ ] Verify: Headers and footers appear on every page
- [ ] Verify: Hebrew text is right-to-left
- [ ] Verify: Cover page is correct
- [ ] Take **screenshot** of `pdflatex` compilation output (no errors)
- [ ] Take **screenshot** of first page of PDF
- [ ] Take **screenshot** of bibliography page

### 3.9 Course Summary LaTeX
- [ ] Convert `docs/course_summary.md` to `latex/course_summary.tex`
- [ ] Create `latex/course_summary_main.tex` (standalone document)
- [ ] Compile: `pdflatex course_summary_main.tex`
- [ ] Verify: ≥ 20 pages

---

## PHASE 4: Validation & Submission

### 4.1 Assignment Requirements Checklist
- [ ] Is the system modular? (each agent in its own file, each tool in its own file)
- [ ] Is the system scalable? (adding a new agent requires only a new file + registration in crew.py)
- [ ] Is the system generic? (topic is a parameter, not hardcoded)
- [ ] Are there ≥ 2 external tools? (Serper + ArXiv)
- [ ] Is memory implemented? (ChromaDB via `memory=True`)
- [ ] Is the Python code 100% working? (all tests pass)
- [ ] Does the paper have 25–30 pages? (verify with `pdfinfo`)
- [ ] Is it in IEEE format? (IEEEtran class)
- [ ] Is it in Hebrew + English? (Hebrew prose, English terms)
- [ ] Is MikTeX/LaTeX used? (compilation command works locally)
- [ ] Are code screenshots included for every component?
- [ ] Are GitHub links included for every component?
- [ ] Is there a 3-minute demo video?
- [ ] Is the 20-page course summary complete?
- [ ] Are all `.env` keys used (no hardcoded credentials)?

### 4.2 Security Audit
- [ ] Run: `grep -r "sk-" src/` → must return nothing
- [ ] Run: `grep -r "ANTHROPIC_API_KEY=" src/` → must return nothing (only in .env)
- [ ] Verify `.env` is in `.gitignore`
- [ ] Verify `.env` is NOT committed to git: `git ls-files .env` → must return nothing

### 4.3 Demo Video
- [ ] Prepare demo script (3 minutes):
  - [ ] 0:00–0:30: Show Streamlit UI, explain what it does
  - [ ] 0:30–1:30: Enter topic, click run, show agents working in real-time
  - [ ] 1:30–2:30: Show generated LaTeX files and compiled PDF
  - [ ] 2:30–3:00: Show GitHub repo, README, all files
- [ ] Record using OBS or Windows Game Bar (Win+G)
- [ ] Trim to ≤ 3 minutes
- [ ] Export as MP4
- [ ] Verify audio is clear

### 4.4 GitHub Repository
- [ ] Repository is public (or accessible to professor)
- [ ] README.md contains:
  - [ ] Project description (what it does)
  - [ ] Architecture overview
  - [ ] Installation instructions (step by step)
  - [ ] Usage: CLI (`python main.py --topic "..."`)
  - [ ] Usage: Web (`streamlit run app.py`)
  - [ ] Required environment variables
  - [ ] Screenshots of running agent
  - [ ] Screenshot of compiled PDF
  - [ ] Link to compiled PDF (if uploaded)
  - [ ] Link to demo video
- [ ] All source code committed
- [ ] LaTeX source files committed
- [ ] Generated figures committed (PNG files)
- [ ] `requirements.txt` committed
- [ ] `.env.example` committed
- [ ] No `.env` committed (verify!)

### 4.5 Submission Package Assembly
- [ ] Compile final `paper.pdf` (clean 3-run compilation)
- [ ] Compile final `course_summary.pdf`
- [ ] Verify `paper.pdf` pages: 25–30
- [ ] Verify `course_summary.pdf` pages: ≥ 20
- [ ] Create submission zip: `assignment3_submission.zip`
  - [ ] `paper.pdf`
  - [ ] `course_summary.pdf`
  - [ ] `demo_video.mp4`
  - [ ] `README.md` (with GitHub link)
  - [ ] `latex/` folder (source)
  - [ ] `src/` folder (source)
- [ ] Submit before **20/06/2026**

---

## Evidence Screenshots Required (per submission guidelines)
- [ ] Screenshot: `pip install` output / all packages installed
- [ ] Screenshot: `pytest` run — all tests green
- [ ] Screenshot: Streamlit UI running in browser
- [ ] Screenshot: Agents running (verbose CrewAI output in terminal)
- [ ] Screenshot: Generated graph (matplotlib PNG)
- [ ] Screenshot: LaTeX source code (a chapter file open in editor)
- [ ] Screenshot: `pdflatex` compilation — no errors
- [ ] Screenshot: Final PDF page 1 (cover)
- [ ] Screenshot: Final PDF table of contents
- [ ] Screenshot: Final PDF bibliography page
- [ ] Screenshot: GitHub repository main page
- [ ] Screenshot: GitHub repository code structure

---

## Bonus Points Opportunities
- [ ] Add a 6th agent: `CitationChecker` — validates all citations are real
- [ ] Add `Process.hierarchical` mode with ResearchDirector as manager
- [ ] Add support for multiple output languages (English/Hebrew toggle)
- [ ] Add a progress bar with estimated completion time
- [ ] Add RAG over the course PDFs (so agent can cite course material)
- [ ] Deploy Streamlit app to Streamlit Cloud for live demo link
