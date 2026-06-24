# Step 1.5 -- Verify Description Integrity

## Context

Task TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## Verification Process

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, it is selected directly (no need to compare `created` timestamps to find the most recent).

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical -- the comment was not edited after initial posting. No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:
- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `sha256-md`
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not the legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged style, so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file (`/tmp/desc-TC-9201.txt`) and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The script exits with status 0 (success).

### 6. Compare format tags

Stored tag: `sha256-md`
Computed tag: `sha256-md`

The tags match -- both are `sha256-md`, meaning both the producer (plan-feature) and the consumer (implement-task) accessed the description in the same format (markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

The digests match. The task description has not been modified since plan-feature created it.

### 8. Outcome

Per the protocol, when digests match: **proceed silently**. No user prompt is displayed, no warning is emitted, no additional latency is introduced. The skill continues directly to Step 2 (Verify Dependencies).

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment) | Proceed to verification |
| Comment edited? | No (created == updated) | No warning, proceed |
| Digest format | `sha256-md` (format-tagged, not legacy) | No legacy warning |
| Format tags match? | Yes (both `sha256-md`) | Proceed to hex comparison |
| Hex digests match? | Yes | Proceed silently to Step 2 |
