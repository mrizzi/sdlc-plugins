## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No conventions are annotated as 'Not applicable' (grep confirms zero matches), which is correct. However, task-3-advisory-summary-endpoint.md line 26 contains a convention reference 'Per Key Conventions §Caching: use tower-http caching middleware to set Cache-Control: max-age=300 (5 minutes) on the response. Reference the existing caching configuration in endpoint route builders for the established pattern.' — this convention does NOT include the prescribed 'Applies: task modifies/creates &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. Instead it uses free-form prose ('Reference the existing caching configuration in endpoint route builders for the established pattern'). Per convention-applicability-rules.md, all included conventions must have a rationale in the prescribed format."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains a convention enrichment section or any 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale. The repo-backend.md manifest shows a CONVENTIONS.md file exists in the repository, so convention-aware enrichment should have been performed. While there are no 'Not applicable' annotations (which is correct), there is also no evidence of convention validation or inclusion with the prescribed rationale format in any of the 5 task files. The convention-applicability-rules.md requires applicable conventions to be included with rationale — the complete absence of any convention section means the enrichment step was not performed."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains any convention references. None of the Implementation Notes sections in tasks 2-6 include 'Per CONVENTIONS.md' lines or applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). Both repo-backend.md and repo-frontend.md show CONVENTIONS.md files exist in their directory trees, indicating conventions should have been processed. There is zero evidence that convention-aware enrichment was performed — no applicable conventions included with rationales, and no indication that inapplicable ones were filtered. Burden of proof is on PASS."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No CONVENTIONS.md file content was provided as input to eval case 4 (the files array contains only feature-adversarial.md and repo-backend.md). No convention-aware enrichment sections appear in any task file. While no 'Not applicable' annotations exist (correct behavior), there are also no 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale lines in any task description. The repo-backend.md directory tree references a CONVENTIONS.md file, but its content was not provided, so convention-aware enrichment could not be demonstrated. No positive evidence of applicability validation occurring."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content appears anywhere in the output files. None of the intermediate task Implementation Notes sections contain any 'Per CONVENTIONS.md' references or 'Applies:' rationale lines. There is zero evidence that convention-aware enrichment was performed. Burden of proof is on PASS and no evidence of convention processing exists."

</details>

**Pass rate:** 91% · **Tokens:** 51,050 · **Duration:** 166s

**Baseline** (`f196a97`): 76% · 51,417 tokens · 222s

