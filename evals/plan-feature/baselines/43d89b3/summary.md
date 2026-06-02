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
  **Evidence:** "No task Implementation Notes contain the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Grep for 'Applies:' across all task files returned zero matches. The tasks reference 'Per docs/constraints.md' sections (e.g., '§2 (Commit Rules)', '§3 (PR Rules)', '§5 (Code Change Rules)') but these are constraint references, not CONVENTIONS.md convention applicability rationales. There is no evidence of convention-applicability-rules.md being applied — no 'Per CONVENTIONS.md §...' lines with 'Applies:' rationale appear in any task. The convention-applicability-rules.md requires the format 'Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;' which is entirely absent."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention enrichment is present in any task file. No references to CONVENTIONS.md, no 'Per CONVENTIONS.md' citations, and no 'Applies:' rationales were found in any of the 7 task descriptions. The repo manifests (repo-backend.md and repo-frontend.md) both mention CONVENTIONS.md files exist in their respective repositories, indicating conventions should have been evaluated for applicability. The absence of any convention-aware enrichment means the skill did not perform the required validation step — there is no evidence that conventions were evaluated and either included with rationale or excluded as inapplicable."

</details>

**Pass rate:** 97% · **Tokens:** 52,427 · **Duration:** 174s

**Baseline** (`566e199`): 78% · 53,515 tokens · 194s

