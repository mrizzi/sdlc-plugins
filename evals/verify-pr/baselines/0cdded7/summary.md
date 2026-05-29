## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/11 | 1 | 91% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 12/14 | 2 | 86% |
| eval-4 | 9/10 | 1 | 90% |
| eval-5 | 8/10 | 2 | 80% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "report.md line 13 states 'Test Quality | PASS | 4 integration tests with doc comments; no repetitive parameterization candidates; no eval results to assess'. While 'no eval results to assess' implies Eval Quality is effectively N/A, the report does NOT explicitly show Eval Quality as a separate N/A verdict nor does it mention the 3-criteria detection mechanism (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals). The assertion requires that the report show this specific detection logic and its N/A outcome; the report only has a brief parenthetical reference within the combined Test Quality row."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md does not contain an 'Eval Quality' row or section anywhere. The Test Quality row (line 21) shows 'N/A | No test files exist in the PR diff' but does not mention Eval Quality. There is no mention of the 3-criteria detection mechanism (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) anywhere in report.md or any criterion file. The assertion requires a specific Eval Quality entry with N/A and details about the detection criteria, which is absent from the outputs."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "The review comment about adding an index (id 30002) is classified as a code change request (or upgraded suggestion) and triggers sub-task creation"
  **Evidence:** "review-30002.md: '## Classification: Suggestion' with explicit statement 'this suggestion cannot be upgraded to a code change request based on convention evidence.' report.md table row: '30002 | reviewer-a | Suggestion | No sub-task (no convention evidence to upgrade)'. No subtask file exists for comment 30002. The assertion requires either direct classification as code change request OR upgrade from suggestion, and sub-task creation. Neither occurred."

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "review-30002.md classified as 'Suggestion' with no upgrade. report.md table row: '30002 | reviewer-a | Suggestion | No sub-task (no convention evidence to upgrade)'. No subtask-2.md or any subtask file referencing comment 30002 exists in the outputs directory. The assertion requires a sub-task to be created for 30002 regardless of classification path, but no sub-task was created."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md does not contain an 'Eval Quality' row or any mention of eval quality, eval result reviews, github-actions[bot], '## Eval Results' marker, or 'sdlc-workflow/run-evals' detection. While the report has a 'Test Quality | WARN' row (line 37), there is no explicit Eval Quality assessment or N/A designation. The assertion requires Eval Quality to be explicitly shown as N/A, but this domain is entirely absent from the report."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "The structural summary or reductive findings identify the relaxed assertion in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers"
  **Evidence:** "Report line 72 identifies the assertion change but characterizes it as 'Assertion specificity: tightened -- assertions now check for exact PURL format and absence of qualifiers, rather than checking qualifier presence'. This contradicts the assertion's characterization as 'relaxed'. Line 84 also identifies the change: 'assertion changed from full qualifier PURL to `pkg:maven/org.apache/commons-lang3@3.12`' but this is in the Test Requirements Verification section, not in the reductive findings. The report does not identify this as a relaxed/reductive signal — it calls it 'tightened' instead."

- **Assertion:** "The test change classification is produced by the Style/Conventions sub-agent (which spawns a test classification sub-agent for modified files) — the classification verdict is attributed to the Style/Conventions domain in the report"
  **Evidence:** "The report does not mention 'Style', 'Conventions', 'sub-agent', or 'domain' anywhere. The Test Change Classification appears as a standalone row in the report table (line 14) and has its own detailed section (lines 66-78) but is not attributed to any Style/Conventions domain or sub-agent."

</details>

**Pass rate:** 88% · **Tokens:** 57,315 · **Duration:** 184s

**Baseline** (`6b49958`): 100% · 59,008 tokens · 180s

