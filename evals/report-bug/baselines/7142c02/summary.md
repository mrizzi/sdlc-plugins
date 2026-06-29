## Eval Results: report-bug

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 9/9 | 0 | 100% |
| eval-3 | 6/6 | 0 | 100% |
| eval-4 | 11/12 | 1 | 92% |
| eval-5 | 7/7 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "outputs/jira-create.md includes the label 'ai-generated-jira'"
  **Evidence:** "jira-create.md does not contain the string 'ai-generated-jira' anywhere. The file lists project_key, issue_type_id, summary, and description fields but no labels field."

</details>

**Pass rate:** 98% · **Tokens:** 18,905 · **Duration:** 32s

**Baseline** (`1dfe8af`): 100% · 19,021 tokens · 31s

