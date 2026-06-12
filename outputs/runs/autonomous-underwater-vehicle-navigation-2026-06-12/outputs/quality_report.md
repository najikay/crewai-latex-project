# Quality Gate Report

**Verdict:** FAIL
**Score:** 74/100
**Threshold:** 90
**Failed Sections:** ['methodology']

## Issues Found

- ch02_bio_basis.tex: citations=0<2
- ch03_sensors.tex: citations=0<2
- ch05_fusion.tex: citations=0<2, words≈1360<1400
- ch06_algorithm.tex: citations=1<3
- ch07_oursystem.tex: citations=0<2, words≈1353<1600
- ch08_results.tex: citations=2<3, words≈1571<1800
- ch09_conclusion.tex: citations=0<1

## Per-Chapter Thresholds

- Default: eq>=2, fig>=1, sub>=3, cite>=2, words>=1400
- abstract.tex: eq>=0, fig>=0, sub>=0, cite>=0, words>=80
- ch01_intro.tex: eq>=1, fig>=0
- ch06_algorithm.tex: eq>=3, sub>=5, cite>=3, words>=1800
- ch07_oursystem.tex: sub>=4, words>=1600
- ch08_results.tex: sub>=5, cite>=3, words>=1800
- ch09_conclusion.tex: eq>=0, fig>=0, sub>=2, cite>=1, words>=700
- references.bib: >=10 entries
- Missing figure files: <=-20 total penalty (capped)

```json
{
  "verdict": "FAIL",
  "score": 74,
  "failed_sections": ["methodology"]
}
```
