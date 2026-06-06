# TODO.md — Assignment 3: ResearchCrew
## Hyper-Granular Micro-Task Checklist | Deadline: 2026-06-20
## Target: 500-800 atomic tasks across 7 modules

> **Rule**: Every checkbox is ONE atomic action. Never check a box until that exact action is complete.
> **Evidence**: Items marked [SCREENSHOT] require a screenshot saved to `docs/evidence/`.

---

# MODULE 1: Environment & Setup
## 1.1 Operating System & Base Tools

- [ ] Open Windows Terminal or WSL2 terminal
- [ ] Run `python --version` and confirm output is Python 3.11 or higher
- [ ] If Python < 3.11: download Python 3.11 installer from python.org
- [ ] If Python < 3.11: run the installer with "Add to PATH" checked
- [ ] If Python < 3.11: restart terminal and confirm `python --version` shows 3.11+
- [ ] Run `git --version` and confirm Git is installed
- [ ] If Git missing: download Git from git-scm.com and install
- [ ] Run `pip --version` and confirm pip is accessible
- [ ] Run `pip install --upgrade pip` to update pip to latest
- [ ] Confirm pip version is 24.0 or higher

## 1.2 MikTeX Installation

- [ ] Open browser and navigate to miktex.org/download
- [ ] Download the MikTeX installer for Windows (64-bit)
- [ ] Run the installer as Administrator
- [ ] Select "Install for all users" option
- [ ] Select installation directory (default is fine)
- [ ] Check "Install missing packages on-the-fly: Yes" option
- [ ] Complete MikTeX installation
- [ ] Open MikTeX Console from Start Menu
- [ ] Click "Check for updates" and install all available updates
- [ ] Open MikTeX Package Manager (from MikTeX Console)
- [ ] Search for and install package: `IEEEtran`
- [ ] Search for and install package: `babel-hebrew`
- [ ] Search for and install package: `polyglossia`
- [ ] Search for and install package: `fontenc`
- [ ] Search for and install package: `inputenc`
- [ ] Search for and install package: `booktabs`
- [ ] Search for and install package: `fancyhdr`
- [ ] Search for and install package: `hyperref`
- [ ] Search for and install package: `amsmath`
- [ ] Search for and install package: `amssymb`
- [ ] Search for and install package: `graphicx`
- [ ] Search for and install package: `listings`
- [ ] Search for and install package: `xcolor`
- [ ] Search for and install package: `geometry`
- [ ] Search for and install package: `biblatex` (or confirm natbib is available)
- [ ] Search for and install package: `caption`
- [ ] Search for and install package: `subcaption`
- [ ] Search for and install package: `float`
- [ ] Open a command prompt and run `pdflatex --version` to confirm MikTeX is in PATH
- [ ] Run `bibtex --version` to confirm BibTeX is accessible [SCREENSHOT]

## 1.3 VS Code Setup

- [ ] Install VS Code if not already installed (code.visualstudio.com)
- [ ] Open VS Code
- [ ] Install extension: "LaTeX Workshop" by James Yu
- [ ] Install extension: "Python" by Microsoft
- [ ] Install extension: "GitLens" (optional but helpful)
- [ ] Open VS Code Settings (Ctrl+,)
- [ ] Set `latex-workshop.latex.tools` to use pdflatex as the default tool
- [ ] Set `latex-workshop.view.pdf.viewer` to "tab"
- [ ] Confirm LaTeX Workshop can compile a minimal .tex file

## 1.4 GitHub Repository

- [ ] Log in to github.com
- [ ] Click "New repository"
- [ ] Set repository name: `assignment3-researchcrew`
- [ ] Set visibility: Public
- [ ] Check "Add a README file"
- [ ] Select .gitignore template: Python
- [ ] Click "Create repository"
- [ ] Copy the HTTPS clone URL
- [ ] Open terminal in your working directory
- [ ] Run `git clone <your-repo-url> assignment3`
- [ ] Run `cd assignment3`
- [ ] Confirm `.git/` folder exists inside the directory
- [ ] Run `git config user.name "Your Name"`
- [ ] Run `git config user.email "your@email.com"`

## 1.5 Python Virtual Environment

- [ ] Inside `assignment3/`, run `python -m venv venv`
- [ ] Confirm `venv/` folder was created
- [ ] Activate venv: run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- [ ] Confirm terminal prompt now shows `(venv)` prefix
- [ ] Run `python --version` inside venv to confirm correct Python version

## 1.6 requirements.txt Creation

- [ ] Create file `requirements.txt` in project root
- [ ] Add line: `crewai>=0.80.0`
- [ ] Add line: `crewai-tools>=0.15.0`
- [ ] Add line: `anthropic>=0.40.0`
- [ ] Add line: `streamlit>=1.35.0`
- [ ] Add line: `python-dotenv>=1.0.0`
- [ ] Add line: `arxiv>=2.1.0`
- [ ] Add line: `matplotlib>=3.9.0`
- [ ] Add line: `plotly>=5.22.0`
- [ ] Add line: `chromadb>=0.5.0`
- [ ] Add line: `langchain-openai>=0.1.0`
- [ ] Add line: `pytest>=8.0.0`
- [ ] Add line: `numpy>=1.26.0`
- [ ] Add line: `pandas>=2.2.0`
- [ ] Run `pip install -r requirements.txt`
- [ ] Wait for all packages to install completely
- [ ] Run `pip list` and verify all packages appear [SCREENSHOT]
- [ ] Run `python -c "import crewai; print(crewai.__version__)"` to verify crewai installed
- [ ] Run `python -c "import anthropic; print('anthropic ok')"` to verify anthropic installed
- [ ] Run `python -c "import streamlit; print('streamlit ok')"` to verify streamlit installed
- [ ] Run `python -c "import arxiv; print('arxiv ok')"` to verify arxiv installed
- [ ] Run `python -c "import chromadb; print('chromadb ok')"` to verify chromadb installed

## 1.7 API Keys Setup

- [ ] Obtain Anthropic API key from console.anthropic.com
- [ ] Obtain Serper API key from serper.dev (free tier available)
- [ ] Obtain OpenAI API key from platform.openai.com (for embeddings)
- [ ] Create file `.env` in project root
- [ ] Add line: `ANTHROPIC_API_KEY=your_actual_key_here`
- [ ] Add line: `SERPER_API_KEY=your_actual_key_here`
- [ ] Add line: `OPENAI_API_KEY=your_actual_key_here`
- [ ] Save `.env` file
- [ ] Create file `.env.example` in project root
- [ ] Add line: `ANTHROPIC_API_KEY=`
- [ ] Add line: `SERPER_API_KEY=`
- [ ] Add line: `OPENAI_API_KEY=`
- [ ] Save `.env.example`

## 1.8 .gitignore Setup

- [ ] Open `.gitignore` file (auto-created by GitHub Python template)
- [ ] Confirm `.env` line exists (add it if missing)
- [ ] Add line: `venv/`
- [ ] Add line: `__pycache__/`
- [ ] Add line: `*.pyc`
- [ ] Add line: `*.pyo`
- [ ] Add line: `outputs/*.pdf`
- [ ] Add line: `.chroma/`
- [ ] Add line: `*.aux`
- [ ] Add line: `*.log`
- [ ] Add line: `*.out`
- [ ] Add line: `*.synctex.gz`
- [ ] Add line: `*.toc`
- [ ] Add line: `*.bbl`
- [ ] Add line: `*.blg`
- [ ] Save `.gitignore`
- [ ] Run `git status` and confirm `.env` does NOT appear in untracked files

## 1.9 Project Directory Structure

- [ ] Create folder: `src/`
- [ ] Create file: `src/__init__.py` (empty)
- [ ] Create folder: `src/agents/`
- [ ] Create file: `src/agents/__init__.py` (empty)
- [ ] Create folder: `src/tasks/`
- [ ] Create file: `src/tasks/__init__.py` (empty)
- [ ] Create folder: `src/tools/`
- [ ] Create file: `src/tools/__init__.py` (empty)
- [ ] Create folder: `latex/`
- [ ] Create folder: `latex/chapters/`
- [ ] Create folder: `latex/figures/`
- [ ] Create folder: `outputs/`
- [ ] Create folder: `tests/`
- [ ] Create folder: `docs/`
- [ ] Create folder: `docs/evidence/`
- [ ] Run `ls -la` (or `dir`) and verify all folders exist [SCREENSHOT]

## 1.10 LaTeX Boilerplate Verification

- [ ] Create file `latex/test_compile.tex` with content: `\documentclass{article}\begin{document}Hello\end{document}`
- [ ] Open terminal in `latex/` folder
- [ ] Run `pdflatex test_compile.tex`
- [ ] Confirm `test_compile.pdf` is generated with no errors
- [ ] Open `test_compile.pdf` and confirm "Hello" appears
- [ ] Delete `test_compile.tex` and `test_compile.pdf` after successful test
- [ ] Run `pdflatex --version` and note the version number [SCREENSHOT]

## 1.11 Initial Git Commit

