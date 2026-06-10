## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 9/12 | 3 | 75% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The description-digest.md file includes a 'Convention Check' section that lists conventions from the repository structure description (Framework, Module pattern, Error handling, etc.) but does NOT use the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Instead, the conventions are listed as bullet points without any applicability rationale. The task Implementation Notes reference patterns and file paths but do not include 'Per CONVENTIONS.md §...' lines with the prescribed 'Applies:' rationale format. The repo-backend.md manifest shows CONVENTIONS.md exists at the repo root, so conventions should have been read and validated per the applicability rules. No task contains the required 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' format."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment with the prescribed format is present in any task. The tasks reference 'key conventions' from the repo manifest in free-form prose (e.g., Task 1: 'Per the repository's key conventions: use Axum for HTTP and SeaORM for database'), but do not use the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The repo-backend.md manifest shows a CONVENTIONS.md file exists in the repo root, so convention enrichment should have been attempted with the prescribed applicability-rationale format. No 'Per CONVENTIONS.md §' references appear anywhere in the output."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 6 (SbomComparePage) extensively references Figma design context with specific PatternFly components: Select (single, typeahead), Button (primary), Dropdown, ExpandableSection, Table (composable), Badge, EmptyState, Skeleton, SeverityBadge, CodeBranchIcon. It includes 'Figma design — PatternFly component mapping' section and 'Diff section specifications (from Figma)'. However, Task 7 (SbomListPage selection UI) is a UI-facing page task that modifies SbomListPage.tsx but does NOT reference Figma design context — it mentions PatternFly Table and Button but without Figma references. Task 5 (API layer) is correctly exempt. Since task 7 is UI-facing but lacks Figma design context, this assertion fails."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains convention enrichment in the prescribed format. No task references 'Per CONVENTIONS.md §' or uses the required rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Tasks mention 'conventions' informally (e.g., task-2: 'demonstrating the project's model conventions', task-4: 'per the error handling convention', task-5: 'naming and field conventions') but these are free-form prose references, not the prescribed format from convention-applicability-rules.md. No CONVENTIONS.md sections are formally referenced, no applicability rationales are provided."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "description-digest.md contains four valid sha256-md: digests with 64 lowercase hex characters in a table (e.g., sha256-md:2c7bdc2cbad94b2707ccf5e7d57c1e42283796230b88dd47dee9de3b8d37355b). However, the required marker format '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' is NOT present with actual hashes. The file only shows the marker as a template: '[sdlc-workflow] Description digest: &lt;tagged-digest&gt;' (line 21) where &lt;tagged-digest&gt; is a placeholder, not an actual hash. The per-task digest comments in the required marker format were never generated."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "No mention of 'workflow:feature-branch' label or any label decision found in any output file. The impact-map.md mentions the feature-branch workflow mode selection but does not include a decision to apply the 'workflow:feature-branch' label to the feature issue. grep for 'label' and 'workflow:feature' across all output files returned no results."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "description-digest.md contains seven SHA-256 digests, all correctly formatted as sha256-md: followed by 64 lowercase hex characters. However, the file uses conditional language ('Each task would receive a Jira comment') indicating the comments were NOT actually posted. The marker format shown is '[sdlc-workflow] Description digest: &lt;digest-value&gt;' which matches the expected format in template only. Additionally, the description says digests would be posted but does not confirm actual posting via Jira API. The assertion requires that comments ARE posted after each task is created, not merely described hypothetically."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention enrichment is present in any task file. No references to 'CONVENTIONS.md', no 'Applies:' rationale lines, and no convention applicability validation found in any output. The only mention of 'convention' is in task-2 referring to 'naming conventions' in a general sense. There is no evidence that convention-aware enrichment was performed or that any CONVENTIONS.md was consulted."

</details>

**Pass rate:** 86% · **Tokens:** 52,125 · **Duration:** 178s

**Baseline** (`0adea80`): 75% · 47,086 tokens · 187s

