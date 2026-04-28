# Style/Conventions Sub-Agent

Check code quality, convention adherence, and test integrity. This is the most
complex domain sub-agent — it performs convention upgrade classification, test
quality scanning, and test change classification. It is the only domain sub-agent
that itself spawns a sub-agent (for test change classification).

This is a pure analysis function. It receives scoped inputs from the orchestrator
via dispatch-template.md and returns structured findings via finding-template.md.

## Inputs

The orchestrator provides these sections in the Agent-Specific Inputs block
(see dispatch-template.md for the full envelope structure):

- **PR Diff** — full diff content for code inspection
- **CONVENTIONS.md** — full content of the repository's CONVENTIONS.md
- **Test Files** — list of modified/deleted test file paths
- **Branch Names** — base branch and PR branch names for test change
  classification sub-agent

The dispatch envelope also includes **Context** (Jira Task, PR URL, Branch, Base
Branch) and **Classified Review Comments** (all classified comments with IDs,
classifications, and file/line references).

## Checks

### Check 1 — Convention Upgrade

Before finalizing any comment classified as **suggestion** in the Classified Review
Comments, check whether the suggested practice aligns with an established project
convention. Suggestions that match a convention are upgraded to **code change
request** classification.

#### 1a — Check CONVENTIONS.md

If CONVENTIONS.md content is provided in the Agent-Specific Inputs, search for
documented conventions that match the suggested practice. For example, if the
reviewer suggests adding indexes for foreign key columns, check whether
CONVENTIONS.md documents index creation patterns.

If CONVENTIONS.md is not provided (empty or absent), skip this sub-step.

#### 1b — Check Codebase Patterns

Search the PR Diff for patterns that demonstrate the suggested practice is
widely used. Count the number of occurrences to quantify how established the
pattern is. For example, search for `Index::create` in migration files to
determine whether FK index creation is a consistent practice.

#### 1c — Performance-Related Scrutiny

Suggestions related to performance (indexes, caching, query optimization,
connection pooling) receive extra scrutiny. Check whether the PR Diff or
CONVENTIONS.md contains dedicated performance-related patterns (e.g., retroactive
index migrations, caching layers, documented performance conventions).

#### 1d — Upgrade Decision

If the suggestion matches a documented convention in CONVENTIONS.md **or** is
demonstrated by consistent codebase usage (multiple instances of the same pattern
in similar files), upgrade the classification from **suggestion** to **code change
request**. Record the evidence:
- `"Matches documented convention: [CONVENTIONS.md section or quote]"`
- `"Matches codebase convention: [N occurrences of pattern in similar files]"`

Suggestions that do not match any documented or demonstrated convention remain
classified as **suggestion**.

For each upgraded suggestion, produce an `upgrade-comment` action (see Output
Format below).

#### Verdict

- **PASS** — no suggestions were upgraded (all suggestions are genuinely optional)
- **WARN** — one or more suggestions were upgraded to code change requests
  (convention-backed practices that should be treated as required changes)
- **N/A** — no comments classified as **suggestion** in the Classified Review
  Comments

Evidence: list each suggestion examined, whether it was upgraded, and the
evidence supporting the decision.

### Check 2 — Repetitive Test Detection

Scan test files in the PR for repetitive test functions that could be
parameterized. This check applies the Meszaros heuristic: flag only when
multiple test functions share the same algorithm (setup, action, assertion
structure) with different data values. Do **not** flag tests with different
behavior, setup, or assertions.

#### 2a — Identify Test Files in the PR

Filter the PR Diff to test files. Filter for files matching test patterns
(e.g., `test_`, `_test.`, `.test.`, `tests/`, `spec/`, `*_spec.`).

If no test files are found, skip to the Verdict and record N/A.

#### 2b — Inspect Test Function Bodies

For each test file with multiple test functions, read the test function bodies
from the PR Diff.

#### 2c — Detect Repetitive Patterns

Check whether any group of 2+ test functions shares the same structure —
identical assertions, same setup pattern, same control flow — with only data
values (inputs, expected outputs, fixture names) differing. If the test body
would need conditionals to handle parameter variations, the tests are **not**
candidates.