- [ ] Run `git add .gitignore requirements.txt .env.example`
- [ ] Run `git add src/ latex/ outputs/ tests/ docs/`
- [ ] Run `git status` to review what will be committed
- [ ] Confirm `.env` is NOT in the staged list
- [ ] Run `git commit -m "chore: project skeleton and environment setup"`
- [ ] Run `git push origin main`
- [ ] Open GitHub in browser and confirm files appear in repository [SCREENSHOT]

---

# MODULE 2: Agent Development (The "Brain")

## 2.1 Configuration Module

- [ ] Create file `src/config.py`
- [ ] Add import: `from dotenv import load_dotenv`
- [ ] Add import: `import os`
- [ ] Call `load_dotenv()` at module level
- [ ] Define `ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")`
- [ ] Define `SERPER_API_KEY = os.getenv("SERPER_API_KEY")`
- [ ] Define `OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")`
- [ ] Define `MODEL_NAME = "claude-sonnet-4-6"`
- [ ] Define `EMBEDDING_MODEL = "text-embedding-3-small"`
- [ ] Define `PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`
- [ ] Define `OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")`
- [ ] Define `LATEX_DIR = os.path.join(PROJECT_ROOT, "latex")`
- [ ] Define `FIGURES_DIR = os.path.join(LATEX_DIR, "figures")`
- [ ] Write a `validate_config()` function that checks all keys are non-empty
- [ ] In `validate_config()`: raise `EnvironmentError` if `ANTHROPIC_API_KEY` is missing
- [ ] In `validate_config()`: raise `EnvironmentError` if `SERPER_API_KEY` is missing
- [ ] In `validate_config()`: print a warning (not error) if `OPENAI_API_KEY` is missing
- [ ] Call `validate_config()` at bottom of `config.py`
- [ ] Test: temporarily remove ANTHROPIC_API_KEY from .env, run `python src/config.py`, confirm error appears
- [ ] Test: restore the key, run `python src/config.py`, confirm no error

## 2.2 ResearchDirector Agent

- [ ] Create file `src/agents/research_director.py`
- [ ] Add import: `from crewai import Agent`
- [ ] Add import: `from src.config import MODEL_NAME`
- [ ] Define function `create_research_director() -> Agent`
- [ ] Set `role="Senior Research Director & Paper Architect"`
- [ ] Write the `goal` string (minimum 3 sentences describing exactly what success looks like)
- [ ] Confirm goal includes: "decompose topic into 7-9 sub-topics"
- [ ] Confirm goal includes: "ensure IEEE 25-30 page requirements are met"
- [ ] Write the `backstory` string — give the agent a name, credentials, personality
- [ ] Confirm backstory is at least 5 sentences
- [ ] Confirm backstory establishes authority and rigor
- [ ] Set `verbose=True`
- [ ] Set `allow_delegation=True`
- [ ] Set `llm=f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter=5`
- [ ] Return the Agent object
- [ ] Test: import and call `create_research_director()`, confirm no errors

## 2.3 DeepResearcher Agent

- [ ] Create file `src/agents/deep_researcher.py`
- [ ] Add import: `from crewai import Agent`
- [ ] Add import: `from src.config import MODEL_NAME`
- [ ] Add import for tools: `from src.tools.search_tools import SerperSearchTool, ArxivSearchTool`
- [ ] Add import for tools: `from src.tools.web_scraper import WebScraperTool`
- [ ] Define function `create_deep_researcher() -> Agent`
- [ ] Set `role="Technical AI Systems Research Specialist"`
- [ ] Write `goal` emphasizing: find 5+ authoritative sources per sub-topic
- [ ] Confirm goal includes: "provide structured Hebrew-compatible notes"
- [ ] Confirm goal includes: "never cite unverified sources"
- [ ] Write `backstory` with academic persona — PhD researcher in AI systems
- [ ] Confirm backstory includes personality traits: meticulous, never approximates
- [ ] Set `tools=[SerperSearchTool(), ArxivSearchTool(), WebScraperTool()]`
- [ ] Set `verbose=True`
- [ ] Set `allow_delegation=False`
- [ ] Set `llm=f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter=10`
- [ ] Return the Agent object
- [ ] Test: import and call `create_deep_researcher()`, confirm no errors

## 2.4 DataVisualizer Agent

- [ ] Create file `src/agents/data_visualizer.py`
- [ ] Add import: `from crewai import Agent`
- [ ] Add import: `from src.config import MODEL_NAME`
- [ ] Add import for tools: `from src.tools.code_executor import PythonCodeExecutorTool`
- [ ] Add import for tools: `from src.tools.file_tools import SafeFileWriterTool`
- [ ] Define function `create_data_visualizer() -> Agent`
- [ ] Set `role="Scientific Data Visualization & Graph Engineering Specialist"`
- [ ] Write `goal` specifying: generate matplotlib/plotly code, save to 300 DPI PNG
- [ ] Confirm goal includes: "framework comparison bar chart"
- [ ] Confirm goal includes: "architecture flowchart"
- [ ] Confirm goal includes: "security risk heatmap"
- [ ] Confirm goal includes: "deployment model radar chart"
- [ ] Write `backstory` with data scientist persona
- [ ] Confirm backstory establishes peer-reviewed publication experience
- [ ] Set `tools=[PythonCodeExecutorTool(), SafeFileWriterTool()]`
- [ ] Set `verbose=True`
- [ ] Set `allow_delegation=False`
- [ ] Set `llm=f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter=8`
- [ ] Return the Agent object
- [ ] Test: import and call `create_data_visualizer()`, confirm no errors

## 2.5 LaTeXAuthor Agent

- [ ] Create file `src/agents/latex_author.py`
- [ ] Add import: `from crewai import Agent`
- [ ] Add import: `from src.config import MODEL_NAME`
- [ ] Add imports for tools: `SafeFileWriterTool`, `FileReaderTool`
- [ ] Define function `create_latex_author() -> Agent`
- [ ] Set `role="IEEE LaTeX Technical Author (Hebrew/English Bilingual)"`
- [ ] Write `goal`: convert research summaries to compilable Hebrew LaTeX chapters
- [ ] Confirm goal includes: "IEEEtran class conventions"
- [ ] Confirm goal includes: "integrate figures, tables, equations, and code listings"
- [ ] Confirm goal includes: "every chapter must compile without errors"
- [ ] Write `backstory` with bilingual academic writer persona
- [ ] Confirm backstory establishes fluency in both LaTeX and Hebrew
- [ ] Add to backstory: "You NEVER write LaTeX that does not compile"
- [ ] Set `tools=[SafeFileWriterTool(), FileReaderTool()]`
- [ ] Set `verbose=True`
- [ ] Set `allow_delegation=False`
- [ ] Set `llm=f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter=15`
- [ ] Return the Agent object
- [ ] Test: import and call `create_latex_author()`, confirm no errors

## 2.6 QualityEditor Agent

- [ ] Create file `src/agents/quality_editor.py`
- [ ] Add import: `from crewai import Agent`
- [ ] Add import: `from src.config import MODEL_NAME`
- [ ] Add import for tools: `FileReaderTool`
- [ ] Define function `create_quality_editor() -> Agent`
- [ ] Set `role="Senior Academic Paper Quality Editor"`
- [ ] Write `goal`: review assembled paper for completeness, citations, page count
- [ ] Confirm goal includes: "verify every \cite{} has a matching .bib entry"
- [ ] Confirm goal includes: "confirm every figure is referenced in the text"
- [ ] Confirm goal includes: "validate page count is 25-30"
- [ ] Confirm goal includes: "produce a detailed remediation report"
- [ ] Write `backstory` with journal editor persona
- [ ] Confirm backstory establishes high standards and rejection authority
- [ ] Set `tools=[FileReaderTool()]`
- [ ] Set `verbose=True`
- [ ] Set `allow_delegation=False`
- [ ] Set `llm=f"anthropic/{MODEL_NAME}"`
- [ ] Set `max_iter=5`
- [ ] Return the Agent object
- [ ] Test: import and call `create_quality_editor()`, confirm no errors

## 2.7 Memory Configuration

- [ ] Create file `src/memory_config.py`
- [ ] Define `get_embedder_config()` function
- [ ] If `OPENAI_API_KEY` is set: return OpenAI embedder config with `text-embedding-3-small`
- [ ] If `OPENAI_API_KEY` is missing: return HuggingFace embedder config with `all-MiniLM-L6-v2`
- [ ] Define `MEMORY_CONFIG = {"memory": True, "embedder": get_embedder_config()}`
- [ ] Test: call `get_embedder_config()`, confirm it returns a dict with "provider" key
- [ ] Test: with OpenAI key present, confirm "openai" is the provider
- [ ] Test: with OpenAI key removed, confirm "huggingface" is the provider

---

# MODULE 3: Tool Implementation

## 3.1 SerperSearchTool

