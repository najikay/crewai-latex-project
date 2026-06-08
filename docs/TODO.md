# NavigatorCrew — TODO / Status

## COMPLETED ✅

### System Architecture
- [x] CrewAI sequential pipeline (5 agents, 5 tasks)
- [x] LangGraph state machine wrapping CrewAI (feedback loop / remediation)
- [x] `--resume` flag with task-level checkpointing via `output_file`
- [x] `--no-pdf` flag for content-only runs

### LLM Configuration
- [x] Migrated from Anthropic Claude to DeepSeek V3 (OpenAI-compatible API)
- [x] Fixed CrewAI v1.14.6 `strict tools` bug (patched `agent_utils.py`)
- [x] Model tiering: SONNET_LLM / HAIKU_LLM both point to deepseek-chat
- [x] `ACTIVE_PROVIDER` env switch: `anthropic` | `deepseek`

### Content
- [x] Acoustic Fovea + AF-AFC controller section injected (Ch. 4)
- [x] BibTeX citations added: Schnitzler1968DSC, Schuller1974DSC + 12 others
- [x] 9/9 figures generated (PNG, 300 DPI)
- [x] All 9 chapter .tex files generated
- [x] references.bib with 14 real BibTeX entries

### LaTeX Compilation
- [x] IEEEtran.cls and IEEEtran.bst downloaded to latex/
- [x] bidi package installed via tlmgr (user tree)
- [x] Windows fonts registered with fontconfig (David, Miriam, Times NR, Arial)
- [x] Package load order fixed (all packages before `\setmainlanguage{hebrew}`)
- [x] `\textlatin` → `\foreignlanguage{english}` throughout
- [x] PDF compiles clean: 8 pages, 2.9 MB
- [x] Automatic PDF compilation integrated into `main.py`

### Project Hygiene
- [x] Junk files deleted (smoke_test, run_log, GEMINI.md, latex/venv/, latex/review/)
- [x] LaTeX aux files excluded from git
- [x] .gitignore updated
- [x] Token report updated (DeepSeek costs, Anthropic failures excluded)

## REMAINING / OPTIONAL

- [ ] Add student name and institution to `latex/chapters/cover.tex`
- [ ] Expand chapter content (currently 8 pages; target 25+)
- [ ] Final README on GitHub
- [ ] Verify no API keys in git history before push
