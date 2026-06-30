## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 9/10 | 1 | 90% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
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
  **Evidence:** "affects-versions.md section 'Proposed Correction' uses proposal framing ('Proposed:', 'Remove', 'Add'). However, remediation.md 'Post-triage' section (lines 196-200) uses imperative executed-action framing: 'Add ai-cve-triaged label to TC-8001', 'Post summary comment on TC-8001', 'Transition TC-8001 to In Progress', 'Assign TC-8001 to current user'. These are stated as actions to execute, not proposals. The Jira Update section in affects-versions.md also shows a concrete jira.edit_issue() call rather than framing it as a proposal. The status transition 'Transition TC-8001 to In Progress' is presented as an action to take, not a recommended proposal."

</details>

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The SBOM verification result is presented alongside the rpms.lock.yaml result in the dependency chain output, not as a separate section (Step 2.3.5 sub-step 6)"
  **Evidence:** "The SBOM verification results are in a separate file (sbom-verification.md), not integrated into the dependency chain output in version-impact.md. In version-impact.md, the dependency chain section (lines 35-37) merely references the separate file: "See sbom-verification.md for the full SBOM verification results and dependency chain analysis for the affected versions." The rpms.lock.yaml results and SBOM results are presented in different files rather than alongside each other in a single dependency chain output. While sbom-verification.md itself does present both signals together in per-version tables, the version-impact.md dependency version extraction table (lines 21-27) contains only rpms.lock.yaml data with no SBOM columns."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The output files only document the behavior for the current CVE (CVE-2026-31812, CVSS 7.5 High). While embargo-check.md line 12 states the threshold as 'Critical or Important severity (CVSS &gt;= 7.0)', there is no explicit statement or evidence in any output file that the gate is skipped silently for CVEs with CVSS &lt; 7.0. The eval only tested a high-severity CVE, so there is no concrete evidence demonstrating the skip behavior for low/moderate severity cases."

</details>

**Pass rate:** 97% · **Tokens:** 49,041 · **Duration:** 111s

**Baseline** (`718f1017`): 99% · 56,582 tokens · 119s

