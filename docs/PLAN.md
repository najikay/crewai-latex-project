# Multi-Phase Implementation Plan
## Assignment 3: NavigatorCrew — Biomimetic Navigation Research Platform
**Version**: 2.0 | **Date**: 2026-06-07 | **Deadline**: 2026-06-20

> **Architecture decision (v2.0)**: Switched from `Process.sequential` to
> `Process.hierarchical`. NavigationResearchDirector is the `manager_agent`
> and is NOT listed in `agents=[]` (CrewAI hierarchical requirement). Tasks
> use granular factory functions (`create_task_outline`, `create_task_research`,
> `create_task_figures`, `create_task_latex`, `create_task_review`) defined in
> `src/tasks/research_tasks.py` with `create_all_tasks()` as the assembler.

---

## Timeline Overview

```
Week 1 (Jun 6–12): Phase 1 — Agent Development + Phase 2 partial
Week 2 (Jun 13–17): Phase 2 — Content Generation + Phase 3 LaTeX
Week 3 (Jun 18–20): Phase 4 — Validation + Submission
```

---

## Phase 1: Agent Development (Days 1–4)

### Step 1.1: Environment Setup
**Goal**: All dependencies installed, keys loaded, project skeleton created.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install crewai crewai-tools anthropic streamlit python-dotenv \
            arxiv matplotlib plotly chromadb langchain-openai

# Create project structure (see PRD Section 10)
```

**Files to create**:
- `requirements.txt` with pinned versions
- `.env.example` with key names (no values)
- `.gitignore` excluding `.env`, `outputs/`, `__pycache__/`, `venv/`
- `src/config.py` — centralized config:
  ```python
  from dotenv import load_dotenv
  import os
  load_dotenv()
  ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
  SERPER_API_KEY = os.getenv("SERPER_API_KEY")
  MODEL_NAME = "claude-sonnet-4-6"
  OUTPUT_DIR = "outputs"
  LATEX_DIR = "latex"
  ```

**Test**: `python -c "import crewai, anthropic, streamlit; print('OK')"` — must print OK.

---

### Step 1.2: Build the Tools Layer
**Goal**: All 6 tools implemented, individually tested.

#### `src/tools/search_tools.py`
```python
# Uses crewai_tools.SerperDevTool (wraps Serper.dev API)
# Custom ArxivSearchTool using arxiv library
# Both inherit from crewai BaseTool
```

**Test each tool standalone**:
```python
from src.tools.search_tools import ArxivSearchTool
tool = ArxivSearchTool()
result = tool.run("multi-agent systems CrewAI 2024")
assert len(result) > 100
```

#### `src/tools/code_executor.py`
```python
# PythonCodeExecutorTool:
# 1. Receives Python code string from agent
# 2. Writes to temp file
# 3. Runs via subprocess.run(["python", tempfile], capture_output=True)
# 4. Saves generated PNG to latex/figures/
# 5. Returns path to saved file + stdout
# SECURITY: Only allows matplotlib/plotly imports, blocks os/sys/subprocess
```

**Test**: Pass a simple `plt.plot([1,2,3])` snippet — verify PNG appears in `latex/figures/`.

#### `src/tools/file_tools.py`
```python
# FileWriterTool: Write text to a specified path under latex/
# FileReaderTool: Read text from a specified path
# Both validate paths stay within project directory (no path traversal)
```

---

### Step 1.3: Build Each Agent
**Goal**: 5 agent definitions, each with correct role/goal/backstory/tools.

**File**: `src/agents/research_director.py`
```python
from crewai import Agent
from src.config import MODEL_NAME

def create_research_director():
    return Agent(
        role="Senior Research Director",
        goal="Decompose the topic '{topic}' into 7 research sub-topics...",
        backstory="You are a veteran IEEE researcher...",
        verbose=True,
        allow_delegation=True,   # Manager: can delegate to other agents
        llm=f"anthropic/{MODEL_NAME}"
    )
