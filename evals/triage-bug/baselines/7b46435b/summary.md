# triage-bug Eval Results

## Run Summary

| Metric | Current | Baseline (`9a6ca95e`) | Delta |
|--------|---------|----------------------|-------|
| **Pass Rate** | 1.00 (18/18) | 1.00 (18/18) | — |
| **Time (mean)** | 53.19s | 76.14s | -22.95s (-30.1%) |
| **Tokens (mean)** | 20,911 | 28,763 | -7,852 (-27.3%) |

## Per-Eval Results

### Eval 1 — Standard Bug Triage (ACME-500)

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Bug parsing extracts all four required sections | PASS |
| 2 | Bug validation confirms issue type ID (10020) matches | PASS |
| 3 | Investigation identifies trailing-whitespace `line[3:]` root cause | PASS |
| 4 | Root cause comment includes what/where/how-to-verify | PASS |
| 5 | Reproducer test is FIRST acceptance criterion | PASS |
| 6 | Reproducer test is FIRST test requirement with assertion guidance | PASS |
| 7 | Bug Context section has Bug key, Steps, Expected/Actual, Root Cause | PASS |
| 8 | Target Branch set to main | PASS |
| 9 | Jira API metadata includes ai-generated-jira label | PASS |

**Result: 9/9 passed** | 23,063 tokens | 77.78s

### Eval 2 — Missing Sections Validation (ACME-501)

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Identifies missing Steps to Reproduce | PASS |
| 2 | Identifies missing Expected Result | PASS |
| 3 | Stops at Step 1 — does NOT proceed to Steps 2-5 | PASS |
| 4 | Error lists missing sections and references template path | PASS |

**Result: 4/4 passed** | 19,060 tokens | 31.28s

### Eval 3 — Decomposition Guard (ACME-502)

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Identifies two independent root causes in different modules | PASS |
| 2 | Decomposition Guard triggered (different modules/code paths) | PASS |
| 3 | Guard presents both issues with affected files/modules | PASS |
| 4 | Guard offers Proceed or Split options | PASS |
| 5 | Does NOT silently create Task — waits for user input | PASS |

**Result: 5/5 passed** | 20,610 tokens | 50.52s

## Comparison vs Baseline

Pass rate is unchanged at 100%. Token usage decreased 27.3% (28,763 → 20,911 mean) and execution time decreased 30.1% (76.14s → 53.19s mean). No regressions detected.