- [ ] Create file `src/tools/search_tools.py`
- [ ] Add import: `from crewai_tools import SerperDevTool`
- [ ] Add import: `from src.config import SERPER_API_KEY`
- [ ] Define `SerperSearchTool` as an instance of `SerperDevTool`
- [ ] Pass `api_key=SERPER_API_KEY` to the constructor
- [ ] Wrap instantiation in try/except: catch missing key error with clear message
- [ ] Write inline docstring explaining when to use this tool vs ArxivSearchTool
- [ ] Test: `from src.tools.search_tools import SerperSearchTool`
- [ ] Test: call `SerperSearchTool.run("CrewAI multi-agent framework 2024")`
- [ ] Test: confirm result is non-empty string
- [ ] Test: confirm result contains at least one URL
- [ ] [SCREENSHOT]: screenshot the test result showing real search output

## 3.2 ArxivSearchTool

- [ ] In `src/tools/search_tools.py`, add import: `from crewai import BaseTool`
- [ ] Add import: `import arxiv`
- [ ] Add import: `from typing import Optional`
- [ ] Define class `ArxivSearchTool(BaseTool)`
- [ ] Set class attribute `name = "arxiv_search"`
- [ ] Write `description` attribute: 2-3 sentences on when to use it (academic papers, cutting-edge research)
- [ ] Define `_run(self, query: str, max_results: int = 5) -> str` method
- [ ] Inside `_run`: create `arxiv.Search(query=query, max_results=max_results)`
- [ ] Inside `_run`: iterate results and format as: `"Title: {r.title} | Authors: {r.authors[0]} | Year: {r.published.year} | URL: {r.pdf_url}"`
- [ ] Handle case where results are empty: return "No ArXiv papers found for this query"
- [ ] Handle `Exception`: catch all, return error message string (do not crash)
- [ ] Add `max_results` validation: if < 1 or > 20, set to default 5
- [ ] Add `query` validation: if empty string, return "Query cannot be empty"
- [ ] Test: instantiate `ArxivSearchTool()`
- [ ] Test: call `tool.run("LangGraph stateful agents 2024")`
- [ ] Test: confirm result contains "Title:" and "URL:"
- [ ] Test: call with empty string, confirm graceful error message
- [ ] [SCREENSHOT]: screenshot showing real ArXiv results returned

## 3.3 PythonCodeExecutorTool

- [ ] Create file `src/tools/code_executor.py`
- [ ] Add import: `from crewai import BaseTool`
- [ ] Add import: `import subprocess`
- [ ] Add import: `import tempfile`
- [ ] Add import: `import os`
- [ ] Add import: `import ast`
- [ ] Add import: `from src.config import FIGURES_DIR`
- [ ] Define class `PythonCodeExecutorTool(BaseTool)`
- [ ] Set `name = "python_code_executor"`
- [ ] Write `description`: explain it runs Python code and saves PNG to latex/figures/
- [ ] Define `ALLOWED_IMPORTS = {"matplotlib", "numpy", "pandas", "plotly", "scipy", "math", "random", "collections"}`
- [ ] Define `BLOCKED_IMPORTS = {"os", "sys", "subprocess", "shutil", "socket", "requests", "urllib", "http", "ftplib"}`
- [ ] Implement `_validate_imports(self, code: str) -> bool` using `ast.parse()`
- [ ] In `_validate_imports`: walk the AST and find all `Import` and `ImportFrom` nodes
- [ ] In `_validate_imports`: for each import, check if module name is in BLOCKED_IMPORTS
- [ ] In `_validate_imports`: return False if any blocked import found, True otherwise
- [ ] Implement `_run(self, code: str, filename: str = "output") -> dict` method
- [ ] Call `_validate_imports(code)` first; if False, return security error dict
- [ ] Create temp directory using `tempfile.mkdtemp()`
- [ ] Write code to `temp_dir/script.py`
- [ ] Inject line at top: `import matplotlib; matplotlib.use('Agg')`
- [ ] Inject line at end: `plt.savefig("{FIGURES_DIR}/{filename}.png", dpi=300, bbox_inches='tight')`
- [ ] Run via `subprocess.run(["python", script_path], capture_output=True, timeout=30, text=True)`
- [ ] If returncode == 0: return `{"status": "success", "png_path": png_path, "stdout": result.stdout}`
- [ ] If returncode != 0: return `{"status": "error", "stderr": result.stderr}`
- [ ] Handle `subprocess.TimeoutExpired`: return timeout error dict
- [ ] Handle generic `Exception`: return exception error dict
- [ ] Clean up temp files in `finally` block
- [ ] Test: pass simple matplotlib code, confirm PNG appears in `latex/figures/`
- [ ] Test: pass code with `import os`, confirm SecurityError is returned
- [ ] Test: pass code that takes 60 seconds, confirm TimeoutError within 30 seconds
- [ ] Test: pass empty code string, confirm graceful error
- [ ] [SCREENSHOT]: terminal showing PNG was created successfully

## 3.4 SafeFileWriterTool

- [ ] Create file `src/tools/file_tools.py`
- [ ] Add import: `from crewai import BaseTool`
- [ ] Add import: `import os`
- [ ] Add import: `from src.config import PROJECT_ROOT`
- [ ] Define class `SafeFileWriterTool(BaseTool)`
- [ ] Set `name = "safe_file_writer"`
- [ ] Write `description`: explains it writes UTF-8 files within allowed project directories
- [ ] Define `ALLOWED_DIRS = ["latex", "outputs", "docs"]` (relative to PROJECT_ROOT)
- [ ] Define `BLOCKED_FILES = [".env", ".gitignore", "requirements.txt", "config.py"]`
- [ ] Implement `_is_safe_path(self, path: str) -> bool`
- [ ] In `_is_safe_path`: resolve absolute path with `os.path.abspath(path)`
- [ ] In `_is_safe_path`: check it starts with `PROJECT_ROOT`
- [ ] In `_is_safe_path`: check the relative portion starts with one of `ALLOWED_DIRS`
- [ ] In `_is_safe_path`: check filename is not in `BLOCKED_FILES`
- [ ] Return False if any check fails
- [ ] Implement `_run(self, path: str, content: str) -> dict`
- [ ] Call `_is_safe_path(path)`, if False: return security error dict
- [ ] Create parent directories: `os.makedirs(os.path.dirname(path), exist_ok=True)`
- [ ] Write content to file with `encoding="utf-8"`
- [ ] Return `{"status": "success", "path": path, "bytes": len(content.encode())}`
- [ ] Handle `IOError`: return error dict
- [ ] Handle `PermissionError`: return error dict
- [ ] Test: write Hebrew text to `outputs/test_hebrew.txt`, confirm file created
- [ ] Test: attempt write to `../.env`, confirm security error returned
- [ ] Test: attempt write to `.env`, confirm security error returned
- [ ] Test: write to `latex/chapters/test.tex`, confirm file created in correct location

## 3.5 FileReaderTool

- [ ] In `src/tools/file_tools.py`, define class `FileReaderTool(BaseTool)`
- [ ] Set `name = "file_reader"`
- [ ] Write `description`: reads any file within the project directory
- [ ] Define `MAX_FILE_SIZE = 1 * 1024 * 1024` (1MB in bytes)
- [ ] Implement `_run(self, path: str) -> str`
- [ ] Validate path is within PROJECT_ROOT (reuse `_is_safe_path` logic)
- [ ] Check file exists: if not, return helpful error with expected path
- [ ] Check file size: if > MAX_FILE_SIZE, return first 1MB with truncation note
- [ ] Read file with `encoding="utf-8"`
- [ ] If `UnicodeDecodeError`: retry with `encoding="latin-1"` and log warning
- [ ] Return file content as string
- [ ] Test: write a file, then read it back, confirm content matches
- [ ] Test: read a non-existent file, confirm helpful error message
- [ ] Test: read `src/config.py`, confirm it succeeds

## 3.6 WebScraperTool

- [ ] Create file `src/tools/web_scraper.py`
- [ ] Add import: `from crewai_tools import ScrapeWebsiteTool`
- [ ] Define `WebScraperTool = ScrapeWebsiteTool()`
- [ ] Test: call `WebScraperTool.run("https://docs.crewai.com")` (or any accessible URL)
- [ ] Confirm result is non-empty string containing actual page text

## 3.7 Tool Integration Tests

- [ ] Create file `tests/test_tools.py`
- [ ] Add import: `import pytest`
- [ ] Add import: `from src.tools.search_tools import SerperSearchTool, ArxivSearchTool`
- [ ] Add import: `from src.tools.code_executor import PythonCodeExecutorTool`
- [ ] Add import: `from src.tools.file_tools import SafeFileWriterTool, FileReaderTool`
- [ ] Write `test_serper_returns_results()`: search and assert `len(result) > 100`
- [ ] Write `test_serper_empty_query_graceful()`: pass empty string, assert no exception
- [ ] Write `test_arxiv_returns_papers()`: search and assert "Title:" in result
- [ ] Write `test_arxiv_max_results_validation()`: pass max_results=0, assert it uses default
- [ ] Write `test_arxiv_empty_query_graceful()`: pass empty string, assert graceful message
- [ ] Write `test_code_executor_creates_png()`: pass matplotlib code, assert PNG file exists
- [ ] Write `test_code_executor_blocks_os_import()`: pass `import os`, assert "security" in result
- [ ] Write `test_code_executor_blocks_subprocess()`: pass `import subprocess`, assert security error
- [ ] Write `test_code_executor_timeout()`: pass `while True: pass`, assert timeout < 35 seconds
- [ ] Write `test_file_writer_creates_file()`: write to outputs/, assert file exists
- [ ] Write `test_file_writer_blocks_env()`: attempt `.env`, assert security error
- [ ] Write `test_file_writer_blocks_traversal()`: attempt `../../.env`, assert security error
- [ ] Write `test_file_reader_reads_content()`: write then read, assert content matches
- [ ] Write `test_file_reader_missing_file()`: read nonexistent path, assert helpful message
- [ ] Run `pytest tests/test_tools.py -v`
- [ ] Confirm all tests pass [SCREENSHOT]
- [ ] Fix any failing tests before proceeding

