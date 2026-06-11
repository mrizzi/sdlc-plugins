## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 8/8 | 0 | 100% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the four task descriptions contain convention applicability rationales in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The Implementation Notes reference docs/constraints.md sections (e.g., 'Per docs/constraints.md §2 (Commit Rules)', 'Per docs/constraints.md §5 (Code Change Rules)') but these are not CONVENTIONS.md conventions, and they do not include the required applicability rationale format. There is no evidence that CONVENTIONS.md conventions were evaluated for applicability using the convention-applicability-rules.md process, and no 'Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;.' rationale lines appear anywhere in the outputs."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention enrichment is present in any task's Implementation Notes. None of the 7 task descriptions contain 'Per CONVENTIONS.md', 'Applies:', or any convention applicability rationale in the prescribed format. The repo manifests (repo-backend.md and repo-frontend.md) both list CONVENTIONS.md in their directory trees and document key conventions (e.g., error handling, module pattern, response types for backend; mutation pattern, naming conventions for frontend). These conventions should have been evaluated for applicability and, where applicable, included with rationales. No positive evidence exists that convention-aware enrichment was performed."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 7 task files contain a convention applicability section or the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The task files contain generic references to constraints (e.g., 'Per docs/constraints.md section 2 (Commit Rules)' in task 2 line 25) but these are free-form Implementation Notes, not structured convention-applicability assessments per the shared/convention-applicability-rules.md specification. No task file validates file-type applicability or includes the prescribed rationale format."

</details>

**Pass rate:** 95% · **Tokens:** 62,477 · **Duration:** 210s

**Baseline** (`6d418de`): 71% · 52,132 tokens · 228s

