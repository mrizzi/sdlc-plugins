# Additive-vs-Reductive Test Change Detection for verify-pr

**Date**: 2026-04-16
**Scope**: Adding test change classification to verify-pr's Step 12 (Test Quality) to distinguish additive from reductive test changes
**Reference**: [Autonomous Readiness Plan — Deliverable #4](../superpowers/specs/2026-04-14-autonomous-readiness-plan.md), [Cross-Pollination Analysis — Security Hardening](../superpowers/specs/2026-04-13-fullsend-cross-pollination-analysis.md)

## Overview

verify-pr's Step 12 (Test Quality) currently checks for repetitive test patterns and missing doc comments. It does not distinguish between test changes that strengthen the safety net (additive) and those that weaken it (reductive). This design adds that classification.

The motivation is security: the fullsend threat model identifies "temporal split-payload test poisoning" — where PR 1 weakens tests (classified as low-risk), and PR 2 exploits the blind spot weeks later. Detecting reductive test changes is the defense against this attack pattern.

This design targets verify-pr as it exists today (monolithic Step 12). When verify-pr is later decomposed into sub-agents (autonomous readiness deliverable #2), the detection logic lifts into the test quality sub-agent without changes.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Analysis input | PR diff + base-branch test files | Diff-only misses too many cases — refactoring looks reductive when it isn't. Reading the pre-change state enables distinguishing restructuring from weakening. |
| Execution model | Sub-agent (isolated from main context) | Loading full test file pairs into the main verify-pr context risks hallucination and context pollution. The main agent already holds Jira task, PR metadata, review comments, and all other step outputs. Precedent: Step 5 (Root-Cause Investigation) already uses a sub-agent. |
| Detection approach | Hybrid — structural scan + semantic assessment | Structural scan provides auditable numbers. Semantic assessment catches what numbers miss (e.g., same assertion count but weaker matchers). The structural data anchors the semantic judgment. |
| Report effect | Advisory (WARN), not blocking (FAIL) | Human-driven mode — the reviewer sees the finding and decides. Matches the existing advisory pattern used by Test Quality and Root-Cause Investigation. |
| Autonomous escalation | Documented intent, not implemented | REDUCTIVE/MIXED should trigger `requires-manual-review` in autonomous mode. Stays as a documented comment in SKILL.md until autonomous mode is operational. |

## 1. Sub-Agent Architecture

### What the main agent does

1. Identifies test files in the PR diff (existing Step 12, step 1).
2. For each test file, classifies it as: **new** (not on base branch), **deleted** (not on PR branch), or **modified** (on both). Uses the base branch resolved in Step 3.
3. If any test files are modified or deleted, spawns a sub-agent. New-only test files are inherently additive and do not need sub-agent analysis.
4. The sub-agent receives:
   - List of modified/deleted test file paths
   - Base branch name (for `git show <base-branch>:<path>`)
   - PR branch name (already checked out)

### What the sub-agent does

The sub-agent performs the structural scan and semantic assessment (Sections 2-3 below) in isolation. It never sees the Jira task description, review comments, or other verify-pr step outputs.

### What the sub-agent returns

```
Classification: ADDITIVE | REDUCTIVE | MIXED | NEUTRAL

Structural summary:
  - <file>: +N test functions, -N test functions, +N assertions,
    -N assertions, <other signals>

Semantic assessment: <1-2 sentence explanation of how coverage
intent changed>

Reductive findings (if any):
  - <file>: <what was weakened and why it matters>
```

### What the main agent does with the result

- Combines the sub-agent classification with new-file analysis (Section 4) to produce the overall classification.
- Incorporates the classification and summary into the Step 14 verification report.
- Does not second-guess the sub-agent's analysis — the main agent never saw the test file contents.

## 2. Structural Scan

The first pass — concrete, countable signals. Performed by the sub-agent.

For each **modified** test file:

1. Read the base-branch version: `git show <base-branch>:<file-path>`
2. Read the PR-branch version (already on the checked-out branch).
3. Count the following signals:

| Signal | Additive | Reductive |
|--------|----------|-----------|
| Test functions | Functions added | Functions removed |
| Assertion statements | Assertions added | Assertions removed |
| Assertion specificity | Matchers tightened (e.g., `toBeTruthy` → `toEqual`) | Matchers relaxed (e.g., `toEqual` → `toBeTruthy`) |
| Disable/skip annotations | Annotations removed (re-enabling tests) | Annotations added (`.skip`, `@Disabled`, `@pytest.mark.skip`, `#[ignore]`) |
| Parameterized cases | Cases added to parameterized sets | Cases removed from parameterized sets |
| Mock scope | Mocks narrowed (more specific return values) | Mocks broadened (e.g., `any()` replacing a concrete value) |

For **deleted** test files: all signals are reductive. Read the base-branch version to count what was lost.

For **new** test files: handled by the main agent (inherently additive, no sub-agent analysis needed).

**Language awareness:** The sub-agent uses its knowledge of test frameworks to identify assertion statements, skip annotations, and mock patterns. It does not need an exhaustive per-language list — it reads the code and applies judgment about what constitutes each signal. The signal categories above are the taxonomy; the sub-agent recognizes the language-specific syntax.

**Output:** A tally per file (e.g., "+2 test functions, +5 assertions, -1 assertion relaxed, +0/-0 skip annotations").

## 3. Semantic Assessment

The second pass — evaluating coverage intent. Performed by the sub-agent after the structural scan.

**Purpose:** Determine whether the *meaning* of test coverage changed, not just the counts. Three specific cases the structural scan cannot catch:

1. **Assertion weakening without count change.** Replacing a specific expected value with a broad matcher. Example: `assertEqual(result, {"id": 1, "name": "Alice"})` → `assertTrue(result is not None)`. Same number of assertions, drastically weaker coverage.

2. **Mock broadening that hides behavior.** Replacing a mock that returns a specific error response with one that returns a generic success. The test still passes but no longer exercises the error path.

3. **Restructuring that preserves coverage.** Splitting one test function into three, or consolidating three into one. The structural scan sees functions added/removed, but coverage intent is unchanged. The semantic assessment classifies this as NEUTRAL, preventing a false REDUCTIVE signal.

**Process for each modified test file:**

1. Identify the **behaviors under test** in the base-branch version — what scenarios does each test function exercise? What properties does it verify?
2. Identify the **behaviors under test** in the PR-branch version — same questions.
3. Compare: did any tested behavior lose coverage? Did any assertion become less specific about the expected outcome?
4. Cross-reference with the structural scan — if the structural numbers look reductive but the semantic assessment finds the same behaviors are still covered (restructuring), the semantic assessment overrides to NEUTRAL.

**Scope boundary:** The semantic assessment only answers: "did the PR make the test suite weaker at catching regressions in the code it covers?" It does not judge whether the tests are good enough overall — that is a different concern.

## 4. Classification Logic

The sub-agent produces a classification from the combined structural and semantic signals.

**ADDITIVE** — All of the following:
- No test functions removed
- No assertions removed or relaxed
- No skip/disable annotations added
- No mocks broadened
- Semantic assessment confirms no pre-existing test behavior was weakened

**REDUCTIVE** — Any of the following, with no additive signals:
- Test functions removed without replacement
- Assertions removed without replacement
- Assertions relaxed (less specific expected values)
- Skip/disable annotations added to previously active tests
- Mocks broadened in a way that eliminates error/edge-case coverage
- Semantic assessment identifies coverage that was lost

**MIXED** — Both additive and reductive signals are present. This is the most common classification for real PRs that modify existing tests while adding new ones.

**NEUTRAL** — Test files were modified but coverage intent is unchanged. Restructuring, renaming, extracting helpers, reformatting. The semantic assessment confirms the same behaviors are tested with equivalent specificity.

**N/A** — No test files in the PR diff. Handled by the main agent before spawning the sub-agent.

**The semantic assessment is the tiebreaker.** When the structural scan shows reductive signals but the semantic assessment determines coverage is preserved (e.g., assertions moved to a different function), the semantic assessment overrides to NEUTRAL. When the structural scan shows no reductive signals but the semantic assessment finds weakened coverage (e.g., same assertion count but less specific matchers), the semantic assessment overrides to MIXED or REDUCTIVE.

### Overall classification (main agent)

After the sub-agent returns, the main agent combines the result with new-file analysis:

- If only new test files and sub-agent was not needed: **ADDITIVE**
- If only new test files and sub-agent returns ADDITIVE: **ADDITIVE**
- If sub-agent returns REDUCTIVE or MIXED: use that classification
- If sub-agent returns NEUTRAL and there are new test files: **ADDITIVE**
- If sub-agent returns NEUTRAL and no new test files: **NEUTRAL**

## 5. Reporting and Escalation

### Verification report

The classification appears as a new row in the Step 14 report table, after Test Quality:

```
| Check                      | Result                                | Details   |
|----------------------------|---------------------------------------|-----------|
| Test Quality               | PASS/WARN                             | <summary> |
| Test Change Classification | ADDITIVE/REDUCTIVE/MIXED/NEUTRAL/N/A | <summary> |
```

The summary field contains:
- Structural tallies (e.g., "+7 test functions, +20 assertions")
- Any reductive findings in brief (e.g., "1 assertion relaxed: `get_recommendations` no longer verifies PURL qualifier presence")
- For NEUTRAL: what changed and why it's neutral (e.g., "test helper extracted, no coverage change")

### Effect on overall result

Test Change Classification is **informational** — it does not elevate the overall result to FAIL. It follows the same advisory pattern as Test Quality and Root-Cause Investigation:

| Classification | Effect on overall |
|---|---|
| ADDITIVE | No effect |
| NEUTRAL | No effect |
| MIXED | WARN |
| REDUCTIVE | WARN |
| N/A | No effect |

### Future autonomous mode escalation

In autonomous mode, REDUCTIVE and MIXED classifications should trigger `requires-manual-review` label addition. This is the defense against temporal split-payload test poisoning. The SKILL.md will include a comment documenting this intent, but the behavior is not implemented until autonomous mode is operational.

## 6. SKILL.md Integration

### Where changes land

All changes are in `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`. No new files, no shared resource changes.

### Step 12 structure after the change

The existing Step 12 has 7 sub-steps. The new sub-steps slot in between the doc comment check (steps 5-6) and the record step (step 7):

1. **Steps 1-4** (existing, unchanged): Repetitive test detection
2. **Steps 5-6** (existing, unchanged): Doc comment check
3. **Step 8** (new): Identify test file change types — classify each test file as new, deleted, or modified using the base branch from Step 3
4. **Step 9** (new): Spawn additive-vs-reductive sub-agent — if any test files are modified or deleted, spawn a sub-agent with the file list, base branch name, and PR branch name
5. **Step 10** (new, sub-agent): Structural scan — count test functions, assertions, skip annotations, parameterized cases, mock scope changes per file
6. **Step 11** (new, sub-agent): Semantic assessment — compare behaviors under test in base vs PR versions, determine whether coverage intent changed
7. **Step 12** (new): Classify overall test changes — combine sub-agent result with new-file analysis
8. **Step 13** (renumbered from 7): Record findings — updated to incorporate the new classification alongside existing repetitive test and doc comment results

### Report table update

Step 14 (Generate Report) adds the new row after Test Quality. The note about informational rows that do not affect the overall result is updated to include Test Change Classification alongside Root-Cause Investigation and Test Quality.

## 7. Concrete Examples

### Example 1: Purely additive (trustify PR #2325)

A PR adding a new `query_all_aibom_models` parameterized test function with 19 `#[case]` variants. No existing tests modified.

**Sub-agent result:**
```
Classification: ADDITIVE

Structural summary:
  - modules/fundamental/src/sbom/endpoints/test.rs:
    +1 test function, +19 parameterized cases, +2 assertions, -0/-0/-0

Semantic assessment: New parameterized test function covers the new
/api/v2/sbom/models endpoint with 19 query variants. No existing test
behavior was modified or weakened.

Reductive findings: None
```

**Report row:**
```
| Test Change Classification | ADDITIVE | +1 test function, +19 parameterized cases, +2 assertions. No existing tests modified. |
```

### Example 2: Mixed — predominantly additive with one relaxed assertion (trustify PR #2318)

A PR adding 7 new test functions and refactoring 2 existing tests. One existing assertion was relaxed: the expected package string in `get_recommendations` changed from a full qualified PURL (with `repository_url` and `type` qualifiers) to a versioned PURL without qualifiers.

**Sub-agent result:**
```
Classification: MIXED

Structural summary:
  - modules/fundamental/src/purl/endpoints/test.rs:
    +7 test functions, +2 parameterized cases, +20 assertions,
    +1 helper function, +9 doc comments
    1 assertion relaxed (package string matching)

Semantic assessment: Predominantly additive — 7 new test functions
substantially expand coverage for the recommend_purls endpoint
(dedup, status variants, edge cases, mixed input). One existing
assertion was weakened: the package string assertion in
get_recommendations no longer verifies PURL qualifiers
(repository_url, type). This matches the production code change
but eliminates test coverage for qualifier presence/absence.

Reductive findings:
  - get_recommendations (line ~350): package assertion relaxed from
    full qualified PURL to versioned PURL without qualifiers. The
    test suite no longer verifies any qualifier behavior in
    recommendation responses.
```

**Report row:**
```
| Test Change Classification | MIXED | +7 test functions, +20 assertions. 1 assertion relaxed: `get_recommendations` no longer verifies PURL qualifier presence in package strings. |
```