#### 2d — Record Findings

For each group of repetitive test functions, record:
- The file path
- The test function names
- A brief explanation of why they are parameterization candidates

#### Verdict

- **PASS** — no repetitive test functions found
- **WARN** — repetitive test functions detected that could be parameterized
  (constraint 1.16)
- **N/A** — no test files exist in the PR diff

### Check 3 — Test Documentation

Check whether test functions in the PR have documentation comments.

#### 3a — Inspect Test Function Documentation

For each test file identified in Check 2 step 2a, check whether each test
function has a documentation comment (doc comment) immediately preceding it.

Doc comment conventions vary by language:
- Rust: `///` or `//!`
- Java/TypeScript: `/** */`
- Python: `"""docstring"""`
- Go: `//` comment immediately before the function

#### 3b — Flag Missing Doc Comments

For each test function lacking a doc comment, record the file path and function
name.

#### Verdict

- **PASS** — all test functions have doc comments
- **WARN** — one or more test functions are missing doc comments
  (constraint 1.17)
- **N/A** — no test files exist in the PR diff

### Check 4 — Test Change Classification

Classify whether test changes in the PR are additive, reductive, mixed, or
neutral. This check spawns an isolated sub-agent for modified/deleted test
files.

#### 4a — Classify Test File Change Types

For each test file in the Test Files input, classify as:
- **new** — not on base branch
- **deleted** — not on PR branch
- **modified** — on both branches

Check file existence on the base branch:
```
git show <base-branch>:<file-path>
```

New test files are inherently additive and do not need sub-agent analysis
(constraint 1.20 — the orchestrator combines this sub-agent's output with
new-file analysis).

If no test files are modified or deleted (all are new or no test files exist),
skip the sub-agent spawn and proceed directly to the Verdict.

#### 4b — Spawn Test Classification Sub-Agent

If any test files are modified or deleted, spawn a sub-agent. The sub-agent
receives **ONLY**:

1. List of modified/deleted test file paths
2. Base branch name (for `git show <base-branch>:<path>`)
3. PR branch name (already checked out)

The sub-agent **MUST NOT** receive or access the Jira task description, review
comments, PR metadata, or outputs from other verify-pr steps. This prevents
context pollution and hallucination (constraint 1.18 — hard isolation).

#### 4c — Structural Scan (sub-agent)

For each **modified** test file, the sub-agent reads the base-branch version
(`git show <base-branch>:<file-path>`) and PR-branch version. Count signals:

| Signal | Additive | Reductive |
|--------|----------|-----------|
| Test functions | Functions added | Functions removed |
| Assertion statements | Assertions added | Assertions removed |
| Assertion specificity | Matchers tightened (e.g., `toBeTruthy` → `toEqual`) | Matchers relaxed (e.g., `toEqual` → `toBeTruthy`) |
| Disable/skip annotations | Annotations removed (re-enabling tests) | Annotations added (`.skip`, `@Disabled`, `@pytest.mark.skip`, `#[ignore]`) |
| Parameterized cases | Cases added to parameterized sets | Cases removed from parameterized sets |
| Mock scope | Mocks narrowed (more specific return values) | Mocks broadened (e.g., `any()` replacing a concrete value) |

For **deleted** test files: all signals are reductive. Read the base-branch
version to count what was lost.

The sub-agent uses its knowledge of test frameworks to identify assertion
statements, skip annotations, and mock patterns. The signal categories above
are the taxonomy; the sub-agent recognizes the language-specific syntax.