```

Repeat pattern for: `DeepResearcher`, `DataVisualizer`, `LaTeXAuthor`, `QualityEditor`.

**Test each agent** by running a minimal crew with one agent and one task — confirm the LLM responds correctly before wiring the full crew.

---

### Step 1.4: Build the Tasks Layer
**Goal**: All tasks defined with clear description and expected_output.

**File**: `src/tasks/research_tasks.py`

Key tasks:
1. `decompose_topic_task` — ResearchDirector breaks topic into sub-topics
2. `research_subtopic_task` — DeepResearcher researches each sub-topic (dynamic task per chapter)
3. `generate_graphs_task` — DataVisualizer creates 3+ matplotlib graphs
4. `write_latex_chapter_task` — LaTeXAuthor writes each chapter in Hebrew LaTeX
5. `compile_bibliography_task` — LaTeXAuthor assembles references.bib
6. `quality_review_task` — QualityEditor reviews full paper, requests fixes

**Critical**: Each task's `expected_output` must be extremely specific:
```python
Task(
    description="Research the topic of CrewAI framework architecture...",
    expected_output="""A structured research summary with:
    - 5-7 key findings with citations
    - At least 2 authoritative sources (ArXiv or IEEE)  
    - Hebrew section titles
    - Technical English terminology preserved
    Format: Markdown with clear headings""",
    agent=deep_researcher,
    output_file="outputs/research_crewai.md"
)
```

---

### Step 1.5: Assemble the Crew
**File**: `src/crew.py`

```python
from crewai import Crew, Process

def build_crew(topic: str) -> Crew:
    # Instantiate all agents
    director = create_research_director()
    researcher = create_deep_researcher()
    visualizer = create_data_visualizer()
    author = create_latex_author()
    editor = create_quality_editor()
    
    # Define task sequence
    tasks = build_tasks(topic, researcher, visualizer, author, editor)
    
    return Crew(
        agents=[director, researcher, visualizer, author, editor],
        tasks=tasks,
        process=Process.sequential,
        memory=True,
        embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}},
        output_log_file="outputs/crew_log.txt",
        verbose=True
    )
```

**Test**: Run with a simple topic like "Python programming" to verify end-to-end flow before using the real topic.

---

### Step 1.6: Build CLI Interface
**File**: `main.py`

```python
import argparse
from src.crew import build_crew

def main():
    parser = argparse.ArgumentParser(description="ResearchCrew — AI Paper Generator")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    args = parser.parse_args()
    
    crew = build_crew(args.topic)
    result = crew.kickoff(inputs={"topic": args.topic})
    print(f"\n✅ Done! Output: {args.output_dir}/")

if __name__ == "__main__":
    main()
```

**Test**: `python main.py --topic "AI Agent Architecture 2026"` — verify it runs without errors.

---

### Step 1.7: Build Streamlit Interface
**File**: `app.py`

```python
import streamlit as st
from src.crew import build_crew

st.set_page_config(page_title="ResearchCrew", layout="wide")
st.title("🤖 ResearchCrew — AI Paper Generator")

with st.sidebar:
    topic = st.text_input("Research Topic", value="AI Agent Architecture 2026")
    run_btn = st.button("▶ Generate Paper", type="primary")

col1, col2 = st.columns(2)

if run_btn:
    with st.spinner("Agents working..."):
        crew = build_crew(topic)
        result = crew.kickoff(inputs={"topic": topic})
    st.success("Paper generated!")
    # Show download buttons for .tex, .bib, figures
