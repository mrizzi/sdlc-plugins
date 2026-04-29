# Eval Coverage Propagation

When a task modifies a skill's `SKILL.md`, check whether eval infrastructure exists for
that skill and propagate eval coverage requirements into the task description. This ensures
that skill behavior changes are accompanied by eval assertion updates, preventing gaps
where new behavior ships without eval coverage.

## How to apply

1. For each task, check whether its **Files to Modify** includes a file matching the
   pattern `plugins/<plugin>/skills/<skill-name>/SKILL.md`.
2. If it does, check whether `evals/<skill-name>/evals.json` exists (using the eval
   infrastructure detected during repository analysis).
3. If eval infrastructure exists, enrich the task description:
   - Add `evals/<skill-name>/evals.json` to **Files to Modify** with the reason:
     "add or update eval assertions to cover the new behavior"
   - Add to **Test Requirements**: "Update eval assertions in
     `evals/<skill-name>/evals.json` to cover the behavior changes introduced by
     this task. Add new eval cases if existing cases do not exercise the modified
     behavior, or update assertions on existing cases if their expected output changes."
   - Add existing eval fixture files (from `evals/<skill-name>/files/`) to
     **Reuse Candidates** so the implementer follows the established fixture patterns.
     List 2-3 representative fixture files with a brief description of what each
     demonstrates (e.g., a passing scenario, a failing scenario, a scenario with
     review comments).

## Example -- verify-pr skill with existing evals

When a task modifies `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` and
`evals/verify-pr/evals.json` exists:

> **Files to Modify** (appended):
> - `evals/verify-pr/evals.json` -- add or update eval assertions to cover the new behavior
>
> **Test Requirements** (appended):
> - [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior
>   changes introduced by this task
>
> **Reuse Candidates** (appended):
> - `evals/verify-pr/files/task-passing.md` -- example task fixture for a passing
>   verification scenario
> - `evals/verify-pr/files/pr-diff-passing.md` -- example PR diff fixture for a
>   passing scenario
