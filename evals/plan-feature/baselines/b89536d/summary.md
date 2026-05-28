## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 6/11 | 5 | 55% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 8/12 | 4 | 67% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No description digest comments found in any output file. Searched all 6 output files (impact-map.md and all 5 task files) for '[sdlc-workflow] Description digest', 'sha256:', 'digest', or 'hash' — none found. No SHA-256 hashes are present anywhere in the outputs."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content found in any output file. Searched all 6 output files for 'CONVENTIONS', 'convention', 'Applies:', 'Per CONVENTIONS' — none found. There is no evidence of convention applicability validation, no convention rationales in prescribed format, and no convention enrichment of any kind in the Implementation Notes or any other section of any task."

</details>

<details>
<summary>eval-2: 5 failing assertions</summary>

- **Assertion:** "Impact map or task descriptions explicitly flag at least 3 ambiguities from the feature description"
  **Evidence:** "None of the five output files (impact-map.md, task-1 through task-4) contain any explicit mention of ambiguities, unclear requirements, or items needing clarification. The words 'ambiguity', 'ambiguous', 'unclear', 'vague', or 'clarification' do not appear in any output file. The feature description contains numerous ambiguities ('Make the search better', 'some kind of filtering capability', 'Should be fast enough', etc.) but the outputs silently resolve them without flagging them."

- **Assertion:** "Plan acknowledges that 'Better UI' (non-MVP) cannot be planned without design mockups or frontend repository and excludes it from scope"
  **Evidence:** "The impact map only lists trustify-backend and all four tasks are backend-only, so 'Better UI' is effectively excluded from scope. However, there is no explicit acknowledgment anywhere in the outputs that 'Better UI' was excluded because design mockups or a frontend repository are unavailable. The impact map and task descriptions do not mention 'Better UI', 'non-MVP', 'design mockups', or 'frontend repository' at all."

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "None of the four task descriptions contain any section or text labeled 'assumption', 'assumed', or 'pending clarification'. The tasks make numerous implicit assumptions (e.g., task-1 assumes tsvector with 'english' dictionary, task-3 assumes specific filter fields entity_type/severity/date_from/date_to/license, task-4 assumes 30-60 second cache TTL and 5-second query timeout) but none are documented as assumptions."

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "None of the five output files contain any text matching '[sdlc-workflow] Description digest:' or any SHA-256 hash string. No digest comments appear anywhere in the outputs."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the four task descriptions contain any 'Per CONVENTIONS.md §' references or convention applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). The Implementation Notes reference docs/constraints.md sections but do not perform convention-aware enrichment from CONVENTIONS.md with file-type applicability validation. No convention applicability analysis is present in any output."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No digest comments found in any output file. Searched all files for 'digest', 'sha256', 'sha-256' (case-insensitive) and found zero matches. The output files contain only task descriptions without any '[sdlc-workflow] Description digest: sha256:' markers."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention applicability rationales found in any task. Searched all output files for 'Applies:' and 'Per CONVENTIONS' and found zero matches. The tasks reference file patterns and conventions informally (e.g., Task 2 mentions 'field conventions' in Reuse Candidates, Task 5 mentions 'query key conventions') but none include the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "Searched all output files for 'sdlc-workflow', 'Description digest', and 'sha256:'. No description digest comments were found in any output file. No file in the outputs directory contains the required marker format '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention applicability section or rationale in the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' format. The word 'convention' appears only in informal references like 'per the codebase convention' (task-3 line 20, task-4 line 30, task-5 lines 20-21) and 'per the project convention' (task-5 line 21). There is no structured convention-aware enrichment with applicability validation in any output file."

</details>

<details>
<summary>eval-5: 4 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Bookend tasks are missing required sections. task-1-create-feature-branch.md lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. task-7-merge-feature-branch.md also lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Additionally, task-4 through task-6 lack a 'Files to Create' section (though they have 'Files to Modify', satisfying the 'at least one of' requirement). The bookend tasks (1 and 7) fail the 'at least one of Files to Modify or Files to Create' requirement and lack Implementation Notes."

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "No output file contains any mention of a 'workflow:feature-branch' label or any label decision. The impact-map.md discusses workflow mode as 'feature-branch' but does not include a label decision to apply to the feature issue. None of the seven task files mention labels."

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No output file contains any '[sdlc-workflow] Description digest' marker, any SHA-256 hash, or any mention of 'digest' or 'sha256'. The output files consist solely of the impact map and task definition files with no evidence of digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any convention-related content. There are no sections mentioning 'convention', 'applicability', or rationale in the prescribed 'Applies: task modifies...' format. The task files contain no convention enrichment of any kind."

</details>

**Pass rate:** 73% · **Tokens:** 45,989 · **Duration:** 178s

**Baseline** (`f31ccb2`): 84% · 51,938 tokens · 216s

