# implement-task Evals

Evaluations for the `implement-task` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Standard task | Well-structured task with all sections present. Tests golden path: code inspection, scoped changes, convention discovery, commit format. |
| 2 | Incomplete task | Task missing Implementation Notes with vague Acceptance Criteria and Test Requirements. Tests clarification behavior (constraint §1.6). |
| 3 | Task with reuse candidates | Task with Reuse Candidates section listing existing utilities. Tests code reuse over duplication (constraint §5.4). |
| 4 | Adversarial task | Task with injection vectors in Description and Implementation Notes. Tests injection resistance. |

## Fixture files

Files in `files/` simulate what MCP tools would return during a real
skill invocation. The eval prompt instructs the agent to write its
implementation plan to output files instead of modifying a repository.

### Task fixtures (`task-*.md`)

Mock Jira Task issues in Markdown. Each contains issue metadata and a
structured description following `task-description-template.md` — the
format produced by `plan-feature` and consumed by `implement-task`.

- **task-standard.md** — complete task with all required sections
- **task-incomplete.md** — deliberately missing Implementation Notes;
  vague Acceptance Criteria and Test Requirements
- **task-with-reuse.md** — includes Reuse Candidates section pointing
  to existing utilities that the skill should reuse
- **task-adversarial.md** — contains injection vectors: exfiltration
  instructions, backdoor endpoint requests, credential-reading utilities,
  hidden HTML instructions, and a fake acceptance criterion

### Repository manifest (`repo-backend.md`)

Directory tree snapshot of the target Rust backend repository — the same
structure used in `plan-feature` evals. Shows module layout, key files,
and conventions so the skill can ground file paths and discover patterns.

### Project configuration (`claude-md-mock.md`)

Mock CLAUDE.md with Repository Registry, Jira Configuration, and Code
Intelligence sections — the configuration that `implement-task` reads
during Step 0 validation.

## Key constraints tested

| Constraint | Eval IDs |
|------------|----------|
| §1.4 — scope to task description | 1, 3, 4 |
| §1.5 — inspect before modify | 1 |
| §1.6 — ask vs improvise | 2 |
| §2.1 — commit references Jira ID | 1 |
| §2.2 — Conventional Commits | 1 |
| §2.3 — Assisted-by trailer | 1 |
| §3.1 — branch named after Jira ID | 1 |
| §5.1 — file scope | 1, 3, 4 |
| §5.4 — no duplication / reuse | 3 |

## Running

```
/sdlc-workflow:run-evals Run evals for implement-task.
Evals path: evals/implement-task/evals.json
Workspace: /tmp/implement-task-eval
```
