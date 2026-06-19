# Step 1.5 -- Verify Description Integrity

## Context

Task: TC-9201 -- Add advisory severity aggregation service and endpoint

After fetching the task description in Step 1, I proceed to Step 1.5 to verify
that the description has not been modified since plan-feature created it. This
follows the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string:

```
[sdlc-workflow] Description digest:
```

One matching comment is found:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected (if multiple had matched, the most
recent by `created` timestamp would be selected).

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the
timestamps are identical -- the comment has not been edited after initial posting.
No warning is needed for comment tampering. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response. Write it to a
temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain markdown text in this case) and
outputs a tagged digest. Example output:

```
sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
```

The script exits with status 0, so the computed digest is valid.

### 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match -- both are `sha256-md`. This means the producer
(plan-feature) and the consumer (implement-task) used the same API access method
(both received markdown). Proceed to hex digest comparison.

### 7. Compare Hex Digests

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`

**MISMATCH.** The hex digests differ, which means the task description was modified
after plan-feature created it.

## Alert to User

> **Warning: Task description integrity check failed.**
>
> The description of TC-9201 has been modified since plan-feature created it.
> The digest recorded at creation time does not match the current description.
>
> **Expected digest (from plan-feature comment):**
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest (computed from current description):**
> `sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`
>
> This means someone (or an automated process) edited the task description after
> the plan-feature skill generated it. The implementation may not match the
> original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Please choose (1/2):

## Execution State

**Execution is STOPPED.** No further steps (Step 2, Step 3, or beyond) will be
executed until the user responds with their choice.

- If the user chooses **Proceed (1)**: continue to Step 2 (Verify Dependencies)
  using the current description, acknowledging that it differs from the original
  plan.
- If the user chooses **Stop (2)**: halt execution entirely. The user should
  re-run plan-feature on the parent feature to regenerate task descriptions that
  reflect the updated feature specification, then re-run implement-task on the
  resulting tasks.
