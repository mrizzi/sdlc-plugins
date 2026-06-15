# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

After fetching the Jira task TC-9201 in Step 1, implement-task proceeds to Step 1.5
to verify that the task description has not been modified since plan-feature created it.
This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker
string `[sdlc-workflow] Description digest:`. In this scenario, exactly one comment
matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since there is only one matching comment, it is selected directly. If multiple
comments matched (e.g., from plan-feature re-runs), the most recent one by `created`
timestamp would be selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
`created` and `updated` timestamps are identical, which means the comment has not
been edited after initial posting. This is the expected state -- no warning is emitted,
and verification proceeds normally.

If the timestamps had differed (i.e., `updated` later than `created`), a warning
would be surfaced: "Digest comment was edited after initial posting -- integrity
cannot be fully guaranteed." Verification would still proceed, but the warning would
be displayed alongside the result.

If the API response did not include these timestamp fields, this check would be
skipped silently.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed in markdown format)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:` (untagged/legacy), so no legacy-format warning is
needed. If the tag had been bare `sha256:<hex>`, the skill would log "Legacy digest
format detected -- skipping integrity check" and proceed without comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temp
file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format. Since the description is retrieved in markdown
format (via MCP), the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exits non-zero, a warning is logged and the integrity check is skipped
(non-blocking).

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match,
so hex digest comparison proceeds.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), this
would indicate the producer and consumer used different Jira API access methods. A
warning would be logged: "Digest format mismatch (stored: sha256-adf, current:
sha256-md) -- producer and consumer used different API access methods. Skipping
integrity check." Verification would proceed without blocking.

### 7. Compare hex digests

The stored hex digest and the computed hex digest are compared:

- **Stored**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.** The digests are identical, confirming that the task description has
not been modified since plan-feature created it.

## Outcome

When the digests match, the skill proceeds silently -- no user prompt, no warning, no
added latency. This is the happy path. The implementation continues directly to
Step 2 (Verify Dependencies).

Had the digests mismatched, the skill would alert the user, display the expected and
actual digests, and ask whether to:
1. **Proceed** with the current description as-is
2. **Stop** so they can re-run plan-feature to regenerate tasks

Execution would halt immediately until the user responded.

## Summary of decision tree

| Condition | Action |
|---|---|
| No digest comment found | Log warning, proceed (non-blocking) |
| Legacy untagged format (`sha256:<hex>`) | Log warning, skip check, proceed |
| Comment was edited (`updated` > `created`) | Log warning, continue with comparison |
| Format tags differ (`sha256-md` vs `sha256-adf`) | Log warning, skip comparison, proceed |
| Format tags match, hex digests match | Proceed silently (happy path -- this scenario) |
| Format tags match, hex digests mismatch | Alert user, ask to proceed or stop, halt until response |
| Script exits non-zero | Log warning, skip check, proceed |
