## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-2 | 10/10 | 0 | 100% |
| eval-3 | 13/13 | 0 | 100% |
| eval-4 | 9/9 | 0 | 100% |
| eval-5 | 8/9 | 1 | 89% |

### Failed Assertions

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "The test change classification is produced by the Style/Conventions sub-agent (which spawns a test classification sub-agent for modified files) — the classification verdict is attributed to the Style/Conventions domain in the report"
  **Evidence:** "No reference to 'Style/Conventions' domain, sub-agent, or any domain attribution appears anywhere in report.md or any criterion file. The Test Change Classification row in the report table (line 14) has no domain attribution. The detailed 'Test Change Classification Detail' section (lines 21-48) presents the classification directly without attributing it to any specific domain or sub-agent. Searched all 6 output files — zero mentions of 'Style', 'Conventions', 'sub-agent', or 'domain'."

</details>

**Pass rate:** 98% · **Tokens:** 58,919 · **Duration:** 172s

**Baseline** (`f31ccb2`): 98% · 30,102 tokens · 193s

