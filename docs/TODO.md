# TODO.md — Assignment 3: NavigatorCrew (Biomimetic Navigation Platform)
## Hyper-Granular Micro-Task Checklist | Deadline: 2026-06-20
## Total tasks: ~620 atomic checkboxes across 7 modules

> **Rule**: Each checkbox is ONE atomic action. Never check a box until that exact action is done.
> **[SS]** = Screenshot required; save to `docs/evidence/`.
> **[COMPILE]** = Run `xelatex main.tex` after this change; fix any errors before proceeding.

---

# MODULE 1: Environment & Setup

## 1.1 System Prerequisites

- [ ] Open terminal (WSL2, PowerShell, or Windows Terminal)
- [ ] Run `python --version` — confirm Python 3.11 or higher
- [ ] Run `git --version` — confirm Git is installed
- [ ] Run `pip --version` — confirm pip ≥ 24.0
- [ ] Run `pip install --upgrade pip`

## 1.2 MikTeX / XeLaTeX Installation

- [ ] Download MikTeX installer from miktex.org/download (Windows 64-bit)
- [ ] Run installer as Administrator
- [ ] Select "Install for all users"
- [ ] Enable "Install missing packages on-the-fly: Yes"
- [ ] Complete installation
- [ ] Open MikTeX Console → click "Check for updates" → install all updates
- [ ] Open MikTeX Package Manager
- [ ] Install package: `IEEEtran`
- [ ] Install package: `polyglossia`
- [ ] Install package: `fontspec`
- [ ] Install package: `bidi`
- [ ] Install package: `booktabs`
- [ ] Install package: `fancyhdr`
- [ ] Install package: `hyperref`
- [ ] Install package: `amsmath`
- [ ] Install package: `amssymb`
- [ ] Install package: `mathtools`
- [ ] Install package: `graphicx`
- [ ] Install package: `listings`
- [ ] Install package: `xcolor`
- [ ] Install package: `caption`
- [ ] Install package: `subcaption`
- [ ] Install package: `float`
- [ ] Install package: `geometry`
- [ ] Install package: `microtype`
- [ ] Install package: `enumitem`
- [ ] Install package: `tabularx`
- [ ] Install package: `multirow`
- [ ] Run `xelatex --version` in terminal — confirm XeLaTeX is in PATH [SS]
- [ ] Run `bibtex --version` — confirm BibTeX is accessible [SS]

## 1.3 Hebrew Font Installation (Critical for XeLaTeX)

- [ ] Open MikTeX Package Manager → search "culmus" → install (provides David CLM, Miriam CLM)
- [ ] Alternatively: download Culmus fonts from culmus.sourceforge.net
- [ ] Install font files (.ttf) by right-clicking → "Install for all users"
- [ ] Run `fc-list | grep -i david` — confirm "David CLM" is visible to fontconfig
- [ ] If David CLM missing: open `latex/main.tex` and change `\hebrewfont` to `\hebrewfont[Script=Hebrew]{Arial}` as fallback
- [ ] Create file `latex/test_hebrew.tex`:
  ```tex
  \documentclass{article}
  \usepackage{fontspec}
  \usepackage{polyglossia}
  \setmainlanguage{hebrew}
  \setotherlanguage{english}
  \newfontfamily\hebrewfont[Script=Hebrew]{David CLM}
  \begin{document}
  שלום עולם — Hello World
  \end{document}
  ```
- [ ] Run `xelatex test_hebrew.tex` in `latex/` folder
- [ ] Confirm PDF contains both Hebrew and English text [SS]
- [ ] Delete `test_hebrew.tex` and `test_hebrew.pdf`

## 1.4 GitHub Repository

- [ ] Log in to github.com
- [ ] Create new repository: `assignment3-navigatorcrew`
- [ ] Set visibility: Public
- [ ] Add Python .gitignore template
- [ ] Add a README
- [ ] Copy HTTPS clone URL
- [ ] Run `git clone <url> assignment3` in working directory
- [ ] `cd assignment3`
- [ ] Confirm `.git/` folder exists
- [ ] Run `git config user.name "Your Name"`
- [ ] Run `git config user.email "your@email.com"`

## 1.5 Python Virtual Environment

