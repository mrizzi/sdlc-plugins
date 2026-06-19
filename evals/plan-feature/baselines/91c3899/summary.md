## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 10/12 | 2 | 83% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The digests.md file contains 5 digests with correct format (sha256-md: prefix followed by exactly 64 lowercase hex characters) for all 5 tasks. However, the assertion requires the marker format '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' and that it is posted as a comment. The digests.md file presents digests in a table format (| task-file | sha256-md:... |) without the required '[sdlc-workflow] Description digest:' marker prefix. There is no evidence that the digests were posted as comments with the prescribed marker format."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "digests.md contains SHA-256 hashes for all 5 tasks with correct sha256-md: prefix and 64 lowercase hex characters (e.g., sha256-md:232a898939e8a7691077ca2fda4834338bd5440feee936a0a90a298a75c1737e). However, the required marker format '[sdlc-workflow] Description digest: sha256-md:&lt;hex&gt;' is not present anywhere in the output files. The digests are recorded in a markdown table format rather than the prescribed comment marker format. No evidence that digest comments were posted using the required '[sdlc-workflow] Description digest:' marker."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content found anywhere in the output files. Searched all files for 'convention', 'Convention', 'CONVENTIONS.md', 'Per CONVENTIONS', and 'Applies:' — zero matches. No convention enrichment of any kind appears in any task description's Implementation Notes or elsewhere. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The digests.md file contains 7 digests, all with valid sha256-md: prefix and 64 lowercase hex characters. However, the digests are recorded in a table format in digests.md, not as comments with the required marker format '[sdlc-workflow] Description digest: sha256-md:&lt;hex&gt;'. The assertion requires that after each task is created, a description digest comment is posted with that specific marker format. The digests.md file uses a table format ('| Task 1 ... | sha256-md:... |') rather than the prescribed '[sdlc-workflow] Description digest:' comment format. There is no evidence the digests were posted as comments using the required marker format, nor evidence that scripts/sha256-digest.py was used."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No CONVENTIONS.md conventions are referenced anywhere in the task files. The Implementation Notes in intermediate tasks reference 'docs/constraints.md' sections (e.g., '§2 (Commit Rules)', '§5.2', '§5.4', '§5.9', '§5.11', '§5.12') but none include the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. There is no evidence of convention applicability validation per convention-applicability-rules.md. No 'Applies:' rationale strings appear anywhere in any task file. Convention-aware enrichment was not performed."

</details>

**Pass rate:** 90% · **Tokens:** 0 · **Duration:** 0s

**Baseline** (`796c88c`): 77% · 36,268 tokens · 184s