---

# MODULE 4: Research & Content Generation

## 4.1 Task Definitions — Research Phase

- [ ] Create file `src/tasks/research_tasks.py`
- [ ] Add import: `from crewai import Task`
- [ ] Define `create_decompose_task(director_agent) -> Task`
- [ ] Task description: "Analyze topic '{topic}' and produce a structured outline of 7-9 sub-topics..."
- [ ] Task expected_output: numbered list of sub-topics with estimated page count per sub-topic
- [ ] Set `output_file="outputs/paper_outline.md"`
- [ ] Define `create_research_task(researcher_agent, subtopic: str, chapter_num: int) -> Task`
- [ ] Task description: "Research '{subtopic}' in depth for chapter {chapter_num}..."
- [ ] Confirm description specifies: find 5+ sources, provide BibTeX entries, summarize in Hebrew-compatible notes
- [ ] Task expected_output: structured markdown with sections: Summary, Key Findings, Sources (BibTeX), Hebrew Section Titles
- [ ] Set `output_file=f"outputs/research_ch{chapter_num:02d}.md"`
- [ ] Test: instantiate each task, confirm no errors

## 4.2 Task Definitions — Visualization Phase

- [ ] Create file `src/tasks/visualization_tasks.py`
- [ ] Add import: `from crewai import Task`
- [ ] Define `create_framework_comparison_task(visualizer_agent) -> Task`
- [ ] Task description: "Generate Python matplotlib code for a bar chart comparing CrewAI, LangGraph, AutoGen, PydanticAI on 5 metrics..."
- [ ] Confirm description specifies: x-axis = frameworks, y-axis = score 1-10, Hebrew axis labels
- [ ] Confirm description specifies: save as `latex/figures/fig_framework_comparison.png` at 300 DPI
- [ ] Task expected_output: path to saved PNG file + confirmation of 300 DPI
- [ ] Set `output_file="outputs/graph_framework_log.md"`
- [ ] Define `create_architecture_diagram_task(visualizer_agent) -> Task`
- [ ] Task description: "Generate Python matplotlib code for a flowchart showing Agent Runtime architecture..."
- [ ] Confirm description specifies: boxes for Planner, Memory, Tools, RAG with arrows
- [ ] Confirm description specifies: save as `latex/figures/fig_architecture.png` at 300 DPI
- [ ] Define `create_security_heatmap_task(visualizer_agent) -> Task`
- [ ] Task description: "Generate Python matplotlib code for a 2D heatmap of OWASP AI security risks..."
- [ ] Confirm description specifies: x-axis = likelihood, y-axis = impact, Hebrew labels
- [ ] Confirm description specifies: save as `latex/figures/fig_security_heatmap.png` at 300 DPI
- [ ] Define `create_deployment_radar_task(visualizer_agent) -> Task`
- [ ] Task description: "Generate Python code for a radar/spider chart comparing Local vs Cloud vs Hybrid deployment..."
- [ ] Confirm description specifies: axes = latency, cost, privacy, scalability, maintenance
- [ ] Confirm description specifies: save as `latex/figures/fig_deployment_radar.png` at 300 DPI
- [ ] Test: instantiate all tasks, confirm no errors

## 4.3 Task Definitions — Writing Phase

- [ ] Create file `src/tasks/writing_tasks.py`
- [ ] Add import: `from crewai import Task`
- [ ] Define `create_chapter_task(author_agent, chapter_num: int, chapter_title: str, research_file: str) -> Task`
- [ ] Task description: "Read research from {research_file} and write chapter {chapter_num}: {chapter_title}..."
- [ ] Confirm description specifies: all prose in Hebrew, technical terms in English inline
- [ ] Confirm description specifies: must include at least one \begin{figure} environment
- [ ] Confirm description specifies: must include at least one \begin{table} environment
- [ ] Confirm description specifies: must include at least one \cite{} reference
- [ ] Confirm description specifies: must use \section{} and at least two \subsection{}
- [ ] Confirm description specifies: write to `latex/chapters/ch{num:02d}_{slug}.tex`
- [ ] Task expected_output: path to saved .tex file + word count confirmation
- [ ] Define `create_bibliography_task(author_agent) -> Task`
- [ ] Task description: "Compile all citations from chapter research files into references.bib..."
- [ ] Confirm description specifies: minimum 15 BibTeX entries
- [ ] Confirm description specifies: at least 5 @article entries, at least 3 @misc entries
- [ ] Confirm description specifies: verify all entries have title, author, year fields
- [ ] Task expected_output: content of references.bib file + count of entries
- [ ] Set `output_file="latex/references.bib"`
- [ ] Define `create_cover_task(author_agent) -> Task`
- [ ] Task description: "Write the LaTeX cover sheet for the paper..."
- [ ] Confirm description specifies: course name in Hebrew, assignment number, submission date
- [ ] Confirm description specifies: student names placeholder
- [ ] Set `output_file="latex/chapters/cover.tex"`
- [ ] Define `create_abstract_task(author_agent) -> Task`
- [ ] Task description: "Write Hebrew and English abstracts (150-250 words each) and 5-7 keywords..."
- [ ] Set `output_file="latex/chapters/abstract.tex"`
- [ ] Define `create_quality_review_task(editor_agent) -> Task`
- [ ] Task description: "Review the assembled LaTeX paper for completeness..."
- [ ] Confirm description specifies: check every \cite{} has matching .bib entry
- [ ] Confirm description specifies: check every \ref{fig:...} has matching \label
- [ ] Confirm description specifies: estimate page count
- [ ] Confirm description specifies: check Hebrew text appears in every chapter
- [ ] Task expected_output: structured quality report with PASS/FAIL per criterion
- [ ] Set `output_file="outputs/quality_report.md"`

## 4.4 Crew Assembly

- [ ] Create file `src/crew.py`
- [ ] Add all necessary imports (crewai, agents, tasks, config)
- [ ] Define `build_research_crew(topic: str) -> Crew`
- [ ] Inside function: instantiate all 5 agents by calling their factory functions
- [ ] Inside function: build task list in correct sequential order:
- [ ] Task order step 1: decompose_task (director)
- [ ] Task order step 2: research all sub-topics (researcher, 7 tasks)
- [ ] Task order step 3: generate all 4 graphs (visualizer)
- [ ] Task order step 4: write cover.tex (author)
- [ ] Task order step 5: write abstract.tex (author)
- [ ] Task order step 6: write ch01_intro.tex (author)
- [ ] Task order step 7: write ch02_architecture.tex (author)
- [ ] Task order step 8: write ch03_frameworks.tex (author)
- [ ] Task order step 9: write ch04_protocols.tex (author)
- [ ] Task order step 10: write ch05_security.tex (author)
- [ ] Task order step 11: write ch06_deployment.tex (author)
- [ ] Task order step 12: write ch07_our_system.tex (author)
- [ ] Task order step 13: write ch08_results.tex (author)
- [ ] Task order step 14: write ch09_conclusion.tex (author)
- [ ] Task order step 15: compile references.bib (author)
- [ ] Task order step 16: quality review (editor)
- [ ] Set `process=Process.sequential`
- [ ] Set `memory=True`
- [ ] Set `embedder` using `get_embedder_config()` from memory_config
- [ ] Set `output_log_file="outputs/crew_log.txt"`
- [ ] Set `verbose=True`
- [ ] Return the assembled `Crew` object
- [ ] Test: call `build_research_crew("test topic")`, confirm Crew object returned with no errors

## 4.5 CLI Interface

- [ ] Create file `main.py`
- [ ] Add import: `import argparse`
- [ ] Add import: `from src.crew import build_research_crew`
- [ ] Add import: `from src.config import validate_config`
- [ ] Define `main()` function
- [ ] Create `argparse.ArgumentParser` with description
- [ ] Add argument `--topic` (required=True, help text)
- [ ] Add argument `--output-dir` (default="outputs", help text)
- [ ] Add argument `--dry-run` (action="store_true", help="Build crew but don't run it")
- [ ] Call `validate_config()` at start of main
- [ ] Call `build_research_crew(args.topic)` to build the crew
- [ ] If not dry-run: call `crew.kickoff(inputs={"topic": args.topic})`
- [ ] Print completion message with output directory path
- [ ] Add `if __name__ == "__main__": main()` guard
- [ ] Test: `python main.py --help` — confirm help text appears
- [ ] Test: `python main.py --topic "test" --dry-run` — confirm no API calls made, crew built

## 4.6 Streamlit Interface

