# Policy Mapping: Human Touchpoints → Autonomous Policies

**Date:** 2026-04-21
**Prerequisite:** [Autonomous Readiness Plan](../superpowers/specs/2026-04-14-autonomous-readiness-plan.md)
**Deliverable:** 30-day phase, item #1

---

## Context

This document maps every human interaction point across the five sdlc-workflow skills to an autonomous policy equivalent. The audit identified **66 touchpoints** (up from the readiness plan's ~50 estimate), primarily because the MCP/REST API fallback flow and additional implement-task self-verification checks were added after the plan was written.

Each touchpoint gets one of five policy types:

| Policy type | Meaning |
|---|---|
| **Human-driven** | Stays human-driven. Strategic intent requires human input. No autonomous equivalent. |
| **Automated** | Already runs without human input. No change needed. |
| **Default** | Replace prompt with a deterministic default. Skip optional prompts, use configuration values. |
| **Auto-proceed** | Replace approval gate with automated validation. Proceed if valid, escalate if not. |
| **Reject/Escalate** | Replace exception prompt with a deterministic rule: fix automatically if safe, otherwise hard stop or flag `requires-manual-review`. |

---

## Application Strategy

This section explains how the policies in this document will be applied, so reviewers can evaluate each policy with the intended mechanism in mind.

### Principle: skills don't decide autonomy

Following fullsend's architecture (ADR 0018 — scripted pipelines, ADR 0002 — label state machine), skills are deterministic specifications — they describe what an agent does at each step, not whether a human should be involved. The decision to prompt a human or let the agent proceed is made by the **orchestration layer** outside the skill, not by conditional branches inside it.

This means the policies in this document are **not embedded into SKILL.md files as if/else branches**. Instead:

1. **Skills stay unchanged.** Each SKILL.md continues to describe its steps as it does today — including the human interaction points. The skills don't gain a "mode" flag.
2. **The orchestration layer consults this document.** When a pipeline invokes a skill autonomously, the pipeline is responsible for handling each touchpoint according to the policy defined here. At a touchpoint where the skill says "ask the user," the pipeline either supplies the answer prescribed by the policy (for Default and Auto-proceed types) or blocks execution and escalates (for Reject/Escalate types).
3. **Escalation is platform-native.** The `requires-manual-review` label on a Jira issue is the escalation signal. The pipeline sets it; a human clears it. This aligns with fullsend's label state machine where labels govern workflow transitions, not agent-internal logic.

### Relationship to fullsend concepts

| This document | fullsend equivalent |
|---|---|
| Human-driven touchpoints (define-feature) | Tier 2/3 intent — requires human authorization |
| Default policies | Standing rules (Tier 0) — pre-authorized, no intent needed |
| Auto-proceed policies | Tier 1 tactical — issue is sufficient intent, proceed if validation passes |
| Reject/Escalate policies | `requires-manual-review` label — split verdict or safety concern |
| Escalation mechanism | Label state machine transition to blocked state |

### What reviewers should evaluate

For each policy, reviewers should ask:

1. **Is the autonomous action safe?** Could it produce an irreversible bad outcome (data loss, security exposure, broken production)? If yes, the policy should escalate rather than auto-proceed.
2. **Is the autonomous action correct?** Does the deterministic default match what an experienced engineer would decide in >90% of cases? Edge cases should escalate, not guess.
3. **Is the policy enforceable by an orchestration layer?** Could a scripted pipeline unambiguously apply this policy at the touchpoint without LLM judgment, or does it require interpretation that only the skill's agent could provide? Policies that require interpretation should be decomposed into deterministic checks.

### What this document is NOT

- **Not a skill modification.** The policies are consumed by the orchestration layer, not compiled into skill instructions. Skills remain the same for interactive use.
- **Not a policy engine.** This document defines the policies; deliverable #12 (90-day phase — Policy Engine Integration) builds the mechanism that reads and enforces them at runtime.
- **Not changing interactive mode.** When a human runs `/implement-task`, the skill behaves exactly as it does today. These policies only apply when an automated pipeline invokes the skill.

---

## Cross-Cutting Policies

These policies apply identically in every skill where the touchpoint appears.

### XC-1: MCP Failure → REST API Fallback

**Appears in:** setup (S-C), define-feature (D-A), plan-feature (P-A), implement-task (I-A), verify-pr (V-A)

**Current behavior:** Prompt user with Yes/No/Retry options when Atlassian MCP fails.

**Autonomous policy:** Attempt REST API automatically if credentials are pre-configured in CLAUDE.md (`## Jira Configuration` → `### REST API Credentials`). If credentials are not configured, escalate (`requires-manual-review`). Never retry MCP — if MCP failed once, it will fail again in the same session.

### XC-2: REST API Credential Collection

**Appears in:** setup (S-D), define-feature (D-B)

**Current behavior:** Interactively collect Server URL, Email, API Token and ask storage preference.

**Autonomous policy:** Credentials must be pre-configured. If missing, escalate (`requires-manual-review`). Autonomous agents must not collect or store secrets interactively.

### XC-3: Project Configuration Validation

**Appears in:** All skills (Step 0)

**Current behavior:** If Project Configuration is missing, stop and tell user to run `/setup`.

**Autonomous policy:** Same — hard stop. Project Configuration is a mandatory prerequisite. This is already autonomous-compatible.

---

## Setup (15 touchpoints)

Setup is a one-time configuration skill. In autonomous mode, setup must have already been run — downstream skills require Project Configuration to exist. The autonomous policies below apply if setup is invoked programmatically (e.g., during automated project onboarding).

| # | Step | Current interaction | Category | Autonomous policy |
|---|---|---|---|---|
| 1 | Step 2 | "What is the repository short name?" | Human-driven | **Human-driven.** Repository identity is a naming decision. |
| 2 | Step 2 | "What is the repository role?" | Human-driven | **Human-driven.** Role is a classification decision. |
| 3 | Step 3 | "Which Jira project do you want to use?" | Human-driven | **Human-driven.** Project selection is an organizational decision. |
| 4 | Step 3 | "Which issue type is the Feature type?" | Human-driven | **Human-driven.** Issue type mapping is project-specific. |
| 5 | Step 3.3 | "Do you have a Git Pull Request custom field ID?" | Procedural | **Default:** skip. If the field exists in Project Configuration from a prior run, preserve it. Otherwise, leave unconfigured — it is optional. |
| 6 | Step 3.3 | "Do you have a GitHub Issue custom field ID?" | Procedural | **Default:** same as #5. |
| 7 | Step 4 | "Are there any known limitations for Serena instances?" | Procedural | **Default:** assume no limitations. Write "No limitations known" in the Limitations section. If Serena tools fail during downstream skill execution, those failures will surface naturally. |
| 8 | Step 7 | "Would you like to scaffold CONVENTIONS.md for this repo?" | Procedural | **Default:** always scaffold. CONVENTIONS.md is needed for convention checking in plan-feature and implement-task. Scaffolding is non-destructive (only creates if absent). |
| 9 | Step 7 | "Would you like me to fill in CONVENTIONS.md now?" | Procedural | **Default:** always auto-populate using codebase analysis. The analysis is deterministic and best-effort. Content is refinable later via convention gap tasks. |
| 10 | Step 5 | "Ready to write changes?" | Approval gate | **Auto-proceed.** Validate generated config: all required fields present (Project key, Cloud ID, Feature issue type ID), Repository Registry has ≥1 entry, Code Intelligence section exists. If valid, write. If validation fails, escalate. |
| S-A | Step 2 | "Repo local path?" (when `get_diagnostics` fails) | Exception handling | **Reject/Escalate.** If `get_diagnostics` is unavailable, escalate (`requires-manual-review`). The local path cannot be safely guessed. |
| S-B | Step 2 | "Continue without code intelligence or set up Serena first?" | Procedural | **Default:** continue without code intelligence. Downstream skills handle the absence of Serena gracefully (fallback to Glob/Grep/Read). |
| S-C | Step 3.2 | MCP failure → "Use REST API fallback?" | Exception handling | **XC-1** (see cross-cutting). |
| S-D | Step 3.3 | REST API credential collection + storage preference | Procedural | **XC-2** (see cross-cutting). |
| S-E | Step 7 | "Review auto-populated CONVENTIONS.md before writing" | Approval gate | **Auto-proceed.** Auto-populated content is best-effort codebase analysis. Proceed without review. Content is validated and refined through convention gap tasks created by verify-pr's root-cause flywheel. |

---

## Define-feature (19 touchpoints)

Define-feature collects strategic intent. All content-collection touchpoints remain human-driven — this is by design. An autonomous agent cannot invent product requirements.

| # | Step | Current interaction | Category | Autonomous policy |
|---|---|---|---|---|
| 11 | Step 1 | "Are you ready to begin?" | Procedural | **Default:** skip. Proceed directly to content collection. |
| 12 | Step 2 | Confirm or provide Feature title | Human-driven | **Human-driven.** Feature naming is a product decision. |
| 13 | Step 3a | "Provide high-level description — the What & Why" | Human-driven | **Human-driven.** |
| 14 | Step 3b | "How does this fit into product strategy?" | Human-driven | **Human-driven.** |
| 15 | Step 3c | "Who benefits? Current vs. target state?" | Human-driven | **Human-driven.** |
| 16 | Step 3d | "Which input mode: row-by-row or batch paste?" | Human-driven | **Human-driven.** |
| 17 | Step 3d | "Add another requirement, or done?" | Human-driven | **Human-driven.** |
| 18 | Step 3e | "Architecture characteristics and NFRs?" | Human-driven | **Human-driven.** |
| 19 | Step 3f | "Success scenarios with personas, outcomes?" | Human-driven | **Human-driven.** |
| 20 | Step 3g | "Prerequisites, dependencies, assumptions?" | Human-driven | **Human-driven.** |
| 21 | Step 3h | "SRE metrics, observability, feedback?" | Human-driven | **Human-driven.** |
| 22 | Step 3i | "Documentation impact categories?" | Human-driven | **Human-driven.** |
| 23 | Step 4 | "Assign to yourself or leave unassigned?" | Procedural | **Default:** leave unassigned. Assignment happens when implement-task picks up the work (Step 3 of implement-task already auto-assigns). |
| 24 | Step 5 | "Ready to create this Feature in Jira?" | Approval gate | **Human-driven.** This is the final approval for strategic content. Unlike technical approval gates, this guards product intent. Stays human-driven even in autonomous mode. |
| 25 | Step 5 | "Which section(s) to revise?" | Human-driven | **Human-driven.** |
| 26 | Step 5 | Re-display preview, re-ask "Ready to create?" | Approval gate | **Human-driven.** Same reasoning as #24. |
| 27 | Step 5 | Re-collect content for revised section | Human-driven | **Human-driven.** |
| D-A | Step 0.5 | MCP failure → "Use REST API fallback?" | Exception handling | **XC-1** (see cross-cutting). |
| D-B | Step 0.5 | REST API credential collection | Procedural | **XC-2** (see cross-cutting). |

---

## Plan-feature (3 touchpoints)

| # | Step | Current interaction | Category | Autonomous policy |
|---|---|---|---|---|
| 28 | Step 2 | Discover or request Figma URL | Procedural | **Default:** discover from skill arguments or Jira issue description. If not found, proceed without Figma analysis. Do not request. Note: the current skill already behaves this way — it never explicitly requests a Figma URL. The spec's "or request" is aspirational; the policy matches current behavior. |
| 29 | Step 4 | "Approve impact map before task generation" | Approval gate | **Auto-proceed.** Validate: (1) every requirement from the Feature description maps to at least one change in the impact map, (2) all impacted repos are in the Repository Registry, (3) no repo outside the Registry is listed. If all three pass, proceed to task generation. If any fails, escalate (`requires-manual-review`). |
| P-A | Step 0.5 | MCP failure → "Use REST API fallback?" | Exception handling | **XC-1** (see cross-cutting). |

---

## Implement-task (16 touchpoints)

| # | Step | Current interaction | Category | Autonomous policy |
|---|---|---|---|---|
| 30 | Step 1 | "Task description missing required sections — clarify" | Exception handling | **Reject.** If required sections (Repository, Description, Files to Modify/Create, Acceptance Criteria, Test Requirements) are missing, flag `requires-manual-review` on the Jira issue and stop. The task is not ready for autonomous execution. |
| 31 | Step 4 | "Convention conflict between task and codebase — which to follow?" | Exception handling | **Default:** follow CONVENTIONS.md. CONVENTIONS.md is the project authority for patterns and style. If the task contradicts a documented convention, follow the convention and log the deviation. If the conflict is with an undocumented codebase pattern (no CONVENTIONS.md entry), follow the task description — undocumented patterns are not binding. |
| 32 | Step 6 | "API contract mismatch with backend — stop and report" | Exception handling | **Reject.** Do not implement with mismatched contracts. Create a sub-task on the parent Feature documenting the mismatch (affected endpoint, expected vs. actual, backend source file). Flag `requires-manual-review`. |
| 33 | Step 9 | "Out-of-scope file modified — approve or revert?" | Exception handling | **Default:** revert out-of-scope changes, with exceptions. Auto-include if the file is: (a) a lockfile (`package-lock.json`, `Cargo.lock`, etc.), (b) a generated file from a code generation command listed in CONVENTIONS.md, or (c) a build artifact required by CI. Revert all others and log the reversion. |
| 34 | Step 9 | "Untracked file found near modified files — stage for commit?" | Exception handling | **Default:** stage if referenced by code (compile-time includes, imports, config references found in the diff). Skip if not referenced. Log all decisions. |
| 35 | Step 9 | "Secrets found in diff — do not proceed" | Exception handling | **Hard stop.** Remove the sensitive content from the staged diff. Do not commit. Flag `requires-manual-review`. This is non-negotiable — secrets must never be committed. |
| 36 | Step 9 | "Data-flow trace incomplete — is missing stage intentionally out of scope?" | Exception handling | **Default:** if the missing stage is in a file listed in the task's Files to Modify/Create, implement it (the task intended it). If the missing stage is in files NOT in the task's scope, escalate (`requires-manual-review`). The task may be underspecified. |
| 37 | Step 9 | "Sibling parity gap — is omission intentional?" | Exception handling | **Default:** implement the missing capability if it is mechanical (e.g., error handling, logging, input validation that all siblings have and requires no design decisions). Escalate if the gap requires design choices (e.g., choosing between implementation strategies, adding new API surface). |
| 38 | Step 5 | Target PR flow depends on user-provided Target PR | Procedural | **Default:** follow the Target PR if present in the task description. Otherwise, create a new branch. The task description is authoritative — no human decision needed. |
| I-A | Step 0.5 | MCP failure → "Use REST API fallback?" | Exception handling | **XC-1** (see cross-cutting). |
| I-B | Step 6 | Sort order mismatch → "stop and report to user" | Exception handling | **Reject.** Same policy as #32 (API contract mismatch). Create a sub-task documenting the sort order discrepancy and escalate. Positional assumptions on unsorted data are a correctness bug. |
| I-C | Step 9 | Cross-module shared entity anomaly → "confirm if intentional" | Exception handling | **Default:** align with the established cross-module pattern. The existing pattern is authoritative — other modules already interact with the shared entity safely. Deviating without explicit justification in the task is a defect. Log the alignment. |
| I-D | Step 9 | Caller-site parity anomaly → "confirm if intentional" | Exception handling | **Default:** align with the established caller pattern. Same reasoning as I-C. If all existing callers use `queryClient.invalidateQueries()` and the new code uses `window.location.reload()`, the new code is wrong. Align and log. |
| I-E | Rules | Same test fails 3× with same error → "stop and ask for guidance" | Exception handling | **Escalate.** Flag `requires-manual-review`. Three identical failures indicate a problem the agent cannot solve. Include the test name, error message, and the three attempted fixes in the escalation. |
| I-F | Rules | Same file edited 5× for same change → "stop and present alternatives" | Exception handling | **Escalate.** Flag `requires-manual-review`. The agent is stuck in a loop. Include the file, the intended change, and the five attempts in the escalation. |
| I-G | Rules | Build error persists after 2 fix attempts → "stop and present alternatives" | Exception handling | **Escalate.** Flag `requires-manual-review`. Include the error, the two attempted fixes, and their outcomes in the escalation. |

---

## Verify-pr (13 touchpoints)

| # | Step | Current interaction | Category | Autonomous policy |
|---|---|---|---|---|
| 39 | Step 2 | "PR URL not in custom field — provide it" | Exception handling | **Default:** search for PRs on the task's branch name: `gh pr list --head <jira-issue-id> -R <owner/repo>`. If exactly one PR found, use it. If zero or multiple, escalate (`requires-manual-review`). |
| 40 | Step 4c | Classify each comment (code change request / suggestion / question / nit) | Automated | **No change.** Already autonomous. |
| 41 | Step 4c | Upgrade suggestion to code change request if matches CONVENTIONS.md | Automated | **No change.** Already autonomous. |
| 42 | Step 4f | Post classification reasoning to each comment | Automated | **No change.** Already autonomous. |
| 43 | Step 5a | "Would this knowledge apply to ANY repo, or only this one?" (universality test) | Sub-agent decision | **No change.** Already a sub-agent decision, not a human touchpoint. The universality test is a deterministic classification the sub-agent performs internally. |
| 44 | Step 5a | "Can guidance be expressed as method without language-specific references?" (method-vs-fact) | Sub-agent decision | **No change.** Same as #43. |
| 45 | Step 10b | Analyze CI failure logs; if inconclusive, ask user | Exception handling | **Default:** if the failure is deterministic (test assertion, compilation error, lint violation), create a sub-task with the fix. If the failure is non-deterministic or infrastructure-related (timeout, flaky test, network error, runner OOM), flag `requires-manual-review`. Heuristic: if re-running the same commit would produce the same failure, it is deterministic. |
| 46 | Step 11 | Verify each acceptance criterion by inspecting code | Automated | **No change.** Already autonomous. |
| 47 | Step 12 | Check for repetitive tests (Meszaros heuristic) | Automated | **No change.** Already autonomous. |
| 48 | Step 12 | Check for doc comments on test functions | Automated | **No change.** Already autonomous. |
| 49 | Step 14 | Compile and post verification report | Automated | **No change.** Already autonomous. |
| 50 | Step 15 | Post report to Jira as comment | Automated | **No change.** Already autonomous. |
| V-A | Step 0.5 | MCP failure → "Use REST API fallback?" | Exception handling | **XC-1** (see cross-cutting). |

---

## Summary

### Revised category breakdown

| Category | Count | Autonomous policy |
|---|---|---|
| Human-driven | 22 | Stays human-driven. All in define-feature (content collection) and setup (identity/naming). |
| Automated | 9 | No change needed. Already runs without human input. |
| Default | 14 | Replace with deterministic defaults. Includes all procedural prompts plus exception handling cases where the correct action is unambiguous. |
| Auto-proceed | 3 | Replace approval gates with automated validation checks. Proceed if valid, escalate if not. |
| Reject/Escalate | 13 | Hard stop or `requires-manual-review`. Includes secrets detection, contract mismatches, retry exhaustion, and missing prerequisites. |
| Cross-cutting (XC-1, XC-2) | 5 + 2 | MCP fallback (auto-use REST if configured, else escalate) and credential collection (must be pre-configured, else escalate). Counted per-skill but defined once. |
| **Total** | **66** | |

### Escalation mechanism

All policies that escalate use the `requires-manual-review` label on the Jira issue. This label is the single signal that autonomous execution could not complete and a human must intervene. The label should:

1. Be added to the Jira issue via `jira.edit_issue(<id>, labels=["requires-manual-review"])`
2. Include a Jira comment explaining what triggered the escalation
3. Not be removed by any skill — only a human removes it after review

### Prerequisites for autonomous execution

For a task to be eligible for autonomous execution, the following must be true before the pipeline starts:

1. **Project Configuration exists** — setup has been run, CLAUDE.md has all required sections
2. **REST API credentials are configured** — if MCP is unreliable, the fallback path must work without interaction
3. **CONVENTIONS.md exists** — either scaffolded by setup or manually created
4. **Task description follows the template** — all required sections present (enforced by plan-feature)
5. **Dependencies are Done** — all prerequisite tasks are completed

If any prerequisite is missing, the first skill to encounter it will escalate immediately rather than attempting partial execution.
