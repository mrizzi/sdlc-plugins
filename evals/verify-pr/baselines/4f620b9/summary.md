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
  **Evidence:** "Report line 6: 'Root-Cause Investigation | N/A | Review feedback is a feature enhancement request, not a defect requiring root-cause investigation'. The Root-Cause Investigation verdict is N/A, indicating the investigation pipeline did NOT process the eval failure sub-tasks. The N/A reason references only the review feedback (feature enhancement), not the eval regression sub-task."

</details>

**Pass rate:** 98% · **Tokens:** 74,715 · **Duration:** 312s

**Baseline** (`d37fb89`): 100% · 65,340 tokens · 273s

