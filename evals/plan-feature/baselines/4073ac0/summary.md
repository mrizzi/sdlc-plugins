## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related sections found in any of the 7 task descriptions. Searched for 'convention', 'Applies:', and 'applicability' across all output files — no matches. The assertion requires convention-aware enrichment with applicability validation and rationale in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Since no convention enrichment is present at all, this fails."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention-aware enrichment. Searched all 5 task files for 'convention', 'CONVENTIONS', 'Applies:', and 'Per CONVENTIONS' — no matches found. The repo-backend.md fixture lists a CONVENTIONS.md file in the directory tree, indicating the repository has conventions that should have been evaluated for applicability. The convention-applicability-rules.md requires that applicable conventions include a rationale in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;.' No such rationale appears in any task. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention -- inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content found in any task file. Searched all output files for 'convention', 'Applies:', and convention-related sections -- none present. There is no evidence of convention-aware enrichment with applicability validation and prescribed rationale format in any task."

</details>

**Pass rate:** 94% · **Tokens:** 42,269 · **Duration:** 174s

**Baseline** (`6f405ac`): 93% · 0 tokens · 0s