- [ ] Create file `app.py`
- [ ] Add import: `import streamlit as st`
- [ ] Add import: `from src.crew import build_research_crew`
- [ ] Add import: `from src.config import validate_config`
- [ ] Add import: `import os`
- [ ] Set `st.set_page_config(page_title="ResearchCrew", layout="wide")`
- [ ] Add `st.title("ResearchCrew — AI Paper Generator")`
- [ ] Create sidebar with `st.sidebar`
- [ ] Add `topic = st.text_input("Research Topic", value="AI Agent Architecture 2026")` in sidebar
- [ ] Add `model = st.selectbox("LLM Model", ["claude-sonnet-4-6", "claude-opus-4-6"])` in sidebar
- [ ] Add `target_pages = st.slider("Target Pages", 25, 30, 28)` in sidebar
- [ ] Add `run_btn = st.button("Generate Paper", type="primary")` in sidebar
- [ ] Create two columns with `col1, col2 = st.columns([2, 1])`
- [ ] In col1: add `st.subheader("Agent Progress")`
- [ ] Add progress placeholders for each agent (use `st.empty()`)
- [ ] In col2: add `st.subheader("Download Files")`
- [ ] Add download button placeholders
- [ ] When `run_btn` is clicked: wrap in `with st.spinner("Agents working...")`
- [ ] Call `validate_config()` inside the button handler
- [ ] Call `build_research_crew(topic)`
- [ ] Call `crew.kickoff(inputs={"topic": topic})`
- [ ] After completion: show `st.success("Paper generated!")`
- [ ] After completion: scan `latex/figures/` and add download buttons for each PNG
- [ ] After completion: add download button for each `.tex` file in `latex/chapters/`
- [ ] After completion: add download button for `latex/references.bib`
- [ ] In log area: read and display `outputs/crew_log.txt` with `st.text_area`
- [ ] Add `st.image` previews for each generated PNG graph
- [ ] Add `st.code` for preview of `latex/main.tex`
- [ ] Test: `streamlit run app.py` — confirm browser opens without errors [SCREENSHOT]
- [ ] Test: UI layout looks correct with all components visible
- [ ] Test: Click run button — confirm spinner appears

## 4.7 Agent Tests

- [ ] Create file `tests/test_agents.py`
- [ ] Write `test_all_agents_instantiate()`: call all 5 factory functions, assert no exceptions
- [ ] Write `test_research_director_has_delegation()`: assert `director.allow_delegation == True`
- [ ] Write `test_researcher_has_correct_tools()`: assert len(researcher.tools) == 3
- [ ] Write `test_visualizer_has_code_executor()`: assert PythonCodeExecutorTool in visualizer.tools
- [ ] Write `test_latex_author_has_file_writer()`: assert SafeFileWriterTool in author.tools
- [ ] Write `test_quality_editor_no_delegation()`: assert `editor.allow_delegation == False`
- [ ] Run `pytest tests/test_agents.py -v` and confirm all pass [SCREENSHOT]

## 4.8 Crew Integration Test

- [ ] Create file `tests/test_crew.py`
- [ ] Write `test_crew_builds_without_error()`: call `build_research_crew("test")`, assert Crew object returned
- [ ] Write `test_crew_has_memory_enabled()`: assert `crew.memory == True`
- [ ] Write `test_crew_has_correct_agent_count()`: assert `len(crew.agents) == 5`
- [ ] Write `test_crew_has_correct_task_order()`: assert first task's agent is director
- [ ] Run `pytest tests/test_crew.py -v` and confirm all pass [SCREENSHOT]

## 4.9 Full Crew Execution

- [ ] Run full crew on the research topic:
  `python main.py --topic "AI Agent Architecture and Orchestration 2026"`
- [ ] Monitor terminal for agent outputs
- [ ] Confirm `outputs/paper_outline.md` is created
- [ ] Confirm `outputs/research_ch01.md` through `outputs/research_ch07.md` are created
- [ ] Open each research file and confirm it is at least 800 words
- [ ] Confirm `latex/figures/fig_framework_comparison.png` exists
- [ ] Confirm `latex/figures/fig_architecture.png` exists
- [ ] Confirm `latex/figures/fig_security_heatmap.png` exists
- [ ] Confirm `latex/figures/fig_deployment_radar.png` exists
- [ ] Open each PNG and confirm it is a valid, readable graph [SCREENSHOT each one]
- [ ] Confirm `latex/chapters/cover.tex` exists
- [ ] Confirm `latex/chapters/abstract.tex` exists
- [ ] Confirm `latex/chapters/ch01_intro.tex` through `ch09_conclusion.tex` exist
- [ ] Confirm `latex/references.bib` exists
- [ ] Confirm `outputs/quality_report.md` exists
- [ ] Read `outputs/quality_report.md` and note any FAIL items
- [ ] If QualityEditor found issues: fix them manually and re-run relevant tasks

---

# MODULE 5: LaTeX/IEEE Mastering

## 5.1 Main LaTeX File

- [ ] Create file `latex/main.tex`
- [ ] First line: `\documentclass[10pt, a4paper, journal]{IEEEtran}`
- [ ] Add: `\usepackage[utf8]{inputenc}`
- [ ] Add: `\usepackage[T1]{fontenc}`
- [ ] Add Hebrew language support: `\usepackage[hebrew, english]{babel}` OR `\usepackage{polyglossia}` + `\setmainlanguage{hebrew}` + `\setotherlanguage{english}`
- [ ] Add: `\usepackage{graphicx}`
- [ ] Add: `\usepackage{booktabs}` (for professional tables)
- [ ] Add: `\usepackage{amsmath}`
- [ ] Add: `\usepackage{amssymb}`
- [ ] Add: `\usepackage{hyperref}`
- [ ] Add: `\usepackage{fancyhdr}`
- [ ] Add: `\usepackage{listings}`
- [ ] Add: `\usepackage{xcolor}`
- [ ] Add: `\usepackage{caption}`
- [ ] Add: `\usepackage{subcaption}`
- [ ] Add: `\usepackage{float}`
- [ ] Add: `\usepackage{geometry}` with margins: `\geometry{margin=2.5cm}`
- [ ] Add: `\usepackage{microtype}` (for better text spacing)
- [ ] Configure `listings` package for Python syntax highlighting:
  - [ ] Set `language=Python`
  - [ ] Set `basicstyle=\small\ttfamily`
  - [ ] Set `keywordstyle=\color{blue}\bfseries`
  - [ ] Set `commentstyle=\color{gray}`
  - [ ] Set `stringstyle=\color{green!50!black}`
  - [ ] Set `showstringspaces=false`
  - [ ] Set `numbers=left`
  - [ ] Set `numberstyle=\tiny`
  - [ ] Set `frame=single`
- [ ] Configure `fancyhdr`:
  - [ ] `\pagestyle{fancy}`
  - [ ] `\fancyhead[L]{AI Agent Orchestration 2026}`
  - [ ] `\fancyhead[R]{\thepage}`
  - [ ] `\fancyfoot[C]{Course: Orchestration of AI Agents | 2026}`
  - [ ] `\renewcommand{\headrulewidth}{0.4pt}`
- [ ] Add `\begin{document}` marker
- [ ] Add `\selectlanguage{hebrew}` right after `\begin{document}`
- [ ] Add: `\input{chapters/cover}`
- [ ] Add IEEEtran abstract block: `\begin{abstract}\input{chapters/abstract}\end{abstract}`
- [ ] Add: `\input{chapters/ch01_intro}`
- [ ] Add: `\input{chapters/ch02_architecture}`
- [ ] Add: `\input{chapters/ch03_frameworks}`
- [ ] Add: `\input{chapters/ch04_protocols}`
- [ ] Add: `\input{chapters/ch05_security}`
- [ ] Add: `\input{chapters/ch06_deployment}`
- [ ] Add: `\input{chapters/ch07_our_system}`
- [ ] Add: `\input{chapters/ch08_results}`
- [ ] Add: `\input{chapters/ch09_conclusion}`
- [ ] Add: `\bibliographystyle{IEEEtran}`
- [ ] Add: `\bibliography{references}`
- [ ] Add: `\end{document}`

## 5.2 Cover Sheet

- [ ] Create/verify file `latex/chapters/cover.tex`
- [ ] Add titlepage environment: `\begin{titlepage}`
- [ ] Add `\centering`
- [ ] Add institution name in Hebrew
- [ ] Add course name in Hebrew: "קורס: אורקסטרציה של סוכני בינה מלאכותית"
- [ ] Add assignment designation: "עבודה מס' 3"
- [ ] Add paper title in Hebrew (the full title from PRD)
- [ ] Add subtitle in English
- [ ] Add student name line (fill in real names)
- [ ] Add submission date: "20 יוני 2026"
- [ ] Add `\vfill` for spacing
- [ ] Add semester/year info
- [ ] Close with `\end{titlepage}`
- [ ] Test compile `main.tex` and confirm cover page renders correctly

## 5.3 Abstract

