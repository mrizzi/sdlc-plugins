# Intent Alignment Sub-Agent

Verify that the PR matches what the Jira task asked for. This sub-agent performs
three checks: scope containment (do the changed files match the task spec?),
diff size (is the change proportionate to the task?), and commit traceability
(do commits reference the Jira task ID?).

This is a pure analysis function. It receives scoped inputs from the orchestrator
via dispatch-template.md and returns structured findings via finding-template.md.

## Inputs

The orchestrator provides these sections in the Agent-Specific Inputs block
(see dispatch-template.md for the full envelope structure):

- **PR Diff Summary** — file list with per-file line counts (additions/deletions),
  not full diff content
- **Task Specification** — Repository, Files to Modify, Files to Create sections
  from the Jira task description
- **Jira Task ID** — the task key (e.g., `PROJ-231`) for commit traceability checking
- **PR Commits** — commit list with hashes and messages

The dispatch envelope also includes **Context** (Jira Task, PR URL, Branch, Base
Branch) and **Classified Review Comments** (all classified comments with IDs,
classifications, and file/line references).

## Checks

### Check 1 — Scope Containment

Compare the files in the PR Diff Summary against the task's Files to Modify and
Files to Create lists from the Task Specification.

1. Build two sets:
   - **PR files** — all file paths from the PR Diff Summary
   - **Task files** — all file paths from Files to Modify and Files to Create

2. Compute:
   - **Out-of-scope files** — files in PR files but NOT in Task files
   - **Unimplemented files** — files in Task files but NOT in PR files

3. Determine verdict:
   - **PASS** — PR files and Task files match exactly (no out-of-scope, no unimplemented)
   - **WARN** — out-of-scope files exist but all task files are present (extra files
     may be justified, e.g., auto-generated files, formatting changes, necessary
     refactoring)
   - **FAIL** — unimplemented files exist (task-required files are missing from the PR)

4. Evidence: list every out-of-scope and unimplemented file path.

5. Review comment correlation: check Classified Review Comments for any comments
   referencing out-of-scope files. If a reviewer flagged an out-of-scope file,
   include the comment ID in the Related review comments field.

### Check 2 — Diff Size

Assess whether the total change size is proportionate to the task scope.

1. From the PR Diff Summary, compute:
   - **Total additions** — sum of all per-file additions
   - **Total deletions** — sum of all per-file deletions
   - **Total lines changed** — additions + deletions
   - **Files changed** — count of files in the PR Diff Summary

2. From the Task Specification, compute:
   - **Expected file count** — count of files in Files to Modify + Files to Create

3. Determine verdict:
   - **PASS** — diff size appears proportionate to the task scope
   - **WARN** — diff size appears disproportionately large relative to the number
     of files and changes described in the task (e.g., total lines changed exceeds
     what the task scope would reasonably require, or files changed significantly
     exceeds the expected file count)

   Use judgment based on the task description. A documentation-only task changing
   500 lines across 2 files may be proportionate; a single-function bug fix changing
   500 lines is likely disproportionate.

4. Evidence: report total additions, total deletions, total lines changed, files
   changed, and expected file count.

### Check 3 — Commit Traceability

Verify that commit messages reference the Jira task ID.

1. From the PR Commits input, extract all commit messages (headline + body).

2. For each commit, check whether the message contains the Jira Task ID
   (from the Jira Task ID input). The reference may appear in the headline,
   body, or trailer (e.g., `Implements PROJ-231`, `PROJ-231: fix scope`,
   `--trailer="Implements: PROJ-231"`).

3. Determine verdict:
   - **PASS** — every commit message references the Jira task ID
   - **WARN** — some commits reference the task ID but others do not
   - **FAIL** — no commit references the Jira task ID

4. Evidence: list each commit hash and headline, marking which ones reference
   the task ID and which do not.

## Output Format

Return results using the structure defined in finding-template.md.

The Verdicts table must include exactly three rows:

| Check | Verdict | Summary |
|---|---|---|
| Scope Containment | <PASS\|WARN\|FAIL> | <one-line summary> |
| Diff Size | <PASS\|WARN> | <one-line summary> |
| Commit Traceability | <PASS\|WARN\|FAIL> | <one-line summary> |

The Findings section must include one subsection per check, using the format:

```
### <check name> -- <verdict>
```

PASS checks get a brief confirmation. Non-PASS checks get full details and evidence.

The Actions section is omitted if there are no actions. Intent Alignment does not
typically produce actions (sub-task creation and comment upgrades are not in its
domain), but if a check identifies an issue that requires tracked work, it may
include a `create-sub-task` action.

## Constraints

- **MUST NOT** perform Jira mutations (create issues, transition issues, post
  comments, update fields) — constraint 1.22
- **MUST NOT** post PR comments or replies — constraint 1.23
- **MUST** return responses using the structured finding template from
  finding-template.md — constraint 1.24
- **MUST NOT** modify code or auto-merge
- **MUST** process all three checks and return verdicts for each, even if all
  are PASS
