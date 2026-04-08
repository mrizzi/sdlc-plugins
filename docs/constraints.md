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
| 1.7 | `define-feature` MUST NOT modify, create, or delete any files in any repository. Only Jira MCP tools are permitted for output. | `define-feature/SKILL.md` — Guardrails |
| 1.8 | `define-feature` MUST NOT fabricate content. All Feature description content must come from user input. | `define-feature/SKILL.md` — Guardrails |
| 1.9 | `define-feature` MUST NOT create a Jira issue without showing a full preview and receiving explicit user approval. | `define-feature/SKILL.md` — Important Rules |
| 1.10 | `verify-pr` MUST read PR reviews and comments to identify code change requests from reviewers. | `verify-pr/SKILL.md` — Step 4 (Review Feedback Resolution) |
| 1.11 | `verify-pr` MUST NOT modify code. It only verifies, creates sub-tasks, and reports. | `verify-pr/SKILL.md` — Important Rules |
| 1.12 | `verify-pr` sub-tasks MUST follow the plan-feature task template structure and include Target PR and Review Context sections. | `verify-pr/SKILL.md` — Step 4d |
| 1.13 | `verify-pr` MUST NOT auto-merge. Merging is always a human decision. | `verify-pr/SKILL.md` — Important Rules |
| 1.14 | `verify-pr` root-cause tasks MUST target the workflow phase where the gap originated, not always the implementation phase. | `verify-pr/SKILL.md` — Step 5b |
| 1.15 | `implement-task` MUST check out the existing PR branch (instead of creating a new one) when a Target PR section is present in the task description. | `implement-task/SKILL.md` — Step 5 (Target PR flow) |
| 1.16 | `verify-pr` MUST flag repetitive test functions that could be parameterized as a WARN finding, applying the Meszaros heuristic as the decision boundary. | `verify-pr/SKILL.md` — Step 12 |
| 1.17 | `verify-pr` MUST flag test functions missing doc comments as a WARN finding. | `verify-pr/SKILL.md` — Step 12 |

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
| 4.5 | Sections that do not apply (e.g., API Changes for a pure UI task, Documentation Updates when no docs are impacted) MUST be omitted rather than left empty. | `plan-feature/SKILL.md` — Template rules |
| 4.6 | File paths in tasks MUST be real paths discovered during repository analysis, not guessed. | `plan-feature/SKILL.md` — Template rules |
| 4.7 | Implementation Notes MUST reference existing patterns found in the code, not abstract guidance. | `plan-feature/SKILL.md` — Template rules |
| 4.8 | Every task created in Jira MUST include the `ai-generated-jira` label. | `plan-feature/SKILL.md` — Step 6a |
| 4.9 | Tasks that change public APIs, configuration, setup steps, or architectural patterns SHOULD include an optional **Documentation Updates** section listing which docs need updating and what content to add or revise. | `plan-feature/SKILL.md` — Template rules |
| 4.10 | Tasks SHOULD include a **Reuse Candidates** section when overlapping code (domain logic, components, utilities, or patterns) was found during repository analysis, listing file paths, symbol names, and relevance descriptions. | `plan-feature/SKILL.md` — Task Description Template |
| 4.11 | When a task's scope matches a convention from CONVENTIONS.md (e.g., migrations with FK columns requiring indexes), the Implementation Notes MUST include explicit guidance referencing the convention by section name with a concrete example file. | `plan-feature/SKILL.md` — Step 5 (Convention-aware task enrichment) |

---

## 5. Code Change Rules

| # | Constraint | Source |
|---|---|---|
| 5.1 | Changes MUST be scoped to the files listed in Files to Modify and Files to Create — no unrelated files. | `implement-task/SKILL.md` — Step 6, Important Rules |
| 5.2 | Code MUST NOT be modified without first inspecting it (via Serena or Read/Grep/Glob). | `implement-task/SKILL.md` — Step 4, Important Rules |
| 5.3 | Implementation MUST follow the patterns referenced in the task's Implementation Notes. | `implement-task/SKILL.md` — Important Rules |
| 5.4 | Code MUST NOT duplicate existing functionality — reuse or extend existing utilities, helpers, and shared modules when equivalent logic exists. | `implement-task/SKILL.md` — Step 4, Step 6, Step 9 |
| 5.5 | AI MUST NOT start work autonomously — a human must trigger it. | `methodology.md` — Core Principles (Human Driven Workflow) |
| 5.6 | After implementation, each new feature MUST be traced through its complete data-flow lifecycle (input → processing → output) — incomplete paths must be fixed before committing. | `implement-task/SKILL.md` — Step 9 |
| 5.7 | Modified or created code that implements an interface, trait, or type contract MUST have all required methods, properties, and type signatures verified as complete before committing. | `implement-task/SKILL.md` — Step 9 |
| 5.8 | Modified or created code MUST be compared against sibling implementations for parity on cross-cutting concerns (capabilities, error handling, logging, configuration) — gaps must be fixed or explicitly approved by the user before committing. | `implement-task/SKILL.md` — Step 9 |
| 5.9 | implement-task SHOULD prefer parameterized tests when multiple test cases exercise the same behavior with different inputs, applying the Meszaros heuristic as the decision boundary. | `implement-task/SKILL.md` — Step 7 |
| 5.10 | implement-task MUST NOT introduce parameterized test patterns if sibling test analysis shows the project does not use them. | `implement-task/SKILL.md` — Step 7 |
| 5.11 | `implement-task` MUST add a doc comment to every test function it creates, regardless of sibling test documentation patterns. | `implement-task/SKILL.md` — Step 7 |
| 5.12 | `implement-task` MUST add given-when-then inline comments to non-trivial test functions (tests with distinct setup, action, and assertion phases). | `implement-task/SKILL.md` — Step 7 |
| 5.13 | `implement-task` MUST NOT add given-when-then comments to trivial tests (single assertion, no distinct setup phase). | `implement-task/SKILL.md` — Step 7 |

---

## Traceability Index

Each constraint above references its source. The full source files are:

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Guardrails (§1.1–1.3), Task Description Template (§4.1–4.10), Step 5 Convention-aware task enrichment (§4.11)
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md` — Important Rules (§1.4–1.6, §5.1–5.3), Step 4/6/9 (§5.4), Step 5 (§1.15, §3.1), Step 7 (§5.9–5.13), Step 9 (§2.1–2.3, §5.6–5.8), Step 10 (§3.2)
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — Step 4 (§1.10, §1.12), Important Rules (§1.11, §1.13), Step 5b (§1.14), Step 12 (§1.16, §1.17)
- `plugins/sdlc-workflow/skills/define-feature/SKILL.md` — Guardrails (§1.7–1.8), Important Rules (§1.9)
- `docs/methodology.md` — Core Principles (§2.1, §3.2, §5.5)
