# Product Requirements Document (PRD)
## Assignment 3: NavigatorCrew — Biomimetic Navigation & Sensor Fusion AI Platform
**Version**: 3.0 | **Date**: 2026-06-06 | **Deadline**: 2026-06-20

---

## 1. Executive Summary

**NavigatorCrew** is a specialized multi-agent AI research platform built on **CrewAI**, designed to autonomously produce a peer-reviewed IEEE paper on the subject of **bat-inspired drone navigation via bio-mimetic multi-modal sensor fusion**. The platform's five agents are domain experts in robotics, SLAM, signal processing, and sensor fusion — not generic researchers.

The system simultaneously *demonstrates* the AI orchestration principles of the course while producing substantive engineering research on a distinct, high-complexity domain: translating the biological echolocation mechanism of *Chiroptera* (bats) into embedded navigation algorithms for GPS-denied quadrotor UAV flight.

### Paper Title
**"Bat-Inspired Drone Navigation via Bio-Mimetic Multi-Modal Sensor Fusion"**
*ניווט רחפנים ביומימטי מבוסס-עטלף באמצעות היתוך חישתי מרובה-מודאלי*

### Why This Topic?
1. **Technical depth**: Spans signal processing (FM pulse matched-filtering), probabilistic robotics (EKF-SLAM, graph optimization), deep learning (PointNet, Vision Transformers), and embedded systems — easily sustaining 30 pages.
2. **Differentiation**: Unique in the course context; not a generic LLM paper.
3. **Visualization richness**: Naturally produces 3D trajectory plots, sensor-fusion heatmaps, Cochleagram spectrograms, range-Doppler maps, and architecture diagrams.
4. **Academic credibility**: Active IEEE research area with a strong citation base (Thrun, Simmons, Kalman, ORB-SLAM3, etc.).

---

## 2. Architecture Decision

**Framework**: CrewAI with `Process.sequential`
**LLM**: `claude-sonnet-4-6` (primary), all agents
**Memory**: ChromaDB long-term + entity memory (persistent across runs)
**Compiler**: XeLaTeX (mandatory for Hebrew BiDi — pdflatex cannot handle Unicode Hebrew)

---

## 3. Agent Team — Domain Expert Specifications

### Agent 1: NavigationResearchDirector (Manager)
```
Role:       Senior Research Fellow — Autonomous Navigation Systems
Goal:       Decompose the biomimetic navigation research topic into 7 sub-domains,
            assign each to the SLAM & Fusion Researcher, and ensure every chapter
            contains: formal problem definitions, mathematical models, comparative
            analysis, and IEEE-quality citations. Reject vague deliverables.
Backstory:  Dr. Yael Cohen — 22 years in autonomous robotics at the Weizmann
            Institute. Author of "Probabilistic Methods in Aerial SLAM" (2019).
            You are incapable of accepting hand-wavy engineering prose.
            Every claim must be quantified; every formula must be derived.
LLM:        claude-sonnet-4-6
Delegation: allow_delegation=True (hierarchical manager)
Tools:      None
Max iter:   5
```

### Agent 2: SLAMAndFusionResearcher
```
Role:       SLAM, Sensor Fusion & Signal Processing Research Specialist
Goal:       For each assigned sub-domain, find 5+ authoritative sources (IEEE,
            ArXiv, Nature), extract algorithms, mathematical formulations, and
            benchmark results. Produce structured Hebrew-compatible research notes
            with full BibTeX entries and LaTeX-ready equation skeletons.
Backstory:  Prof. Amir Ben-David — PhD in probabilistic robotics from Technion.
            10 years implementing EKF-SLAM, Graph-SLAM, and LiDAR odometry on
            embedded ARM platforms. You never approximate; you cite page numbers.
LLM:        claude-sonnet-4-6
Tools:      [SerperSearchTool, ArxivSearchTool, WebScraperTool]
Max iter:   12
Memory:     Long-term ChromaDB (avoids re-searching robotics literature)
```

