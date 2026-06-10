# Description Integrity Verification — Step 1.5 Handling for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") was fetched
from Jira in Step 1. Step 1.5 requires verifying that the task description has not
been modified since plan-feature originally created it, using the digest protocol
defined in `shared/description-digest-protocol.md`.

## Step 1.5 Execution Trace

### 1. Retrieve issue comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

**Result:** One comment found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (no need to pick the most
recent among multiple).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. Per the scenario, these
timestamps are identical, meaning the comment was **not** edited after initial posting.

**Result:** No edit detected. The digest comment is unmodified. Proceed with digest
comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged convention (not the legacy untagged `sha256:<hex>`
format), so the legacy skip does not apply. Proceed with comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of
the task description as returned by the Jira API). Write it to a temporary file and
compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest:

```
sha256-md:<actual-64-char-hex-digest>
```

(where `<actual-64-char-hex-digest>` is the real SHA-256 hash of the current description
content, which differs from the stored all-zeros hash)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task)
used the same API access method (markdown/MCP path). Proceed to hex digest comparison.

### 7. Compare hex digests

- **Expected digest (from comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest (computed from current description):** `sha256-md:<actual-64-char-hex-digest>`

**MISMATCH DETECTED.** The hex digests differ. The task description was modified after
plan-feature created it.

## Alert to User

Upon detecting the mismatch, the skill presents the following alert to the user:

---

**WARNING: Description integrity check failed for TC-9201.**

The task description has been modified since plan-feature originally created it.

| | Digest |
|---|---|
| **Expected** (from plan-feature digest comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:<actual-64-char-hex-digest>` |

Someone (or an automated process) changed the task description after the planning
phase completed. The implementation may not match what was originally planned.

**Choose how to proceed:**

1. **Proceed** — Use the current (modified) description as-is and continue with
   implementation. The implementation will be based on the current description,
   which may differ from what was originally planned.

2. **Stop** — Halt execution so you can investigate the change. You may want to
   re-run plan-feature to regenerate tasks based on the updated feature description,
   ensuring the plan and implementation are aligned.

---

## Execution State: STOPPED

**Execution is halted immediately.** The skill does NOT proceed to Step 2
(Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent
implementation steps. No branch is created, no code is modified, no Jira
transitions are made.

The skill waits for the user to respond with their choice before taking any
further action.

### If user chooses "Proceed"

The skill continues with Step 2 (Verify Dependencies) using the current task
description as the specification, acknowledging that it may differ from the
original plan.

### If user chooses "Stop"

The skill terminates. The user can then:
- Review the description changes in Jira's change history
- Re-run plan-feature to regenerate tasks aligned with the updated description
- Manually reconcile the description and digest before re-running implement-task

## Rationale

The digest mismatch guard exists to prevent silent drift between planning and
implementation. If a feature description is modified after plan-feature breaks it
into tasks, the task descriptions may no longer accurately reflect the intended
feature. Implementing stale or inconsistent task descriptions could produce code
that does not match the feature's current requirements.

By detecting the mismatch, alerting the user with both the expected and actual
digests, and offering a clear choice to proceed or stop, the skill ensures the
user is aware of the discrepancy and can make an informed decision. The hard stop
prevents the skill from silently implementing potentially outdated instructions.
