## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 9/10 | 1 | 90% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 4/5 | 1 | 80% |
| eval-16 | 7/7 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "The analysis presents triage recommendations as proposed actions — framing Affects Versions changes, label additions, and status transitions as proposals rather than executed mutations (Guardrails)"
  **Evidence:** "Mixed framing. affects-versions.md correctly uses 'Proposed Correction' (line 32) and 'Proposed Jira Mutation' (line 42). remediation.md uses 'Proposed Jira Linkage' (line 137) and 'Proposed Cross-Stream Impact Comment' (line 164). However, remediation.md lines 182-190 list 'Post-Triage Actions' as imperative directives: '1. Add ai-cve-triaged label to TC-8001', '3. Transition TC-8001 to In Progress', '4. Assign TC-8001 to current user'. These are framed as actions to take, not proposals. Additionally, line 17 states 'The Affects Versions field has been corrected' using past tense suggesting the mutation was already executed rather than proposed. The label additions and status transitions in the Post-Triage Actions section are not framed as proposals."

</details>

<details>
<summary>eval-15: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the ProdSec Jira account ID from the Security Configuration as an optional field without raising an error (Step 0 config validation)"
  **Evidence:** "No Step 0 output file exists in the outputs directory. The four output files are: data-extraction.md (Step 1), version-impact.md (Step 2), affects-versions.md (Step 3), and remediation.md (Step 7). There is no explicit evidence of Step 0 config validation extracting the ProdSec Jira account ID as an optional field from the Security Configuration."

</details>

**Pass rate:** 98% · **Tokens:** 41,725 · **Duration:** 94s

**Baseline** (`1dfe8af`): 99% · 42,610 tokens · 91s