### Agent 3: VisualizationEngineer
```
Role:       Scientific Visualization & Sensor Data Engineering Specialist
Goal:       Generate publication-quality Python code to produce ALL required
            figures: 3D UAV trajectory plots, sensor-fusion heatmaps,
            FM pulse spectrograms (Cochleagram), range-Doppler maps, EKF
            covariance ellipses, and architecture diagrams. All figures
            must be 300 DPI PNG, with Hebrew axis labels where appropriate.
Backstory:  Noa Shapira — MSc in computational neuroscience, 8 years producing
            figures for robotics conferences (ICRA, IROS, IEEE RA-L).
            You believe a poorly labeled axis is professional negligence.
LLM:        claude-sonnet-4-6
Tools:      [PythonCodeExecutorTool, SafeFileWriterTool]
Max iter:   10
```

### Agent 4: LaTeXAuthor
```
Role:       IEEE LaTeX Technical Author (Hebrew/English Bilingual, Robotics Domain)
Goal:       Convert research notes and figure references into compilable Hebrew
            LaTeX chapters conforming to IEEEtran. Every chapter must include:
            formal definitions, numbered equations, figure references, tables,
            and inline English technical terminology. Output must compile with
            XeLaTeX on the first attempt.
Backstory:  Yael Mizrahi — bilingual technical writer, 10+ years publishing IEEE
            papers in robotics and signal processing. You have never submitted a
            chapter that fails to compile. You treat LaTeX syntax errors as
            personal failures.
LLM:        claude-sonnet-4-6
Tools:      [SafeFileWriterTool, FileReaderTool]
Max iter:   15
```

### Agent 5: QualityEditor
```
Role:       Senior IEEE Journal Technical Editor — Robotics & Autonomous Systems
Goal:       Perform a rigorous editorial review: verify mathematical notation
            consistency, confirm all \cite{} keys exist in .bib, check every
            figure is referenced in text, validate equation numbering,
            estimate page count, and flag any section below 400 words.
Backstory:  Prof. Daniel Stern — Associate Editor, IEEE Transactions on Robotics.
            You have rejected 65% of papers submitted to your desk.
            You find missing equation labels physically upsetting.
LLM:        claude-sonnet-4-6
Tools:      [FileReaderTool]
Max iter:   5
```

---

## 4. Tool Specifications

### Tool 1: SerperSearchTool (External API — required tool #1)
```
Purpose:    Web search for robotics papers, SLAM benchmarks, UAV systems
API:        Serper.dev (Google Search API)
Key:        SERPER_API_KEY
Query bias: agent prompts pre-pend "site:ieee.org OR site:arxiv.org" for quality
Error:      Exponential backoff (1s, 2s, 4s), max 3 retries; cache results in memory
```

### Tool 2: ArxivSearchTool (External API — required tool #2)
```
Purpose:    Academic paper lookup — robotics, SLAM, sensor fusion, biomimetics
Lib:        arxiv Python library
Categories: cs.RO (Robotics), eess.SP (Signal Processing), cs.CV (Computer Vision)
Output:     Title | Authors | Year | ArXiv ID | Abstract | PDF URL
Validation: max_results clamped to [1, 20]; empty query returns error message
```

### Tool 3: PythonCodeExecutorTool
```
Purpose:    Execute Python visualization code; save outputs to latex/figures/
Whitelist:  matplotlib, mpl_toolkits, numpy, scipy, pandas, plotly, sklearn
Blacklist:  os, sys, subprocess, shutil, socket, requests (AST-validated)
Timeout:    45 seconds (3D plots are slower than 2D)
Output dir: latex/figures/ (path-locked)
DPI:        All savefig() calls enforced at dpi=300
```

### Tool 4: SafeFileWriterTool
```
Purpose:    Write .tex chapters, .bib entries, .py scripts, research notes
Allowed:    latex/, outputs/, docs/
Blocked:    .env, config.py, requirements.txt, .gitignore
Security:   os.path.abspath() + PROJECT_ROOT prefix check
Encoding:   UTF-8 always
```

