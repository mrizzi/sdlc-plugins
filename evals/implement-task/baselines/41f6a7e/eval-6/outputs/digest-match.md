# Step 1.5 -- Description Integrity Verification

## Overview

This document describes how the implement-task skill handles description integrity
verification for task TC-9201 under Step 1.5 of the workflow. In this scenario, the
stored digest matches the computed digest, so execution proceeds silently.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker
string `[sdlc-workflow] Description digest:`. This marker is defined in
`shared/description-digest-protocol.md` and is the fixed identifier used by all
producer and consumer skills in the sdlc-workflow plugin.

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the
most recent one by `created` timestamp would be selected per the protocol. In
this case there is only one matching comment.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical, which confirms the comment has not been edited since it
was originally posted by plan-feature. No warning is necessary -- proceed with
digest comparison.

(If `updated` were later than `created`, a warning would be surfaced to the user:
"Digest comment was edited after initial posting -- integrity cannot be fully
guaranteed." The digest comparison would still proceed regardless.)

(If the API response did not include `created`/`updated` fields -- e.g., the MCP
tool omits them -- this check would be skipped silently.)

### 4. Parse the Stored Digest

Extract the format-tagged digest value from the comment body:

- **Full tagged digest:** `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag:** `sha256-md` (indicates the digest was computed from the markdown
  representation of the description)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md`, not the legacy untagged format (`sha256:<hex>`), so
no legacy warning is needed. Proceed with full verification.

### 5. Compute the Current Digest

Extract the description field from the Jira issue response (the markdown text
fetched via `jira.get_issue("TC-9201")`). Write it to a temporary file and compute
the digest using the project script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown in this case, since the
description was fetched via MCP which returns markdown) and outputs a
format-tagged digest. In this scenario, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script had exited non-zero, a warning would be logged and the integrity
check skipped without blocking execution.

### 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer
(implement-task) used the same API access method (MCP, which returns markdown),
so the digests are directly comparable. Proceed to hex digest comparison.

(If tags had differed -- e.g., stored was `sha256-adf` but computed was
`sha256-md` -- a warning would be logged: "Digest format mismatch (stored:
sha256-adf, current: sha256-md) -- producer and consumer used different API
access methods. Skipping integrity check." Execution would proceed normally
without blocking.)

### 7. Compare Hex Digests

- **Stored hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests **match**.

## Result

The description has not been modified since plan-feature created the task. The
digests match, so execution proceeds **silently** -- no user prompt, no additional
latency, no warning message. The workflow continues directly to Step 2 (Verify
Dependencies) without any interruption.

This is the expected happy-path behavior: when the digest matches, the integrity
check adds no observable delay or user interaction. The user is not informed of
the check at all -- it happens transparently as part of Step 1.5.

(If the digests had mismatched, the user would be alerted with expected vs. actual
digest values and asked whether to (1) proceed with the current description or
(2) stop so they can re-run plan-feature. Execution would halt until the user
responds.)
