## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: plan-feature did not apply eval coverage propagation when generating task TC-9106, which modifies `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`. Per the eval coverage propagation protocol (shared/eval-coverage-propagation.md), when a task modifies a skill's SKILL.md and eval infrastructure exists at `evals/<skill-name>/`, the task description should include eval-related files in Files to Modify and eval verification in Test Requirements. TC-9106's task description omits these, so the implementer did not verify existing eval assertions pass, allowing eval-3 regressions to reach the PR without detection.

Improve plan-feature to reliably apply eval coverage propagation whenever a task modifies a skill's SKILL.md and eval infrastructure exists.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add or strengthen the eval coverage propagation check so that tasks modifying skill SKILL.md files always include eval-related requirements when eval infrastructure exists

## Implementation Notes
- The eval coverage propagation protocol is documented in `plugins/sdlc-workflow/shared/eval-coverage-propagation.md`
- When plan-feature generates a task that modifies `plugins/<plugin>/skills/<skill-name>/SKILL.md`, it must check whether `evals/<skill-name>/evals.json` exists
- If eval infrastructure exists, the task description must be enriched with:
  - `evals/<skill-name>/evals.json` added to Files to Modify
  - Eval verification added to Test Requirements ("Update eval assertions to cover behavior changes")
  - Existing eval fixture files listed in Reuse Candidates
- The current plan-feature skill may already reference eval coverage propagation but may not enforce it reliably -- investigate whether the check exists but is not triggered, or is missing entirely
- Reference: TC-9106 task description is missing eval coverage requirements despite modifying `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` with eval infrastructure at `evals/verify-pr/`

## Acceptance Criteria
- [ ] plan-feature reliably applies eval coverage propagation when generating tasks that modify skill SKILL.md files
- [ ] Tasks generated for skills with eval infrastructure include eval-related Files to Modify and Test Requirements
- [ ] The propagation check handles both direct SKILL.md modifications and cases where SKILL.md is modified alongside other skill files

## Test Requirements
- [ ] Verify that a task generated for a skill with eval infrastructure includes eval coverage requirements
- [ ] Verify that a task generated for a skill without eval infrastructure does not include spurious eval references
