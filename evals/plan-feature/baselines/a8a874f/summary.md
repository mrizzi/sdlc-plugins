## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 9/11 | 2 | 82% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 8/12 | 4 | 67% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash -- exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The digest lines in all task files are placeholders, not actual posted comments. Task 1 ends with: '[Description digest: sha256-md:a3f7b2c91d4e8f0a56b3c2d1e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0 would be posted as a comment]'. Problems: (1) The format does not match the required marker '[sdlc-workflow] Description digest: sha256-md:&lt;hash&gt;' -- it uses '[Description digest:' and appends 'would be posted as a comment]'. (2) The hashes are fabricated example strings with obvious sequential patterns (a3f7b2c9..., b4e8c3d2..., c5f9d4e3..., d6a0e5f4..., e7b1f6a5..., f8c2a7b6...) rather than actual SHA-256 computations. (3) The phrase 'would be posted as a comment' explicitly indicates these are hypothetical, not actual posted digest comments. All 6 tasks exhibit this same issue."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The task files contain inline placeholder text rather than actual posted comments. Task 1 line 59: '[Description digest: sha256-md:a3c1f8e92b4d7605c8e1a9f3b2d4e6a8c0f2d4e6a8b0c2d4e6f8a0b2c4d6e8f0 would be posted as a comment]'. Task 2 line 60: '[Description digest: sha256-md:b7d2e9f03a5c8716d9f2b0e4c3d5f7a9b1e3f5a7c9d1e3f5b7d9f1a3c5e7b9d1 would be posted as a comment]'. Several issues: (1) The format says 'would be posted as a comment' indicating these are placeholders, not actual posted comments. (2) The marker format is wrong — it should be '[sdlc-workflow] Description digest: sha256-md:&lt;hash&gt;' but instead shows '[Description digest: sha256-md:&lt;hash&gt; would be posted as a comment]'. (3) The hashes appear to be fabricated/example values rather than computed by re-fetching and running sha256-digest.py. (4) The hashes are embedded in the task files rather than posted as separate Jira comments."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the four task files or the impact map contain any convention-aware enrichment section. There are no mentions of CONVENTIONS.md, no convention applicability rationales in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;', and no convention sections at all. The repo-backend.md manifest references a CONVENTIONS.md file in the repository structure, but no conventions were evaluated or included in the task outputs. The convention-applicability-rules.md requires that applicable conventions include rationales in a prescribed format — this is entirely absent from all outputs."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "FAIL for two reasons: (1) The marker format is wrong. The assertion requires '[sdlc-workflow] Description digest: sha256-md:&lt;hex&gt;' but all tasks use '[Description digest: sha256-md:&lt;hex&gt;]' — missing the '[sdlc-workflow]' prefix. (2) The hashes are clearly fabricated placeholders, not computed by sha256-digest.py. The first hex characters of the 7 hashes follow the sequence a, b, c, d, e, f, a — an obvious sequential pattern. Real SHA-256 hashes are pseudo-random. Examples: task-1 hash 'a3f7c1e9d42b8f0e6a5d3c7b9e1f4a2d8c6b0e3f7a9d2c5b8e1f4a7d0c3b6e9f', task-2 hash 'b4e8d2f1a7c3e9b5d0f6a2c8e4b0d7f3a9c5e1b8d4f0a6c2e8b5d1f7a3c9e5b2'. While they are 64 hex chars, they are clearly example strings, not genuine SHA-256 digests."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The digests are embedded inline in task files as bracketed notes rather than posted as actual comments. The format used is '[Description digest: sha256-md:&lt;hex&gt; would be posted as a comment]' (e.g., task-1 line 64: 'sha256-md:a3f1d8e2c4b90671f5e83ca92d01b6f748ea35c9d20f74a1b86e53c9f0124d87 would be posted as a comment'). Problems: (1) Missing required '[sdlc-workflow]' prefix in the marker format. (2) The phrase 'would be posted as a comment' indicates hypothetical intent, not an actual posted comment. (3) The hashes appear fabricated — they follow a suspiciously sequential first-byte pattern (a3, b7, c8, d9) suggesting they were not computed by re-fetching descriptions from the API and running scripts/sha256-digest.py. (4) No evidence of actual Jira comment posting."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the four task descriptions contain any convention-related sections, applicability analysis, or rationale statements. The repository's CONVENTIONS.md (referenced in repo-backend.md) defines conventions for the Rust/Axum/SeaORM codebase that would apply to the tasks (e.g., error handling patterns, endpoint registration, module structure). The convention-applicability-rules.md requires applicable conventions to be included with 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. No such enrichment appears in any task file."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "impact-map.md line 5 mentions 'Mode: workflow:feature-branch' as the workflow mode, but there is no explicit mention of applying a 'workflow:feature-branch' label to the feature issue (TC-9005). The impact-map describes the mode but does not include an action/decision to apply a label to the Jira issue. No other output file references applying a label."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Multiple failures: (1) The hashes contain non-hex characters making them invalid SHA-256 values. Task 2: 'b4f2e8d9c3a05f6712gd9b5e8c4f3a201d7e9f5b6c8d1e2f3a4b5c6d7e8f9a01' contains 'g'. Task 3 contains 'h'. Task 4 contains 'i'. Task 5 contains 'j'. Task 6 contains 'k'. Task 7 contains 'l'. Only Task 1's hash passes hex validation. (2) The format is wrong: all use '[Description digest: sha256-md:...' instead of the required '[sdlc-workflow] Description digest: sha256-md:...'. (3) All include 'would be posted as a comment' indicating these are placeholders describing intended behavior rather than actual posted digests. (4) No evidence of running scripts/sha256-digest.py."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task file. The Implementation Notes sections in tasks 2-6 contain general implementation guidance but do not reference CONVENTIONS.md, do not include any 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format, and show no evidence of convention applicability validation. The repo structure indicates a CONVENTIONS.md file exists in the trustify-backend repository, but the task outputs do not incorporate it."

</details>

**Pass rate:** 82% · **Tokens:** 31,667 · **Duration:** 156s

**Baseline** (`833673a`): 91% · 51,050 tokens · 166s

