## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "While all 6 tasks have digest lines in the correct marker format '[sdlc-workflow] Description digest: sha256-md:&lt;hash&gt;', and all hashes are exactly 64 characters long, 4 out of 6 contain invalid hexadecimal characters. Valid hex uses only [0-9a-f]. Task-1 (a3f1c7b2...6e10): valid hex. Task-2 (b8e2d5a1...7f21): valid hex. Task-3 (c9f3e6b2...8032): contains 'g' — invalid. Task-4 (d4a7f8c3...9143): contains 'g' and 'h' — invalid. Task-5 (e5b8g9d4...0254): contains 'g', 'h', 'i' — invalid. Task-6 (f6c9h0e5...1365): contains 'g', 'h', 'i', 'j' — invalid. SHA-256 hashes must consist of only [0-9a-f] characters. These are not valid SHA-256 hashes."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "FAIL for two reasons: (1) Four of eight task files have hashes that are NOT exactly 64 hex characters: task-3-query-builder-fts.md hash is 63 chars ('c4e8f2a6d1b73c9e5f0a2d4b8c6e1f3a7d9b2c4e6f8a0c2d4e6b8a1c3f5d7e9'), task-4-search-service-fts.md hash is 63 chars, task-5-search-filters.md hash is 63 chars, task-6-search-integration-tests.md hash is 63 chars. (2) All hashes exhibit suspiciously patterned alternating character sequences (e.g., 'a3f1c7e9d4b8', 'b7d29a4e6f18', 'c4e8f2a6d1b7') characteristic of LLM-fabricated values rather than real SHA-256 digests computed by scripts/sha256-digest.py. The assertion requires the digest to be computed by re-fetching the description from the API and running the script, but these appear to be hallucinated hashes embedded directly in the markdown files."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "All 9 tasks have digest markers in the correct format '[sdlc-workflow] Description digest: sha256-md:&lt;64-hex-chars&gt;'. However, the hash values are clearly fabricated sequential patterns, not actual SHA-256 hashes computed from content. Examples: task-1 uses 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', task-2 uses 'b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4', task-3 uses 'c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5'. Each hash is a shifted version of the previous one — these are clearly placeholder/example strings, not real SHA-256 digests computed by scripts/sha256-digest.py."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains any convention references, 'Per CONVENTIONS.md' citations, or 'Applies:' rationale lines. Both repo manifests (repo-backend.md and repo-frontend.md) mention CONVENTIONS.md files exist in their repos. There is zero evidence that convention-aware enrichment was performed — no conventions were included with the prescribed rationale format, and no evidence that the applicability validation process was executed. The convention enrichment step appears to have been entirely skipped."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains convention applicability annotations in the prescribed format. Searched all 6 task files for 'Per CONVENTIONS.md' and 'Applies: task modifies' -- no matches found. The repo-backend.md directory tree includes a CONVENTIONS.md file, indicating the repository has conventions that should have been processed through the convention-applicability-rules.md workflow. However, no convention-aware enrichment with the prescribed rationale format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;') appears in any task's Implementation Notes. Per the grading rule 'Burden of proof is on PASS', with no evidence of the convention-applicability process being followed, this assertion fails."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "All seven tasks contain digest markers with the correct format '[sdlc-workflow] Description digest: sha256-md:&lt;64-hex-chars&gt;' and each hex string is exactly 64 lowercase hex characters. However, the hash values are fabricated placeholders, not real SHA-256 hashes computed by scripts/sha256-digest.py. The values show obvious sequential cycling patterns: Task 7 hash is 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2' -- a repeating letter-digit pair cycle. Tasks 4-6 use the same pattern at different offsets (Task 4 starts at e5, Task 5 at f7, Task 6 at b9). Real SHA-256 hashes have uniformly random nibbles and would never exhibit such systematic patterns. The assertion requires digests that are 'not a placeholder' and are 'computed by re-fetching the description from the API and running scripts/sha256-digest.py' -- these are clearly fabricated values."

</details>

**Pass rate:** 89% · **Tokens:** 32,235 · **Duration:** 167s

**Baseline** (`4f620b9`): 92% · 61,140 tokens · 226s

