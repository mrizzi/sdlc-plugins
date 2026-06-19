# Step 1.5 — Description Integrity Verification: Digest Mismatch Handling

## Context

Task: TC-9201 (Add advisory severity aggregation service and endpoint)

After fetching and parsing the Jira task in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on the Jira issue using:

```
jira.get_issue_comments("TC-9201")
```

(Or, if MCP fails, fall back to `python3 scripts/jira-client.py get_comments TC-9201` per Step 0.5.)

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This exact marker prefix is defined in `shared/description-digest-protocol.md` and is the canonical way to identify digest comments among all issue comments. In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected. In this case, only one comment matches.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. Per the scenario, these timestamps are identical, meaning the comment has not been edited after initial posting. No edit warning is needed. Proceed to digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." Digest comparison would still proceed.)

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full stored value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format tag `sha256-md` indicates the digest was computed from the markdown representation of the description. This is not the legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest, e.g.:

```
sha256-md:a3f7b9c1d4e6f8091b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e
```

- **Computed format tag:** `sha256-md`
- **Computed hex digest:** `a3f7b9c1d4e6f8091b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e`

(If the script exits non-zero, warn and skip the integrity check without blocking execution.)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same API access method (markdown representation). Proceed to hex digest comparison.

(If the tags differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." And execution would proceed normally.)

### 7. Compare hex digests — MISMATCH DETECTED

- **Expected (from digest comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `a3f7b9c1d4e6f8091b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e`

The hex digests do not match. This means the task description was modified after plan-feature created it.

## User Alert

The following message is presented to the user:

> **Description integrity check: MISMATCH**
>
> The task description for TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:a3f7b9c1d4e6f8091b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e`
>
> Someone (or an automated process) modified the Jira task description after plan-feature generated it. The implementation may no longer match the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Choose (1/2):

## Execution Halt

Execution stops immediately at this point. No subsequent steps are performed:

- Step 2 (Verify Dependencies) is NOT executed.
- Step 3 (Transition to In Progress) is NOT executed.
- Step 4 (Understand the Code) is NOT executed.
- Step 5 (Create Branch) is NOT executed.
- No implementation planning, branching, code changes, or Jira updates occur.

This follows the same pause-and-ask pattern used when the structured description has missing or incomplete sections in Step 1: the skill presents the problem, offers choices, and waits for the user's explicit decision before taking any further action.

### If the user chooses "Proceed" (option 1)

Implementation continues with Step 2 using the current (modified) description. The mismatch is noted but does not block work. The user accepts responsibility for any divergence from the original plan.

### If the user chooses "Stop" (option 2)

The skill terminates. The user is expected to:
1. Review the description changes in Jira
2. Re-run plan-feature to regenerate tasks that reflect the updated feature description
3. Re-run implement-task on the regenerated task

No Jira state changes are made (no transition, no assignment, no comments) since the skill stops before Step 3.
