## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 13/14 | 1 | 93% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 6/10 | 4 | 60% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "review-30002.md classifies comment 30002 as 'suggestion' and explicitly states 'The suggestion remains classified as a suggestion -- no sub-task is created.' report.md confirms: '30002 | migration/src/m0042_sbom_soft_delete/mod.rs:14 | suggestion | No sub-task (no convention match)'. No subtask-30002.md file exists in the outputs directory. The assertion requires a sub-task regardless of path, but none was created."

</details>

<details>
<summary>eval-6: 4 failing assertions</summary>

- **Assertion:** "Test Quality verdict is WARN (not N/A or PASS) — the Eval Quality component is WARN because eval-3 has 2 failing assertions, and WARN in any component produces WARN in the combined Test Quality verdict"
  **Evidence:** "The report's Test Quality row shows verdict 'N/A', not 'WARN'. Exact text: '| Test Quality | N/A | Eval Quality: WARN (eval-3 has 2 failing assertions at 85% pass rate)...'. While the Eval Quality component is correctly identified as WARN, the combined Test Quality verdict is N/A instead of being elevated to WARN as required by the assertion."

- **Assertion:** "An eval failure sub-task is created for failing eval-3 — a sub-task description file targets eval-3 assertion failures and includes the failing assertion text and evidence"
  **Evidence:** "The only sub-task file is subtask-1.md, which targets reviewer-b's code change request about Markdown documentation coverage rules. Its description is 'Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent.' There is no sub-task file targeting eval-3 assertion failures. No sub-task mentions eval-3, convention upgrade eligibility evaluation, or sub-task creation for comment 30002."

- **Assertion:** "Sub-task descriptions include Review Context with the failing assertion text and evidence from the eval review — the Review Context section quotes the two failing assertions about convention upgrade eligibility and sub-task creation, including the evidence text explaining what was missing"
  **Evidence:** "The only sub-task (subtask-1.md) has a Review Context section that quotes reviewer-b's comment about Markdown documentation coverage, not eval-3 failing assertions. There is no sub-task with Review Context quoting the two failing assertions about convention upgrade eligibility and sub-task creation. The eval-3 assertion details only appear in the report's Test Quality row, not in any sub-task description."

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "The report shows '| Root-Cause Investigation | N/A | Review feedback is repo-specific (Markdown-centric repository); convention gap, not a skill deficiency |'. The verdict is N/A, indicating the investigation pipeline did not process any eval failure sub-tasks. This is consistent with the absence of eval failure sub-tasks (assertion 5 also failed)."

</details>

**Pass rate:** 92% · **Tokens:** 55,871 · **Duration:** 158s

**Baseline** (`0adea80`): 100% · 57,632 tokens · 179s

