## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/16 | 5 | 69% |
| eval-2 | 5/14 | 9 | 36% |
| eval-3 | 9/15 | 6 | 60% |
| eval-4 | 6/11 | 5 | 55% |
| eval-5 | 8/15 | 7 | 53% |

### Failed Assertions

<details>
<summary>eval-1: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output files contain any reference to 'sha256', 'digest', or '[sdlc-workflow] Description digest'. Searched all files in /tmp/plan-feature-eval-baseline/eval-1/outputs/ with grep and found no matches. There are no comment files or log files showing digest comments were posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any reference to 'CONVENTIONS.md', 'Applies:', or convention applicability rationales. Grep for 'convention', 'CONVENTIONS', and 'Applies:' across all output files found only incidental uses of the word 'conventions' in lowercase referring to Rust/code conventions (e.g., 'Rust's unsigned integer conventions'), not CONVENTIONS.md-based enrichment. No convention-aware enrichment was performed."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture (feature-standard.md) shows Priority: Major. However, no task file contains 'priority', 'additional_fields', or 'Major'. Grep for 'priority', 'fixVersion', and 'additional_fields' returned no matches in any output file. The priority was not propagated to tasks."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture shows 'Fix Versions: RHTPA 1.5.0' (non-empty). The CLAUDE.md has no '### Jira Field Defaults' section, so fixVersion scope defaults to 'both', meaning tasks should inherit fixVersions. However, no task file contains 'fixVersions', 'RHTPA', 'additional_fields', or any version reference. The fixVersions were not propagated to tasks."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment referencing priority ('Major') or fixVersion ('RHTPA 1.5.0'). There is no summary comment file in the outputs directory. The impact-map.md does not mention priority or fixVersion propagation. No evidence of a Step 6c summary comment exists in the outputs."

</details>

<details>
<summary>eval-2: 8 failing assertions</summary>

- **Assertion:** "Plan acknowledges that 'Better UI' (non-MVP) cannot be planned without design mockups or frontend repository and excludes it from scope"
  **Evidence:** "The impact-map.md mentions 'Better UI' in the ambiguities table with resolution 'Excluded from this plan per the feature's own MVP classification. Backend-only changes.' However, it does not explicitly state that Better UI cannot be planned without design mockups or a frontend repository. It only acknowledges it's non-MVP and excluded — the reasoning about missing design mockups or frontend repo is absent."

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "The tasks make concrete design decisions to fill in ambiguous requirements (e.g., task 1 assumes tsvector/GIN indexes, task 3 assumes filters for entity_type/date_range/severity), but none of the four task descriptions contain the word 'assumption' or any section/label marking these decisions as 'assumptions pending clarification'. The ambiguities are acknowledged in the impact map but the tasks themselves do not label their gap-filling decisions as assumptions."

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the repo-backend.md mock repository structure manifest, not invented paths"
  **Evidence:** "Most file paths reference real paths from repo-backend.md, but task-3 has 'Files to Create: modules/search/src/model/mod.rs' — this path does not exist in the repo-backend.md directory tree. The repo-backend.md shows modules/search/ containing only src/lib.rs, src/service/mod.rs, and src/endpoints/mod.rs. There is no model/ directory under modules/search/. Also, task-1 creates 'migration/src/m0002_search_indexes/mod.rs' — while this follows the pattern of m0001_initial/, the specific path m0002_search_indexes/ is invented (though this is a new file creation following an established pattern, which is reasonable). The modules/search/src/model/mod.rs path in task-3 is clearly an invented path not derivable from the manifest."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "There are no output files containing description digest comments. The outputs directory contains only impact-map.md and four task description files. No file contains the string 'sha256-md:', 'sha256-adf:', '[sdlc-workflow] Description digest:', or any 64-character hex string. There is no evidence that digest comments were posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the four task descriptions contain any convention references in the prescribed format. There are no 'Per CONVENTIONS.md §...' references, no 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale strings in any task. The repo-backend.md mentions a CONVENTIONS.md file exists in the repository, but the tasks do not reference any conventions from it. Convention-aware enrichment appears to not have been performed at all."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture (feature-ambiguous.md) shows Priority: Normal (not 'Undefined'), so every task should inherit the priority. However, none of the four task description files contain 'additional_fields', 'priority', or 'Normal' anywhere in their content. There is no evidence that priority was inherited or propagated to the tasks."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture shows 'Fix Versions: RHTPA 1.6.0' (non-empty). CLAUDE.md has no '### Jira Field Defaults' section, so fixVersion scope defaults to 'both', meaning tasks should inherit fixVersions. However, none of the four task description files contain 'additional_fields', 'fixVersions', or 'RHTPA 1.6.0'. There is no evidence that fixVersions were inherited or propagated to the tasks."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "There is no output file representing a summary comment on the feature issue. The outputs directory contains only impact-map.md and four task files. No file mentions 'summary comment', 'Step 6c', inherited priority 'Normal', or inherited fixVersion 'RHTPA 1.6.0' in the context of a feature-level summary. There is no evidence that a summary comment was posted."

</details>

<details>
<summary>eval-3: 6 failing assertions</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 6 (SbomComparisonPage) references Figma design extensively with PatternFly components: Select (single, typeahead), ExpandableSection, Badge, Table (composable), EmptyState with CodeBranchIcon, Skeleton, Button, Dropdown. However, Task 7 (SbomListPage compare action) is UI-facing (modifies src/pages/SbomListPage/SbomListPage.tsx, a page component) but contains no Figma design context reference. It mentions PatternFly Table and isSelectableRow but without citing Figma design context. Since Task 7 is a UI-facing page task, the assertion requires Figma references, and none are present."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any 'sha256-md:', 'sha256-adf:', 'Description digest', or '[sdlc-workflow]' text. None of the 10 output files (impact-map.md and task-1 through task-9) include a digest comment in any form."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any 'Applies:' rationale, 'Per CONVENTIONS.md' reference, or any convention-aware enrichment text. The repo manifests (repo-backend.md and repo-frontend.md) both list CONVENTIONS.md files in their directory trees, indicating conventions exist that should have been processed. No evidence of convention applicability validation in any output file."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture specifies 'Priority: Critical'. No task description file contains the word 'priority' or 'Critical' in any context related to Jira field inheritance or additional_fields. The task descriptions are markdown files with no evidence of priority propagation to the created tasks."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture specifies 'Fix Versions: RHTPA 1.5.0'. The CLAUDE.md has no '### Jira Field Defaults' section, so fixVersion scope defaults to 'both', meaning tasks should inherit fixVersions. No task description file contains 'fixVersions', 'RHTPA', or '1.5.0' in any context. No evidence of fixVersions propagation."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment. The impact-map.md discusses workflow mode decision but does not mention priority ('Critical') or fixVersions ('RHTPA 1.5.0'). No file in the outputs directory represents a summary comment on the feature issue."

</details>

<details>
<summary>eval-4: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Searched all output files for 'sha256', 'digest', and 'sdlc-workflow'. No matches found. There are no digest comments in any of the output files. The outputs only contain the impact map and four task description files — no evidence of digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Searched all task files for 'CONVENTIONS', 'convention', and 'Per CONVENTIONS'. The only match is in task-4-license-report-integration-tests.md line 23: 'The tests hit a real PostgreSQL test database per the project's testing conventions.' This is a general reference to project conventions, not a convention-aware enrichment following the prescribed format. No task contains 'Per CONVENTIONS.md §...' references with applicability rationales in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The repo-backend.md fixture mentions a CONVENTIONS.md file exists in the repository, but no convention enrichment was performed."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture (feature-adversarial.md) has Priority: Major. Searched all four task files for 'priority', 'Major', and 'additional_fields'. No matches found. None of the task descriptions contain an additional_fields section or any mention of priority inheritance. The feature's 'Major' priority was not propagated to any task."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture has Fix Versions: RHTPA 1.5.0. The CLAUDE.md has no '### Jira Field Defaults' section, so the fixVersion scope defaults to 'both', meaning fixVersions should be propagated to tasks. Searched all four task files for 'fixVersion', 'fix version', 'RHTPA', and 'additional_fields'. No matches found. None of the task descriptions contain an additional_fields section or any fixVersions inheritance. The feature's 'RHTPA 1.5.0' fixVersion was not propagated to any task."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "Searched all output files for 'summary', 'Step 6c', and 'propagat'. No summary comment file exists in the outputs directory. The outputs contain only the impact map and four task description files. There is no summary comment that mentions priority inheritance (Major) or fixVersion inheritance (RHTPA 1.5.0)."

</details>

<details>
<summary>eval-5: 6 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "task-1-create-feature-branch.md (bookend) is missing: Files to Modify, Files to Create, and Implementation Notes. task-8-merge-feature-branch.md (bookend) is missing: Files to Modify, Files to Create, and Implementation Notes. While these are bookend tasks, the assertion says 'Each task file' without exception. Intermediate tasks 2-7 all have the required sections."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any reference to 'sha256', 'digest', 'sdlc-workflow', or any SHA-256 hash. Grep across all output files returned no matches. There is no evidence that description digest comments were posted after task creation."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any reference to 'convention', 'applicability', 'enrichment', or the 'Applies:' rationale format. There is no evidence of convention-aware enrichment in any task file."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture has Priority: High. However, no output file contains any reference to 'priority', 'High', or 'additional_fields'. There is no evidence of priority inheritance in any task file."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture has Fix Versions: RHTPA 2.0.0 and no fixVersion scope config exists in CLAUDE.md (defaulting to 'both'). However, no output file contains any reference to 'fixVersions', 'RHTPA', or 'additional_fields'. There is no evidence of fixVersion inheritance in any task file."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains any reference to a summary comment, Step 6c, priority propagation, or fixVersion propagation. There is no evidence that a summary comment was generated that documents these field inheritance decisions."

</details>

**Pass rate:** 54% · **Tokens:** 56,598 · **Duration:** 187s

**Baseline** (`718f1017`): 93% · 0 tokens · 0s

