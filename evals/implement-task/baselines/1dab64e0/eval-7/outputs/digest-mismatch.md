# Step 1.5 -- Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 (Add advisory severity aggregation service and endpoint)

After fetching the task description in Step 1, Step 1.5 performs a description integrity verification to detect whether the task description was modified after plan-feature originally created it.

## Procedure Followed

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (no need to compare timestamps for recency).

### 3. Check for comment editing

The comment's `created` and `updated` timestamps are identical. This means the comment has not been edited since it was originally posted. No warning is needed -- proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest, for example:

```
sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
```

(The actual hex value would be computed from the current description content.)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match -- both are `sha256-md`. This means the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both received markdown). Proceed to hex digest comparison.

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`

The format tags match (`sha256-md` = `sha256-md`), but the hex hashes differ. This means the task description was modified after plan-feature originally created it.

## Alert to User

The following alert would be presented to the user:

---

**WARNING: Task description integrity check failed.**

The description of TC-9201 has been modified since plan-feature created it. The content digest recorded at creation time does not match the current description.

**Expected digest (recorded by plan-feature):**
`sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

**Actual digest (computed from current description):**
`sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`

Someone (or an automated process) modified the task description after plan-feature generated it. The implementation may no longer match the original plan.

**How would you like to proceed?**

1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description

Choose (1/2):

---

## Execution State

**Execution is STOPPED.** The skill does not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps until the user responds to the prompt above.

- If the user chooses **1 (Proceed)**: the skill continues with Step 2 using the current description content, accepting that it differs from what plan-feature originally generated.
- If the user chooses **2 (Stop)**: the skill terminates immediately. The user is expected to re-run plan-feature to regenerate task descriptions that reflect the current feature requirements, then re-invoke implement-task.

No plan.md is written. No branches are created. No code changes are made. No Jira transitions occur.
