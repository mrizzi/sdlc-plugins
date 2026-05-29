# Step 1.5 -- Description Integrity Verification

## Overview

Step 1.5 verifies that the Jira task description has not been modified since
plan-feature created it. This uses the digest protocol defined in
`shared/description-digest-protocol.md`.

## Detailed Procedure

### 1. Retrieve Issue Comments

After fetching and parsing the task description in Step 1, fetch all comments on
the Jira issue:

```
jira.get_issue_comments(TC-9201)
```

This returns the full list of comments on the issue, including their body text,
`created` timestamps, and `updated` timestamps.

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker
string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment matches:

```
[sdlc-workflow] Description digest: sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the
protocol requires selecting the most recent one by `created` timestamp. In this
case there is only one matching comment, so it is used directly.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the
two timestamps are identical, which means the comment has not been edited after
initial posting. No warning is needed.

If `updated` were later than `created`, the skill would warn: "Digest comment
was edited after initial posting -- integrity cannot be fully guaranteed." and
still proceed with the digest comparison. If the timestamps were not available in
the API response, this check would be skipped silently.

### 4. Extract the Stored Digest

Parse the `sha256:<hex-digest>` value from the comment body:

```
a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

This is the digest that plan-feature computed from the description content it
wrote to the issue at creation time.

### 5. Compute the Current Digest

Compute SHA-256 of the current description field text from the Jira issue. The
normalization depends on the format:

- **ADF JSON** (MCP path): parse the description as JSON and re-serialize with
  compact separators (`json.dumps(parsed, separators=(',', ':'))`) before
  hashing. This ensures consistent hashing regardless of whitespace or key
  formatting differences in the original JSON.
- **Raw text** (REST API path): strip leading and trailing whitespace only.

The preferred method is to use the `scripts/sha256-digest.py` tool, which
handles normalization and outputs the correct 64-character lowercase hex digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc.json
```

This eliminates LLM hashing errors (placeholders, abbreviated hashes, incorrect
computation). The script output is correct by construction.

The result is a lowercase 64-character hexadecimal SHA-256 digest of the current
description content.

### 6. Compare Digests

Compare the stored digest (from the comment) with the computed digest (from the
current description).

In this scenario, the digests **match** -- the current description is identical
to what plan-feature originally wrote.

### 7. Outcome: Match -- Proceed Silently

Since the digests match, the skill proceeds silently to the next step (Step 2 --
Verify Dependencies). There is:

- **No user prompt** -- the user is not asked to confirm or approve anything
- **No warning message** -- no output is generated about the digest check
- **No additional latency** -- the happy path adds only the time to fetch
  comments and compute the hash, with no user interaction delay
- **No pause in execution** -- the skill moves directly to subsequent steps
  without stopping

This is the designed behavior for the happy path: when the description integrity
check passes, the verification is transparent and adds minimal overhead to the
workflow.

## Contrast with Mismatch Behavior

For comparison, if the digests did NOT match, the skill would:

1. Alert the user that the task description was modified after plan-feature
   created it
2. Display the expected digest (from the comment) and the actual digest
   (computed from the current description)
3. Ask the user whether to:
   - **Proceed** with the current description as-is
   - **Stop** so they can re-run plan-feature to regenerate tasks
4. **Stop execution immediately** -- no subsequent steps (branching,
   implementation, code changes) would proceed until the user responds

## Contrast with Missing Digest Behavior

If no comment matching the marker string were found at all, the skill would:

1. Log a warning: "No description digest found -- skipping integrity check. This
   task may have been created before digest tracking was introduced."
2. Proceed with implementation normally -- missing digests are non-blocking to
   support backward compatibility with tasks created before the protocol was
   introduced.
