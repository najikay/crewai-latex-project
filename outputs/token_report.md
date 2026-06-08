# NavigatorCrew — Token & Cost Report
Generated: 2026-06-08 | Final Clean Run

## Model Configuration
| Role | Model | Provider |
|------|-------|----------|
| All Agents (Tier 1) | deepseek-chat (DeepSeek V3) | DeepSeek |
| All Agents (Tier 2) | deepseek-chat (DeepSeek V3) | DeepSeek |

> **Note on provider history:** During development, Anthropic Claude models were
> tested but encountered API-level restrictions (`strict tools` not supported by
> Claude Sonnet 4 / Claude Haiku 4.5 in CrewAI v1.14.6's native tool-calling mode).
> The system was migrated to DeepSeek V3, which is fully compatible and significantly
> more cost-effective. Anthropic API costs incurred during debugging are excluded
> from this report as they were infrastructure failures, not research compute.

## DeepSeek V3 Pricing Reference
| Metric | Rate |
|--------|------|
| Input tokens | $0.27 / 1M tokens |
| Output tokens | $1.10 / 1M tokens |
| Cache hit (input) | $0.07 / 1M tokens |

## Estimated Usage — Production Run
| Phase | Agent | Est. Input Tokens | Est. Output Tokens |
|-------|-------|------------------|--------------------|
| Outline | NavigationDirector | ~2,000 | ~1,500 |
| Research | SLAMResearcher | ~8,000 | ~6,000 |
| Figures | VisualizationEngineer | ~4,000 | ~3,000 |
| LaTeX | LaTeXAuthor | ~12,000 | ~10,000 |
| Review | QualityEditor | ~8,000 | ~2,000 |
| **Total** | | **~34,000** | **~22,500** |

## Estimated Cost
| Item | Tokens | Cost |
|------|--------|------|
| Input | 34,000 | $0.009 |
| Output | 22,500 | $0.025 |
| **Grand Total** | **56,500** | **~$0.034** |

> Full run cost: approximately **3.4 cents** using DeepSeek V3.

## LangGraph Feedback Loop
- Remediation cycles triggered: **0** (quality passed on first attempt)
- Quality score: **100/100**
