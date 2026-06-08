# NavigatorCrew — Implementation Plan (v5.0)

## Architecture Summary

```
main.py  →  LangGraph pipeline  →  CrewAI 4-agent crew  →  XeLaTeX PDF
```

**LangGraph state machine** wraps CrewAI:
1. `run_main_pipeline` — runs 4-agent CrewAI crew sequentially
2. `run_quality_gate` — programmatic LaTeX checker (no LLM, no loop risk)
3. `run_remediation` — targeted fix crew (max 2 cycles)
4. `→ END` — PDF compilation via `xelatex → bibtex → xelatex × 2`

---

## Phase 1: Architecture (COMPLETE)

- [x] Sequential CrewAI process (`Process.sequential`)
- [x] Model tiering in `src/config.py` (DeepSeek V3 primary, Anthropic fallback)
- [x] Task-level checkpointing via `output_file`
- [x] LangGraph state machine with feedback loop (max 2 remediation cycles)
- [x] PDF auto-compilation in `main.py`
- [x] DeepSeek V3 integration (OpenAI-compatible, ~$0.07/run)
- [x] CrewAI v1.14.6 `strict=True` bug patched in venv

## Phase 2: Quality & Content (COMPLETE)

- [x] Programmatic quality gate (replaces looping LLM reviewer)
  - Checks: equation count, figure count, subsection count, word estimate
  - Checks: required BibTeX keys, no placeholders, no em dashes, no `\begin{center}`
- [x] `cover.tex` protected from agent overwrite (XeLaTeX crash fix)
- [x] Required BibTeX keys baked into agent prompts (14 keys)
- [x] Em dash prohibition in LaTeX author goal
- [x] 25–30 page target in all task descriptions
- [x] Token budget documented in `docs/BUDGET.md`

## Phase 3: Current Run Targets

- [ ] Paper reaches 25–30 pages in PDF output
- [ ] All chapters pass programmatic quality gate (score ≥ 75)
- [ ] `references.bib` contains all 14 required keys
- [ ] No LaTeX compilation errors (xelatex exits 0)
- [ ] Push clean version to GitHub

## Phase 4: Future Improvements (Backlog)

- [ ] Add ArXiv search tool to researcher for real citations
- [ ] Add a post-processing hook that auto-restores references.bib
  if the agent generates wrong keys
- [ ] Soft fact-check: verify numeric claims (34% improvement, etc.)
  against simulation data in outputs/
- [ ] Consider a separate `CitationFixer` agent that runs after LaTeXAuthor
  to verify and patch references.bib
- [ ] Token-budget enforcement: abort run if projected cost exceeds threshold
