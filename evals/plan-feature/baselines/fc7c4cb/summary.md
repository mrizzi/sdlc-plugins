## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 8/8 | 0 | 100% |
| eval-5 | 12/12 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task file. The repo-backend.md mentions a CONVENTIONS.md file exists in the trustify-backend repository structure, but no conventions were extracted or applied to any task's Implementation Notes. There are no 'Per CONVENTIONS.md' references, no 'Applies:' rationale lines, and no convention sections in any task. While no inapplicable conventions are listed (which is correct), the absence of any convention processing — even for potentially applicable conventions from the repo's CONVENTIONS.md — indicates the convention applicability workflow was not executed. The assertion requires that applicable conventions include the prescribed rationale format, which is entirely absent."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the task files (tasks 2-7) contain any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Searching all task files for 'Applies:' or 'Per CONVENTIONS.md' or 'convention' yields no matches. While no inapplicable conventions are listed (which is good), the repo manifests mention CONVENTIONS.md files exist in both repos (repo-backend.md line 16: CONVENTIONS.md, repo-frontend.md line 7: CONVENTIONS.md). If conventions existed and were applicable, they should have been included with proper rationale. If conventions were checked and found inapplicable, the output is correct. However, the assertion requires that 'applicable ones include a rationale in the prescribed format' — given that both repos have CONVENTIONS.md files and the tasks modify files in those repos, the absence of any convention processing evidence means we cannot confirm the enrichment validation occurred. The output lacks any evidence of convention-aware enrichment being performed."

</details>

**Pass rate:** 97% · **Tokens:** 58,088 · **Duration:** 285s

**Baseline** (`6b49958`): 91% · 57,513 tokens · 184s

