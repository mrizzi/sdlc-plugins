# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

After fetching and parsing the Jira task TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature originally created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. Here, only one comment matches.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, which means the comment has not been edited after initial posting. No warning is emitted for comment editing. Proceed to digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed.)

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full stored value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format tag `sha256-md` indicates the digest was computed from the markdown representation of the description (i.e., the producer used the MCP path to fetch the description after task creation).

This is not a legacy untagged format (`sha256:<hex>`), so integrity checking proceeds normally.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response. Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain markdown text in this case) and outputs a tagged digest. Suppose the script outputs:

```
sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84847a8048e8fcd1b1c37287f1
```

Check that the script exited with status 0. If non-zero, warn and skip the integrity check without blocking execution.

### 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same API access method (MCP, which returns markdown). Proceed to hex digest comparison.

(If the tags had differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and execution would proceed normally without blocking.)

### 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected (from digest comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `b7e23ec29af22b0b4e41da31e868d57226121c84847a8048e8fcd1b1c37287f1`

The hex hashes differ. This means the task description was modified after plan-feature created the task.

### 8. Alert the User

The skill alerts the user with the following message:

> **Description integrity check: MISMATCH**
>
> The task description for TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84847a8048e8fcd1b1c37287f1`
>
> The description may have been edited manually in Jira after the planning phase.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature specification
>
> Please choose (1 or 2):

### 9. Stop Execution and Wait

**Execution stops immediately.** The skill does not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation step. No branch is created, no code is read or modified, and no Jira transitions occur.

This follows the same pause-and-ask pattern used when a task description is incomplete -- the skill halts and waits for explicit user input before continuing.

- If the user chooses **option 1 (Proceed):** the skill continues to Step 2 with the current description, treating it as the authoritative specification for implementation.
- If the user chooses **option 2 (Stop):** the skill terminates. The user is expected to re-run plan-feature against the updated feature description, which will regenerate tasks with fresh descriptions and post new digest comments reflecting the current content.

## Rationale

The digest mismatch check guards against a class of errors where the task description is manually edited in Jira after plan-feature has created it. Without this check, implement-task could silently implement a specification that has drifted from the planned design -- potentially introducing inconsistencies between tasks planned together, or implementing changes that no longer reflect the reviewed plan. By surfacing the mismatch and requiring explicit user acknowledgment, the workflow ensures the human remains in control of whether to accept the modified description or return to the planning phase.