```

**Test**: `streamlit run app.py` — verify browser opens, button triggers crew run.

---

## Phase 2: Content Generation (Days 4–8)

### Step 2.1: Run Research Phase
**Goal**: All 7 chapter research summaries saved to `outputs/research_*.md`.

Run the crew on the actual topic:
```bash
python main.py --topic "ארכיטקטורת סוכני בינה מלאכותית ואורקסטרציה בשנת 2026"
```

**Expected outputs**:
- `outputs/research_intro.md`
- `outputs/research_architecture.md`
- `outputs/research_frameworks.md`
- `outputs/research_protocols.md`
- `outputs/research_security.md`
- `outputs/research_deployment.md`
- `outputs/research_our_system.md`

**Quality check**: Each file must be ≥ 800 words with citations.

---

### Step 2.2: Generate Graphs & Visuals
**Goal**: ≥ 4 publication-quality figures saved to `latex/figures/`.

The `DataVisualizer` agent will generate Python code for:

1. **Framework Comparison Bar Chart** — CrewAI vs LangGraph vs AutoGen on 5 metrics
2. **Agent Architecture Diagram** — matplotlib flowchart of Planner→Memory→Tools→RAG
3. **Security Risk Heatmap** — OWASP top threats by likelihood × impact
4. **Deployment Model Comparison** — radar chart: Local vs Cloud vs Hybrid

Each graph must:
- Use Hebrew labels where appropriate
- Be saved as 300 DPI PNG
- Have a descriptive filename: `fig_framework_comparison.png`
- Be accompanied by a LaTeX `\figure{}` snippet

**Manual fallback**: If code executor fails, generate graphs manually using `generate_figures.py` script.

---

### Step 2.3: Write the 20-Page Course Summary
**Goal**: Separate document covering all 5 previous assignments.

**File**: `docs/course_summary.md` → will be compiled separately as `course_summary.tex`

Structure (20 pages):
- Course overview and objectives
- Task 1 summary (with screenshots)
- Task 2 summary
- Task 3 summary  
- Task 4 summary
- Task 5 summary
- Reflection and lessons learned
- Appendix: code samples

This can be partially AI-assisted but must reflect your actual work from previous tasks.

---

## Phase 3: LaTeX/IEEE Integration (Days 8–13)

### Step 3.1: MikTeX Setup & Template
**Goal**: MikTeX installed, IEEE template working.

1. Install MikTeX from miktex.org (if not already done)
2. Install required packages via MikTeX Package Manager:
   - `babel-hebrew` (right-to-left Hebrew support)
   - `fontenc`, `inputenc`
   - `IEEEtran` class
   - `biblatex` or `natbib` for citations
   - `graphicx`, `booktabs`, `amsmath`

3. Create `latex/main.tex` master file:
```latex
\documentclass[10pt, a4paper, journal]{IEEEtran}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[hebrew, english]{babel}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath, amssymb}
\usepackage{hyperref}
\usepackage{fancyhdr}

% Headers and footers
\pagestyle{fancy}
\fancyhead[L]{AI Agent Orchestration 2026}
\fancyhead[R]{\thepage}
\fancyfoot[C]{Course: Orchestration of AI Agents | 2026}

\begin{document}
\selectlanguage{hebrew}

% Cover sheet
\input{chapters/cover.tex}

% Abstract
\begin{abstract}
\input{chapters/abstract.tex}
\end{abstract}

% Chapters
\input{chapters/ch01_intro.tex}
\input{chapters/ch02_architecture.tex}
% ... etc

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

**Test compile**: `pdflatex main.tex` — must produce PDF with no critical errors.

---

### Step 3.2: Convert Research to LaTeX Chapters
**Goal**: Each `outputs/research_*.md` → `latex/chapters/ch0N_*.tex`.

The `LaTeXAuthor` agent performs this conversion. Key rules:
- All prose in Hebrew (`\selectlanguage{hebrew}`)
- Technical terms stay in English (inline): `ה-\texttt{CrewAI framework}`
- Every chapter must have: `\section{}`, `\subsection{}`, at least one figure reference, at least one table
- Math formulas use proper `\begin{equation}` environments

