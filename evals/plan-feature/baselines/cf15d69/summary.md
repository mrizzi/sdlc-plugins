## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 12/12 | 0 | 100% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 12/12 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the repo-backend.md mock repository structure manifest, not invented paths"
  **Evidence:** "Task 3 Files to Create lists 'modules/search/src/model/mod.rs' but the repo-backend.md manifest does not include a model/ directory under modules/search/src/. The manifest shows modules/search/src/ contains only lib.rs, service/, and endpoints/ — no model/ subdirectory. While the convention says modules follow 'model/ + service/ + endpoints/' structure, the actual manifest for the search module does not include model/. Task 1 Files to Create lists 'migration/src/m0002_search_indexes/mod.rs' which is a new migration directory following the existing m0001_initial pattern — this is a reasonable extension. However, task 3's model/ path is not from the manifest."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No 'Not applicable' annotations were found (good). However, several convention rationales fail the prescribed format requirement. The convention-applicability-rules.md (lines 124, 133-136) requires the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' where every rationale must 'name at least one specific file from the task's Files to Modify or Files to Create.' Multiple rationales violate this: (1) task-1 line 24: 'Applies: task creates a new response type in the model layer' — no specific file named; (2) task-2 line 22: 'Applies: task creates database queries in a service file matching the convention's query helpers scope' — no specific file named; (3) task-3 line 48: 'Applies: task creates a new endpoint response matching the convention's response types scope' — no specific file named; (4) task-3 line 49: 'Applies: task creates a new route that may benefit from caching matching the convention's caching scope' — no specific file named, and uses free-form prose ('that may benefit from caching'). These are generic rationales without specific file paths, violating the prescribed format."

</details>

**Pass rate:** 96% · **Tokens:** 34,759 · **Duration:** 166s

**Baseline** (`9aaab88`): 98% · 41,356 tokens · 180s

