## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-2 | 10/10 | 0 | 100% |
| eval-3 | 13/13 | 0 | 100% |
| eval-4 | 9/9 | 0 | 100% |
| eval-5 | 8/9 | 1 | 89% |

**Pass rate:** 98% · **Tokens:** 30,103 · **Duration:** 193s

**Baseline** (`0b0c981`): 98% · 32,679 tokens · 172s

### Failures

**eval-5, assertion 8:** "The test change classification is produced by the Style/Conventions sub-agent (which spawns a test classification sub-agent for modified files) — the classification verdict is attributed to the Style/Conventions domain in the report"
- **Evidence:** Test Change Classification appears as its own top-level section in the report, separate from the Style/Conventions section. The classification is not attributed to or nested under the Style/Conventions domain.
