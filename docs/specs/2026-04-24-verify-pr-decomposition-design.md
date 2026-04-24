# verify-pr Decomposition into Sub-Agents

**Date:** 2026-04-24
**Purpose:** Design for decomposing verify-pr's 15 steps into an orchestrator and 4 specialized domain sub-agents, enabling parallel execution, independent testability, and domain-specific autonomous policies.
**Origin:** fullsend [docs/problems/code-review.md](https://github.com/fullsend-ai/fullsend/blob/f0d3032d6df02a6d4e00385e926dbc90317d8a77/docs/problems/code-review.md) — "Why review must be decomposed into sub-agents" establishes decomposition as an architectural necessity; "Review sub-agent decomposition" defines the sub-agent roles
**Prerequisite:** [Autonomous Readiness Plan](../superpowers/specs/2026-04-14-autonomous-readiness-plan.md) (30-day deliverable #2)

---

## Context

verify-pr is a 994-line SKILL.md that runs 15 verification checks sequentially in a single agent context. It already spawns sub-agents in two places (root-cause investigation in Step 5, test change classification in Step 12), proving the pattern works. The autonomous readiness plan calls for decomposing the domain checks into specialized sub-agents so that:

- Each domain can have its own autonomous escalation policy (security findings escalate differently than style findings)
- Sub-agents can be tested independently against behavioral contracts
- Domain checks run in parallel for throughput
- The root-cause flywheel receives richer, domain-attributed findings

The decomposition changes how findings are produced, not how they are investigated. User-facing behavior is unchanged — same invocation, same report format, same sub-task creation.

---

## Architecture

Three layers:

**Layer 1 — Orchestrator (SKILL.md):** Setup, review comment classification, sub-agent dispatch, all side effects (Jira mutations, PR comment replies, sub-task creation, idempotency deduplication), report assembly, root-cause dispatch.

**Layer 2 — Domain sub-agents (4, dispatched in parallel):** Pure analysis functions. Each receives scoped inputs, performs domain-specific checks, returns structured findings using the finding template. No Jira access, no PR posting, no side effects.

**Layer 3 — Test classification sub-sub-agent (spawned by Style/Conventions):** Preserved from current Step 12 with hard isolation — receives only file paths and branch names, no Jira task, review comments, or PR metadata. Returns ADDITIVE/REDUCTIVE/MIXED/NEUTRAL classification.

### Data Flow

```
Orchestrator
|-- Steps 0-3: Setup, fetch task, identify PR, checkout branch
|-- Step 4a-c: Enumerate threads, load CONVENTIONS.md, classify comments
|
|-- PARALLEL DISPATCH -----------------------------------------------
|   |-- Intent Alignment (Steps 6, 7, 8)  -> findings
|   |-- Security (Step 9)                 -> findings
|   |-- Correctness (Steps 10, 11, 13)    -> findings
|   +-- Style/Conventions (4c up, 12)     -> findings + upgrades
|       +-- Test Classification sub-agent -> classification
|
|-- AGGREGATE -------------------------------------------------------
|   |-- Apply convention upgrades (suggestion -> change request)
|   |-- Create sub-tasks for all change requests (Step 4e)
|   |-- Post classification replies to PR (Step 4f)
|   |-- Idempotency deduplication (Step 4g)
|   +-- Assemble report table (Step 14)
|
|-- Root-Cause Investigation (Step 5) <- aggregated findings from all sub-agents
|
+-- Post report to GitHub PR + Jira (Step 15)
```

All classified review comments go to ALL sub-agents. Each sub-agent filters for what is relevant to its domain.

---

## Orchestrator Responsibilities

The orchestrator is the rewritten SKILL.md. It keeps everything that is cross-cutting or side-effect-producing, and delegates only the domain analysis.

| Phase | Steps | Responsibility |
|---|---|---|
| Setup | 0, 0.5 | Validate Project Configuration, initialize Jira access |
| Fetch | 1, 2, 3 | Fetch Jira task, identify PR (from custom field or user), checkout PR branch |
| Classify | 4a, 4b, 4c | Enumerate all PR threads (mandatory, idempotent), load CONVENTIONS.md, classify each new comment as code-change-request / suggestion / question / nit |
| Dispatch | -- | Spawn 4 domain sub-agents in parallel via Agent tool, passing scoped inputs and finding template to each |
| Aggregate | 4c up, 4d, 4e, 4f, 4g | Apply convention upgrades from Style/Conventions, create Jira sub-tasks for all change requests, post classification replies to PR comments, deduplicate against existing sub-tasks |
| Root-cause | 5 | Dispatch root-cause sub-agent with aggregated findings from all domain sub-agents (if any sub-tasks exist). Root-cause logic is preserved unchanged: universality test, method-vs-fact test, convention check, skill phase investigation, decision matrix |
| Report | 14, 15 | Assemble verification report table from all sub-agent verdicts, post to GitHub PR and Jira |

### Orchestrator Invariants Preserved

- Step 4a mandatory thread enumeration runs every invocation (catches comments arriving between runs)
- Idempotency deduplication (Step 4g) checks existing sub-tasks before creating new ones
- Comment Footnote on all Jira comments (version from plugin.json)
- Never modifies code, never auto-merges

---

## Domain Sub-Agent Definitions

Each sub-agent is a pure analysis function. It receives scoped inputs, performs its checks, and returns structured findings using the finding template. No Jira mutations, no PR comment posting.

### Intent Alignment (`intent-alignment.md` -- Steps 6, 7, 8)

**Purpose:** Verify the PR matches what the task asked for.

**Inputs:**
- PR diff file list with line counts
- Jira task description (Repository, Files to Modify, Files to Create sections)
- Jira task ID
- PR commit list with messages
- Classified review comments

**Checks:**
- Step 6 (scope containment): Compare modified files against the task's Files to Modify and Files to Create lists
- Step 7 (diff size): Count total lines changed, compare against thresholds
- Step 8 (commit traceability): Verify each commit message references the Jira task ID

### Security (`security.md` -- Step 9)

**Purpose:** Detect sensitive patterns in the diff.

**Inputs:**
- PR diff (full content for line-level scanning)
- Classified review comments

**Checks:**
- Step 9 (sensitive patterns): Scan for secrets, credentials, tokens, API keys, private keys, hardcoded passwords

A FAIL from the Security sub-agent is a hard stop in autonomous mode. This is the lightest sub-agent but its findings carry the most weight.

### Correctness (`correctness.md` -- Steps 10, 11, 13)

**Purpose:** Verify the PR is functionally correct.

**Inputs:**
- PR diff (full content)
- Jira task description (Acceptance Criteria, Test Requirements, Verification Commands sections)
- CI status and failure logs (fetched via `gh` CLI -- read-only)
- Repository path and Serena instance info (for code inspection)
- Classified review comments

**Checks:**
- Step 10 (CI status): Check CI pass/fail status; if failed, analyze failure logs and determine root cause
- Step 11 (acceptance criteria): Verify each acceptance criterion by inspecting the code
- Step 13 (verification commands): Run verification commands from the task description

The Correctness sub-agent uses `gh` CLI for reading CI status (a read operation, not a side effect) and can run verification commands via shell access.

### Style/Conventions (`style-conventions.md` -- Step 4c upgrade, Step 12)

**Purpose:** Check code quality, convention adherence, and test integrity.

**Inputs:**
- PR diff (full content)
- CONVENTIONS.md content
- Classified review comments (especially suggestions for convention upgrade checking)
- Modified/deleted test file paths
- Base branch and PR branch names
- Repository path

**Checks:**
- Convention upgrade: Check if any classified suggestions match patterns in CONVENTIONS.md. Return upgrade recommendations (suggestion to code change request) with the matching convention
- Step 12 (test quality):
  - Doc comments on test functions
  - Repetitive tests (Meszaros heuristic)
  - Test change classification: Spawns isolated test classification sub-agent with ONLY file paths and branch names (constraint 1.18 preserved). Returns ADDITIVE/REDUCTIVE/MIXED/NEUTRAL with structural summary and reductive findings. Semantic assessment overrides structural signals (constraint 1.21)

This is the only domain sub-agent that itself spawns a sub-agent — the test change classification sub-agent from current Step 12, with its hard isolation guarantee preserved unchanged.

---

## Finding Contract -- Structured Template

Each sub-agent returns its results using a structured markdown template defined in `finding-template.md`. The orchestrator expects this exact structure.

### Template

```markdown
## Verdicts

| Check | Verdict | Summary |
|---|---|---|
| <check name> | <PASS|WARN|FAIL|N/A> | <one-line summary> |

## Findings

### <check name> -- <PASS|WARN|FAIL|N/A>

**Details:** <what was found>

**Evidence:**
- <file path, line number, command output, or other concrete evidence>

**Related review comments:** <comment IDs, or "none">

## Actions

### <action type>: <short title>

**Type:** <create-sub-task | upgrade-comment>
**Details:** <action-specific fields>
```

### Action Type Fields

**create-sub-task** (used by Correctness for CI failures or other issues needing tracked work):

```markdown
**Type:** create-sub-task
**Title:** <suggested sub-task title>
**Relevant files:** <file paths>
**Root cause:** <what caused the issue>
```

**upgrade-comment** (used by Style/Conventions for convention-matching suggestions):

```markdown
**Type:** upgrade-comment
**Comment ID:** <PR comment ID>
**Original classification:** suggestion
**Matching convention:** <the CONVENTIONS.md section that matches>
```

### Rules

- Verdicts table is mandatory, even if all checks are PASS
- Findings section includes one subsection per check. PASS checks get a brief confirmation; non-PASS checks get full evidence
- Actions section is omitted entirely if there are no actions (not an empty section -- omitted)
- The template is the same for all 4 sub-agents; each fills in its own checks

---

## Root-Cause Integration

Root-cause investigation (Step 5) is preserved as-is. Its internal logic does not change: universality test, method-vs-fact test, convention check, skill phase investigation, decision matrix. What changes is the shape of its input.

**Current model:** Root-cause receives findings produced by the orchestrator's single-pass analysis (Steps 4-13).

**Decomposed model:** Root-cause receives aggregated findings from all 4 domain sub-agents, with source attribution.

### Aggregated Input Format

The orchestrator assembles a findings summary after collecting all sub-agent results:

```markdown
## Aggregated Findings for Root-Cause Investigation

### From Intent Alignment
<Findings section from intent-alignment sub-agent>

### From Security
<Findings section from security sub-agent>

### From Correctness
<Findings section from correctness sub-agent>

### From Style/Conventions
<Findings section from style-conventions sub-agent>

### Sub-tasks Created
<List of sub-tasks the orchestrator created from Actions, with Jira IDs>
```

The rest of root-cause's input stays the same: feature description (fetched via "incorporates" link), task description, review comments (original + any convention upgrades applied), relevant code, CONVENTIONS.md.

Root-cause still creates root-cause tasks with labels `["ai-generated-jira", "root-cause"]` and "Relates" links, and still checks idempotency before creating tasks (Step 5c).

The improvement: root-cause now has richer, domain-attributed input. If the Security sub-agent found a hardcoded credential, root-cause can trace whether the task description failed to mention credential handling (plan-feature gap) or whether CONVENTIONS.md lacks a secrets management convention (convention gap).

---

## File Structure

```
plugins/sdlc-workflow/skills/verify-pr/
|-- SKILL.md                  # Orchestrator (rewritten)
|-- finding-template.md       # Structured output template for all sub-agents
|-- intent-alignment.md       # Steps 6, 7, 8
|-- security.md               # Step 9
|-- correctness.md            # Steps 10, 11, 13
+-- style-conventions.md      # Step 4c upgrade, Step 12
                              #   spawns test classification sub-agent (inline, as today)
```

**Orchestrator (SKILL.md):** Rewritten from the current 994-line file. Keeps Steps 0-3 (setup), Step 4a-c (classification), dispatch logic, aggregation (sub-tasks, replies, idempotency), root-cause dispatch (Step 5 instructions stay inline), and report generation (Steps 14-15).

**Sub-agent files:** Each is a self-contained file with: purpose statement, input description, check instructions (moved from current SKILL.md), reference to finding template, and constraints (what the sub-agent must/must not do).

**Finding template:** Shared by all sub-agents. The orchestrator passes the template content to each sub-agent as part of its dispatch prompt (sub-agents spawned via Agent tool receive everything in their prompt).

**Shared references stay where they are:** `shared/task-description-template.md`, `shared/jira-rest-fallback.md`, `plugin.json` — referenced by the orchestrator, not by sub-agents.

### What Moves Where

| Current SKILL.md content | Destination |
|---|---|
| Steps 0-3, 4a-c, 4e-g (setup, classification, side effects) | SKILL.md (orchestrator) |
| Step 5 (root-cause) | SKILL.md (orchestrator, inline -- unchanged) |
| Steps 6, 7, 8 (scope, diff size, commits) | intent-alignment.md |
| Step 9 (sensitive patterns) | security.md |
| Steps 10, 11, 13 (CI, acceptance, verification) | correctness.md |
| Step 4c upgrade logic, Step 12 (conventions, test quality) | style-conventions.md |
| Steps 14-15 (report, posting) | SKILL.md (orchestrator) |

---

## Constraints Updates

Updates to `docs/constraints.md` for the decomposition.

### Re-scoped Constraints

Existing rules re-attributed to the component that now owns them:

| Constraint | Current scope | New scope |
|---|---|---|
| 1.10: Must read PR reviews to identify code change requests | verify-pr | verify-pr orchestrator |
| 1.11: Must NOT modify code | verify-pr | verify-pr orchestrator + all sub-agents |
| 1.12: Sub-tasks must follow template with Target PR and Review Context | verify-pr | verify-pr orchestrator |
| 1.13: Must NOT auto-merge | verify-pr | verify-pr orchestrator |
| 1.14: Root-cause tasks must target originating phase | verify-pr | verify-pr orchestrator (root-cause) |
| 1.16: Must flag repetitive tests as WARN | verify-pr | style-conventions sub-agent |
| 1.17: Must flag missing test doc comments as WARN | verify-pr | style-conventions sub-agent |
| 1.18: Test classification sub-agent MUST operate in isolation | verify-pr | style-conventions sub-agent (spawns test classification) |
| 1.19: REDUCTIVE/MIXED test changes are WARN | verify-pr | style-conventions sub-agent |
| 1.20: New test files classified as additive without sub-agent | verify-pr | verify-pr orchestrator (combines with style-conventions output) |
| 1.21: Semantic assessment overrides structural signals | verify-pr | style-conventions sub-agent (test classification) |

### New Constraints

| # | Constraint | Rationale |
|---|---|---|
| 1.22 | Domain sub-agents MUST NOT perform Jira mutations (create sub-tasks, post comments, transition issues) | Side effects are orchestrator-only |
| 1.23 | Domain sub-agents MUST NOT post PR comments or replies | Side effects are orchestrator-only |
| 1.24 | Domain sub-agents MUST return responses using the structured finding template (`finding-template.md`) | Consistent contract for orchestrator consumption |
| 1.25 | Orchestrator MUST dispatch domain sub-agents in parallel | Throughput requirement |
| 1.26 | Root-cause investigation MUST receive aggregated findings from all domain sub-agents with source attribution | Richer input for phase tracing |

---

## Migration Strategy

**User-facing behavior:** Unchanged. The skill is still invoked as `/verify-pr`, takes the same inputs, produces the same verification report, creates the same sub-tasks.

**Migration approach:** Atomic. The orchestrator and sub-agents are tightly coupled, so a half-decomposed skill does not work. One set of changes:

1. Create `finding-template.md`
2. Create 4 sub-agent files by extracting their steps from current SKILL.md
3. Rewrite SKILL.md as the orchestrator (dispatch + aggregation + side effects)
4. Update `docs/constraints.md` with re-scoped and new constraints

**Validation:**
- Run the decomposed skill against the same PR that the current skill last verified. The report should produce equivalent verdicts
- Verify sub-task creation still works (idempotency means re-running against an already-verified PR creates no duplicates)
- Verify root-cause investigation still triggers when sub-tasks exist

**Out of scope for this deliverable:**
- Autonomous escalation policies (readiness plan deliverable #1, policy mapping)
- Skill testing framework (readiness plan deliverable #3, but decomposed sub-agents are designed to be testable by it)
- New additive-vs-reductive behavior for autonomous mode (readiness plan deliverable #4 -- existing classification is preserved; autonomous escalation policy is separate)
