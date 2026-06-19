# Step 1.5 -- Description Integrity Verification

## Overview

After fetching the Jira task TC-9201 in Step 1, the implement-task skill performs description integrity verification to ensure the task description has not been modified since plan-feature originally created it. This step uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Detailed Procedure

### 1. Retrieve Issue Comments

The skill fetches all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns a list of comment objects, each containing at minimum a `body` field, and typically `created` and `updated` timestamps.

### 2. Locate the Digest Comment by Marker String

The skill iterates through all returned comments and searches for any whose body starts with the exact marker string:

```
[sdlc-workflow] Description digest:
```

This marker is defined in `shared/description-digest-protocol.md` and is fixed across all skills and invocations. In this scenario, there is exactly one comment matching the marker, with the full body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the skill would select the most recent one by `created` timestamp. In this case, only one digest comment exists, so it is selected directly.

### 3. Comment Edit Detection

Before proceeding with digest comparison, the skill checks whether the digest comment was edited after initial posting by comparing the comment's `created` and `updated` timestamps.

In this scenario, the `created` and `updated` timestamps are identical. This means the comment has not been edited since it was originally posted. The skill proceeds with full confidence in the digest comment's integrity -- no warning is emitted.

If `updated` were later than `created`, the skill would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed," but would still proceed with the digest comparison. If timestamps were not available in the API response (e.g., MCP omits them), the skill would skip this check silently.

### 4. Parse the Format Tag from the Stored Digest

The skill extracts the tagged digest value from the comment body by parsing the text after the marker prefix. The full stored value is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

This is parsed into two components:

- **Format tag**: `sha256-md` -- indicates the digest was computed from the markdown representation of the description
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` (64 hexadecimal characters, as required for SHA-256)

The format tag is not `sha256:<hex>` (the legacy untagged format), so no legacy-format warning is needed. If it were untagged (e.g., `sha256:a1b2...`), the skill would log "Legacy digest format detected -- skipping integrity check" and proceed normally without attempting comparison.

### 5. Compute the Current Digest

The skill extracts the description field from the Jira issue response (fetched in Step 1), writes it to a temporary file, and computes the digest using the project's script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format:
- If the description content is valid JSON (ADF format from REST API), it outputs `sha256-adf:<hex>`
- If it is plain text (markdown from MCP), it strips leading/trailing whitespace and outputs `sha256-md:<hex>`

If the script exits non-zero (e.g., empty input), the skill would warn and skip the integrity check without blocking execution. In this scenario, the script succeeds and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The skill compares the format tag from the stored digest against the format tag from the computed digest:

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The tags match. This confirms that both the producer (plan-feature) and the consumer (implement-task) accessed the Jira description using the same API method (both used MCP, which returns markdown). The skill proceeds to hex digest comparison.

If the tags differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), the skill would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare Hex Digests

With matching format tags, the skill performs a direct string comparison of the hex digest values:

- **Expected** (from comment): `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Actual** (computed from current description): `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests match.

### 8. Outcome: Proceed Silently

Because the digests match, the description has not been modified since plan-feature created the task. The skill proceeds silently to Step 2 (Verify Dependencies) with no additional user prompt, no warning message, and no added latency.

Per the protocol specification: "Match: proceed silently -- no additional user prompt, no added latency."

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment with marker) | Continue to verification |
| Multiple digest comments? | No (1 match) | Use the single match |
| Comment edited? (`created` vs `updated`) | No (timestamps identical) | No warning, proceed |
| Digest format tagged or legacy? | Tagged (`sha256-md`) | Continue (no legacy warning) |
| Format tags match? | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match? | Yes (identical) | Proceed silently |