### Tool 5: FileReaderTool
```
Purpose:    Read research notes, existing .tex files, .bib for cross-check
Max size:   1 MB
Security:   Path must be within PROJECT_ROOT
Fallback:   latin-1 if UTF-8 decode fails
```

### Tool 6: WebScraperTool
```
Source:     crewai_tools.ScrapeWebsiteTool
Purpose:    Scrape specific IEEE/ArXiv pages for paper details
```

---

## 5. Required Figures (VisualizationEngineer Output)

| Filename | Type | Description | Libraries |
|---|---|---|---|
| `fig_bat_vs_artificial.png` | Flowchart | Biological echolocation vs artificial pipeline | matplotlib, patches |
| `fig_trajectory_3d.png` | 3D line plot | GT vs SLAM trajectory in tunnel environment | mpl_toolkits.mplot3d |
| `fig_sensor_fusion_heatmap.png` | 2D heatmap | Sensor confidence across environment grid | matplotlib, seaborn |
| `fig_cochleagram.png` | Spectrogram | FM pulse Cochleagram — frequency vs time | scipy.signal, matplotlib |
| `fig_range_doppler.png` | 2D map | Range-Doppler map of sonar returns | numpy FFT, matplotlib |
| `fig_ekf_covariance.png` | 2D scatter | EKF localization covariance ellipses over trajectory | matplotlib.patches.Ellipse |
| `fig_framework_comparison.png` | Bar chart | SLAM algorithm accuracy benchmarks | matplotlib |
| `fig_sensor_modalities.png` | Architecture | Multi-modal sensor fusion block diagram | matplotlib, patches |
| `fig_results_summary.png` | Multi-panel | Error metrics: RMSE, ATE, RPE across methods | matplotlib subplots |

---

## 6. Paper Structure (25–30 pages, IEEE, Hebrew-primary)

| # | Chapter Title (Hebrew) | Est. Pages | Key Content |
|---|---|---|---|
| Cover | דף שער | 1 | Title, course, names, date |
| Abstract | תקציר | 1 | Hebrew + English, 5–7 keywords |
| 1 | מבוא — רקע, בעיה, מוטיבציה | 2–3 | FM pulse formulas, EKF intro, placeholders |
| 2 | הבסיס הביולוגי: אקולוקציה של עטלפים | 3–4 | CF/FM signals, Cochleagram, neural processing |
| 3 | מודאליות החישנים: LiDAR, סונאר, Vision-AI | 3–4 | Sensor specs, noise models, depth estimation |
| 4 | אלגוריתמי SLAM ביומימטיים | 3–4 | EKF-SLAM, Graph-SLAM, Neural SLAM survey |
| 5 | ארכיטקטורת היתוך החישנים | 3–4 | Bayesian fusion, Kalman, DNN fusion heads |
| 6 | האלגוריתם הביומימטי המוצע | 3–4 | Full system description, pseudocode |
| 7 | NavigatorCrew — עיצוב ומימוש | 2–3 | Agent system, CrewAI code, Streamlit UI |
| 8 | תוצאות סימולציה וניתוח | 3–4 | RMSE/ATE/RPE tables, 3D trajectory, heatmap |
| 9 | סיכום, מגבלות ועתיד | 1–2 | Conclusions, limitations, future directions |
| Refs | ביבליוגרפיה | 1–2 | ≥ 15 BibTeX entries |

**Total target**: 28–32 raw pages → trimmed to 25–30

---

## 7. Required Mathematical Content

| Equation | Chapter | Description |
|---|---|---|
| LFM pulse $s(t)$ | 2 | Linear Frequency Modulated pulse definition |
| Matched-filter $y(\tau)$ | 2 | Cross-correlation output |
| Range resolution $\Delta r = c/2B$ | 2 | Sonar range accuracy |
| EKF predict step | 4 | State prediction with Jacobian |
| EKF update step (Kalman gain) | 4 | Measurement update |
| Bayesian fusion $p(x|z_1,z_2,z_3)$ | 5 | Multi-modal posterior |
| RMSE formula | 8 | Localization error metric |
| ATE / RPE metrics | 8 | Trajectory evaluation |