- [ ] Create/verify file `latex/chapters/abstract.tex`
- [ ] Write Hebrew abstract (150-250 words) covering: topic, methodology, results, significance
- [ ] Add English abstract (same content, 150-250 words)
- [ ] Add Hebrew keywords list (5-7 keywords)
- [ ] Add English keywords list
- [ ] Confirm abstract mentions: CrewAI, multi-agent, IEEE, LaTeX
- [ ] Test compile and confirm abstract appears correctly

## 5.4 Chapter 1: Introduction (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch01_intro.tex`
- [ ] Add: `\selectlanguage{hebrew}`
- [ ] Add `\section{מבוא}` — Introduction
- [ ] Add `\subsection{רקע}` — Background
- [ ] Write 2-3 paragraphs in Hebrew on the evolution of AI agents
- [ ] Add `\subsection{מוטיבציה}` — Motivation
- [ ] Write 2 paragraphs explaining why this research matters
- [ ] Add `\subsection{מבנה המאמר}` — Paper structure
- [ ] Write 1 paragraph describing each chapter briefly
- [ ] Add at least 2 `\cite{}` citations
- [ ] Add a figure reference using `(ראו איור \ref{fig:timeline})`
- [ ] Include a simple timeline figure or reference to one
- [ ] Verify all Hebrew text is inside `\selectlanguage{hebrew}` scope
- [ ] Verify English terms appear in `\textit{term}` or `\texttt{term}` format
- [ ] Test compile and confirm chapter renders without errors

## 5.5 Chapter 2: Agent Architecture (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch02_architecture.tex`
- [ ] Add `\section{ארכיטקטורת סוכן בינה מלאכותית}`
- [ ] Add `\subsection{ה-Runtime של הסוכן}` — Agent Runtime
- [ ] Write content covering: Planner, Memory, Tools, RAG components
- [ ] Add `\subsection{מתכנן — Planner}` — subsection on planning
- [ ] Write 2+ paragraphs with technical details
- [ ] Add `\subsection{זיכרון — Memory}` — subsection on memory
- [ ] Write 2+ paragraphs on short-term vs long-term memory
- [ ] Add `\subsection{כלים — Tools}` — subsection on tools
- [ ] Write 2+ paragraphs on tool types and API integration
- [ ] Add `\subsection{RAG}` — subsection on retrieval-augmented generation
- [ ] Write 2+ paragraphs on RAG architecture
- [ ] Include architecture flowchart figure:
  ```latex
  \begin{figure}[h]
  \centering
  \includegraphics[width=0.9\columnwidth]{figures/fig_architecture.png}
  \caption{ארכיטקטורת סוכן בינה מלאכותית — רכיבי ה-Runtime}
  \label{fig:architecture}
  \end{figure}
  ```
- [ ] Include a comparison table of memory types
- [ ] Add at least 3 `\cite{}` citations
- [ ] Test compile and confirm chapter renders

## 5.6 Chapter 3: Frameworks Comparison (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch03_frameworks.tex`
- [ ] Add `\section{מסגרות עבודה לסוכנים}`
- [ ] Add `\subsection{CrewAI}` with 3+ paragraphs
- [ ] Add `\subsection{LangGraph}` with 3+ paragraphs
- [ ] Add `\subsection{AutoGen / AG2}` with 2+ paragraphs
- [ ] Add `\subsection{PydanticAI}` with 2+ paragraphs
- [ ] Add `\subsection{השוואה}` — Comparison subsection
- [ ] Include framework comparison bar chart figure:
  ```latex
  \begin{figure}[h]
  \centering
  \includegraphics[width=0.9\columnwidth]{figures/fig_framework_comparison.png}
  \caption{השוואת מסגרות עבודה לפי קריטריונים מרכזיים}
  \label{fig:frameworks}
  \end{figure}
  ```
- [ ] Include comparison table (at least 5 rows, 4 columns) with `booktabs`:
  ```latex
  \begin{table}[h]
  \centering
  \begin{tabular}{lccc}
  \toprule
  קריטריון & CrewAI & LangGraph & AutoGen \\
  \midrule
  ...rows... \\
  \bottomrule
  \end{tabular}
  \caption{השוואה מפורטת של מסגרות עבודה}
  \label{tab:frameworks}
  \end{table}
  ```
- [ ] Add at least 4 `\cite{}` citations
- [ ] Test compile

## 5.7 Chapter 4: Protocols (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch04_protocols.tex`
- [ ] Add `\section{פרוטוקולי תקשורת בין סוכנים}`
- [ ] Add `\subsection{MCP — Model Context Protocol}` with 3+ paragraphs
- [ ] Add `\subsection{A2A — Agent-to-Agent Protocol}` with 3+ paragraphs
- [ ] Add `\subsection{השוואה בין MCP ל-A2A}` with 2+ paragraphs
- [ ] Include a protocol sequence diagram figure
- [ ] Include a comparison table of MCP vs A2A
- [ ] Add at least 3 `\cite{}` citations
- [ ] Test compile

## 5.8 Chapter 5: Security (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch05_security.tex`
- [ ] Add `\section{אבטחת סוכני בינה מלאכותית}`
- [ ] Add `\subsection{OWASP Top 10 לסוכני AI}` with 3+ paragraphs
- [ ] Add subsections for each top threat:
  - [ ] `\subsection{חטיפת מטרה — Goal Hijacking}`
  - [ ] `\subsection{שימוש לרעה בכלים — Tool Misuse}`
  - [ ] `\subsection{הרעלת זיכרון — Memory Poisoning}`
  - [ ] `\subsection{ניצול זהות — Identity Abuse}`
- [ ] Include security risk heatmap figure:
  ```latex
  \begin{figure}[h]
  \centering
  \includegraphics[width=0.9\columnwidth]{figures/fig_security_heatmap.png}
  \caption{מפת חום של סיכוני אבטחה בסוכני AI}
  \label{fig:security}
  \end{figure}
  ```
- [ ] Include a threats-by-category table
- [ ] Add at least 4 `\cite{}` citations
- [ ] Test compile

## 5.9 Chapter 6: Deployment (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch06_deployment.tex`
- [ ] Add `\section{מודלי פריסה ואובזרבביליות}`
- [ ] Add `\subsection{פריסה מקומית — Local Deployment}` with 3+ paragraphs
- [ ] Add `\subsection{פריסה בענן — Cloud Deployment}` with 3+ paragraphs
- [ ] Add `\subsection{פריסה היברידית — Hybrid}` with 2+ paragraphs
- [ ] Add `\subsection{אובזרבביליות — Observability}` with 2+ paragraphs
- [ ] Include deployment radar chart figure
- [ ] Include deployment comparison table (cost, latency, privacy, scalability)
- [ ] Add at least 3 `\cite{}` citations
- [ ] Test compile

## 5.10 Chapter 7: Our System (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch07_our_system.tex`
- [ ] Add `\section{המערכת שלנו: ResearchCrew}`
- [ ] Add `\subsection{סקירה כללית}` — overview
- [ ] Write 3+ paragraphs describing the system from a user perspective
- [ ] Add `\subsection{ארכיטקטורת המערכת}` — system architecture
- [ ] Include the system architecture diagram figure
- [ ] Add `\subsection{הסוכנים — Agents}` — describe each agent
- [ ] Add `\subsection{הכלים — Tools}` — describe each tool
- [ ] Add `\subsection{הזיכרון — Memory}` — describe memory strategy
- [ ] Add `\subsection{ממשק המשתמש}` — UI description
- [ ] Include a code listing of the crew assembly (`src/crew.py` key section)
- [ ] Include a code listing of the most interesting tool
- [ ] Include a screenshot of Streamlit UI running (as a figure)
- [ ] Add `\subsection{אתגרים ופתרונות}` — challenges faced and solutions
- [ ] Add at least 3 `\cite{}` citations
- [ ] Test compile

## 5.11 Chapter 8: Results (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch08_results.tex`
- [ ] Add `\section{תוצאות וניתוח}`
- [ ] Add `\subsection{מדדי ביצועים}` — performance metrics
- [ ] Create a results table: tokens used, time per phase, output quality scores
- [ ] Add `\subsection{ניתוח המוצר הסופי}` — analysis of final paper output
- [ ] Add `\subsection{מגבלות}` — limitations observed
- [ ] Include a results bar chart figure (compare phases: research, writing, editing)
- [ ] Add at least 2 `\cite{}` citations
- [ ] Test compile

## 5.12 Chapter 9: Conclusion (Hebrew LaTeX)

- [ ] Open/create `latex/chapters/ch09_conclusion.tex`
- [ ] Add `\section{סיכום}`
- [ ] Add `\subsection{תרומות המחקר}` — research contributions (3+ paragraphs)
- [ ] Add `\subsection{מגבלות ועבודה עתידית}` — limitations and future work (2+ paragraphs)
- [ ] Add `\subsection{מסקנות סופיות}` — final conclusions (1-2 paragraphs)
- [ ] Test compile

## 5.13 Mathematical Formulas

- [ ] In `ch02_architecture.tex`: add Transformer attention formula:
  ```latex
  \begin{equation}
  \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
  \label{eq:attention}
  \end{equation}
  ```
