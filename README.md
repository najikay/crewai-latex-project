# NavigatorCrew

An autonomous multi-agent research platform that takes a `--topic` argument and produces a complete, compiled IEEE-formatted academic paper in XeLaTeX (Hebrew/English bilingual).

Built for Assignment 3 — *Orchestration of AI Agents*, Semester B 2026.

---

## Architecture

```
main.py --topic "..."
        │
        ▼
┌─────────────────────────────────────────────┐
│           LangGraph State Machine           │
│                                             │
│  [run_main_pipeline]                        │
│         │                                   │
│         ▼                                   │
│  [run_quality_gate] ──PASS──► [END]         │
│         │                                   │
│        FAIL                                 │
│         ▼                                   │
│  [run_remediation] ──────────► [run_quality_gate]
│         (max 2 cycles)                      │
└─────────────────────────────────────────────┘
        │
        ▼
  CrewAI Sequential Crew (inside each node)
  ┌──────────────────────────────────────────┐
  │  1. NavigationDirector   → paper_outline │
  │  2. SLAMResearcher       → research_briefs│
  │  3. VisualizationEngineer → 9 PNG figures │
  │  4. LaTeXAuthor          → .tex + .bib   │
  │  5. QualityEditor        → quality_report│
  └──────────────────────────────────────────┘
        │
        ▼
  XeLaTeX compiler (automatic)
        │
        ▼
  outputs/NavigatorCrew_paper.pdf
```

### Key Design Decisions

| Feature | Implementation |
|---|---|
| **Feedback loop** | LangGraph conditional edge: quality score < 75 → targeted remediation sub-crew |
| **Fault tolerance** | Every task writes an `output_file`; `--resume` skips completed tasks |
| **Cost optimization** | DeepSeek V3 (~$0.03/full run vs ~$3+ with GPT-4) |
| **Strict tools fix** | Patched `crewai/utilities/agent_utils.py` — hardcoded `strict: True` → `False` |
| **Bilingual LaTeX** | XeLaTeX + polyglossia + bidi; correct package load order (bidi must be last) |

---

## Setup

### 1. Prerequisites

- Python 3.11+
- XeLaTeX: `sudo apt install texlive-xetex texlive-lang-other`
- bidi (installed automatically via `make setup` or `tlmgr`)

### 2. Install

```bash
git clone https://github.com/najikay/crewai-latex-project
cd crewai-latex-project
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
cp .env.example .env
# Edit .env:
```

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...     # or leave blank if using DeepSeek
SERPER_API_KEY=...               # free at serper.dev

# DeepSeek (recommended — much cheaper, fully compatible)
DEEPSEEK_API_KEY=sk-...          # get at platform.deepseek.com
ACTIVE_PROVIDER=deepseek         # switch: "anthropic" | "deepseek"
```

### 4. Install bidi (first time only)

```bash
tlmgr init-usertree
tlmgr --repository http://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2023/tlnet-final install bidi
```

And register Windows fonts with fontconfig (WSL only):

```bash
mkdir -p ~/.config/fontconfig
cat > ~/.config/fontconfig/fonts.conf << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>/mnt/c/Windows/Fonts</dir>
</fontconfig>
EOF
fc-cache -f ~/.config/fontconfig
```

---

## Usage

```bash
source venv/bin/activate

# Full run — generates content + compiles PDF
python main.py --topic "Bat-Inspired Drone Navigation via Bio-Mimetic Sensor Fusion"

# Resume after crash (skips completed tasks)
python main.py --topic "..." --resume

# Content only, skip PDF compilation
python main.py --topic "..." --no-pdf
```

Output is written to:
```
outputs/
├── NavigatorCrew_paper.pdf    ← final compiled paper
├── paper_outline.md           ← Director's decomposition
├── research_briefs.md         ← Researcher's findings
├── figures_manifest.md        ← figure metadata
├── quality_report.md          ← Editor's structured review (JSON verdict)
└── token_report.md            ← cost accounting

latex/
├── main.tex                   ← master document
├── chapters/                  ← 9 chapter files + abstract + cover
├── figures/                   ← 9 PNG figures (300 DPI)
├── references.bib             ← 14 BibTeX entries
├── IEEEtran.cls               ← IEEE document class
└── IEEEtran.bst               ← IEEE bibliography style
```

---

## Agents

| Agent | Model | Tools | Role |
|---|---|---|---|
| NavigationDirector | DeepSeek V3 | FileWriter | Decomposes topic → 7 sub-domains, writes outline |
| SLAMResearcher | DeepSeek V3 | Serper, ArXiv, WebScraper | Deep literature research, produces briefs |
| VisualizationEngineer | DeepSeek V3 | CodeExecutor, FileWriter | Generates 9 IEEE-standard figures via matplotlib |
| LaTeXAuthor | DeepSeek V3 | FileWriter, FileReader | Writes bilingual XeLaTeX chapters + BibTeX |
| QualityEditor | DeepSeek V3 | FileReader | Peer review with structured JSON verdict |

---

## Originality Contributions

### AF-AFC Controller (Acoustic Fovea — Adaptive Frequency Controller)

The paper's central original contribution, derived from the biology of *Rhinolophus ferrumequinum* (horseshoe bats):

> Horseshoe bats lower their emission frequency by exactly the expected Doppler shift so the echo always lands at their cochlear "acoustic fovea" — a hyperacuity zone covering 30% of the basilar membrane tuned to 83 kHz.

We translate this into a closed-loop drone sonar controller:

$$f_{e,k}(t) = f_0\!\left(1 - \frac{2\hat{v}_{r,k}(t)}{c}\right) + K_p\varepsilon_k(t) + K_i\int_0^t \varepsilon_k(\tau)\,d\tau$$

where $\hat{v}_{r,k}$ comes from the EKF posterior and $\varepsilon_k$ is the foveal error (echo frequency deviation from $f_0$). This eliminates Doppler smearing in range resolution without sacrificing velocity measurement.

---

## Cost

| Provider | Model | Full Run Cost |
|---|---|---|
| DeepSeek | deepseek-chat (V3) | ~$0.03 |
| Anthropic | claude-haiku-4-5 | ~$0.15 |
| Anthropic | claude-sonnet-4 | ~$1.50 |

---

## Project Structure

```
.
├── main.py                    ← entry point
├── requirements.txt
├── .env.example
├── src/
│   ├── config.py              ← LLM init, model switching, logging
│   ├── crew.py                ← CrewAI assembly
│   ├── agents/                ← 5 agent factory functions
│   ├── tasks/                 ← task factories + remediation task
│   ├── tools/                 ← ArXiv, Serper, WebScraper, FileWriter, CodeExecutor
│   ├── graph/                 ← LangGraph state machine (state, nodes, graph)
│   └── utils/                 ← TokenAccountant
├── latex/                     ← generated LaTeX source + figures
├── outputs/                   ← generated research artifacts + final PDF
├── docs/                      ← PLAN.md, PRD.md, TODO.md
└── tests/                     ← agent and tool unit tests
```