---

## 8. Memory Architecture

```python
crew = Crew(
    memory=True,
    embedder=get_embedder_config()   # OpenAI or HuggingFace fallback
)
```

| Layer | Content | Benefit |
|---|---|---|
| Short-term | Research summaries within one run | Research → Writing handoff |
| Long-term (ChromaDB) | SLAM papers, sensor specs, formulas | Cross-run knowledge retention |
| Entity memory | Algorithm names, sensor models, paper authors | Consistent citation and terminology |

---

## 9. Repository Structure

```
assignment3/
+-- .env                          (gitignored)
+-- .env.example
+-- .gitignore
+-- requirements.txt
+-- README.md
+-- app.py                        (Streamlit UI)
+-- main.py                       (CLI)
+-- src/
|   +-- config.py                 (paths, keys, logging, embedder)
|   +-- agents/
|   |   +-- navigation_director.py
|   |   +-- slam_researcher.py
|   |   +-- visualization_engineer.py
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
|   +-- main.tex                  (XeLaTeX master)
|   +-- chapters/
|   |   +-- cover.tex
|   |   +-- abstract.tex
|   |   +-- ch01_intro.tex        (done — formulas + placeholders)
|   |   +-- ch02_bio_basis.tex
|   |   +-- ch03_sensors.tex
|   |   +-- ch04_slam.tex
|   |   +-- ch05_fusion.tex
|   |   +-- ch06_algorithm.tex
|   |   +-- ch07_our_system.tex
|   |   +-- ch08_results.tex
|   |   +-- ch09_conclusion.tex
|   +-- figures/                  (9 PNG files — VisualizationEngineer output)
|   +-- references.bib            (≥ 15 entries)
+-- outputs/                      (gitignored for PDFs)
+-- tests/
+-- docs/
    +-- PRD.md
    +-- TODO.md
    +-- course_summary.md
```

---

## 10. Success Metrics

| Requirement | Criterion | Verification |
|---|---|---|
| End-to-end run | crew.kickoff() completes | pytest tests/test_crew.py |
| External tools ≥ 2 | Serper + ArXiv return real results | pytest tests/test_tools.py |
| Memory active | .chroma/ exists after run | os.path.exists check |
| 3D trajectory figure | fig_trajectory_3d.png in figures/ | ls + visual check |
| Sensor fusion heatmap | fig_sensor_fusion_heatmap.png exists | ls + visual check |
| Paper 25–30 pages | PDF page count in range | pdfinfo main.pdf |
| XeLaTeX compiles | Zero critical errors | xelatex exit code 0 |
| Hebrew RTL | Text direction correct | Visual PDF inspection |
| ≥ 8 equations | Equation environments present | grep "begin{equation}" |
| ≥ 6 figures | Figure environments present | grep "begin{figure}" |
| ≥ 4 tables | Table environments present | grep "begin{table}" |
| Bibliography ≥ 15 | Entry count in .bib | grep -c "@" references.bib |
| No hardcoded keys | No secrets in src/ | grep -r "sk-ant" src/ |
| All tests pass | 0 failures | pytest tests/ -v |

---

## 11. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| 3D matplotlib plots slow/fail | Medium | High | 45s timeout; fallback to 2D projection |
| XeLaTeX Hebrew font missing | High | High | Provide font install script; fallback font list in main.tex |
| Agent generates non-compiling LaTeX | High | Medium | QualityEditor reviews; manual LaTeX fix fallback |
| ArXiv robotics papers irrelevant | Low | Medium | Category filter (cs.RO); keyword refinement |
| Paper under 25 pages | Medium | High | QualityEditor page-count check triggers "expand" subtask |
| EKF equations LLM-hallucinated | Medium | High | SLAMResearcher verifies vs Thrun textbook; manual review |
| ChromaDB corruption | Low | Low | Memory rebuild from research .md files |
| OpenAI key missing (embeddings) | Medium | Low | HuggingFace local fallback in get_embedder_config() |
