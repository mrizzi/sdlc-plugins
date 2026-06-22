# Description Integrity Verification — Step 1.5 (TC-9201)

## Overview

After fetching and parsing the Jira task TC-9201 in Step 1, Step 1.5 performs description integrity verification to detect whether the task description was modified after plan-feature created it. This document describes how each sub-step of Step 1.5 would be executed and the resulting outcome for this scenario.

---

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the full list of comments on the issue, including metadata such as `created` and `updated` timestamps and the comment body text.

## 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. In this case there is only one matching comment, so it is used directly.

## 3. Check for Comment Editing (Timestamp Comparison)

Compare the digest comment's `created` and `updated` timestamps. In this scenario, the two timestamps are identical, meaning the comment has not been edited since it was originally posted.

**Result:** The comment is unmodified. No warning is emitted. Proceed with digest comparison.

(If `updated` had been later than `created`, a warning would be logged: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed.)

## 4. Parse the Format Tag and Hex Digest from the Comment

Extract the tagged digest value from the comment body:

- **Full tagged digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format tag `sha256-md` indicates the digest was computed from markdown text (the MCP access path). This is not a legacy untagged format (`sha256:<hex>`), so full verification proceeds.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text describing the advisory severity aggregation service and endpoint). Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script outputs a tagged digest in the form:

```
sha256-md:<64-char-hex-of-current-description>
```

For example (illustrative, not the actual hash):

```
sha256-md:7f3a1b9c4e2d8f6a0b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a
```

If the script exits non-zero, a warning would be logged and the integrity check would be skipped (non-blocking). In this scenario, the script exits successfully.

## 6. Compare Format Tags

Compare the format tag from the stored digest comment against the format tag from the computed digest:

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

**Result:** Format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (MCP, which returns markdown). Proceed to hex digest comparison.

(If the tags had differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." The skill would proceed normally without blocking.)

## 7. Compare Hex Digests -- MISMATCH DETECTED

Compare the hex digest from the stored comment against the hex digest computed from the current description:

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `7f3a1b9c4e2d8f6a0b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a` *(actual value would be computed by sha256-digest.py)*

**Result: MISMATCH.** The hex digests do not match. The task description for TC-9201 has been modified since plan-feature originally created it.

## 8. Alert the User

The following alert is displayed to the user:

```
WARNING: Task description integrity check FAILED for TC-9201.

The task description was modified after plan-feature created this task.
The digest recorded at creation time does not match the current description.

Expected digest (from plan-feature comment):
  sha256-md:0000000000000000000000000000000000000000000000000000000000000000

Actual digest (computed from current description):
  sha256-md:<computed-64-char-hex>

The description content has changed since the planning phase. This may
indicate manual edits to the task description in Jira after plan-feature
generated it.
```

## 9. Offer the User a Choice

Present the user with two options:

```
How would you like to proceed?

1. Proceed — continue implementing with the current (modified) description as-is
2. Stop — abort implementation so you can re-run plan-feature to regenerate
   tasks based on the updated feature description

Choose (1/2):
```

## 10. STOP EXECUTION -- Awaiting User Response

**Execution is halted at Step 1.5.** The skill does not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent steps. No implementation planning occurs. No branches are created. No code changes are made.

The skill waits for the user to respond with their choice before taking any further action:

- If the user chooses **1 (Proceed)**: the skill would continue to Step 2 and proceed with implementation using the current description as-is.
- If the user chooses **2 (Stop)**: the skill would terminate, allowing the user to re-run plan-feature to regenerate task descriptions that reflect the updated feature scope.

---

**No plan.md is written. No further steps are executed. The skill is blocked pending user input.**
