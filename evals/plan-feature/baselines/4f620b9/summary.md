## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains any 'Per CONVENTIONS.md §...' references or 'Applies:' rationales in the prescribed format. All convention references in Implementation Notes point to 'docs/constraints.md' sections (§2, §3, §5, §5.11, §5.12) but none reference CONVENTIONS.md with the required applicability rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The convention-applicability-rules.md requires that applicable conventions include rationale in the format 'Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;.' This format is absent from all 5 tasks."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any formal CONVENTIONS.md references (no 'Per CONVENTIONS.md §' markers, no '§' section references). No task contains the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The word 'conventions' appears only informally in task-2 (e.g., 'serialization conventions from PackageSummary') meaning coding patterns, not referencing CONVENTIONS.md sections. Both repo manifests (repo-backend.md and repo-frontend.md) mention CONVENTIONS.md exists in the repos, so conventions should have been extracted and applied with applicability rationale. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format or any 'Per CONVENTIONS.md §...' references. The repo-backend.md lists a CONVENTIONS.md file with Key Conventions (Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching). These conventions should have been enriched into relevant tasks using the prescribed format per convention-applicability-rules.md. Instead, the tasks use free-form prose in Implementation Notes (e.g., task-1: 'Follow the established module pattern in common/src/', task-3: 'Follow the existing endpoint pattern in modules/fundamental/src/sbom/endpoints/get.rs') and reference 'Per constraints doc section...' but never use the required 'Per CONVENTIONS.md §... Applies:' format. Searched all output files for 'Applies:' and 'Per CONVENTIONS' — no matches found."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains a convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The repo-backend.md indicates a CONVENTIONS.md exists in the trustify-backend repository. Intermediate tasks reference 'Per docs/constraints.md' sections (e.g., task-2 lines 25-26, task-3 line 22) but no task references 'Per CONVENTIONS.md' with the required applicability rationale format. There is no evidence that CONVENTIONS.md conventions were evaluated for file-type applicability per the convention-applicability-rules.md. The prescribed format ('Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;') appears nowhere in any task file."

</details>

**Pass rate:** 92% · **Tokens:** 61,140 · **Duration:** 226s

**Baseline** (`d37fb89`): 94% · 39,822 tokens · 174s

