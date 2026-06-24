# Step 1.5 — Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 — "Add advisory severity aggregation service and endpoint"

After completing Step 1 (Fetch and Parse Jira Task), the implement-task skill proceeds to Step 1.5 to verify that the task description has not been modified since plan-feature created it.

## Step 1.5 Execution

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search through all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (if multiple had matched, the most recent by `created` timestamp would be selected).

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, `created` equals `updated` — the comment has not been edited after initial posting. No warning is needed; proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the description). Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest, for example:

```
sha256-md:b7e3f1a9c2d4e5f6a8b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2
```

(The actual hex value would be the SHA-256 of the current description content after stripping leading/trailing whitespace.)

### 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both accessed the description as markdown). No format-mismatch warning is needed. Proceed to hex digest comparison.

### 7. Compare Hex Digests — MISMATCH DETECTED

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:b7e3f1a9c2d4e5f6a8b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2`

The hex digests do NOT match. This means the task description was modified after plan-feature originally created it.

### 8. Alert the User and Stop Execution

The skill presents the following alert to the user:

> **Description integrity check failed.**
>
> The task description for TC-9201 has been modified since plan-feature created it. The recorded digest does not match the current description content.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:b7e3f1a9c2d4e5f6a8b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2`
>
> The description may have been manually edited in Jira after plan-feature generated it. Implementing a modified description risks diverging from the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** — implement the task using the current (modified) description as-is
> 2. **Stop** — abort implementation so you can re-run plan-feature to regenerate tasks from the updated feature description

**Execution stops immediately.** The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent steps. No branch is created, no code is modified, and no Jira transitions are made. The skill waits for the user's explicit response before taking any further action.

## Why This Matters

The description digest protocol guards against silent tampering between the planning and implementation phases. If someone modifies a task description in Jira after plan-feature created it — whether intentionally or accidentally — the implementation could diverge from the approved plan. By detecting the mismatch and stopping, the skill ensures the user is aware of the change and can make an informed decision:

- If the modification was intentional and correct, the user can choose to proceed.
- If the modification was accidental or unauthorized, the user can stop and re-run plan-feature to regenerate a consistent plan.

## Summary of Decision Points in Step 1.5

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes — one comment with marker `[sdlc-workflow] Description digest:` | Proceed to verification |
| Comment edited? | No — `created` equals `updated` | No warning needed |
| Legacy format? | No — uses tagged format `sha256-md:...` | No legacy warning |
| Format tags match? | Yes — both `sha256-md` | Proceed to hex comparison |
| Hex digests match? | No — hashes differ | Alert user, offer proceed/stop, STOP execution |