- [ ] Ensure equation is referenced in text: `(ראו משוואה \ref{eq:attention})`
- [ ] In `ch05_security.tex`: add risk scoring formula:
  ```latex
  \begin{equation}
  R = P \times I \times (1 - M)
  \label{eq:risk}
  \end{equation}
  ```
  where P = probability, I = impact, M = mitigation factor
- [ ] Reference this formula in the text
- [ ] In `ch08_results.tex`: add a performance efficiency formula or metric definition
- [ ] Test compile and confirm all equations render correctly

## 5.14 Bibliography (BibTeX)

- [ ] Create/verify file `latex/references.bib`
- [ ] Add entry 1: @misc for CrewAI official documentation
- [ ] Add entry 2: @misc for LangGraph documentation
- [ ] Add entry 3: @misc for Anthropic Claude documentation
- [ ] Add entry 4: @article for a foundational multi-agent systems paper from ArXiv
- [ ] Add entry 5: @article for a paper on LLM agent frameworks
- [ ] Add entry 6: @article for OWASP AI security guidelines
- [ ] Add entry 7: @inproceedings for a paper on RAG systems
- [ ] Add entry 8: @article for a paper on agent memory systems
- [ ] Add entry 9: @misc for MCP protocol specification
- [ ] Add entry 10: @misc for AutoGen documentation
- [ ] Add entry 11: @article for a benchmark comparison of LLM frameworks
- [ ] Add entry 12: @article for a paper on tool-use in LLMs
- [ ] Add entry 13: @inproceedings for a paper on agent orchestration
- [ ] Add entry 14: @misc for Streamlit documentation
- [ ] Add entry 15: @unpublished for course lecture notes (L06)
- [ ] Verify each entry has: author, title, year, and url/journal/booktitle
- [ ] Count entries: confirm minimum 15
- [ ] Search all .tex files for `\cite{` and list every citation key used
- [ ] Confirm every citation key in .tex files has a matching entry in references.bib
- [ ] Fix any missing entries

## 5.15 Full Compilation

- [ ] Open terminal in `latex/` folder
- [ ] Run: `pdflatex main.tex`
- [ ] Check terminal output for errors (lines starting with !)
- [ ] Fix any LaTeX errors found before proceeding
- [ ] Run: `bibtex main`
- [ ] Check for BibTeX errors or warnings
- [ ] Fix any missing .bib entries flagged by BibTeX
- [ ] Run: `pdflatex main.tex` (second pass)
- [ ] Run: `pdflatex main.tex` (third pass — needed for TOC and cross-references)
- [ ] Open `main.pdf` in PDF viewer
- [ ] Count pages: confirm 25-30 pages
- [ ] Verify cover page is correct (Hebrew title, names, date)
- [ ] Verify Table of Contents appears and is correct
- [ ] Verify all chapter headings appear in TOC
- [ ] Verify all figures render (no missing figure placeholders)
- [ ] Verify all tables render correctly
- [ ] Verify all equations render correctly
- [ ] Verify bibliography appears at end with all 15+ references
- [ ] Verify headers appear on every page
- [ ] Verify footers appear on every page
- [ ] Verify page numbers are correct
- [ ] Verify Hebrew text flows right-to-left
- [ ] Verify English technical terms appear correctly within Hebrew text
- [ ] [SCREENSHOT]: terminal showing `pdflatex` with zero errors
- [ ] [SCREENSHOT]: first page of compiled PDF (cover)
- [ ] [SCREENSHOT]: Table of Contents page
- [ ] [SCREENSHOT]: a page with a figure
- [ ] [SCREENSHOT]: a page with a table
- [ ] [SCREENSHOT]: bibliography page

---

# MODULE 6: Final Summary (20-Page Course Document)

## 6.1 Document Planning

- [ ] Create file `docs/course_summary.md` (source for the 20-page summary)
- [ ] Plan structure: one major section per previous task + overview + reflection
- [ ] Estimate page budget: Overview (2p) + Task 1-5 (3p each) + Reflection (3p) = 20p
- [ ] Identify which code files and screenshots to reference for each task

## 6.2 Course Overview Section

- [ ] Write section: "סקירת הקורס — Course Overview"
- [ ] Write paragraph: course objectives and learning outcomes (Hebrew)
- [ ] Write paragraph: technology stack used across all tasks
- [ ] Write paragraph: key concepts: agents, orchestration, memory, tools
- [ ] Write paragraph: evolution of your understanding from Task 1 to Task 5
- [ ] Verify this section is at least 400 words

## 6.3 Task 1 Summary Section

- [ ] Write section header: "משימה 1 — [Task 1 Name]"
- [ ] Write sub-section: "תיאור המשימה" — describe what was required
- [ ] Write sub-section: "הגישה שלנו" — describe what you built
- [ ] Write sub-section: "טכנולוגיות בשימוש" — list technologies used
- [ ] Write sub-section: "תוצאות" — describe outcomes/what was learned
- [ ] Add: link to GitHub repository for Task 1
- [ ] Add: code screenshot reference (add actual screenshot to docs/evidence/)
- [ ] Verify this section is at least 600 words

## 6.4 Task 2 Summary Section

- [ ] Write section header: "משימה 2 — [Task 2 Name]"
- [ ] Write sub-section: "תיאור המשימה"
- [ ] Write sub-section: "הגישה שלנו"
- [ ] Write sub-section: "טכנולוגיות בשימוש"
- [ ] Write sub-section: "תוצאות"
- [ ] Add: GitHub link for Task 2
- [ ] Add: code screenshot reference
- [ ] Verify this section is at least 600 words

## 6.5 Task 3 Summary Section

- [ ] Write section header: "משימה 3 — [Task 3 Name]"
- [ ] Write sub-section: "תיאור המשימה"
- [ ] Write sub-section: "הגישה שלנו"
- [ ] Write sub-section: "טכנולוגיות בשימוש"
- [ ] Write sub-section: "תוצאות"
- [ ] Add: GitHub link for Task 3
- [ ] Add: code screenshot reference
- [ ] Verify this section is at least 600 words

## 6.6 Task 4 Summary Section

- [ ] Write section header: "משימה 4 — [Task 4 Name]"
- [ ] Write sub-section: "תיאור המשימה"
- [ ] Write sub-section: "הגישה שלנו"
- [ ] Write sub-section: "טכנולוגיות בשימוש"
- [ ] Write sub-section: "תוצאות"
- [ ] Add: GitHub link for Task 4
- [ ] Add: code screenshot reference
- [ ] Verify this section is at least 600 words

## 6.7 Task 5 Summary Section

- [ ] Write section header: "משימה 5 — [Task 5 Name]"
- [ ] Write sub-section: "תיאור המשימה"
- [ ] Write sub-section: "הגישה שלנו"
- [ ] Write sub-section: "טכנולוגיות בשימוש"
- [ ] Write sub-section: "תוצאות"
- [ ] Add: GitHub link for Task 5
- [ ] Add: code screenshot reference
- [ ] Verify this section is at least 600 words

## 6.8 Reflection Section

- [ ] Write section: "סיכום ורפלקציה — Reflection"
- [ ] Write sub-section: "מה למדתי" — what I learned (personal reflection)
- [ ] Write sub-section: "אתגרים" — biggest challenges faced
- [ ] Write sub-section: "כישורים שרכשתי" — skills acquired
- [ ] Write sub-section: "שימוש עתידי" — how I will use this knowledge
- [ ] Verify this section is at least 500 words

## 6.9 Summary LaTeX Conversion

- [ ] Create file `latex/course_summary_main.tex`
- [ ] Set `\documentclass[12pt, a4paper]{article}` (not IEEEtran for this one)
- [ ] Add same Hebrew/language packages as main.tex
- [ ] Add same fancyhdr configuration
- [ ] Add cover page with: "סיכום קורס", course name, student names, date
- [ ] Add `\tableofcontents`
- [ ] Add `\newpage`
- [ ] Create `latex/chapters/summary_ch01.tex` through `summary_ch07.tex`
- [ ] Convert each markdown section to LaTeX chapter
- [ ] Add `\input{}` for each chapter in course_summary_main.tex
- [ ] Add `\usepackage{graphicx}` for screenshots
- [ ] Add each code screenshot as a figure with caption
- [ ] Run: `pdflatex course_summary_main.tex`
- [ ] Run: `pdflatex course_summary_main.tex` (second pass for TOC)
- [ ] Open `course_summary_main.pdf` and count pages
- [ ] Confirm page count is ≥ 20 pages
- [ ] Verify TOC is correct
- [ ] Verify all sections appear
- [ ] Verify Hebrew text renders correctly
- [ ] [SCREENSHOT]: first page of course summary PDF
- [ ] [SCREENSHOT]: Table of Contents of course summary

---

# MODULE 7: Validation & Submission

## 7.1 Security Audit

