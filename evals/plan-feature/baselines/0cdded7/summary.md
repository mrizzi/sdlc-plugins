## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 8/11 | 3 | 73% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 9/12 | 3 | 75% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task's Implementation Notes contain any convention references using the prescribed format 'Per CONVENTIONS.md §...' with an 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale. The repo-backend.md directory tree includes a CONVENTIONS.md file at the repository root, indicating conventions exist that should have been evaluated for applicability. None of the 6 tasks show evidence of convention-aware enrichment having been performed. While no inapplicable conventions are incorrectly listed (no 'Not applicable' annotations found), there is also no evidence that applicable conventions were identified and included with the required rationale format. The burden of proof is on PASS, and no positive evidence of convention-aware enrichment exists."

</details>

<details>
<summary>eval-2: 3 failing assertions</summary>

- **Assertion:** "Plan acknowledges that 'Better UI' (non-MVP) cannot be planned without design mockups or frontend repository and excludes it from scope"
  **Evidence:** "The impact-map.md and all task descriptions make no mention of 'Better UI' at all. The non-MVP requirement from the feature description ('Better UI | Make it look nicer | No') is not addressed — it is neither acknowledged as out of scope nor explained as unplannable without design mockups or a frontend repository. The plan silently omits it without any explicit acknowledgment."

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "The impact-map.md flags ambiguities and states 'resolved with reasonable defaults during planning. These should be confirmed with stakeholders' but does not label these as 'assumptions pending clarification'. Individual task descriptions do not contain any sections or labels identifying assumptions. For example, task-1 describes creating GIN indexes and B-tree indexes as definite implementation plans without labeling them as assumptions. Task-2 states 'Title/name matches are weighted higher than description matches' as a fact, not an assumption. Task-3 specifies filter types (entity type, severity, date range) without labeling these choices as assumptions. The word 'assumption' does not appear in any output file."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any convention-aware enrichment. There are no references to CONVENTIONS.md, no 'Per CONVENTIONS.md' lines, and no 'Applies:' rationale lines in any of the 5 task files or the impact map. The convention-applicability-rules.md requires that applicable conventions include a rationale in the prescribed format, but no conventions are referenced at all. While the repo-backend.md lists Key Conventions, the outputs do not demonstrate convention-aware enrichment with applicability validation as required by convention-applicability-rules.md."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the corresponding mock repository structure manifests (repo-backend.md or repo-frontend.md), not invented paths"
  **Evidence:** "Several tasks create new files at paths that extend existing directories from the repo manifests, which is expected. However, Task 8 lists 'tests/api/sbom_compare.rs' as Files to Create and 'tests/api/mod.rs' as Files to Modify — but repo-backend.md does not show a 'tests/api/mod.rs' file (it shows tests/api/sbom.rs, tests/api/advisory.rs, tests/api/search.rs but no mod.rs). The task itself hedges with 'or equivalent test module file', suggesting the path may be invented. Task 2 creates 'modules/fundamental/src/sbom/model/comparison.rs' (new file, extends existing model/ directory — acceptable). Task 3 creates 'modules/fundamental/src/sbom/service/compare.rs' (extends existing service/ directory — acceptable). Task 4 creates 'modules/fundamental/src/sbom/endpoints/compare.rs' (extends existing endpoints/ directory — acceptable). Task 5 creates 'src/hooks/useSbomComparison.ts' (extends existing hooks/ directory — acceptable). Files to Modify references are generally valid. However, Task 8's 'tests/api/mod.rs' is not in the repo manifest and appears invented."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The Implementation Notes sections reference existing code patterns and file paths but do not include any 'Per CONVENTIONS.md' references with the required 'Applies:' rationale format. For example, Task 2's Implementation Notes reference 'Follow the existing model pattern in modules/fundamental/src/sbom/model/summary.rs' but do not cite any CONVENTIONS.md section with the prescribed rationale format. None of the tasks contain text matching 'Applies: task modifies' or 'Per CONVENTIONS.md'. The convention-applicability-rules.md requires that when conventions are applied, they include a rationale in the format 'Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;'. This is entirely absent from all task outputs."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No conventions or 'Per CONVENTIONS.md' references appear in any of the four task descriptions. No 'Applies:' rationale lines are present in any Implementation Notes section. There is zero evidence that the convention-aware enrichment process was performed — no conventions were included with prescribed-format rationales, and no conventions were excluded. The assertion requires that applicable conventions include a rationale in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;', but no such rationales exist in any output file. With burden of proof on PASS, the complete absence of convention enrichment evidence means this assertion cannot be satisfied."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Task 1 (create-branch bookend) is missing Files to Modify, Files to Create, and Implementation Notes sections. Task 7 (merge-branch bookend) is missing Files to Modify, Files to Create, and Implementation Notes sections. The assertion requires ALL task files to contain these sections. While bookend tasks may reasonably omit file lists and implementation notes, the assertion requires 'each task file' to have 'at least one of Files to Modify or Files to Create' and 'Implementation Notes', which tasks 1 and 7 do not."

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "Searched all output files for 'label' and 'workflow:feature-branch' references. The impact-map.md mentions 'Selected mode: feature-branch' but does not mention applying a 'workflow:feature-branch' label to the feature issue. No output file contains any reference to a label or labeling decision."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention -- inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Reviewing all task Implementation Notes sections: Tasks 2-6 reference 'Per docs/constraints.md' rules (e.g., SS2, SS5.4, SS5.11, SS5.12) but none include the prescribed applicability rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No task contains any 'Applies:' rationale line in the format specified by convention-applicability-rules.md. The convention references use free-form prose like 'Per docs/constraints.md SS2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005' without the required applicability rationale."

</details>

**Pass rate:** 82% · **Tokens:** 51,715 · **Duration:** 191s

**Baseline** (`6b49958`): 91% · 57,513 tokens · 184s

