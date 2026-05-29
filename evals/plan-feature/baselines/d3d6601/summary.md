## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 9/11 | 2 | 82% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 10/12 | 2 | 83% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No output file contains the string 'Description digest' or '[sdlc-workflow]' or 'sha256:'. The task files contain only the task descriptions themselves with no digest comments. The outputs directory contains only impact-map.md and 5 task files, none of which include a description digest comment."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No task references CONVENTIONS.md sections with the 'Per CONVENTIONS.md' pattern. The Implementation Notes sections contain implementation guidance but no convention-aware enrichment with applicability rationales as required by convention-applicability-rules.md."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "None of the output files contain any digest comment or SHA-256 hash. The outputs directory contains only impact-map.md and 4 task description files (task-1 through task-4). No file contains the marker '[sdlc-workflow] Description digest:' or any SHA-256 hash string. There are no separate comment files or digest records."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task's Implementation Notes contain the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The tasks reference 'docs/constraints.md' sections (e.g., 'Per docs/constraints.md §2 (Commit Rules)', 'Per docs/constraints.md §5 (Code Change Rules)', 'Per docs/constraints.md §5.4') but these are not CONVENTIONS.md references with applicability rationales. There is no evidence that convention-applicability-rules.md was followed: no 'Applies:' rationale lines appear in any task description, and no CONVENTIONS.md sections are referenced with the prescribed format."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No digest comments found in any output file. Searched all files in /tmp/plan-feature-eval-baseline/eval-3/outputs/ for 'digest', 'sha256', and 'sdlc-workflow' — no matches. The output files contain only the task descriptions and impact map, with no evidence of description digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task. Searched all output files for 'CONVENTIONS', 'Per CONVENTIONS', and 'Applies:' — found only incidental mentions of 'conventions' in the sense of 'naming conventions' (e.g., task-2: 'reference the severity field type and naming convention', task-5: 'following the naming and style conventions of existing interfaces'). No task contains the prescribed 'Per CONVENTIONS.md §...' format or the 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. The convention-applicability-rules.md requires that applicable conventions include this rationale, and inapplicable ones be excluded entirely. The output shows no evidence of CONVENTIONS.md being consulted or applicability rules being applied."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 5 task descriptions contain any 'Per CONVENTIONS.md' references or 'Applies:' rationale lines in the prescribed format. The repo-backend.md fixture indicates the trustify-backend repository has a CONVENTIONS.md file with key conventions (Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching). The task Implementation Notes reference existing patterns informally (e.g., 'Follow the existing model pattern established in...', 'Follow the service pattern established in...') but do not use the convention-aware enrichment format prescribed by convention-applicability-rules.md. No evidence of convention applicability validation or prescribed-format rationale ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;') was found in any task file."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Bookend tasks are missing required sections. task-1-create-feature-branch.md lacks: Files to Modify, Files to Create, and Implementation Notes sections. task-5-merge-feature-branch.md also lacks: Files to Modify, Files to Create, and Implementation Notes sections. Intermediate tasks (2, 3, 4) all contain the required sections: Repository, Target Branch, Description, Files to Modify and/or Files to Create, Implementation Notes, Acceptance Criteria, and Test Requirements."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention references or applicability rationales appear anywhere in the task files. None of the Implementation Notes sections in tasks 2, 3, or 4 contain 'Per CONVENTIONS.md' references or 'Applies:' rationale lines as prescribed by convention-applicability-rules.md. The repo structure manifest (repo-backend.md) shows a CONVENTIONS.md file exists in the repository root, yet no evidence of convention-aware enrichment processing is present in any output file. Without any evidence that conventions were evaluated for applicability, the assertion cannot be marked as PASS."

</details>

**Pass rate:** 84% · **Tokens:** 52,160 · **Duration:** 186s

**Baseline** (`fc7c4cb`): 97% · 58,088 tokens · 285s

