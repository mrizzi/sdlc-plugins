# Architectural Constraints

Deterministic, verifiable rules that all SDLC workflow skills must follow.
Every rule is pass/fail — not subjective. Each rule traces back to an
existing instruction in a SKILL.md or CLAUDE.md file.

---

## 1. Skill Scope Rules

| # | Constraint | Source |
|---|---|---|
| 1.1 | `plan-feature` MUST NOT modify, create, or delete any source code files in any repository. | `plan-feature/SKILL.md` — Guardrails |
| 1.2 | `plan-feature` MUST NOT use Edit, Write, or Bash tools to change files. Only read-only tools (Read, Glob, Grep, Serena search) are permitted. | `plan-feature/SKILL.md` — Guardrails |
| 1.3 | `plan-feature` output goes to Jira (tasks, comments) — never to the filesystem. | `plan-feature/SKILL.md` — Guardrails |
| 1.4 | `implement-task` MUST keep changes scoped to what the task describes — no unrelated refactoring. | `implement-task/SKILL.md` — Important Rules |
| 1.5 | `implement-task` MUST NOT guess code structure — it must inspect code before modifying it using Serena or Read/Grep/Glob. | `implement-task/SKILL.md` — Important Rules |
| 1.6 | `implement-task` MUST ask the user rather than improvising when the structured description is incomplete. | `implement-task/SKILL.md` — Important Rules |

---

## 2. Commit Rules

| # | Constraint | Source |
|---|---|---|
| 2.1 | Every commit MUST reference a Jira issue ID in the footer (e.g., `Implements TC-123`). | `implement-task/SKILL.md` — Step 9; `methodology.md` — Traceable Implementation |
| 2.2 | Commit messages MUST follow the Conventional Commits specification (`<type>[optional scope]: <description>`). | `implement-task/SKILL.md` — Step 9 |
| 2.3 | Every commit MUST include `--trailer="Assisted-by: Claude Code"` to attribute AI assistance. | `implement-task/SKILL.md` — Step 9 |

---

## 3. PR Rules

| # | Constraint | Source |
|---|---|---|
| 3.1 | The feature branch MUST be named after the Jira issue ID (e.g., `TC-123`). | `implement-task/SKILL.md` — Step 5 |
| 3.2 | After opening a PR, its link MUST be posted as a comment on the Jira task. | `implement-task/SKILL.md` — Step 10; `methodology.md` — Pull Request Workflow |

---

## 4. Task Template Rules

| # | Constraint | Source |
|---|---|---|
| 4.1 | Every generated task description MUST include a **Repository** section (single repository per task). | `plan-feature/SKILL.md` — Task Description Template |
| 4.2 | Every generated task description MUST include a **Description** section. | `plan-feature/SKILL.md` — Task Description Template |
| 4.3 | Every generated task description MUST include an **Acceptance Criteria** section. | `plan-feature/SKILL.md` — Task Description Template |
| 4.4 | Every generated task description MUST include a **Test Requirements** section. | `plan-feature/SKILL.md` — Task Description Template |
| 4.5 | Sections that do not apply (e.g., API Changes for a pure UI task) MUST be omitted rather than left empty. | `plan-feature/SKILL.md` — Template rules |
| 4.6 | File paths in tasks MUST be real paths discovered during repository analysis, not guessed. | `plan-feature/SKILL.md` — Template rules |
| 4.7 | Implementation Notes MUST reference existing patterns found in the code, not abstract guidance. | `plan-feature/SKILL.md` — Template rules |
| 4.8 | Every task created in Jira MUST include the `ai-generated-jira` label. | `plan-feature/SKILL.md` — Step 6a |

---

## 5. Code Change Rules

| # | Constraint | Source |
|---|---|---|
| 5.1 | Changes MUST be scoped to the files listed in Files to Modify and Files to Create — no unrelated files. | `implement-task/SKILL.md` — Step 6, Important Rules |
| 5.2 | Code MUST NOT be modified without first inspecting it (via Serena or Read/Grep/Glob). | `implement-task/SKILL.md` — Step 4, Important Rules |
| 5.3 | Implementation MUST follow the patterns referenced in the task's Implementation Notes. | `implement-task/SKILL.md` — Important Rules |
| 5.4 | Code MUST NOT duplicate existing functionality — reuse or extend existing utilities, helpers, and shared modules when equivalent logic exists. | `implement-task/SKILL.md` — Step 4, Step 6, Step 9 |
| 5.5 | AI MUST NOT start work autonomously — a human must trigger it. | `methodology.md` — Core Principles (Human Driven Workflow) |

---

## Traceability Index

Each constraint above references its source. The full source files are:

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Guardrails (§1.1–1.3), Task Description Template (§4.1–4.8)
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md` — Important Rules (§1.4–1.6, §5.1–5.3), Step 4/6/9 (§5.4), Step 5 (§3.1), Step 9 (§2.1–2.3), Step 10 (§3.2)
- `docs/methodology.md` — Core Principles (§2.1, §3.2, §5.5)
