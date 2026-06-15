## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 5/10 | 5 | 50% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-5: 5 failing assertions</summary>

- **Assertion:** "The report contains a Test Change Classification row with MIXED — both additive and reductive signals are present across the test file changes"
  **Evidence:** "The report summary table (report.md line 14) shows: '| Test Change Classification | ADDITIVE | Net +3 test functions, +10 assertions; removed test (`test_recommend_purls_with_qualifiers`) replaced by stronger behavioral equivalent (`test_recommend_purls_dedup`); 3 new tests in `purl_simplify.rs` |'. The classification is ADDITIVE, not MIXED."

- **Assertion:** "The structural summary or reductive findings identify the removed test function test_recommend_purls_with_qualifiers as a reductive signal"
  **Evidence:** "Report.md line 14 mentions the removed test but characterizes it as 'replaced by stronger behavioral equivalent (`test_recommend_purls_dedup`)' rather than identifying it as a reductive signal. The overall classification is ADDITIVE, and no reductive findings section exists in the report."

- **Assertion:** "The structural summary or reductive findings note the assertion change in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers, which the semantic assessment may identify as a relaxation contributing to the MIXED classification"
  **Evidence:** "Criterion-1.md references the assertion 'assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")' but only describes it as confirming the new behavior, not as a change from a previous assertion that checked a fully qualified PURL with qualifiers. No file in the outputs identifies this assertion change as a relaxation or reductive signal. The report.md does not mention this assertion change at all."

- **Assertion:** "The test change classification verdict appears in the verification report summary table and is accompanied by a detailed analysis section explaining the structural and semantic assessment"
  **Evidence:** "The verdict appears in the summary table (report.md line 14): '| Test Change Classification | ADDITIVE |'. However, there is no separate detailed analysis section explaining structural and semantic assessment. The details are provided only as inline text within the table cell ('Net +3 test functions, +10 assertions; removed test... replaced by stronger behavioral equivalent...; 3 new tests in purl_simplify.rs'). No heading like 'Test Change Classification Analysis' or subsections for structural/semantic assessment exist in the report."

- **Assertion:** "The test change classification analysis is based on comparing base-branch and PR-branch file content (function additions, removals, assertion changes) — the structural and semantic assessment references test file content, not acceptance criteria or task requirements (constraint 1.18)"
  **Evidence:** "The report does not contain a structural and semantic assessment section. The Test Change Classification row in the summary table provides summary metrics ('Net +3 test functions, +10 assertions') but does not explicitly reference comparing base-branch and PR-branch file content. No output file describes a comparison of base-branch vs PR-branch test files. The criterion files analyze the PR changes against acceptance criteria, not base-branch vs PR-branch test content."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "report.md line 6: '| Root-Cause Investigation | N/A | Review feedback is repo-specific (Markdown convention for this project); no universal skill gap identified |'. The Root-Cause Investigation verdict IS N/A. While the investigation pipeline did process the review feedback (the N/A reasoning explains why -- 'repo-specific' finding, 'no universal skill gap'), the verdict is still N/A, which contradicts the assertion that requires 'not N/A'."

</details>

**Pass rate:** 90% · **Tokens:** 65,214 · **Duration:** 256s

**Baseline** (`f196a97`): 95% · 65,724 tokens · 275s