- [ ] Run: `grep -r "ANTHROPIC_API_KEY=" src/` — confirm returns nothing
- [ ] Run: `grep -r "sk-ant-" src/` — confirm returns nothing
- [ ] Run: `grep -r "sk-ant-" tests/` — confirm returns nothing
- [ ] Run: `grep -r "SERPER_API_KEY=" src/` — confirm returns nothing
- [ ] Run: `grep -r "OPENAI_API_KEY=" src/` — confirm returns nothing
- [ ] Run: `git ls-files .env` — confirm returns nothing (file not tracked)
- [ ] Open `.gitignore` and confirm `.env` is listed
- [ ] Run `git log --all --oneline` and confirm `.env` never appeared in any commit
- [ ] Verify `PythonCodeExecutorTool` uses AST-based import validation (not string matching)
- [ ] Verify `SafeFileWriterTool` validates path before writing
- [ ] Verify `FileReaderTool` validates path before reading
- [ ] [SCREENSHOT]: grep results showing no hardcoded keys

## 7.2 Full Requirements Checklist

- [ ] **Modularity**: Open `src/agents/` — confirm each agent is in its own file
- [ ] **Modularity**: Open `src/tools/` — confirm each tool is in its own file
- [ ] **Modularity**: Open `src/tasks/` — confirm tasks are organized by phase
- [ ] **Scalability**: Confirm adding a new agent requires only: new file + one line in crew.py
- [ ] **Generic design**: Confirm topic is a parameter passed at runtime, not hardcoded
- [ ] **2+ external tools**: Confirm SerperSearchTool works and returns real results
- [ ] **2+ external tools**: Confirm ArxivSearchTool works and returns real results
- [ ] **Memory**: Run crew, confirm `.chroma/` directory is created
- [ ] **Memory**: Run crew twice, confirm second run is faster (memory hit)
- [ ] **100% working code**: Run `pytest tests/ -v` — confirm 0 failures
- [ ] **Paper 25-30 pages**: Run `pdfinfo latex/main.pdf | grep Pages` — confirm range
- [ ] **IEEE format**: Confirm `\documentclass{IEEEtran}` is in main.tex
- [ ] **Hebrew primary**: Open any chapter .tex file — confirm Hebrew text is the majority
- [ ] **English terms**: Open any chapter — confirm technical terms are in English
- [ ] **MikTeX/LaTeX used**: Confirm PDF was generated by `pdflatex` (not a Word export)
- [ ] **Code screenshots**: Confirm docs/evidence/ contains screenshots for all components
- [ ] **GitHub links**: Confirm README.md contains live GitHub URL
- [ ] **Demo video**: Confirm video file exists and is ≤ 3 minutes
- [ ] **20-page summary**: Run `pdfinfo latex/course_summary_main.pdf | grep Pages`
- [ ] **Visuals**: Confirm ≥ 4 PNG files exist in `latex/figures/`
- [ ] **Figures in paper**: Confirm each PNG is referenced in at least one .tex file
- [ ] **Tables in paper**: Confirm at least 5 tables exist across all chapters
- [ ] **Math formulas**: Confirm at least 2 `\begin{equation}` environments exist
- [ ] **Code listings**: Confirm at least 2 `\begin{lstlisting}` environments exist
- [ ] **BibTeX**: Confirm `latex/references.bib` has ≥ 15 entries
- [ ] **All cited**: Confirm every key in .tex \cite{} commands exists in .bib
- [ ] **Cover page**: Open PDF page 1, confirm all required fields are present
- [ ] **Headers/footers**: Scroll through PDF, confirm they appear on every page
- [ ] **TOC**: Confirm Table of Contents lists all 9 chapters

## 7.3 Demo Video Planning

- [ ] Write video script (≤ 3 minutes):
  - [ ] 0:00–0:20: Introduction — what ResearchCrew is
  - [ ] 0:20–0:45: Show Streamlit UI — sidebar, topic input, agent list
  - [ ] 0:45–1:30: Click "Generate Paper" — show agents running, verbose output
  - [ ] 1:30–2:00: Show generated files: .tex chapters, .bib, PNG graphs
  - [ ] 2:00–2:30: Show compiled PDF — cover, TOC, a chapter, bibliography
  - [ ] 2:30–3:00: Show GitHub repo — code structure, README
- [ ] Install screen recorder: OBS Studio (obsproject.com) or use Windows Game Bar (Win+G)
- [ ] Set recording resolution: 1920x1080
- [ ] Set recording frame rate: 30fps
- [ ] Configure microphone if doing voice narration
- [ ] Do a test recording of 10 seconds and confirm audio+video quality
- [ ] Run the full demo workflow to have it ready before recording
- [ ] Start recording
- [ ] Follow the script, showing each component clearly
- [ ] Stop recording
- [ ] Review recording — confirm all sections are visible
- [ ] Check duration — if > 3 minutes, trim with video editor
- [ ] Export as MP4 (H.264 encoding)
- [ ] Save as `demo_video.mp4`
- [ ] Confirm file size is reasonable (< 500MB)
- [ ] Watch the final video from start to finish [SCREENSHOT: video thumbnail]

## 7.4 README.md

- [ ] Open `README.md` in project root
- [ ] Add project title: `# ResearchCrew — AI Research Paper Generator`
- [ ] Add badge: Python version
- [ ] Add badge: License
- [ ] Write "About" section (3-5 sentences)
- [ ] Write "Architecture" section with ASCII diagram
- [ ] Write "Requirements" section listing Python 3.11+, MikTeX, API keys
- [ ] Write "Installation" section with step-by-step commands
- [ ] Write "Configuration" section explaining .env setup
- [ ] Write "Usage — CLI" section: `python main.py --topic "..."`
- [ ] Write "Usage — Web UI" section: `streamlit run app.py`
- [ ] Add screenshots section with 3 embedded images:
  - [ ] Screenshot of Streamlit UI
  - [ ] Screenshot of agents running in terminal
  - [ ] Screenshot of compiled PDF page
- [ ] Write "Output Files" section listing what gets generated
- [ ] Write "Running Tests" section: `pytest tests/ -v`
- [ ] Add link to compiled paper PDF (upload to GitHub releases or Google Drive)
- [ ] Add link to demo video (upload to YouTube unlisted or GitHub)
- [ ] Add "Course" section: course name, assignment number, student names
- [ ] Verify all links in README work
- [ ] [SCREENSHOT]: README as rendered on GitHub

## 7.5 GitHub Final Push

- [ ] Run `git status` — review all changed/new files
- [ ] Run `git add src/`
- [ ] Run `git add tests/`
- [ ] Run `git add latex/chapters/`
- [ ] Run `git add latex/figures/`
- [ ] Run `git add latex/references.bib`
- [ ] Run `git add latex/main.tex`
- [ ] Run `git add latex/course_summary_main.tex`
- [ ] Run `git add app.py main.py requirements.txt README.md`
- [ ] Run `git add docs/`
- [ ] Run `git add .env.example`
- [ ] Run `git status` — confirm `.env` is NOT staged
- [ ] Run `git commit -m "feat: complete ResearchCrew implementation with LaTeX paper"`
- [ ] Run `git push origin main`
- [ ] Open GitHub in browser and verify all files appear [SCREENSHOT]
- [ ] Click on `src/agents/research_director.py` — confirm content is visible
- [ ] Click on `latex/main.tex` — confirm content is visible
- [ ] Click on `README.md` — confirm it renders correctly with images

## 7.6 Submission Package Assembly

- [ ] Create folder `submission/`
- [ ] Copy `latex/main.pdf` → `submission/paper.pdf`
- [ ] Copy `latex/course_summary_main.pdf` → `submission/course_summary.pdf`
- [ ] Copy `demo_video.mp4` → `submission/demo_video.mp4`
- [ ] Create `submission/README.md` with:
  - [ ] GitHub repository URL
  - [ ] Instructions to run the code
  - [ ] Description of what each submitted file is
- [ ] Verify `submission/paper.pdf` opens correctly
- [ ] Verify `submission/course_summary.pdf` opens correctly
- [ ] Verify `submission/demo_video.mp4` plays correctly
- [ ] Create zip: `assignment3_final_submission.zip` containing the `submission/` folder
- [ ] Verify zip file opens correctly
- [ ] Verify zip file size is reasonable

## 7.7 Final Pre-Submission Checklist

- [ ] Page count of paper.pdf is between 25 and 30
- [ ] Page count of course_summary.pdf is 20 or more
- [ ] Demo video is 3 minutes or less
- [ ] GitHub repository is publicly accessible
- [ ] All tests pass: `pytest tests/ -v` shows 0 failures
- [ ] No API keys in any committed file
- [ ] All figures appear in the paper PDF
- [ ] All tables appear in the paper PDF
- [ ] At least 2 math formulas appear
- [ ] At least 2 code listings appear
- [ ] Bibliography has 15+ references
- [ ] Cover page has correct student names and date
- [ ] Headers/footers appear on every page
- [ ] Hebrew text is the primary language throughout
- [ ] English technical terms appear correctly
- [ ] Submission zip is complete and accessible
- [ ] Submit before 2026-06-20 23:59 local time

---

## Quick Stats
- **Module 1** (Environment): ~95 tasks
- **Module 2** (Agent Brain): ~80 tasks
- **Module 3** (Tools): ~80 tasks
- **Module 4** (Content Generation): ~90 tasks
- **Module 5** (LaTeX/IEEE): ~110 tasks
- **Module 6** (Course Summary): ~55 tasks
- **Module 7** (Validation): ~85 tasks
- **TOTAL**: ~595 micro-tasks
