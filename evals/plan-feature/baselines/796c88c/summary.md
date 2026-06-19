## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 9/11 | 2 | 82% |
| eval-3 | 7/12 | 5 | 58% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 10/12 | 2 | 83% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Task 1 (task-1-advisory-summary-model.md) is missing the 'Test Requirements' section. It has Repository, Target Branch, Description, Files to Create, Files to Modify, Implementation Notes, Acceptance Criteria, and Verification Commands — but no Test Requirements section. Tasks 2-5 all contain Test Requirements sections."

- **Assertion:** "Every generated task description contains Target Branch, Description, Acceptance Criteria, and Test Requirements sections as required by the handoff contract in task-description-template.md"
  **Evidence:** "Task 1 (task-1-advisory-summary-model.md) is missing the 'Test Requirements' section. It contains Target Branch (line 4-5), Description (line 7-8), and Acceptance Criteria (lines 27-30), but no Test Requirements section exists anywhere in the file. The template in task-description-template.md lists Test Requirements as a required section. Tasks 2-5 all contain Test Requirements."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "None of the output files (impact-map.md, task-1-fulltext-search-migration.md, task-2-search-relevance-ranking.md, task-3-search-filter-parameters.md) contain any description digest comments. There is no '[sdlc-workflow] Description digest: sha256-md:' or 'sha256-adf:' marker anywhere in the outputs. No evidence of SHA-256 hash computation or digest posting."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The tasks include Conventions sections with rationales, but the format does not fully match the prescribed format from convention-applicability-rules.md. Task 1: 'Applies: task modifies `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` matching the convention's SeaORM entity scope.' — uses 'SeaORM entity scope' rather than referencing a specific convention scope signal from CONVENTIONS.md. Task 2: 'Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `Result&lt;T, AppError&gt;` with `.context()` scope.' — this format is non-standard, using code patterns as the scope rather than the convention's section-defined scope signal. The prescribed format is 'Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;' where scope signal refers to explicit scope statements, file paths in examples, or language-specific syntax from the convention definition. The rationales do reference specific files and use a structured format rather than free-form prose, but they do not reference actual CONVENTIONS.md section names with the 'Per CONVENTIONS.md §&lt;Section Name&gt;' prefix as required by the applicability rules format. Additionally, conventions are listed as standalone items in a Conventions section rather than appended to Implementation Notes as specified in the rules ('append a rationale to the "Per CONVENTIONS.md §..." line in Implementation Notes')."

</details>

<details>
<summary>eval-3: 5 failing assertions</summary>

- **Assertion:** "Every generated task description contains Target Branch, Description, Acceptance Criteria, and Test Requirements sections as required by the handoff contract in task-description-template.md"
  **Evidence:** "Bookend tasks (task-1 create-branch and task-10 merge-branch) do not contain a 'Test Requirements' section. While the task-description-template.md allows omitting sections that don't apply, and bookend tasks arguably don't need test requirements, the assertion says 'every generated task description' must contain these sections. Tasks 2-9 all contain Target Branch, Description, Acceptance Criteria, and Test Requirements. But tasks 1 and 10 are missing Test Requirements."

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the corresponding mock repository structure manifests (repo-backend.md or repo-frontend.md), not invented paths"
  **Evidence:** "Task 8 (frontend ComparisonPage) lists 'src/App.tsx' under Files to Modify. The frontend manifest (trustify-ui) lists: src/api/ (client.ts, models.ts, rest.ts), src/hooks/, src/pages/, src/components/, src/routes.tsx, src/utils/, tests/mocks/, tests/e2e/. 'src/App.tsx' is not present in the manifest. All other file paths are well-grounded in the manifests: backend paths under modules/fundamental/src/sbom/, common/src/, tests/api/; frontend paths under src/api/, src/hooks/, src/pages/, src/components/, src/routes.tsx, tests/mocks/. But src/App.tsx is not from the manifest."

- **Assertion:** "Implementation Notes in every non-bookend task reference specific file paths and code patterns from the repository, not abstract or generic guidance — bookend tasks (create-branch, merge-branch) are exempt as they omit Implementation Notes by design"
  **Evidence:** "Bookend tasks (1 and 10) DO contain Implementation Notes sections — they are not omitted. Task 1 Implementation Notes: 'Create the branch TC-9003 from main in both repositories: trustify-backend: git checkout -b TC-9003 main; trustify-ui: git checkout -b TC-9003 main'. Task 10 Implementation Notes: 'Merge TC-9003 into main in trustify-backend first (via pull request). After backend merge is confirmed...' These are procedural instructions, not references to specific file paths and code patterns. The assertion exempts bookend tasks, and the non-bookend tasks (2-9) all contain specific file paths and code patterns. Task 2 references 'modules/fundamental/src/sbom/model/' patterns. Task 3 references 'modules/fundamental/src/sbom/service/sbom.rs' patterns. Task 4 references 'modules/fundamental/src/sbom/endpoints/get.rs' and 'list.rs' patterns. Task 5 references 'tests/api/sbom.rs' patterns. Task 6 references 'src/api/models.ts' and 'src/api/rest.ts' patterns. Task 7 references 'src/hooks/useSboms.ts' and 'src/hooks/useSbomById.ts' patterns. Task 8 references specific PatternFly components and existing components like 'src/components/SeverityBadge.tsx'. Task 9 references 'tests/mocks/handlers.ts' patterns. All non-bookend tasks PASS this check."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any SHA-256 digest, 'sha256-md:', 'sha256-adf:', or '[sdlc-workflow] Description digest:' marker. Grep for 'sha256', 'digest', and 'Description digest' across all output files returned no matches. No digest comments were posted after task creation."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task output contains any convention-aware enrichment section, 'Applies:' rationale annotations, or references to convention-applicability-rules.md. The word 'convention' appears only in informal usage (e.g., 'Reference for struct conventions', 'per project conventions') in Implementation Notes and Reuse Candidates, not as a structured convention-applicability section with the prescribed format."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Searched all output files for 'sha256', 'digest', and '[sdlc-workflow]'. No matches found in any file. No digest comments are present in the outputs directory. The outputs contain only the impact map and 5 task description files with no evidence of description digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Searched all output files for 'convention', 'CONVENTIONS.md', 'Applies:', and 'Per CONVENTIONS.md'. No matches found in any task description. None of the 5 task files contain any convention references, applicability rationales, or 'Per CONVENTIONS.md' citations in their Implementation Notes sections. There is no evidence that convention-aware enrichment was performed at all."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The outputs contain SHA-256 digests in impact-map.md lines 75-81 (e.g., 'sha256-md:3193f81c13f8415a1684ed22dbb7adf034b35f905899a9d74fa0400d31525b5f'), and these are valid 64-character lowercase hex values with the sha256-md: prefix. However, the required marker format '[sdlc-workflow] Description digest: sha256-md:&lt;hash&gt;' is not present anywhere in the output files. grep for 'sdlc-workflow' returns zero matches across all output files. The digests are listed in a 'Description Digests' section in the impact map but not as posted comments in the required marker format."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content exists in any output file. grep for 'convention', 'Convention', 'Applies:', and 'applicab' across all output files returns zero matches. Convention-aware enrichment is entirely absent from the plan output."

</details>

**Pass rate:** 77% · **Tokens:** 36,268 · **Duration:** 184s

**Baseline** (`fb811c4`): 93% · 34,548 tokens · 160s

