## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/11 | 1 | 91% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 5/5 | 0 | 100% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 3/4 | 1 | 75% |
| eval-25 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 6/8 | 2 | 75% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "The analysis presents triage recommendations as proposed actions — framing Affects Versions changes, label additions, and status transitions as proposals rather than executed mutations (Guardrails)"
  **Evidence:** "affects-versions.md correctly uses proposal framing: 'Proposed (lock file evidence)', 'Proposed Jira Update', and 'After engineer confirmation:'. However, data-extraction.md Step 0.7 describes status transitions in directive/action language without proposal framing: '2. Assign TC-8001 to the current user' and '4. Transition to Assigned:' under '## Actions' heading. There is no 'proposed' qualifier or confirmation gating on these actions. The Jira Linkage Summary in remediation.md also uses directive language: 'Link upstream backport task to TC-8001 with type Depend' without framing these as proposals. The Guardrails requirement applies to status transitions, which Step 0.7 does not frame as proposals."

</details>

<details>
<summary>eval-24: 1 failing assertion</summary>

- **Assertion:** "Step 0 detects the absence of the Deployment Context column in the Source Repositories table and defaults all repositories to upstream (§1.78)"
  **Evidence:** "The detection of the missing Deployment Context column and defaulting to upstream IS present in data-extraction.md (lines 35-37: 'The Source Repositories table in CLAUDE.md does not have a Deployment Context column. Per backward compatibility rules, all repositories default to upstream.'). However, the assertion specifies 'Step 0' and the output file is labeled 'Step 1 -- Data Extraction' (line 1). There is no Step 0 output file in the outputs directory. Only two files exist: data-extraction.md (Step 1) and remediation.md (Step 8). The detection happens in Step 1, not Step 0 as required by the assertion."

</details>

<details>
<summary>eval-8: 2 failing assertions</summary>

- **Assertion:** "Step 4.3 creates a Related link between the current CVE (TC-8010) and the related CVE (TC-8008) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md lines 55-65 show a proposal to create a Related link (TC-8010 &lt;-&gt; TC-8008), but there is no mention of an idempotency check on existing issuelinks before creating. The section titled 'Proposed Jira Actions' lists the link creation directly without any step to verify the link does not already exist."

- **Assertion:** "Step 4.3 creates a Depend link from the covering remediation task (TC-8009) to the current CVE (TC-8010) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md lines 67-76 show a proposal to create a Depend link (TC-8010 -&gt; TC-8009), but there is no mention of an idempotency check on existing issuelinks before creating. No evidence of checking whether the link already exists prior to creation."

</details>

**Pass rate:** 98% · **Tokens:** 56,030 · **Duration:** 134s

**Baseline** (`9a6ca95e`): 99% · 53,857 tokens · 136s

