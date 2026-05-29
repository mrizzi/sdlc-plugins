## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 8/8 | 0 | 100% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention -- inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Searched all 7 task files for convention applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). No task contains any 'Applies:' rationale line. The Implementation Notes reference docs/constraints.md sections (e.g., 'Per docs/constraints.md section 5 (Code Change Rules)') but never include convention applicability rationales from CONVENTIONS.md per the convention-applicability-rules.md format. The repo-backend.md fixture lists a CONVENTIONS.md file in the repository tree, but no task includes convention enrichment with the prescribed rationale format."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task Implementation Notes contain CONVENTIONS.md references with the prescribed applicability rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The tasks reference docs/constraints.md sections (e.g., 'Per docs/constraints.md §5.4:', 'Per docs/constraints.md §2.1-2.3:') but these do not use the convention-applicability-rules.md prescribed format. The repo-backend.md fixture lists a CONVENTIONS.md file in the repository root, so convention-aware enrichment should have been performed. No evidence of the required 'Applies:' rationale lines anywhere in the outputs."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task output contains any convention enrichment in the prescribed format. There are no 'Per CONVENTIONS.md' references, no 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale strings anywhere in the outputs. While the repo manifests mention CONVENTIONS.md files exist in both repos (trustify-backend/CONVENTIONS.md and trustify-ui/CONVENTIONS.md), the task descriptions do not include any convention-aware enrichment at all. The absence of convention enrichment means the prescribed format requirement cannot be verified as satisfied."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any 'Per CONVENTIONS.md §' reference with an 'Applies:' rationale line. The repo fixture (repo-backend.md) shows CONVENTIONS.md exists in the repository tree, yet none of the intermediate task Implementation Notes sections reference it or include applicability rationales in the prescribed format. The tasks only reference 'docs/constraints.md' sections. There is no evidence that convention-aware enrichment was performed at all."

</details>

**Pass rate:** 93% · **Tokens:** 48,830 · **Duration:** 190s

**Baseline** (`b89536d`): 73% · 45,989 tokens · 178s

