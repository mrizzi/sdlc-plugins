# Description Integrity Verification (Step 1.5) for TC-9201

## Overview

Step 1.5 of implement-task verifies that the Jira task description has not been modified since plan-feature originally created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Step-by-Step Verification Process

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on the Jira issue TC-9201:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the Digest Comment

Search through all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This exact marker prefix is defined in `shared/description-digest-protocol.md` and is used by all sdlc-workflow skills to identify digest comments.

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker string, it is selected directly. If multiple comments had matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected.

### 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are compared. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is issued.

If `updated` were later than `created`, a warning would be logged: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The verification would still proceed regardless.

If the API response did not include `created`/`updated` fields, this check would be skipped silently.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full tagged digest**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (indicating the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest does not use the legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged format (`sha256-md:<hex>`), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), it strips leading/trailing whitespace and computes the SHA-256 hash, outputting a tagged digest in the format `sha256-md:<64-char-hex>`.

If the script exited non-zero, we would warn and skip the integrity check without blocking execution.

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md`. The tags match, so we proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs computed `sha256-md`), a warning would be logged: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." Execution would proceed normally without blocking.

### 7. Compare Hex Digests

Per the eval scenario, the computed digest matches the stored digest (`a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`).

**Result: MATCH**

### 8. Outcome: Proceed Silently

Since the digests match, the skill proceeds silently to Step 2 (Verify Dependencies). There is:

- No user prompt or confirmation dialog
- No warning message
- No added latency
- No log output about the match (silence indicates success)

This is the expected behavior per SKILL.md Step 1.5, item 4e: "Match: proceed silently -- no additional user prompt, no added latency."

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (one comment with marker `[sdlc-workflow] Description digest:`) | Proceed to verification |
| Comment edited? | No (`created` == `updated`) | No warning needed |
| Digest format? | Tagged (`sha256-md:...`), not legacy | Proceed (no legacy warning) |
| Format tags match? | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match? | Yes | Proceed silently to Step 2 |

## What Would Happen on Mismatch

If the digests had not matched, the skill would:

1. Alert the user that the task description was modified after plan-feature created it
2. Display the expected digest (from the comment) and the actual digest (computed from the current description)
3. Ask the user whether to:
   - **Proceed** with the current description as-is
   - **Stop** so they can re-run plan-feature to regenerate tasks
4. Stop execution immediately until the user responds
