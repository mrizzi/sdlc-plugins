# Step 1.5 -- Verify Description Integrity for TC-9201

## Overview

After fetching and parsing the task description in Step 1, Step 1.5 performs a description integrity verification to detect whether the task description was modified after plan-feature originally created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this case, one matching comment is found:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple comments matched, the most recent one by `created` timestamp would be selected.)

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical -- the comment has not been edited since it was posted. No edit warning is needed. Proceed with digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The comparison would still proceed.)

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the modern format-tagged syntax (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP), the script outputs a tagged digest in the form:

```
sha256-md:<64-char-hex>
```

For this scenario, assume the computed digest is (example):

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same API access method (markdown via MCP). Proceed to hex digest comparison.

(If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- the check would log a warning about the format mismatch and proceed normally without blocking.)

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected (from digest comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The hex digests do NOT match. This means the task description for TC-9201 was modified after plan-feature originally created it.

## Action Taken: Alert User and Stop Execution

The following message is presented to the user:

---

**WARNING: Task description integrity check failed for TC-9201.**

The task description has been modified since plan-feature created it. The content digest recorded at creation time does not match the current description.

| | Digest |
|---|---|
| **Expected** (from plan-feature comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

This means someone (or something) edited the Jira task description after the planning phase completed. The implementation may no longer align with the original plan.

**Options:**
1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate tasks with a consistent plan

Choose (1/2):

---

**Execution is halted immediately.** No subsequent steps are performed -- Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), Step 5 (Create Branch), Step 6 (Implement Changes), and all later steps are NOT executed. The skill waits for the user's explicit response before taking any further action.

## Rationale

This is a critical safety check in the SDLC workflow. The digest protocol guards against silent tampering between planning and implementation phases. If the description was modified -- whether intentionally by a team member refining requirements, or accidentally, or maliciously -- the implementation agent must not silently proceed with potentially inconsistent instructions. The user must make an informed decision about whether the current description is acceptable or whether re-planning is needed to restore consistency between the feature plan and its constituent tasks.
