# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

This document describes how the description integrity verification (Step 1.5 of implement-task) would be handled for task TC-9201, given that the stored digest matches the computed digest.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple comments had matched, the most recent one by `created` timestamp would be selected.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical (the comment was not edited after initial posting). This means the comment is unmodified, so no warning is raised. Proceed with digest comparison.

If `updated` had been later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed, but the warning would be shown to the user.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicating the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file `/tmp/desc-TC-9201.txt`, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest, e.g.:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exits non-zero, a warning would be logged and the integrity check would be skipped (non-blocking).

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so hex digest comparison proceeds.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), this would indicate the producer and consumer used different Jira API access methods. A warning would be logged ("Digest format mismatch -- skipping integrity check") and implementation would proceed normally without comparing hex values.

### 7. Compare Hex Digests

The stored hex digest and the computed hex digest are identical:

- **Stored**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

### 8. Outcome

Since the digests match, the description has not been modified since plan-feature created it. Proceed silently to the next step -- no additional user prompt, no added latency, no warning messages. The description integrity is confirmed.

## Summary of Decision Path

```
Digest comment found?  --> YES
Comment edited?        --> NO  (created == updated)
Legacy format?         --> NO  (tagged as sha256-md, not bare sha256)
Format tags match?     --> YES (both sha256-md)
Hex digests match?     --> YES
Outcome:               --> Proceed silently to Step 2
```

## What Would Happen on Mismatch

For completeness: if the hex digests had not matched, the skill would alert the user that the task description was modified after plan-feature created it, display both the expected and actual digests, and ask the user whether to (1) proceed with the current description as-is or (2) stop so they can re-run plan-feature. Execution would halt until the user responds.