**Template for each chapter**:
```latex
\selectlanguage{hebrew}
\section{כותרת הפרק}

\subsection{רקע}
טקסט בעברית עם \textit{technical terms} באנגלית...

\begin{figure}[h]
\centering
\includegraphics[width=0.9\columnwidth]{figures/fig_name.png}
\caption{תיאור הגרף}
\label{fig:name}
\end{figure}

\begin{table}[h]
\centering
\begin{tabular}{lcc}
\toprule
פריימוורק & יתרונות & חסרונות \\
\midrule
CrewAI & ... & ... \\
\bottomrule
\end{tabular}
\caption{השוואת פריימוורקים}
\end{table}
```

---

### Step 3.3: Build BibTeX References
**File**: `latex/references.bib`

Minimum 15 references:
- IEEE papers from ArXiv on CrewAI, LangGraph, multi-agent systems
- Official framework documentation
- OWASP AI Security guidelines 2026
- Course textbook/slides (cited as unpublished)

Format each as `@article{}` or `@misc{}` with full metadata.

---

### Step 3.4: Cover Sheet & Formal Elements
**File**: `latex/chapters/cover.tex`

Required elements:
```latex
\begin{titlepage}
\centering
{\Large מוסד לימודים} \\[0.5em]
{\large קורס: אורקסטרציה של סוכני בינה מלאכותית} \\[1em]
{\Huge\bfseries ארכיטקטורת סוכני AI \\[0.3em] ואורקסטרציה בשנת 2026} \\[1em]
{\large עבודה מס' 3} \\[2em]
{\large שם הסטודנט: ...} \\
{\large תאריך הגשה: 20 יוני 2026} \\
\end{titlepage}
```

---

### Step 3.5: Full Compilation & PDF Generation

```bash
cd latex/
pdflatex main.tex
bibtex main
pdflatex main.tex   # Run twice for cross-references
pdflatex main.tex   # Run third time for TOC
```

**Verify**:
- [ ] PDF opens without errors
- [ ] Page count: 25–30 pages
- [ ] All figures render correctly
- [ ] Table of Contents shows correct page numbers
- [ ] Bibliography appears with all citations
- [ ] Headers/footers on every page
- [ ] Hebrew text renders right-to-left

---

## Phase 4: Validation (Days 13–15)

### Step 4.1: Technical Validation Checklist
Run through `assignment_requirements.md` final checklist:

```bash
# Count pages in PDF
pdfinfo outputs/paper.pdf | grep Pages

# Verify all Python tests pass
python -m pytest tests/ -v

# Verify no hardcoded API keys
grep -r "sk-" src/  # Should return nothing
grep -r "AIza" src/ # Should return nothing
```

### Step 4.2: Content Review
- Read every chapter — minimum 3 sentences per subsection
- Verify every figure has a caption and is referenced in text: `(ראו איור \ref{fig:name})`
- Verify every table has a caption and is referenced
- Verify every citation in text appears in references.bib

### Step 4.3: Demo Video Preparation
**Duration**: Max 3 minutes
**Script**:
1. (0:00–0:30) Show the Streamlit UI, enter topic
2. (0:30–1:30) Show agents running live (CrewAI verbose output in terminal alongside)
3. (1:30–2:30) Show generated LaTeX files and compiled PDF
4. (2:30–3:00) Show GitHub repo with all files committed

**Tools**: OBS Studio (free) or Windows screen recorder (Win+G)

### Step 4.4: GitHub Repository Setup
```bash
git init
git add .
git commit -m "feat: initial ResearchCrew implementation"
git remote add origin https://github.com/<username>/assignment3-researchcrew
git push -u origin main
```

**Required README.md sections**:
- Project description
- Architecture diagram (can be a simple ASCII diagram)
- Installation instructions
- Usage (CLI + Streamlit)
- Environment variables
- Screenshots of running agent
- Link to compiled PDF

### Step 4.5: Final Submission Package
```
submission/
├── paper.pdf               # The 25-30 page IEEE paper
├── course_summary.pdf      # The 20-page course summary
├── latex/                  # Full LaTeX source
├── src/                    # All Python code
├── demo_video.mp4          # 3-minute video
└── README.md               # GitHub link + instructions
```
