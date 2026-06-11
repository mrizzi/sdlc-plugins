# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

Step 1.5 verifies that the task description has not been modified since plan-feature
originally created it. This uses the Description Digest Protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the most
recent one by `created` timestamp would be selected. In this case there is only one
matching comment, so it is used directly.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. According to the task
specification, the `created` and `updated` timestamps on the digest comment are
identical. This means the comment has not been edited after initial posting, which
is the expected (clean) state.

**Result**: The comment is unmodified. No warning is emitted. Proceed with digest
comparison.

If `updated` had been later than `created`, we would warn: "Digest comment was
edited after initial posting -- integrity cannot be fully guaranteed." We would
still proceed with the digest comparison, but surface the warning to the user
alongside the match/mismatch result.

If the API response did not include `created`/`updated` fields (e.g., the MCP
tool omits them), this check would be skipped silently.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged value**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (indicates the digest was computed from markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the format-tagged format (`sha256-md:...`), not the legacy untagged
format (`sha256:...`). Therefore, we proceed with the full verification rather than
logging a legacy format warning and skipping.

### 5. Compute the current digest

Extract the description field from the issue response (fetched in Step 1). Write it
to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text
(as returned by MCP), the script outputs a format-tagged digest:

```
sha256-md:<64-char-hex-digest>
```

If the script exits non-zero, we would warn and skip the integrity check without
blocking execution.

### 6. Compare format tags

Compare the format tag from the stored digest (`md`) with the format tag from the
computed digest. According to the task specification, the script is assumed to produce
a digest with the same format tag (`sha256-md`), so the tags match.

**Result**: Tags match (`md` == `md`). Proceed to hex digest comparison.

If the tags had differed (e.g., stored was `sha256-adf` but computed was `sha256-md`),
we would log: "Digest format mismatch (stored: adf, current: md) -- producer and
consumer used different API access methods. Skipping integrity check." and proceed
normally without blocking.

### 7. Compare hex digests

Compare the hex digest from the stored comment with the hex digest computed from the
current description. According to the task specification, we are told to assume the
digests MATCH (same format tag and same hash).

**Result**: The digests match. Proceed silently -- no additional user prompt, no added
latency, no warning.

This confirms that the task description has not been modified since plan-feature
created it. The integrity check passes cleanly.

## Summary of outcomes by scenario

| Scenario | Action |
|---|---|
| No digest comment found | Log warning, proceed (non-blocking) |
| Legacy untagged format (`sha256:<hex>`) | Log warning, skip check, proceed |
| Comment was edited (`updated` > `created`) | Warn user, still compare digests |
| Format tags differ (`adf` vs `md`) | Log format mismatch warning, skip check, proceed |
| Format tags match, hex digests match | Proceed silently (this scenario) |
| Format tags match, hex digests mismatch | Alert user, ask to proceed or stop, halt until response |
| Script exits non-zero | Warn, skip check, proceed |

## This scenario's path

For TC-9201, the verification follows the cleanest path:

1. Digest comment found (single match) -- no ambiguity
2. Comment not edited (created == updated) -- no tampering warning
3. Format tag is `sha256-md` (not legacy) -- full verification proceeds
4. Format tags match (both `md`) -- hex comparison is valid
5. Hex digests match -- description is unmodified since planning
6. **Outcome: proceed silently to Step 2**