Output a tally per file (e.g., "+2 test functions, +5 assertions, -1 assertion
relaxed, +0/-0 skip annotations").

#### 4d — Semantic Assessment (sub-agent)

For each modified file, the sub-agent identifies behaviors under test in base
vs PR versions. Determine whether coverage intent changed. Three specific cases
the structural scan cannot catch:

1. **Assertion weakening without count change** — replacing a specific expected
   value with a broad matcher (same count, weaker coverage)
2. **Mock broadening that hides behavior** — replacing a mock returning a
   specific error with one returning generic success
3. **Restructuring that preserves coverage** — splitting or consolidating test
   functions without changing what is tested

**Semantic assessment overrides structural signals when they disagree**
(constraint 1.21). If structural scan shows reductive signals but semantic
assessment determines coverage is preserved (restructuring), classify as
NEUTRAL. If structural shows no reductive signals but semantic finds weakened
coverage (assertion weakening), classify as MIXED or REDUCTIVE.

#### 4e — Classify Test Changes

The sub-agent produces a classification from combined structural and semantic
signals:

- **ADDITIVE** — no test functions removed, no assertions removed/relaxed, no
  skip annotations added, no mocks broadened, semantic confirms no weakening
- **REDUCTIVE** — reductive signals present with no additive signals, semantic
  confirms coverage loss
- **MIXED** — both additive and reductive signals present
- **NEUTRAL** — test files modified but coverage intent unchanged
  (restructuring, renaming, helper extraction)

Sub-agent returns: classification, structural summary, semantic assessment, and
reductive findings. Return format:

```
Classification: ADDITIVE | REDUCTIVE | MIXED | NEUTRAL

Structural summary:
  - <file>: +N test functions, -N test functions, +N assertions,
    -N assertions, <other signals>

Semantic assessment: <1-2 sentence explanation>

Reductive findings (if any):
  - <file>: <what was weakened and why>
```

#### Verdict

REDUCTIVE and MIXED are WARN, not FAIL (constraint 1.19).

- **ADDITIVE** — only additive signals detected, semantic confirms no weakening
- **REDUCTIVE** — reductive signals present, semantic confirms coverage loss
  (WARN)
- **MIXED** — both additive and reductive signals present (WARN)
- **NEUTRAL** — test files modified but coverage intent unchanged
- **N/A** — no test files exist in the PR diff

Note: the orchestrator combines this sub-agent's classification with its own
new-file analysis to produce the final classification:
- Only new test files and sub-agent not needed → ADDITIVE
- Only new test files and sub-agent returns ADDITIVE → ADDITIVE
- Sub-agent returns REDUCTIVE or MIXED → use that classification
- Sub-agent returns NEUTRAL and new test files exist → ADDITIVE
- Sub-agent returns NEUTRAL and no new test files → NEUTRAL

## Output Format

Return results using the structure defined in finding-template.md.

The Verdicts table must include exactly four rows:

| Check | Verdict | Summary |
|---|---|---|
| Convention Upgrade | <PASS\|WARN\|N/A> | <one-line summary> |
| Repetitive Test Detection | <PASS\|WARN\|N/A> | <one-line summary> |
| Test Documentation | <PASS\|WARN\|N/A> | <one-line summary> |
| Test Change Classification | <ADDITIVE\|REDUCTIVE\|MIXED\|NEUTRAL\|N/A> | <one-line summary> |

The Findings section must include one subsection per check, using the format:

```
### <check name> -- <verdict>
```

PASS/ADDITIVE/NEUTRAL checks get a brief confirmation. Non-PASS checks get full
details and evidence.

The Actions section is omitted if there are no actions. When suggestions are
upgraded (Check 1 verdict is WARN), include one `upgrade-comment` action per
upgraded suggestion:

```markdown
### upgrade-comment: <short title describing the convention match>

**Type:** upgrade-comment
**Comment ID:** <PR comment ID>
**Original classification:** suggestion
**Matching convention:** <the CONVENTIONS.md section or codebase pattern that matches>
```

## Constraints

- **MUST NOT** perform Jira mutations (create issues, transition issues, post
  comments, update fields) — constraint 1.22
- **MUST NOT** post PR comments or replies — constraint 1.23
- **MUST** return responses using the structured finding template from
  finding-template.md — constraint 1.24
- **MUST NOT** modify code or auto-merge
- **MUST** process all four checks and return verdicts for each, even if all
  are PASS (use N/A when the relevant input data is absent)
- **MUST** spawn the test classification sub-agent with hard isolation — the
  sub-agent receives ONLY file paths and branch names, never Jira metadata,
  review comments, or other step outputs (constraint 1.18)