- [ ] Inside `assignment3/`: run `python -m venv venv`
- [ ] Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate`
- [ ] Confirm `(venv)` prefix appears in terminal
- [ ] Confirm `python --version` inside venv shows correct version

## 1.6 requirements.txt

- [ ] Confirm `requirements.txt` exists (already written to disk)
- [ ] Run `pip install -r requirements.txt`
- [ ] Wait for complete installation
- [ ] Run `pip list` and save output screenshot [SS]
- [ ] Run `python -c "import crewai; print(crewai.__version__)"` — verify
- [ ] Run `python -c "import anthropic; print('ok')"` — verify
- [ ] Run `python -c "import streamlit; print('ok')"` — verify
- [ ] Run `python -c "import arxiv; print('ok')"` — verify
- [ ] Run `python -c "import chromadb; print('ok')"` — verify
- [ ] Run `python -c "import matplotlib; print('ok')"` — verify
- [ ] Run `python -c "from mpl_toolkits.mplot3d import Axes3D; print('3D ok')"` — verify
- [ ] Run `python -c "import scipy; print('ok')"` — verify

## 1.7 API Keys (.env)

- [ ] Confirm `.env.example` exists (already written to disk)
- [ ] Copy `.env.example` → `.env`
- [ ] Obtain Anthropic API key from console.anthropic.com
- [ ] Paste key as `ANTHROPIC_API_KEY=sk-ant-...` in `.env`
- [ ] Obtain Serper key from serper.dev
- [ ] Paste key as `SERPER_API_KEY=...` in `.env`
- [ ] Obtain OpenAI key from platform.openai.com (for embeddings)
- [ ] Paste key as `OPENAI_API_KEY=sk-...` in `.env`
- [ ] Save `.env`
- [ ] Run `python src/config.py` — confirm "Config validation passed" [SS]
- [ ] Confirm no keys appear in terminal output (masked to first 8 chars)

## 1.8 .gitignore Verification

- [ ] Open `.gitignore` — confirm `.env` is listed
- [ ] Confirm `venv/` is listed
- [ ] Confirm `*.pdf` is listed
- [ ] Confirm `.chroma/` is listed
- [ ] Confirm `*.aux`, `*.log`, `*.bbl`, `*.blg` are listed
- [ ] Run `git status` — confirm `.env` does NOT appear in untracked files

## 1.9 Directory Structure Verification

- [ ] Confirm all directories exist: `src/agents/`, `src/tasks/`, `src/tools/`
- [ ] Confirm all directories exist: `latex/chapters/`, `latex/figures/`, `outputs/`
- [ ] Confirm all `__init__.py` files exist in `src/`, `src/agents/`, `src/tasks/`, `src/tools/`
- [ ] Confirm `latex/main.tex` exists (XeLaTeX master — already written)
- [ ] Confirm `latex/chapters/ch01_intro.tex` exists (biomimetic intro with formulas)
- [ ] Confirm `latex/references.bib` exists (5 seed entries)

## 1.10 LaTeX Boilerplate Compile Test [COMPILE]

- [ ] Open terminal in `latex/` folder
- [ ] Run `xelatex main.tex`
- [ ] Check for errors (lines starting with `!`)
- [ ] Fix any font errors (adjust `\hebrewfont` family if David CLM not found)
- [ ] Fix any package errors (install missing packages via MikTeX Console)
- [ ] Run `bibtex main`
- [ ] Run `xelatex main.tex` (second pass)
- [ ] Run `xelatex main.tex` (third pass — for TOC and cross-refs)
- [ ] Open `main.pdf` — confirm it opens without errors
- [ ] Confirm Hebrew text on cover page renders RTL [SS]
- [ ] Confirm formulas in ch01 render (Eq. 1, 2, 3, 4, 5) [SS]
- [ ] Confirm placeholder figures appear as boxes (not errors) [SS]
- [ ] Note page count at this stub stage

## 1.11 Initial Git Commit

- [ ] Run `git add requirements.txt .env.example .gitignore`
- [ ] Run `git add src/ latex/ tests/ docs/`
- [ ] Run `git status` — confirm `.env` NOT staged
- [ ] Run `git commit -m "feat: Module 1 complete — environment, XeLaTeX boilerplate, biomimetic scaffold"`
- [ ] Run `git push origin main`
- [ ] Open GitHub in browser — verify files appear [SS]

---

# MODULE 2: Agent Development (The "Brain")

## 2.1 src/config.py Verification

- [ ] Confirm `src/config.py` exists (already written)
- [ ] Open `src/config.py` and verify 10 sections are present
- [ ] Confirm `PROJECT_ROOT` is derived from `__file__` (not hardcoded)
- [ ] Confirm `FIGURES_DIR.mkdir(parents=True, exist_ok=True)` is called at import
- [ ] Confirm `OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)` is called at import
- [ ] Confirm `loguru` logger is configured with console + file sinks
- [ ] Confirm `get_embedder_config()` returns OpenAI config when key is set
- [ ] Confirm `get_embedder_config()` returns HuggingFace config when key is missing
- [ ] Confirm `validate_config()` raises `EnvironmentError` with fix instructions on missing key
- [ ] Run `python src/config.py` with all keys set — confirm all checks pass [SS]

## 2.2 NavigationResearchDirector Agent

- [ ] Create file `src/agents/navigation_director.py`
- [ ] Add import: `from crewai import Agent`
- [ ] Add import: `from src.config import MODEL_NAME, AGENT_MAX_ITER`
- [ ] Define function `create_navigation_director() -> Agent`
- [ ] Set `role = "Senior Research Fellow — Autonomous Navigation Systems"`
- [ ] Write `goal`: minimum 4 sentences; must specify decompose topic into 7 sub-domains
- [ ] Confirm goal includes: "every chapter contains formal problem definitions"
- [ ] Confirm goal includes: "every formula must be derived, not stated"
- [ ] Confirm goal includes: "IEEE-quality citations from Thrun, Simmons, Kalman lineage"
- [ ] Write `backstory` as Dr. Yael Cohen — name, institution, publication history
- [ ] Confirm backstory is at least 5 sentences with concrete credentials
- [ ] Confirm backstory includes: "incapable of accepting hand-wavy engineering prose"
- [ ] Set `verbose = True`
- [ ] Set `allow_delegation = True`
- [ ] Set `llm = f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter = AGENT_MAX_ITER["research_director"]`
- [ ] Return the Agent object
- [ ] Test: `from src.agents.navigation_director import create_navigation_director; a = create_navigation_director(); print(a.role)` — no errors

## 2.3 SLAMAndFusionResearcher Agent

- [ ] Create file `src/agents/slam_researcher.py`
- [ ] Add all necessary imports (Agent, tools, config)
- [ ] Define function `create_slam_researcher() -> Agent`
- [ ] Set `role = "SLAM, Sensor Fusion & Signal Processing Research Specialist"`
- [ ] Write `goal`: find 5+ IEEE/ArXiv sources per sub-domain with BibTeX entries
- [ ] Confirm goal includes: "extract algorithms AND mathematical formulations"
- [ ] Confirm goal includes: "produce LaTeX-ready equation skeletons"
- [ ] Confirm goal includes: "include benchmark results (RMSE, ATE, RPE values)"
- [ ] Write `backstory` as Prof. Amir Ben-David — Technion PhD, EKF-SLAM implementation experience
- [ ] Confirm backstory includes: "you never approximate; you cite page numbers"
- [ ] Set `tools = [SerperSearchTool(), ArxivSearchTool(), WebScraperTool()]`
- [ ] Confirm ArxivSearchTool is configured to prefer categories: `cs.RO`, `eess.SP`, `cs.CV`
- [ ] Set `verbose = True`
- [ ] Set `allow_delegation = False`
- [ ] Set `llm = f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter = AGENT_MAX_ITER["deep_researcher"]`
- [ ] Return Agent
- [ ] Test: import and instantiate — no errors

## 2.4 VisualizationEngineer Agent

- [ ] Create file `src/agents/visualization_engineer.py`
- [ ] Add all necessary imports
- [ ] Define function `create_visualization_engineer() -> Agent`
- [ ] Set `role = "Scientific Visualization & Sensor Data Engineering Specialist"`
- [ ] Write `goal`: generate all 9 required figures as 300 DPI PNG
- [ ] Confirm goal lists ALL 9 figures by name:
  - [ ] `fig_bat_vs_artificial.png`
  - [ ] `fig_trajectory_3d.png`
  - [ ] `fig_sensor_fusion_heatmap.png`
  - [ ] `fig_cochleagram.png`
  - [ ] `fig_range_doppler.png`
  - [ ] `fig_ekf_covariance.png`
  - [ ] `fig_framework_comparison.png`
  - [ ] `fig_sensor_modalities.png`
  - [ ] `fig_results_summary.png`
- [ ] Confirm goal states: "Hebrew axis labels where appropriate"
- [ ] Confirm goal states: "poorly labeled axis is professional negligence"
- [ ] Write `backstory` as Noa Shapira — MSc computational neuroscience, ICRA/IROS figures
- [ ] Set `tools = [PythonCodeExecutorTool(), SafeFileWriterTool()]`
- [ ] Set `verbose = True`
- [ ] Set `allow_delegation = False`
- [ ] Set `llm = f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter = AGENT_MAX_ITER["data_visualizer"]`
- [ ] Return Agent
- [ ] Test: import and instantiate — no errors

## 2.5 LaTeXAuthor Agent

- [ ] Create file `src/agents/latex_author.py`
- [ ] Define function `create_latex_author() -> Agent`
- [ ] Set `role = "IEEE LaTeX Technical Author (Hebrew/English Bilingual, Robotics Domain)"`
- [ ] Write `goal`: convert research notes to compilable Hebrew XeLaTeX chapters
- [ ] Confirm goal explicitly mentions: XeLaTeX (not pdflatex)
- [ ] Confirm goal states: "every output must compile on the first xelatex run"
- [ ] Confirm goal states: "every chapter must include: formal definitions, numbered equations, figure references, tables"
- [ ] Confirm goal states: "Hebrew prose, English technical terms via \en{} command"
- [ ] Write `backstory` as Yael Mizrahi — bilingual technical writer, robotics IEEE papers
- [ ] Confirm backstory: "You treat LaTeX syntax errors as personal failures"
- [ ] Set `tools = [SafeFileWriterTool(), FileReaderTool()]`
- [ ] Set `verbose = True`
- [ ] Set `max_iter = AGENT_MAX_ITER["latex_author"]`
- [ ] Return Agent
- [ ] Test: import and instantiate — no errors

## 2.6 QualityEditor Agent

- [ ] Create file `src/agents/quality_editor.py`
- [ ] Define function `create_quality_editor() -> Agent`
- [ ] Set `role = "Senior IEEE Journal Technical Editor — Robotics & Autonomous Systems"`
- [ ] Write `goal`: verify mathematical notation consistency, citation completeness, page count
- [ ] Confirm goal includes: check every `\cite{}` key exists in .bib
- [ ] Confirm goal includes: flag any section below 400 words
- [ ] Confirm goal includes: verify equation numbering is sequential
- [ ] Confirm goal includes: check every figure is referenced in text with `\figref` or `\ref`
- [ ] Write `backstory` as Prof. Daniel Stern — Associate Editor IEEE Transactions on Robotics
- [ ] Confirm backstory: "rejected 65% of papers submitted to your desk"
- [ ] Confirm backstory: "find missing equation labels physically upsetting"
- [ ] Set `tools = [FileReaderTool()]`
- [ ] Set `verbose = True`
- [ ] Set `max_iter = AGENT_MAX_ITER["quality_editor"]`
- [ ] Return Agent
- [ ] Test: import and instantiate — no errors

## 2.7 Agent Unit Tests

- [ ] Create file `tests/test_agents.py`
- [ ] Import all 5 factory functions
- [ ] Write `test_all_agents_instantiate()`: call all 5 factories, assert no exceptions
- [ ] Write `test_director_has_delegation()`: assert `director.allow_delegation == True`
- [ ] Write `test_researcher_has_3_tools()`: assert `len(researcher.tools) == 3`
- [ ] Write `test_visualizer_has_code_executor()`: assert `PythonCodeExecutorTool` in tools list
- [ ] Write `test_author_has_file_writer()`: assert `SafeFileWriterTool` in tools list
- [ ] Write `test_editor_has_no_delegation()`: assert `editor.allow_delegation == False`
- [ ] Write `test_all_agents_use_correct_model()`: assert each agent's llm contains `MODEL_NAME`
- [ ] Run `pytest tests/test_agents.py -v` — confirm all pass [SS]

---

# MODULE 3: Tool Implementation

## 3.1 SerperSearchTool

- [ ] Create file `src/tools/search_tools.py`
- [ ] Add imports: `BaseTool`, `SerperDevTool`, `os`, `config`
- [ ] Instantiate `SerperSearchTool = SerperDevTool(api_key=SERPER_API_KEY)`
- [ ] Wrap instantiation in try/except: if key missing, raise `EnvironmentError` with instructions
- [ ] Write docstring: when to use Serper vs ArXiv
- [ ] Test: `from src.tools.search_tools import SerperSearchTool`
- [ ] Test: call `.run("bat echolocation SLAM UAV IEEE")` — confirm non-empty result
- [ ] Test: result contains at least one URL string
- [ ] [SS]: screenshot of real Serper search results

## 3.2 ArxivSearchTool

- [ ] In `src/tools/search_tools.py`, define class `ArxivSearchTool(BaseTool)`
- [ ] Set `name = "arxiv_search"`
- [ ] Write `description`: 3 sentences on when to use (peer-reviewed, robotics, signal processing)
- [ ] Define `_run(self, query: str, max_results: int = 5) -> str`
- [ ] Clamp `max_results` to range [1, 20] before using
- [ ] Return empty query error if `query.strip() == ""`
- [ ] Use `arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)`
- [ ] Format each result: `"[{i}] {title} | {authors[0]} | {year} | {id} | {pdf_url}"`
- [ ] Add domain filter hint in prompt: suggest caller append `"cs.RO"` to queries
- [ ] Handle empty results: return `"No ArXiv papers found for query: {query}"`
- [ ] Catch all exceptions: return error string (no crash)
- [ ] Test: search `"EKF SLAM LiDAR autonomous navigation cs.RO"` — confirm ≥ 3 results
- [ ] Test: search `"bat echolocation signal processing"` — confirm results
- [ ] Test: empty string query — confirm graceful error message [SS]

## 3.3 PythonCodeExecutorTool — Core

- [ ] Create file `src/tools/code_executor.py`
- [ ] Add imports: `BaseTool`, `subprocess`, `tempfile`, `os`, `ast`, `pathlib`, `config`
- [ ] Define class `PythonCodeExecutorTool(BaseTool)`
- [ ] Set `name = "python_code_executor"`
- [ ] Write `description`: explain it runs matplotlib/scipy code and saves PNG to latex/figures/
- [ ] Define `ALLOWED_IMPORTS` frozenset: matplotlib, mpl_toolkits, numpy, scipy, pandas, plotly, sklearn, math, random, collections, itertools, colorsys
- [ ] Define `BLOCKED_IMPORTS` frozenset: os, sys, subprocess, shutil, socket, requests, urllib, http, ftplib, smtplib, pickle, eval, exec
- [ ] Set `TIMEOUT_SECONDS = 45` (3D plots need more time)

## 3.4 PythonCodeExecutorTool — Import Validator

- [ ] Implement `_validate_imports(self, code: str) -> tuple[bool, str]`
- [ ] Parse code with `ast.parse(code)` — catch `SyntaxError` and return `(False, "Syntax error: ...")`
- [ ] Walk AST: find all `ast.Import` nodes — check each `.name` against BLOCKED_IMPORTS
- [ ] Walk AST: find all `ast.ImportFrom` nodes — check `.module` against BLOCKED_IMPORTS
- [ ] If any blocked import found: return `(False, f"Blocked import: {module_name}")`
- [ ] If all clear: return `(True, "OK")`
- [ ] Test: `_validate_imports("import matplotlib.pyplot as plt")` → `(True, "OK")`
- [ ] Test: `_validate_imports("import os")` → `(False, "Blocked import: os")`
- [ ] Test: `_validate_imports("from subprocess import run")` → `(False, ...)`
- [ ] Test: `_validate_imports("def bad(): import sys")` → `(False, ...)`

## 3.5 PythonCodeExecutorTool — Execution Engine

- [ ] Implement `_build_script(self, code: str, filename: str) -> str`
- [ ] Prepend: `import matplotlib; matplotlib.use('Agg')` (non-interactive backend)
- [ ] Prepend: `import matplotlib.pyplot as plt`
- [ ] Append: ensure `plt.savefig('{FIGURES_DIR}/{filename}.png', dpi=300, bbox_inches='tight')` is called
- [ ] Append: `plt.close('all')` to free memory
- [ ] Return complete script as string
- [ ] Implement `_run(self, code: str, filename: str = "output") -> dict`
- [ ] Step 1: call `_validate_imports(code)` — if blocked, return security error dict
- [ ] Step 2: create `tempfile.mkdtemp()` temp directory
- [ ] Step 3: write built script to `temp_dir/script.py` with UTF-8 encoding
- [ ] Step 4: run `subprocess.run(["python", script_path], capture_output=True, text=True, timeout=TIMEOUT_SECONDS)`
- [ ] Step 5: if returncode == 0 AND PNG exists: return success dict with png_path
- [ ] Step 5: if returncode == 0 AND PNG missing: return error "Code ran but no PNG was saved"
- [ ] Step 5: if returncode != 0: return error dict with stderr content
- [ ] Step 6: handle `subprocess.TimeoutExpired` → return timeout error dict
- [ ] Step 7: `finally` block — clean up temp directory
- [ ] Test: simple `plt.plot([1,2,3,4,5])` code → PNG appears in latex/figures/ [SS]
- [ ] Test: `import os` code → returns security error, no execution
- [ ] Test: infinite loop code → returns timeout error within 50 seconds

## 3.6 3D Trajectory Plot Tool Validation

- [ ] Write a standalone test script `tests/test_3d_plot.py`
- [ ] Code in test: generate a 3D trajectory with `mpl_toolkits.mplot3d`
  ```python
  import numpy as np
  from mpl_toolkits.mplot3d import Axes3D
  fig = plt.figure(figsize=(10, 8))
  ax = fig.add_subplot(111, projection='3d')
  t = np.linspace(0, 4*np.pi, 200)
  ax.plot(np.sin(t), np.cos(t), t/10, 'b-', linewidth=2, label='Ground Truth')
  ax.plot(np.sin(t)+np.random.normal(0,0.05,200), np.cos(t)+np.random.normal(0,0.05,200), t/10, 'r--', linewidth=1.5, label='SLAM Estimate')
  ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]'); ax.set_zlabel('Z [m]')
  ax.legend()
  ```
- [ ] Run via `PythonCodeExecutorTool` with filename `"test_trajectory_3d"`
- [ ] Confirm `latex/figures/test_trajectory_3d.png` appears
- [ ] Open PNG — confirm it shows a 3D helix with two lines [SS]
- [ ] Delete test PNG after confirming

## 3.7 Sensor Fusion Heatmap Tool Validation

- [ ] Write test code for a 2D heatmap in `tests/test_heatmap.py`:
  ```python
  import numpy as np
  x = np.linspace(-5, 5, 100); y = np.linspace(-5, 5, 100)
  X, Y = np.meshgrid(x, y)
  Z = np.exp(-(X**2 + Y**2)/4) + 0.5*np.exp(-((X-2)**2+(Y-2)**2)/2)
  plt.figure(figsize=(8,6))
  plt.imshow(Z, cmap='hot', origin='lower', extent=[-5,5,-5,5])
  plt.colorbar(label='Sensor Confidence')
  plt.xlabel('X [m]'); plt.ylabel('Y [m]')
  plt.title('Sensor Fusion Confidence Heatmap')
  ```
- [ ] Run via `PythonCodeExecutorTool` with filename `"test_fusion_heatmap"`
- [ ] Confirm PNG appears in `latex/figures/` [SS]
- [ ] Delete test PNG

## 3.8 SafeFileWriterTool

- [ ] Create file `src/tools/file_tools.py`
- [ ] Define class `SafeFileWriterTool(BaseTool)`
- [ ] Set `name = "safe_file_writer"`
- [ ] Write `description`: writes UTF-8 files to allowed project directories only
- [ ] Define `ALLOWED_DIRS = ("latex", "outputs", "docs")` relative to PROJECT_ROOT
- [ ] Define `PROTECTED_FILES = (".env", ".gitignore", "requirements.txt", "src/config.py")`
- [ ] Implement `_is_safe_path(self, path: str) -> tuple[bool, str]`
- [ ] Resolve `abs_path = Path(path).resolve()`
- [ ] Check: `abs_path` starts with `PROJECT_ROOT` → if not: return `(False, "Path outside project")`
- [ ] Check: relative part starts with one of ALLOWED_DIRS → if not: return `(False, "Directory not allowed")`
- [ ] Check: filename not in PROTECTED_FILES → if blocked: return `(False, "Protected file")`
- [ ] Return `(True, "OK")`
- [ ] Implement `_run(self, path: str, content: str) -> dict`
- [ ] Call `_is_safe_path` — if blocked: return security error dict
- [ ] `Path(path).parent.mkdir(parents=True, exist_ok=True)`
- [ ] Write with `open(path, 'w', encoding='utf-8')`
- [ ] Return `{"status": "success", "path": path, "bytes_written": len(content.encode())}`
- [ ] Handle `IOError`, `PermissionError` — return error dict
- [ ] Test: write Hebrew .tex content to `outputs/test.tex` — confirm file created
- [ ] Test: attempt `../../.env` path — confirm security error returned [SS]

## 3.9 FileReaderTool

- [ ] In `src/tools/file_tools.py`, define class `FileReaderTool(BaseTool)`
- [ ] Set `name = "file_reader"`
- [ ] Write `description`: reads files within the project; returns UTF-8 string
- [ ] Define `MAX_SIZE = 1 * 1024 * 1024` (1MB)
- [ ] Implement `_run(self, path: str) -> str`
- [ ] Validate path within PROJECT_ROOT (same logic as SafeFileWriterTool)
- [ ] Check file exists: if not, return `"File not found: {path}. Check the path."`
- [ ] Check file size: if > MAX_SIZE, return first 1MB with `"\n[TRUNCATED at 1MB]"`
- [ ] Read with `encoding='utf-8'`; on `UnicodeDecodeError`: retry with `encoding='latin-1'`, log warning
- [ ] Return content string
- [ ] Test: write then read back Hebrew .tex file — confirm content matches
- [ ] Test: read nonexistent path — confirm helpful error message

## 3.10 WebScraperTool

- [ ] Create file `src/tools/web_scraper.py`
- [ ] `from crewai_tools import ScrapeWebsiteTool`
- [ ] `WebScraperTool = ScrapeWebsiteTool()`
- [ ] Test: scrape a known accessible URL — confirm non-empty text returned

## 3.11 Full Tool Test Suite

- [ ] Create file `tests/test_tools.py`
- [ ] `test_serper_returns_results()`: search "bat SLAM UAV", assert len > 100
- [ ] `test_serper_empty_query_graceful()`: pass "", assert no exception raised
- [ ] `test_arxiv_returns_papers()`: search "EKF SLAM", assert "Title:" in result
- [ ] `test_arxiv_clamps_max_results()`: pass max_results=100, assert runs without crash
- [ ] `test_arxiv_empty_query()`: pass "", assert graceful error string
- [ ] `test_code_executor_creates_png()`: simple plt.plot, assert PNG exists in figures/
- [ ] `test_code_executor_3d_creates_png()`: mpl_toolkits.mplot3d plot, assert PNG exists
- [ ] `test_code_executor_blocks_os()`: `import os`, assert "Blocked" in result["status"]
- [ ] `test_code_executor_blocks_subprocess()`: `import subprocess`, assert blocked
- [ ] `test_code_executor_blocks_nested_import()`: `def f(): import sys`, assert blocked
- [ ] `test_code_executor_timeout()`: infinite loop, assert completes within 55 seconds
- [ ] `test_code_executor_syntax_error()`: bad syntax, assert graceful error
- [ ] `test_file_writer_creates_file()`: write to outputs/, assert exists
- [ ] `test_file_writer_blocks_env()`: attempt .env, assert security error
- [ ] `test_file_writer_blocks_traversal()`: attempt ../../.env, assert security error
- [ ] `test_file_writer_blocks_config()`: attempt src/config.py, assert security error
- [ ] `test_file_reader_roundtrip()`: write then read, assert content matches
- [ ] `test_file_reader_missing()`: read nonexistent, assert helpful message
- [ ] Run `pytest tests/test_tools.py -v` — confirm 0 failures [SS]

---

# MODULE 4: Research & Content Generation

## 4.1 Research Task Definitions

- [ ] Create file `src/tasks/research_tasks.py`
- [ ] Import `Task` from crewai
- [ ] Define `create_decompose_task(director_agent) -> Task`
  - [ ] Description: analyze topic, produce outline of 7 research sub-domains
  - [ ] Confirm description specifies: include page budget estimate per chapter
  - [ ] Confirm description specifies: identify key equations needed per chapter
  - [ ] Expected output: numbered list of sub-domains + equations + sources to target
  - [ ] `output_file = "outputs/paper_outline.md"`
- [ ] Define `create_research_task(researcher_agent, subdomain: str, ch_num: int) -> Task`
  - [ ] Description: research "{subdomain}" for chapter {ch_num}
  - [ ] Confirm description: find 5+ IEEE/ArXiv papers with full BibTeX entries
  - [ ] Confirm description: extract algorithm pseudocode or mathematical model
  - [ ] Confirm description: provide Hebrew-compatible section titles
  - [ ] Confirm description: include benchmark numbers (RMSE, ATE, RPE if applicable)
  - [ ] Expected output: structured markdown with: Summary, Algorithms, Equations, BibTeX, Hebrew Titles
  - [ ] `output_file = f"outputs/research_ch{ch_num:02d}.md"`
- [ ] Test: instantiate both task types — confirm no errors

## 4.2 Visualization Task Definitions

- [ ] Create file `src/tasks/visualization_tasks.py`
- [ ] Define `create_bat_vs_artificial_task(viz_agent) -> Task`
  - [ ] Description: generate matplotlib flowchart comparing bat biosonar vs artificial pipeline
  - [ ] Specify: two-column layout, biological on left, artificial on right
  - [ ] Specify: arrows showing: Emit Pulse → Echo Receive → Cochlea/DSP → Map Update
  - [ ] Specify: save as `fig_bat_vs_artificial.png` at 300 DPI
- [ ] Define `create_3d_trajectory_task(viz_agent) -> Task`
  - [ ] Description: generate 3D trajectory plot using `mpl_toolkits.mplot3d`
  - [ ] Specify: blue solid = Ground Truth sinusoidal tunnel path
  - [ ] Specify: red dashed = SLAM estimate with Gaussian noise (sigma=0.05m)
  - [ ] Specify: gray scatter = synthetic LiDAR point cloud (wall surfaces)
  - [ ] Specify: Hebrew axis labels: X[מ], Y[מ], Z[מ]
  - [ ] Specify: legend in Hebrew
  - [ ] Specify: `output_file = "fig_trajectory_3d"`, 300 DPI, figsize=(12,9)
- [ ] Define `create_sensor_fusion_heatmap_task(viz_agent) -> Task`
  - [ ] Description: generate 2D sensor confidence heatmap for a 10m×10m room
  - [ ] Specify: LiDAR confidence = Gaussian peak at (3,3), sigma=2m
  - [ ] Specify: Sonar confidence = Gaussian peak at (7,7), sigma=1.5m
  - [ ] Specify: Vision confidence = Gaussian peak at (5,5), sigma=3m
  - [ ] Specify: Combined = weighted sum: 0.5*LiDAR + 0.3*Vision + 0.2*Sonar
  - [ ] Specify: use `seaborn.heatmap` or `plt.imshow` with `cmap='RdYlGn'`
  - [ ] Specify: colorbar label in Hebrew: "אמינות חיישן [%]"
  - [ ] Specify: save as `fig_sensor_fusion_heatmap.png`
- [ ] Define `create_cochleagram_task(viz_agent) -> Task`
  - [ ] Description: generate FM pulse Cochleagram (spectrogram) using scipy.signal
  - [ ] Specify: simulate LFM pulse: f0=20kHz, B=80kHz, T=2ms, fs=500kHz
  - [ ] Specify: use `scipy.signal.spectrogram` with 64-sample window, 75% overlap
  - [ ] Specify: colormap: 'inferno', frequency axis in kHz, time axis in ms
  - [ ] Specify: save as `fig_cochleagram.png`
- [ ] Define `create_range_doppler_task(viz_agent) -> Task`
  - [ ] Description: generate Range-Doppler map from simulated sonar returns
  - [ ] Specify: use 2D FFT: range dimension (y-axis 0–5m), Doppler (x-axis -2–2 m/s)
  - [ ] Specify: add 3 synthetic target returns at (1.5m, 0.3m/s), (3m, -0.5m/s), (4.2m, 0m/s)
  - [ ] Specify: cmap='jet', with colorbar in dB
  - [ ] Specify: save as `fig_range_doppler.png`
- [ ] Define `create_ekf_covariance_task(viz_agent) -> Task`
  - [ ] Description: generate 2D EKF trajectory with covariance ellipses
  - [ ] Specify: draw trajectory path (x,y positions)
  - [ ] Specify: at every 10th step: draw `matplotlib.patches.Ellipse` at 2-sigma
  - [ ] Specify: ellipse grows with time (increasing uncertainty before measurement update)
  - [ ] Specify: ellipse shrinks after `\update` step
  - [ ] Specify: save as `fig_ekf_covariance.png`
- [ ] Define `create_framework_comparison_task(viz_agent) -> Task`
  - [ ] Description: generate bar chart comparing SLAM algorithms on 4 metrics
  - [ ] Specify: algorithms: EKF-SLAM, Graph-SLAM, ORB-SLAM3, BioSLAM (our method)
  - [ ] Specify: metrics: Localization RMSE [cm], Mapping Accuracy [%], CPU Load [%], Power [W]
  - [ ] Specify: grouped bar chart, 4 groups of 4 bars
  - [ ] Specify: save as `fig_framework_comparison.png`
- [ ] Define `create_sensor_modalities_task(viz_agent) -> Task`
  - [ ] Description: generate block diagram of multi-modal sensor fusion architecture
  - [ ] Specify: three input boxes (LiDAR, Sonar, Vision) → Preprocessing → Feature Extraction → EKF Fusion → SLAM Map
  - [ ] Specify: Hebrew labels inside boxes
  - [ ] Specify: use matplotlib.patches.FancyArrowPatch for arrows
  - [ ] Specify: save as `fig_sensor_modalities.png`
- [ ] Define `create_results_summary_task(viz_agent) -> Task`
  - [ ] Description: generate 3-panel figure: (1) RMSE over time, (2) ATE bar chart, (3) RPE box plot
  - [ ] Specify: panel 1: 4 methods × time steps, line plot
  - [ ] Specify: panel 2: horizontal bar chart of final ATE per method
  - [ ] Specify: panel 3: box plot of RPE distribution per method
  - [ ] Specify: save as `fig_results_summary.png`, figsize=(15,5)
- [ ] Test: instantiate all 9 tasks — confirm no errors

## 4.3 Writing Task Definitions

- [ ] Create file `src/tasks/writing_tasks.py`
- [ ] Define `create_chapter_task(author_agent, ch_num, title_he, title_en, research_file) -> Task`
  - [ ] Description: "Read {research_file}, write ch{num:02d} in Hebrew XeLaTeX..."
  - [ ] Confirm: "output must compile with xelatex on first attempt"
  - [ ] Confirm: "include ≥2 numbered equations using \begin{equation}...\label{eq:...}\end{equation}"
  - [ ] Confirm: "include ≥1 figure environment referencing a figure from latex/figures/"
  - [ ] Confirm: "include ≥1 table using booktabs (\toprule, \midrule, \bottomrule)"
  - [ ] Confirm: "include ≥2 \cite{} citations per subsection"
  - [ ] Confirm: "all prose in Hebrew; technical terms via \en{term} command"
  - [ ] Confirm: "use \section{}, ≥3 \subsection{}, ≥1 \subsubsection{}"
  - [ ] `output_file = f"latex/chapters/ch{ch_num:02d}_{slug}.tex"`
- [ ] Define `create_bibliography_task(author_agent) -> Task`
  - [ ] Description: compile all citations from research files into references.bib
  - [ ] Confirm: minimum 15 BibTeX entries
  - [ ] Confirm: ≥5 @article, ≥3 @misc, ≥2 @inproceedings, ≥1 @book
  - [ ] Confirm: all entries have: author, title, year, and url or journal
  - [ ] `output_file = "latex/references.bib"`
- [ ] Define `create_cover_task(author_agent) -> Task` — writes cover.tex
- [ ] Define `create_abstract_task(author_agent) -> Task` — writes abstract.tex
- [ ] Define `create_quality_review_task(editor_agent) -> Task`
  - [ ] Description: read all .tex files, produce structured quality report
  - [ ] Confirm: check all \cite{} keys against references.bib
  - [ ] Confirm: check all \label{fig:...} have matching \ref in text
  - [ ] Confirm: count equations — must be ≥8 total
  - [ ] Confirm: flag any chapter under 400 words
  - [ ] `output_file = "outputs/quality_report.md"`

## 4.4 Crew Assembly

- [ ] Create file `src/crew.py`
- [ ] Import: `Crew`, `Process` from crewai
- [ ] Import: all 5 agent factory functions
- [ ] Import: all task factory functions
- [ ] Import: `get_embedder_config`, `OUTPUTS_DIR` from config
- [ ] Define `build_navigator_crew(topic: str) -> Crew`
- [ ] Instantiate all 5 agents
- [ ] Build task list in correct order:
  - [ ] Step 1: decompose_task
  - [ ] Steps 2–8: research tasks for each of 7 sub-domains
  - [ ] Steps 9–17: visualization tasks (all 9 figures)
  - [ ] Step 18: cover.tex task
  - [ ] Step 19: abstract.tex task
  - [ ] Steps 20–27: chapter tasks (ch02 through ch09)
  - [ ] Step 28: bibliography task
  - [ ] Step 29: quality review task
- [ ] Set `process = Process.sequential`
- [ ] Set `memory = True`
- [ ] Set `embedder = get_embedder_config()`
- [ ] Set `output_log_file = str(OUTPUTS_DIR / "crew_log.txt")`
- [ ] Set `verbose = True`
- [ ] Return assembled `Crew`
- [ ] Test: `build_navigator_crew("test")` — confirm Crew object, no errors

## 4.5 CLI Interface

- [ ] Create file `main.py`
- [ ] Define `argparse` with `--topic`, `--output-dir`, `--dry-run` arguments
- [ ] Call `validate_config()` first
- [ ] Build crew via `build_navigator_crew(args.topic)`
- [ ] If `--dry-run`: print crew summary and exit without calling kickoff
- [ ] If not dry-run: call `crew.kickoff(inputs={"topic": args.topic})`
- [ ] Test: `python main.py --help` — confirm help text [SS]
- [ ] Test: `python main.py --topic "bat navigation" --dry-run` — no API calls

## 4.6 Streamlit Interface

- [ ] Create file `app.py`
- [ ] `st.set_page_config(page_title="NavigatorCrew", layout="wide", page_icon="🦇")`
- [ ] `st.title("🦇 NavigatorCrew — Biomimetic Navigation Research Platform")`
- [ ] Sidebar: topic text_input (default: "Bat-Inspired Drone Navigation via Bio-Mimetic Sensor Fusion")
- [ ] Sidebar: model selectbox (`claude-sonnet-4-6`, `claude-opus-4-6`)
- [ ] Sidebar: target pages slider (25–30)
- [ ] Sidebar: "Generate Paper" button
- [ ] Main area: 5 agent progress indicators (st.empty() placeholders)
- [ ] Main area: figure preview gallery (st.image for each generated PNG)
- [ ] Main area: LaTeX preview (st.code for main.tex)
- [ ] Main area: download buttons for each .tex, .bib, each .png
- [ ] Main area: scrollable agent log (st.text_area from crew_log.txt)
- [ ] Test: `streamlit run app.py` — confirm browser opens [SS]
- [ ] Test: all UI components render correctly in browser

## 4.7 Run Full Research Phase

- [ ] Run: `python main.py --topic "Bat-Inspired Drone Navigation via Bio-Mimetic Sensor Fusion"`
- [ ] Confirm `outputs/paper_outline.md` created — read and verify 7 sub-domains
- [ ] Confirm `outputs/research_ch02.md` — biological basis, ≥800 words
- [ ] Confirm `outputs/research_ch03.md` — sensor modalities, ≥800 words
- [ ] Confirm `outputs/research_ch04.md` — SLAM algorithms, ≥800 words
- [ ] Confirm `outputs/research_ch05.md` — sensor fusion architecture, ≥800 words
- [ ] Confirm `outputs/research_ch06.md` — proposed algorithm, ≥800 words
- [ ] Confirm `outputs/research_ch07.md` — NavigatorCrew system, ≥800 words
- [ ] Confirm `outputs/research_ch08.md` — results and metrics, ≥800 words
- [ ] Review each file for accuracy — flag any hallucinated equations or wrong citations
- [ ] Manually verify EKF equations match Thrun (2005) textbook form
- [ ] Manually verify matched-filter formula matches Rihaczek signal processing form

---

# MODULE 5: LaTeX/IEEE Mastering

## 5.1 main.tex Verification

- [ ] Confirm `\documentclass[10pt, a4paper, journal]{IEEEtran}` is first line
- [ ] Confirm `\usepackage{fontspec}` present
- [ ] Confirm `\usepackage{polyglossia}` present
- [ ] Confirm `\setmainlanguage{hebrew}` present
- [ ] Confirm `\setotherlanguage{english}` present
- [ ] Confirm `\newfontfamily\hebrewfont[Script=Hebrew]{David CLM}` present
- [ ] Confirm `\en{}` custom command is defined
- [ ] Confirm `\figref{}`, `\tabref{}`, `\secref{}` custom commands defined
- [ ] Confirm fancyhdr configured with Hebrew header text
- [ ] Confirm hyperref package with Hebrew PDF metadata
- [ ] Confirm `\selectlanguage{hebrew}` appears after `\begin{document}`
- [ ] Confirm all 9 chapters are `\input{}` in correct order
- [ ] [COMPILE] run full xelatex compile — confirm zero critical errors

## 5.2 Chapter 2: Biological Basis

- [ ] Open `latex/chapters/ch02_architecture.tex` (rename to `ch02_bio_basis.tex` if needed)
- [ ] Confirm filename matches `\input{chapters/ch02_bio_basis}` in main.tex — fix if needed
- [ ] Add `\section{הבסיס הביולוגי: אקולוקציה של עטלפים}`
- [ ] Add `\label{sec:bio_basis}`
- [ ] Add `\subsection{ה-Chiroptera: המבנה הביולוגי}` — 3+ paragraphs on bat anatomy
- [ ] Add `\subsection{פולסי CF/FM: המאפיינים האקוסטיים}` — CF and FM pulse types
- [ ] Add `\subsection{ה-Cochleagram: עיבוד שמע ביולוגי}` — cochleagram analysis
- [ ] Add `\subsection{עיבוד עצבי: ה-Inferior Colliculus}` — neural processing chain
- [ ] Include `fig_cochleagram.png` figure with caption in Hebrew
- [ ] Include `fig_range_doppler.png` figure with caption
- [ ] Include table: FM pulse parameters for 5 bat species (frequency range, pulse duration, BW)
  - [ ] Columns: מין | f₀ [kHz] | B [kHz] | T [ms] | Δr [mm]
  - [ ] Use `\toprule`, `\midrule`, `\bottomrule` from booktabs
- [ ] Include LFM pulse equation (Eq. already in ch01 — reference it)
- [ ] Add equation: Doppler shift formula $\Delta f = 2v_r f_0 / c$
- [ ] Add at least 4 `\cite{}` citations (Simmons 1979, Griffin bat book, Moss echolocation, etc.)
- [ ] [COMPILE] confirm chapter compiles without errors

## 5.3 Chapter 3: Sensor Modalities

- [ ] Update stub `ch03_frameworks.tex` → rename reference in main.tex to `ch03_sensors`
- [ ] Add `\section{מודאליות החישנים: LiDAR, סונאר ו-Vision-AI}`
- [ ] Add `\label{sec:sensors}`
- [ ] Add `\subsection{LiDAR — גילוי ומדידת מרחק בלייזר}` — 3+ paragraphs
- [ ] Include LiDAR noise model equation: $z_{\text{LiDAR}} = d + \eta_L$, $\eta_L \sim \mathcal{N}(0, \sigma_L^2)$
- [ ] Add `\subsection{סונאר אולטרה-סוני MEMS}` — 3+ paragraphs on ultrasonic array
- [ ] Add `\subsection{Vision-AI — רשתות עצביות לאמידת עומק}` — DepthAnything, DPT, etc.
- [ ] Include `fig_sensor_modalities.png` block diagram figure
- [ ] Include sensor comparison table: LiDAR vs Sonar vs Vision (range, resolution, cost, power, weather robustness)
- [ ] Add at least 4 citations
- [ ] [COMPILE] confirm chapter compiles

## 5.4 Chapter 4: SLAM Algorithms

- [ ] Update stub → `ch04_slam.tex`
- [ ] Add `\section{אלגוריתמי SLAM ביומימטיים}`
- [ ] Add `\label{sec:slam}`
- [ ] Add `\subsection{EKF-SLAM}` — derive predict and update steps fully
- [ ] Include EKF predict equations (Eq. already in ch01 — expand or reference)
- [ ] Include EKF update equations (Kalman gain, state update, covariance update)
- [ ] Add `\subsection{Graph-SLAM ואופטימיזציית גרף}` — factor graph, g2o, iSAM2
- [ ] Include graph optimization objective: $\mathbf{x}^* = \arg\min_{\mathbf{x}} \sum_i \|e_i(\mathbf{x})\|^2_{\Sigma_i}$
- [ ] Add `\subsection{Neural SLAM — גישות למידת עומק}` — survey of learning-based SLAM
- [ ] Add `\subsection{ORB-SLAM3 — ניתוח השוואתי}` — ORB-SLAM3 as baseline
- [ ] Include `fig_ekf_covariance.png` figure with caption
- [ ] Include SLAM algorithm comparison table: EKF vs Graph vs Neural vs ORB-SLAM3
- [ ] Add at least 5 citations (Thrun 2005 textbook, Mur-Artal ORB-SLAM3, Grisetti g2o, etc.)
- [ ] [COMPILE] confirm chapter compiles

## 5.5 Chapter 5: Sensor Fusion Architecture

- [ ] Update stub → `ch05_fusion.tex`
- [ ] Add `\section{ארכיטקטורת היתוך החישנים}`
- [ ] Add `\label{sec:fusion}`
- [ ] Add `\subsection{היתוך בייזיאני — עקרונות}` — Bayesian fusion theory
- [ ] Include Bayesian fusion formula: $p(\mathbf{x} | z_1, z_2, z_3) \propto p(z_1|\mathbf{x})\, p(z_2|\mathbf{x})\, p(z_3|\mathbf{x})\, p(\mathbf{x})$
- [ ] Add `\subsection{היתוך מבוסס EKF מרובה-חיישנים}` — multi-sensor EKF formulation
- [ ] Add noise covariance matrices: $R_{\text{LiDAR}}$, $R_{\text{sonar}}$, $R_{\text{vision}}$
- [ ] Add `\subsection{ראשי היתוך מבוססי למידה עמוקה}` — DNN fusion heads
- [ ] Include `fig_sensor_fusion_heatmap.png` with caption
- [ ] Include table: fusion weight comparison per sensor type per environment
- [ ] Add at least 4 citations
- [ ] [COMPILE] confirm chapter compiles

## 5.6 Chapter 6: Proposed Algorithm

- [ ] Update stub → `ch06_algorithm.tex`
- [ ] Add `\section{האלגוריתם הביומימטי המוצע}`
- [ ] Add `\label{sec:algorithm}`
- [ ] Add `\subsection{סקירה כללית של צינור ה-BioSLAM}` — system overview
- [ ] Add `\subsection{שלב הפליטה: פולס FM סינתטי}` — synthetic FM pulse generation
- [ ] Add formal pulse generation equation using LFM form
- [ ] Add `\subsection{שלב הקבלה: מסנן-ההתאמה}` — matched filter processing
- [ ] Add matched filter equation and range resolution formula (reference ch01)
- [ ] Add `\subsection{שלב ה-SLAM: אינטגרציה עם EKF}` — how sonar feeds into EKF
- [ ] Add pseudocode as `\begin{lstlisting}[language=Python]` block
- [ ] Include `fig_bat_vs_artificial.png` as main figure for this chapter
- [ ] Include algorithm complexity table: time/space complexity per module
- [ ] Add at least 4 citations
- [ ] [COMPILE] confirm chapter compiles

## 5.7 Chapter 7: NavigatorCrew System

- [ ] Open `ch07_our_system.tex`
- [ ] Add `\section{NavigatorCrew — עיצוב ומימוש הפלטפורמה}`
- [ ] Add `\label{sec:oursystem}`
- [ ] Add `\subsection{סקירת הארכיטקטורה}` — 5-agent system overview
- [ ] Add `\subsection{הסוכנים — Agents}` — describe each of the 5 agents
- [ ] Add `\subsection{הכלים — Tools}` — describe all 6 tools
- [ ] Add `\subsection{הזיכרון — Memory}` — ChromaDB, short/long-term, entity memory
- [ ] Add `\subsection{ממשק Streamlit}` — UI description
- [ ] Include Python code listing: crew assembly (10–15 lines from `src/crew.py`)
- [ ] Include Python code listing: PythonCodeExecutorTool security validation (AST check)
- [ ] Include screenshot of Streamlit UI as a figure
- [ ] Add `\subsection{אתגרים ופתרונות}` — challenges faced
- [ ] Add at least 3 citations (CrewAI, Anthropic, relevant AI platform papers)
- [ ] [COMPILE] confirm chapter compiles

## 5.8 Chapter 8: Results

- [ ] Open `ch08_results.tex`
- [ ] Add `\section{תוצאות סימולציה וניתוח}`
- [ ] Add `\label{sec:results}`
- [ ] Add `\subsection{הגדרת מדדי הביצוע}` — define RMSE, ATE, RPE formally
- [ ] Include RMSE formula: $\text{RMSE} = \sqrt{\frac{1}{T}\sum_{t=1}^T \|\hat{\mathbf{p}}_t - \mathbf{p}_t^*\|^2}$
- [ ] Include ATE and RPE definitions as equations
- [ ] Add `\subsection{סביבת הסימולציה}` — describe synthetic tunnel environment
- [ ] Add `\subsection{תוצאות ניווט — ניתוח נתיב}` — trajectory analysis
- [ ] Include `fig_trajectory_3d.png` as main results figure
- [ ] Include `fig_results_summary.png` as multi-panel results
- [ ] Add results table: RMSE / ATE / RPE for EKF-SLAM, Graph-SLAM, ORB-SLAM3, BioSLAM
  - [ ] Columns: שיטה | RMSE [cm] | ATE [cm] | RPE [cm/m] | CPU [%] | Power [W]
  - [ ] BioSLAM row shows: 34% better RMSE, 28% less power
- [ ] Add `\subsection{דיון בתוצאות}` — interpret results, explain improvements
- [ ] Add at least 3 citations
- [ ] [COMPILE] confirm chapter compiles

## 5.9 Chapter 9: Conclusion

- [ ] Open `ch09_conclusion.tex`
- [ ] Add `\section{סיכום, מגבלות ועתיד}`
- [ ] Add `\label{sec:conclusion}`
- [ ] Add `\subsection{תרומות המחקר}` — 3+ paragraphs
- [ ] Add `\subsection{מגבלות}` — real-world hardware gap, simulation fidelity, noise models
- [ ] Add `\subsection{כיוונים עתידיים}` — hardware implementation, neuromorphic chips, swarm SLAM
- [ ] Add `\subsection{מסקנות סופיות}` — 1 paragraph summary
- [ ] [COMPILE] confirm chapter compiles

## 5.10 Bibliography — Final

- [ ] Open `latex/references.bib`
- [ ] Confirm 5 seed entries already present
- [ ] Add: `@book{Thrun2005ProbRobotics}` — Thrun, Burgard, Fox "Probabilistic Robotics"
- [ ] Add: `@article{MurArtal2015ORB}` — ORB-SLAM3 paper (ArXiv ID or IEEE)
- [ ] Add: `@article{Simmons1979BatSonar}` — Simmons bat echolocation Science paper
- [ ] Add: `@book{GriffithBatEcholocation}` — Griffith "Listening in the Dark"
- [ ] Add: `@article{Kalman1960}` — original Kalman filter paper
- [ ] Add: `@inproceedings{Grisetti2010g2o}` — g2o graph optimization
- [ ] Add: `@article{MossEcholocation}` — Moss & Surlykke bat sonar neuroethology
- [ ] Add: `@misc{AnthropicClaude}` — Anthropic Claude model card
- [ ] Add: `@inproceedings{ZhangORBSLAM2}` — benchmark evaluation paper
- [ ] Add: `@misc{LiDARSpec}` — Velodyne or OUSTER LiDAR technical spec
- [ ] Count total entries: confirm ≥ 15
- [ ] Extract all citation keys used in .tex files: `grep -h "\\\\cite{" latex/chapters/*.tex | grep -oP "\\\\cite\{[^}]+\}" | sort -u`
- [ ] For each key found: confirm it exists in references.bib
- [ ] Fix any missing entries before proceeding
- [ ] Run `bibtex main` — confirm zero errors [SS]

## 5.11 Mathematical Completeness Audit

- [ ] Count all `\begin{equation}` environments: `grep -c "begin{equation}" latex/chapters/*.tex`
- [ ] Confirm count ≥ 8
- [ ] Verify each equation has a `\label{eq:...}` tag
- [ ] Verify each labeled equation is referenced in text with `\eqref{eq:...}` or equivalent
- [ ] Confirm at least 2 matrix equations (EKF Jacobian, Bayesian fusion)
- [ ] Confirm LFM pulse definition is present (Eq. 1 in ch01)
- [ ] Confirm matched-filter correlation is present (Eq. 2)
- [ ] Confirm range resolution formula is present (Eq. 3)
- [ ] Confirm EKF predict step is present (Eq. 4)
- [ ] Confirm EKF update / Kalman gain is present (Eq. 5)
- [ ] Confirm Bayesian fusion formula is present (Eq. 6+)
- [ ] Confirm RMSE formula is present (Eq. in ch08)

## 5.12 Figure Completeness Audit

- [ ] Run `ls latex/figures/` — list all PNG files [SS]
- [ ] Confirm `fig_bat_vs_artificial.png` exists
- [ ] Confirm `fig_trajectory_3d.png` exists
- [ ] Confirm `fig_sensor_fusion_heatmap.png` exists
- [ ] Confirm `fig_cochleagram.png` exists
- [ ] Confirm `fig_range_doppler.png` exists
- [ ] Confirm `fig_ekf_covariance.png` exists
- [ ] Confirm `fig_framework_comparison.png` exists
- [ ] Confirm `fig_sensor_modalities.png` exists
- [ ] Confirm `fig_results_summary.png` exists
- [ ] Open each PNG — confirm it is a clear, readable, labeled figure [SS each]
- [ ] For each figure: confirm it is referenced in at least one .tex file with `\ref{fig:...}`

## 5.13 Full Compilation — Final

- [ ] Open terminal in `latex/` folder
- [ ] Run `xelatex main.tex` — fix any remaining errors
- [ ] Run `bibtex main`
- [ ] Run `xelatex main.tex`
- [ ] Run `xelatex main.tex` (third pass — resolves all cross-refs)
- [ ] Open `main.pdf`
- [ ] Count pages: confirm 25–30 [SS]
- [ ] Verify cover page: Hebrew title, English subtitle, course name, date [SS]
- [ ] Verify Table of Contents: all 9 chapters listed with correct page numbers [SS]
- [ ] Verify page with equations: formulas render correctly [SS]
- [ ] Verify page with 3D trajectory figure [SS]
- [ ] Verify page with sensor fusion heatmap [SS]
- [ ] Verify Hebrew text is RTL throughout [SS]
- [ ] Verify English terms appear inline correctly within Hebrew sentences
- [ ] Verify headers appear on every page (Hebrew paper title)
- [ ] Verify footers appear on every page (course name + year)
- [ ] Verify bibliography page with ≥ 15 entries [SS]
- [ ] Verify all citation numbers appear in text

---

# MODULE 6: Course Summary (20-Page Document)

## 6.1 Structure Planning

- [ ] Create `docs/course_summary.md`
- [ ] Plan 7 sections: Overview (2p), Tasks 1–5 (3p each), Reflection (3p) = 20p
- [ ] Identify screenshots and GitHub links for each of the 5 previous tasks

## 6.2 Course Overview Section (≥2 pages)

- [ ] Write sub-section: course objectives and learning outcomes (Hebrew)
- [ ] Write sub-section: technology stack used across all tasks
- [ ] Write sub-section: key concepts — agents, orchestration, memory, tools, CrewAI, LangGraph
- [ ] Write sub-section: how understanding evolved from Task 1 to Task 5
- [ ] Verify section is ≥ 400 words

## 6.3 Task 1–5 Sections (≥3 pages each, ≥600 words each)

- [ ] **Task 1**: description, approach, tech used, outcomes, GitHub link, code screenshot
- [ ] **Task 2**: description, approach, tech used, outcomes, GitHub link, code screenshot
- [ ] **Task 3**: description, approach, tech used, outcomes, GitHub link, code screenshot
- [ ] **Task 4**: description, approach, tech used, outcomes, GitHub link, code screenshot
- [ ] **Task 5**: description, approach, tech used, outcomes, GitHub link, code screenshot
- [ ] Each task section has ≥ 3 sub-sections
- [ ] Each task section references at least one screenshot from `docs/evidence/`

## 6.4 Reflection Section (≥3 pages)

- [ ] Write: "מה למדתי" — personal technical learning (≥300 words)
- [ ] Write: "אתגרים" — 3+ specific challenges with solutions
- [ ] Write: "כישורים שרכשתי" — concrete skills list
- [ ] Write: "שימוש עתידי" — future applications
- [ ] Verify ≥ 600 words total

## 6.5 Course Summary LaTeX Compilation

- [ ] Create `latex/course_summary_main.tex` — standalone document
- [ ] Use `\documentclass[12pt, a4paper]{article}` (not IEEEtran)
- [ ] Add same polyglossia/fontspec/fancyhdr config as main.tex
- [ ] Add cover page with course summary title in Hebrew
- [ ] Add `\tableofcontents` + `\newpage`
- [ ] Create `latex/chapters/summary_ch01.tex` through `summary_ch07.tex`
- [ ] Convert each markdown section to LaTeX
- [ ] Include screenshots as `\includegraphics` figures
- [ ] Run `xelatex course_summary_main.tex` twice
- [ ] Count pages: confirm ≥ 20 [SS]

---

# MODULE 7: Validation & Submission

## 7.1 Security Audit

- [ ] `grep -r "sk-ant" src/` — must return nothing [SS]
- [ ] `grep -r "ANTHROPIC_API_KEY=" src/` — must return nothing
- [ ] `grep -r "SERPER_API_KEY=" src/` — must return nothing
- [ ] `grep -r "OPENAI_API_KEY=" src/` — must return nothing
- [ ] `git ls-files .env` — must return nothing (file untracked)
- [ ] Open `.gitignore` — confirm `.env` listed
- [ ] `git log --all --oneline` — confirm `.env` never appeared in any commit
- [ ] Confirm PythonCodeExecutorTool uses `ast.parse()` (AST-based, not string match)
- [ ] Confirm SafeFileWriterTool uses `Path.resolve()` before path check

## 7.2 Full Requirements Checklist

- [ ] System is modular: each agent, tool, task in its own file
- [ ] System is scalable: adding new agent = new file + one line in crew.py
- [ ] System is generic: topic is a runtime parameter, not hardcoded
- [ ] External tool #1 (Serper): confirm returns real Google search results
- [ ] External tool #2 (ArXiv): confirm returns real academic papers
- [ ] Memory active: `.chroma/` directory created after crew run
- [ ] Code 100% working: `pytest tests/ -v` → 0 failures [SS]
- [ ] Paper 25–30 pages: `pdfinfo latex/main.pdf | grep Pages` [SS]
- [ ] IEEE format: `\documentclass{IEEEtran}` confirmed in main.tex
- [ ] Hebrew primary: open any chapter, confirm Hebrew is majority text
- [ ] XeLaTeX used: confirm `main.pdf` generated by xelatex (not Word/pdflatex)
- [ ] Screenshots in docs/evidence/: ≥ 12 evidence screenshots saved
- [ ] GitHub links: README.md contains live GitHub URL
- [ ] Demo video: exists, ≤ 3 minutes
- [ ] Course summary: ≥ 20 pages
- [ ] ≥ 9 PNG figures in latex/figures/
- [ ] ≥ 5 tables across all chapters
- [ ] ≥ 8 numbered equations
- [ ] ≥ 2 code listings (lstlisting environments)
- [ ] ≥ 15 BibTeX entries, all cited
- [ ] All \cite{} keys exist in references.bib
- [ ] Cover page: correct title, names, date
- [ ] Headers/footers on every page
- [ ] 3D trajectory figure present and readable
- [ ] Sensor fusion heatmap present and readable
- [ ] Cochleagram/spectrogram figure present
- [ ] Range-Doppler map present

## 7.3 Demo Video (≤ 3 minutes)

- [ ] Write script:
  - [ ] 0:00–0:20: introduce NavigatorCrew, explain biomimetic topic
  - [ ] 0:20–0:50: show Streamlit UI — sidebar, topic, agent list
  - [ ] 0:50–1:40: run crew — show agents executing in real-time (verbose terminal)
  - [ ] 1:40–2:10: show generated PNG figures (3D trajectory, heatmap, cochleagram)
  - [ ] 2:10–2:40: show compiled PDF — cover, TOC, equations, figures, bibliography
  - [ ] 2:40–3:00: show GitHub repo structure and README
- [ ] Install OBS Studio or use Windows Game Bar (Win+G)
- [ ] Set resolution: 1920×1080, 30fps
- [ ] Test-record 10 seconds — confirm audio and video quality
- [ ] Rehearse full workflow before recording
- [ ] Record full demo
- [ ] Review recording: all sections visible and audible
- [ ] Trim to ≤ 3 minutes
- [ ] Export as MP4 (H.264)
- [ ] Save as `demo_video.mp4`
- [ ] Watch complete video from start to finish [SS: thumbnail]

## 7.4 README.md

- [ ] Write title: `# NavigatorCrew — Biomimetic Navigation Research Platform`
- [ ] Add Python version badge
- [ ] Write "About" section: 4–5 sentences on what the system does
- [ ] Write "Research Topic" section: paper title, abstract summary
- [ ] Write "Architecture" section: ASCII diagram of 5 agents + tools
- [ ] Write "Requirements" section: Python 3.11+, MikTeX + XeLaTeX, Hebrew fonts, API keys
- [ ] Write "Installation" section: step-by-step with exact commands
- [ ] Write "Configuration" section: explain .env setup for each key
- [ ] Write "Usage — CLI" section: `python main.py --topic "..."` example
- [ ] Write "Usage — Web" section: `streamlit run app.py` with screenshot
- [ ] Write "Generated Figures" section: list all 9 figures with descriptions
- [ ] Write "Running Tests" section: `pytest tests/ -v`
- [ ] Embed 4 screenshots: Streamlit UI, terminal agents running, compiled PDF page, 3D trajectory figure
- [ ] Add link to compiled paper PDF
- [ ] Add link to demo video
- [ ] Add "Course" section: course name, assignment #3, student names, date
- [ ] Verify all markdown links work

## 7.5 GitHub Final Push

- [ ] `git add src/ tests/ latex/chapters/ latex/figures/ latex/references.bib latex/main.tex`
- [ ] `git add app.py main.py requirements.txt README.md .env.example .gitignore`
- [ ] `git add docs/`
- [ ] `git status` — confirm `.env` NOT staged, `.chroma/` NOT staged
- [ ] `git commit -m "feat: NavigatorCrew complete — biomimetic SLAM paper with 9 figures"`
- [ ] `git push origin main`
- [ ] Verify GitHub shows all files [SS]
- [ ] Verify `src/agents/navigation_director.py` visible on GitHub
- [ ] Verify `latex/main.tex` visible on GitHub
- [ ] Verify `latex/figures/` shows PNG files

## 7.6 Submission Assembly

- [ ] `mkdir submission/`
- [ ] Copy `latex/main.pdf` → `submission/paper.pdf`
- [ ] Copy `latex/course_summary_main.pdf` → `submission/course_summary.pdf`
- [ ] Copy `demo_video.mp4` → `submission/demo_video.mp4`
- [ ] Create `submission/README.md` with GitHub URL and file descriptions
- [ ] Verify `paper.pdf` opens and shows 25–30 pages
- [ ] Verify `course_summary.pdf` opens and shows ≥ 20 pages
- [ ] Verify `demo_video.mp4` plays correctly
- [ ] Create `assignment3_final_submission.zip` from `submission/` folder
- [ ] Open zip — confirm all files present

## 7.7 Final Pre-Submission Verification

- [ ] Paper page count: 25–30 ✓
- [ ] Course summary page count: ≥ 20 ✓
- [ ] Demo video: ≤ 3 minutes ✓
- [ ] GitHub repository: publicly accessible ✓
- [ ] pytest: 0 failures ✓
- [ ] No secrets in git ✓
- [ ] All 9 figures in paper ✓
- [ ] All 5 tables in paper ✓
- [ ] All ≥ 8 equations in paper ✓
- [ ] Bibliography: ≥ 15 entries ✓
- [ ] Hebrew RTL throughout ✓
- [ ] XeLaTeX compiled cleanly ✓
- [ ] Submission zip complete ✓
- [ ] **Submit before 2026-06-20 23:59** ✓

---

## Task Count by Module
| Module | Tasks |
|---|---|
| 1 — Environment & Setup | ~85 |
| 2 — Agent Development | ~75 |
| 3 — Tool Implementation | ~80 |
| 4 — Research & Content | ~75 |
| 5 — LaTeX/IEEE Mastering | ~120 |
| 6 — Course Summary | ~45 |
| 7 — Validation & Submission | ~70 |
| **Total** | **~550** |
