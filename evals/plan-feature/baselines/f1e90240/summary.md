## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 13/15 | 2 | 87% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Three rationales fail to name specific file paths as required by convention-applicability-rules.md ('Every applicability rationale must name at least one specific file from the task's Files to Modify or Files to Create'): (1) Task 2: 'Applies: task modifies service code that uses query helpers matching the convention's query helpers scope.' — uses generic 'service code' instead of naming 'modules/fundamental/src/sbom/service/sbom.rs'. (2) Task 3: 'Applies: task creates an endpoint file matching the convention's caching scope.' — uses generic 'an endpoint file' instead of naming 'modules/fundamental/src/sbom/endpoints/advisory_summary.rs'. (3) Task 3: 'Applies: task creates handler code matching the convention's error handling scope.' — uses generic 'handler code' instead of naming a specific file. The convention-applicability-rules.md Common Mistakes section explicitly prohibits this: 'Do NOT skip the file-type match. Every applicability rationale must name at least one specific file.'"

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "Every generated task description contains a Repository section with a single repository name (not multiple repos per task)"
  **Evidence:** "Task 1 (task-1-create-feature-branch.md) has '## Repository\n\ntrustify-backend, trustify-ui' listing two repositories. Task 9 (task-9-merge-feature-branch.md) has '## Repository\n\ntrustify-backend, trustify-ui' listing two repositories. The task-description-template.md rule states 'Repository must be a single repository per task'. Tasks 2-8 correctly have single repositories, but the assertion requires EVERY task to comply."

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the corresponding mock repository structure manifests (repo-backend.md or repo-frontend.md), not invented paths"
  **Evidence:** "Task 4 lists 'tests/api/mod.rs or test harness' under Files to Modify, but repo-backend.md does not include tests/api/mod.rs in its directory tree. The manifest lists tests/api/sbom.rs, tests/api/advisory.rs, and tests/api/search.rs but no mod.rs file. All other Files to Modify paths are verified in the manifests: modules/fundamental/src/sbom/model/mod.rs, modules/fundamental/src/sbom/service/mod.rs, modules/fundamental/src/sbom/endpoints/mod.rs (all in repo-backend.md); src/api/models.ts, src/api/rest.ts, src/routes.tsx, tests/mocks/handlers.ts (all in repo-frontend.md). Files to Create paths follow manifest directory patterns correctly."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No inapplicable conventions are listed with 'Not applicable' annotations (good). However, several rationales fail the prescribed format requirement by substituting generic descriptions for specific file references. The rules document states 'Every applicability rationale must name at least one specific file from the task's Files to Modify or Files to Create.' Violations: Task 2 error handling says 'Applies: task modifies service code matching...' instead of naming 'modules/fundamental/src/sbom/service/license_report.rs'; Task 2 query helpers says 'Applies: task modifies service code that performs database queries matching...'; Task 3 error handling says 'Applies: task modifies endpoint handler code matching...'; Task 3 framework says 'Applies: task modifies Axum handler code matching...'. These use descriptive terms ('service code', 'endpoint handler code', 'Axum handler code') instead of specific file paths from the task's Files to Modify/Create sections."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (non-documentation) are missing required sections. task-1-create-feature-branch.md lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. task-8-merge-feature-branch.md also lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Implementation tasks 2-6 have all required sections. Documentation task-7 has all required exempt sections (Repository, Target Branch, Description, Acceptance Criteria, Test Requirements)."

</details>

**Pass rate:** 94% · **Tokens:** 41,373 · **Duration:** 219s

**Baseline** (`1dab64e0`): 98% · 79,848 tokens · 368s

