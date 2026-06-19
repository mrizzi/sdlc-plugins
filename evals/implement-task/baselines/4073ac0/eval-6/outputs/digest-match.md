# Step 1.5 -- Description Integrity Verification (Digest Match Scenario)

## Overview

This document describes how the implement-task skill handles Step 1.5 (Description Integrity Verification) for task TC-9201, given that a digest comment exists and the digests match.

## Procedure

### 1. Retrieve issue comments

After fetching the task in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This exact marker prefix is defined in `shared/description-digest-protocol.md` and is used by both producers (plan-feature) and consumers (implement-task) to identify digest comments.

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. In this case, only one exists.

### 3. Check for comment editing (timestamp comparison)

The digest comment's `created` and `updated` timestamps are compared. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is emitted. The skill proceeds to digest comparison.

If `updated` were later than `created`, the skill would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." But it would still proceed with digest comparison regardless.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md` (indicates the description was hashed as markdown text)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:<hex>` (legacy untagged format), so no legacy-format warning is needed. The tag is `sha256-md`, which is a valid format-tagged digest.

### 5. Compute the current digest

Extract the description field from the fetched issue response. Write it to a temporary file and compute the digest using the canonical script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (in this case, markdown/plain text) and outputs a format-tagged digest. Per the eval scenario, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exited non-zero, the skill would warn and skip the integrity check without blocking execution. In this scenario, the script succeeds.

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so the skill proceeds to hex digest comparison.

If the tags differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the skill would log: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare hex digests

The stored hex digest and the computed hex digest are identical:

- Stored:   `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.**

## Outcome: Proceed silently

When the digests match, the skill proceeds silently to subsequent steps (Step 2 -- Verify Dependencies). There is:

- No user prompt or confirmation dialog
- No warning message
- No additional latency or delay
- No log output beyond normal execution flow

The match confirms that the task description has not been modified since plan-feature created it, so the integrity of the description is verified and implementation can proceed with confidence.

This is the happy path -- the most common scenario when tasks flow from plan-feature to implement-task without manual edits. The verification adds negligible overhead (one comment retrieval API call plus one script execution) and produces no visible output to the user.
