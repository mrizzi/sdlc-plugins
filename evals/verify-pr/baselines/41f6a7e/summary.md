## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "report.md line 6 shows: '| Root-Cause Investigation | N/A | Review feedback is repo-specific (Markdown-heavy repository); convention gap, not a skill deficiency |'. The verdict is N/A, which directly contradicts the assertion requirement that the verdict is 'not N/A'. The root-cause investigation did not process the eval failure sub-tasks through the investigation pipeline."

</details>

**Pass rate:** 98% · **Tokens:** 69,884 · **Duration:** 260s

**Baseline** (`4073ac0`): 98% · 60,000 tokens · 300s

