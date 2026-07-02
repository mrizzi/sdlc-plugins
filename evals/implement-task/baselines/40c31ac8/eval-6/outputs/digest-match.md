# Step 1.5 -- Description Integrity Verification (Digest Match Case)

## Overview

Step 1.5 verifies that the task description has not been modified since plan-feature created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`. The process is designed to be zero-latency on the happy path (digests match): no user prompt, no warning, just silent continuation.

## Detailed Procedure

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments(TC-9201)
```

This returns all comments associated with the issue, including metadata such as `created` and `updated` timestamps for each comment.

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This exact marker prefix is defined in `shared/description-digest-protocol.md` and is fixed across all skills and invocations. The search is a simple string prefix match on the comment body text.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the skill would select the most recent one by `created` timestamp. Here, only one comment matches, so it is used directly.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. This is the clean case -- no warning is needed, and the skill proceeds to digest comparison with full confidence in the comment's integrity.

(If `updated` were later than `created`, the skill would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." It would still proceed with digest comparison, but surface the warning to the user. If timestamps were unavailable in the API response, this check would be skipped silently.)

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body. The comment body after the marker prefix is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Extracted components:
- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:` (the legacy untagged format), so no legacy-format warning is triggered. The skill proceeds with the modern tagged comparison.

### 5. Compute the Current Digest

Extract the description field from the issue response obtained in Step 1. Write it to a temporary file and compute the digest using the project's script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (ADF JSON vs. plain markdown text) and outputs a format-tagged digest. In this scenario, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exited non-zero, the skill would warn and skip the integrity check without blocking execution.

### 6. Compare Format Tags

Compare the format tag from the stored digest (`sha256-md`) against the format tag from the computed digest (`sha256-md`).

The tags match. This confirms that both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method (both obtained the description as markdown text). No format mismatch warning is needed.

(If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- the skill would log a warning about the producer and consumer using different API access methods and skip the integrity check entirely, proceeding normally.)

### 7. Compare Hex Digests

With matching format tags, compare the hex digests directly:

- **Stored**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.**

### 8. Outcome -- Proceed Silently

Since the digests match, the description is confirmed to be unmodified since plan-feature created it. The skill proceeds silently to Step 2 (Verify Dependencies) with:

- **No user prompt** -- no confirmation dialog or interactive question
- **No warning message** -- nothing logged about the digest check
- **No additional latency** -- the happy path adds only the time for the API call to fetch comments and the script execution to compute the digest; no user interaction delays

This is the designed behavior for the happy path: the integrity check is transparent when everything is consistent. The user is only interrupted when something is wrong (mismatch, edit detection, format incompatibility).

## Summary of Decision Tree

| Condition | Action |
|---|---|
| No digest comment found | Log warning, proceed normally (backward compatibility) |
| Legacy format (`sha256:<hex>`) | Log warning, skip check, proceed normally |
| Comment edited (`updated` > `created`) | Warn user, proceed with comparison |
| Format tags differ | Log warning, skip comparison, proceed normally |
| Hex digests match | Proceed silently (this case) |
| Hex digests mismatch | Alert user, show expected vs actual, ask proceed/stop |
