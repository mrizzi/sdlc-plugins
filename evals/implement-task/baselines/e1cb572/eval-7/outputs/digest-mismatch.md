# Step 1.5 — Description Integrity Verification for TC-9201

## Context

After fetching and parsing the Jira task TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature originally created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (if multiple had matched, the most recent by `created` timestamp would be selected).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

If `updated` had been later than `created`, the following warning would be displayed:

> "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed."

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy warning applies. Proceed with comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown content describing the advisory severity aggregation service and endpoint). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects that the input is plain markdown text and outputs a tagged digest, for example:

```
sha256-md:b7e4a93f1d2c8e6a5b0f3d9c7e1a4b6d8f2e5c9a3b7d1e4f6a8c0e2d4f6b8a9c
```

(The actual hex value would be whatever SHA-256 produces from the current description content.)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method (both markdown). Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs computed `sha256-md`), the skill would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `b7e4a93f1d2c8e6a5b0f3d9c7e1a4b6d8f2e5c9a3b7d1e4f6a8c0e2d4f6b8a9c`

The hex digests do NOT match. This means the task description was modified after plan-feature created it.

## Action Taken: Alert and Stop

The skill displays the following alert to the user:

---

**Description integrity check FAILED for TC-9201.**

The task description has been modified since plan-feature created it.

| | Digest |
|---|---|
| **Expected** (from plan-feature digest comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:b7e4a93f1d2c8e6a5b0f3d9c7e1a4b6d8f2e5c9a3b7d1e4f6a8c0e2d4f6b8a9c` |

The description was changed after planning. This could mean the requirements have been updated, fields were edited manually, or Jira normalized the content.

**How would you like to proceed?**

1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate tasks with an updated plan

---

**Execution is paused. No subsequent steps (Step 2 onward) will run until the user responds.**

The skill does not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any later step. It waits for the user to make a decision:

- If the user chooses **Proceed**, implementation continues from Step 2 using the current description content, accepting that it differs from what plan-feature originally generated.
- If the user chooses **Stop**, implementation halts entirely so the user can investigate the description changes and optionally re-run plan-feature to regenerate tasks that reflect the current state of the feature plan.
