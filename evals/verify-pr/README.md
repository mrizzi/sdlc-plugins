# verify-pr Evals

Evaluations for the `verify-pr` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Passing PR | PR satisfying all acceptance criteria, no reviews. The golden path. |
| 2 | Failing PR | PR missing several acceptance criteria. Tests gap detection accuracy. |
| 3 | PR with review feedback | PR with reviewer comments requiring classification and sub-task creation. Tests review feedback resolution (Step 4). |
| 4 | Adversarial task | Task description with injected instructions in acceptance criteria. Tests injection resistance. |
| 5 | PR with test changes | PR modifying existing test files with reductive changes. Tests additive-vs-reductive classification (Step 12 sub-steps 8-12). |

## Fixture files

Files in `files/` simulate what MCP tools and GitHub CLI would return during
a real skill invocation. The eval prompt instructs the agent to read these
files instead of calling external tools.

### Task descriptions (`task-*.md`)

Mock Jira task descriptions in Markdown. Each contains task metadata and
structured sections matching the task-description-template.md format
(Repository, Description, Files to Modify, Acceptance Criteria, etc.).

### PR diffs (`pr-diff-*.md`)

Mock `gh pr diff` output in unified diff format. Each diff shows file
changes with `+`/`-` line markers, file headers, and hunk ranges matching
the corresponding task's expected scope.

### Review comments (`pr-review-comments.md`)

Mock `gh api repos/{owner}/{repo}/pulls/{number}/reviews` and
`gh api repos/{owner}/{repo}/pulls/{number}/comments` JSON output.
Contains structured review data with comment IDs, file paths, line
numbers, and reviewer classifications.

### Repository manifest (`repo-backend.md`)

Directory tree snapshot of the trustify-backend repository showing module
structure, key files, and coding conventions. Adapted from the
plan-feature eval suite.

## Constraint coverage

Each test case includes assertions verifying compliance with constraints
from `docs/constraints.md`:

| Constraint | ID | Coverage |
|---|---|---|
| verify-pr MUST read PR reviews | §1.10 | Test 3 (review feedback scenario) |
| verify-pr MUST NOT modify code | §1.11 | All tests (assertion in every case) |
| Sub-tasks MUST follow task template with Target PR and Review Context | §1.12 | Test 3 (sub-task format assertions) |
| verify-pr MUST NOT auto-merge | §1.13 | All tests (assertion in every case) |

## Running

```
/skill-litmus:run-evals Run evals for verify-pr.
Evals path: evals/verify-pr/evals.json
Workspace: /tmp/verify-pr-eval
```
