## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 13/14 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (non-documentation) are missing required sections. Task 1 (task-1-create-feature-branch.md) lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 8 (task-8-merge-feature-branch.md) also lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. The assertion exempts only documentation tasks from these requirements; bookend tasks are classified as 'Bookend (create-branch)' and 'Bookend (merge-branch)' per summary-comment.md, not as documentation tasks. Implementation tasks 2-6 correctly include all required sections. Documentation task 7 correctly includes Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation, non-testing task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks (tasks whose filename or description indicates doc-only scope) and testing tasks (tasks whose filename or description indicates cross-cutting testing scope) are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (Task 1: task-1-create-feature-branch.md and Task 10: task-10-merge-feature-branch.md) are not documentation or testing tasks, yet they lack 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 1 only has Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. Task 10 similarly lacks Files to Modify/Create and Implementation Notes. The assertion exempts only documentation and testing tasks; bookend tasks are not exempted. Implementation tasks 2,3,5,6,7,8 all have the required sections. Task 4 (testing) and Task 9 (documentation) correctly use their exemptions while including the required base sections."

</details>

**Pass rate:** 98% · **Tokens:** 85,343 · **Duration:** 452s

**Baseline** (`4d9733a7`): 100% · 76,410 tokens · 336s

