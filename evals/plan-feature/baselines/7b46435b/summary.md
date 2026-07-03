## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 13/15 | 2 | 87% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (task-1-create-feature-branch.md and task-8-merge-feature-branch.md) are non-documentation tasks but lack 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. The assertion only exempts documentation tasks from these requirements, not bookend tasks. Implementation tasks 2-6 have all required sections. Documentation task-7 has the required exempt set (Repository, Target Branch, Description, Acceptance Criteria, Test Requirements)."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment content found in any output file. None of the 8 task files, impact-map.md, or summary-comment.md contain the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format or any convention-related sections. The feature is entirely absent from the outputs."

</details>

**Pass rate:** 98% · **Tokens:** 81,180 · **Duration:** 334s

**Baseline** (`9a6ca95e`): 96% · 51,739 tokens · 250s

