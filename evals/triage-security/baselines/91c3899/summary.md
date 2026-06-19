## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 9/10 | 1 | 90% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 5/5 | 0 | 100% |
| eval-6 | 5/5 | 0 | 100% |

**Pass rate:** 98% · **Tokens:** 34,099 · **Duration:** 84s

**Baseline** (`796c88c`): 100% · 0 tokens · 0s

### Failures

**eval-1 assertion 3** — *Version impact table includes ALL versions from the security-matrix.md supportability matrix — no versions are skipped (Important Rule 4)*

The version impact table only included 2.2.x stream versions (scoped by the `[rhtpa-2.2]` issue suffix). The 2.1.x versions (2.1.0, 2.1.1) were mentioned in a cross-stream note but not in the main table. The assertion requires all 7 versions from both streams to appear, consistent with Important Rule 4: "Check ALL supported versions."
