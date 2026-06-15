## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 12/12 | 0 | 100% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Tasks 1-4 lack a 'Test Requirements' section. Task 1 has: Repository, Target Branch, Description, Files to Modify, Files to Create, Implementation Notes, Acceptance Criteria, Verification Commands — no Test Requirements. Task 2 has: Repository, Target Branch, Description, Files to Modify, Implementation Notes, Acceptance Criteria, Verification Commands, Dependencies — no Test Requirements. Task 3 has: same pattern, no Test Requirements. Task 4 has: same pattern, no Test Requirements. Only Task 5 has a Test Requirements section. Since the assertion requires ALL task files to contain Test Requirements, this fails."

- **Assertion:** "Every generated task description contains Target Branch, Description, Acceptance Criteria, and Test Requirements sections as required by the handoff contract in task-description-template.md"
  **Evidence:** "Tasks 1-4 do not contain a 'Test Requirements' section. Task 1 has sections: Repository, Target Branch, Description, Files to Modify, Files to Create, Implementation Notes, Acceptance Criteria, Verification Commands. Task 2 has: Repository, Target Branch, Description, Files to Modify, Implementation Notes, Acceptance Criteria, Verification Commands, Dependencies. Task 3 has: Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Verification Commands, Dependencies. Task 4 has: Repository, Target Branch, Description, Files to Modify, Implementation Notes, Acceptance Criteria, Verification Commands, Dependencies. Only Task 5 has a Test Requirements section. However, the template in task-description-template.md says 'Omit sections that don't apply', so Test Requirements is technically optional. But the assertion specifically states these sections are 'required', so tasks 1-4 missing Test Requirements means FAIL."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No inapplicable conventions are annotated (correct — none listed with 'Not applicable'). However, the rationale format does not match the prescribed format. The rules require: 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Actual rationales use free-form prose instead: task-1: 'Applies: task creates common/src/license_policy.rs which uses the shared error type from common/src/error.rs' (free-form prose, missing 'matching the convention's &lt;scope&gt;'); task-2: 'Applies: task creates a new model file under modules/fundamental/src/sbom/model/' (missing 'matching the convention's &lt;scope&gt;'); task-3: 'Applies: task creates modules/fundamental/src/sbom/service/license_report.rs which follows the service pattern' (free-form prose); task-4: 'Applies: task creates modules/fundamental/src/sbom/endpoints/license_report.rs' (missing 'matching the convention's &lt;scope&gt;'); task-5: 'Applies: task creates tests/api/license_report.rs' (missing 'matching the convention's &lt;scope&gt;'). None follow the prescribed format with 'matching the convention's &lt;scope signal&gt;'."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content found in any output file. Grep for 'convention' across all outputs returned no results. No 'Applies:' rationale statements or convention references appear in any task file. Convention-aware enrichment was not performed."

</details>

**Pass rate:** 93% · **Tokens:** 34,548 · **Duration:** 160s

**Baseline** (`a8a874f`): 82% · 31,667 tokens · 156s

