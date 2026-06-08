# Token Budget — NavigatorCrew

## Provider: DeepSeek V3 (`openai/deepseek-chat`)

| Tier       | Price (input) | Price (output) |
|------------|--------------|----------------|
| DeepSeek V3 | $0.27 / 1M   | $1.10 / 1M     |

---

## Per-Run Budget Estimate

| Agent               | Avg Input Tokens | Avg Output Tokens | Est. Cost |
|---------------------|-----------------|-------------------|-----------|
| ResearchDirector    | 3,000            | 2,000             | $0.003    |
| SLAMResearcher      | 15,000           | 8,000             | $0.013    |
| VisualizationEng.   | 8,000            | 5,000             | $0.008    |
| LaTeXAuthor         | 25,000           | 40,000            | $0.051    |
| **Total per run**   | **~51,000**      | **~55,000**       | **~$0.07**|

> Quality gate is now programmatic — no LLM tokens used there.

### Max-cost scenario (remediation × 2 loops)

| Component        | Extra Tokens | Extra Cost |
|------------------|-------------|------------|
| Remediation run 1 | ~25,000 in / ~20,000 out | ~$0.029 |
| Remediation run 2 | ~25,000 in / ~20,000 out | ~$0.029 |
| **Max total**     | ~125,000 in / ~95,000 out | **~$0.14** |

---

## Actual Run History

| Date       | Provider   | Input Tok | Output Tok | Cost   | Notes                          |
|------------|------------|-----------|------------|--------|-------------------------------|
| 2026-06-07 | Anthropic  | ~400,000  | ~120,000   | ~$3.00 | Rate-limited × 73; Haiku only  |
| 2026-06-08 | DeepSeek   | ~51,000   | ~55,000    | ~$0.07 | First DeepSeek run (8 pages)   |

> Actual token counts from `outputs/token_report.md` after each run.

---

## Budget Guardrails

Set in `.env`:
```
DEEPSEEK_API_KEY=sk-...
ACTIVE_PROVIDER=deepseek
```

Hard limits enforced in `src/config.py`:
- `AGENT_MAX_ITER` caps each agent's iteration count
- `MAX_REMEDIATIONS = 2` caps LangGraph feedback loops
- `max_tokens=8192` per LLM call

## Switching Providers

| Scenario           | Provider    | Change in .env              |
|--------------------|-------------|----------------------------|
| Normal runs        | DeepSeek V3 | `ACTIVE_PROVIDER=deepseek` |
| Anthropic (backup) | Claude Haiku 4.5 | `ACTIVE_PROVIDER=anthropic` |
