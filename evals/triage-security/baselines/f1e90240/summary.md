## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 1/4 | 3 | 25% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-26 | 5/5 | 0 | 100% |
| eval-27 | 5/5 | 0 | 100% |
| eval-28 | 5/5 | 0 | 100% |
| eval-29 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-30 | 3/4 | 1 | 75% |
| eval-31 | 4/4 | 0 | 100% |
| eval-32 | 4/4 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "SBOM verification uses cosign download sbom to compare the final container image SBOM against the base image SBOM (Step 2.3.5 sub-steps 2 and 4)"
  **Evidence:** "The outputs mention comparison between final image SBOM and base image SBOM (e.g., 'present in BOTH final image SBOM and base image SBOM') but never reference 'cosign download sbom' or 'cosign' anywhere. There is no evidence that cosign was used as the mechanism to retrieve the SBOMs. The assertion specifically requires cosign download sbom as the tool, and it is absent from both output files."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the positive case where CVSS 7.5 (&gt;= 7.0) triggers the gate. While embargo-check.md line 15 defines 'Threshold | CVSS &gt;= 7.0', there is no explicit statement or evidence showing that the gate is skipped silently for CVEs with CVSS &lt; 7.0. The threshold definition implies below-threshold CVEs would not meet the condition, but there is no direct evidence of silent skipping behavior — the output could equally result in a different message, a log entry, or other non-silent handling. Per grading rules, burden of proof is on PASS, and no explicit evidence of below-threshold behavior exists in the outputs."

</details>

<details>
<summary>eval-20: 3 failing assertions</summary>

- **Assertion:** "Step 0.3 determines the matrix is within the 14-day threshold and proceeds without displaying a staleness warning"
  **Evidence:** "staleness-check.md lines 28-29 compute the age as 24 days and the assessment tables (lines 39-40, 49-50) explicitly state 'STALE (24 days &gt; 14-day threshold)'. Line 54 confirms 'The security matrix was last updated on 2026-06-28 (24 days ago), which exceeds the 14-day staleness threshold.' The matrix was determined to be stale, not within the threshold, and a staleness warning was displayed."

- **Assertion:** "No user prompt or options are presented for a fresh matrix — the check is silent on success"
  **Evidence:** "staleness-check.md lines 58-73 present explicit user-facing options for both streams: '1. Refresh now', '2. Proceed anyway', '3. Stop'. The check was not silent; it surfaced a staleness warning with interactive options because the matrix was deemed stale (24 days old)."

- **Assertion:** "The triage continues to Step 0.5 and beyond without interruption from the staleness check"
  **Evidence:** "staleness-check.md line 76 states 'The staleness warning should be acknowledged before proceeding to Step 1', confirming the staleness check caused an interruption. The workflow only continues because line 76 assumes 'the engineer chooses Option 2: Proceed anyway', meaning continuation was conditional on user acknowledgment rather than uninterrupted."

</details>

<details>
<summary>eval-30: 1 failing assertion</summary>

- **Assertion:** "The missing section is NOT auto-repaired — only Forward Pointer is eligible for auto-repair"
  **Evidence:** "The missing section was not auto-repaired (line 41: 'None.' under Auto-Repairs Applied; line 45: 'non-repairable issues found'). However, the output never states that only Forward Pointer is eligible for auto-repair. No auto-repair eligibility rules are mentioned anywhere in the output, so the Forward Pointer exclusivity claim cannot be verified."

</details>

**Pass rate:** 96% · **Tokens:** 54,480 · **Duration:** 129s

**Baseline** (`1dab64e0`): 99% · 58,180 tokens · 124s

