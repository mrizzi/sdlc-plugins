# Description Integrity Verification -- Step 1.5 Handling

## Scenario

The Jira issue TC-9201 has one comment with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical. The digest computed from the current task description matches the stored digest (same format tag `sha256-md`, same hex hash).

## Step-by-step verification process

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, it is selected directly (no need to resolve multiple candidates by `created` timestamp).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, `created` equals `updated`, which means the comment has not been edited since initial posting. No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the comment body after the marker prefix:
- Full tagged digest: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md`
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the format-tagged format (`sha256-md:...`), not the legacy untagged format (`sha256:...`), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the Jira issue response. Write it to a temp file (`/tmp/desc-TC-9201.txt`). Run the digest script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (markdown text in this case) and outputs a tagged digest: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.

### 6. Compare format tags

Stored tag: `md`. Computed tag: `md`. Tags match -- proceed to hex digest comparison. No format mismatch warning is needed.

### 7. Compare hex digests

Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

Result: **Match**.

### 8. Outcome

The digests match. Per the protocol, the skill proceeds silently -- no user prompt, no warning, no added latency. Implementation continues to Step 2 without any interruption or user interaction regarding description integrity.

## Summary

All conditions for a clean, silent pass are met:
- Digest comment exists (not a pre-protocol task, so no "skipping integrity check" warning)
- Comment was not edited (`created` == `updated`, so no "integrity cannot be fully guaranteed" warning)
- Format tag is not legacy untagged (not `sha256:<hex>`, so no "Legacy digest format" warning)
- Format tags match (`sha256-md` on both sides, so no "format mismatch" warning)
- Hex digests match (description has not been modified since plan-feature created it)

The skill proceeds to Step 2 (Verify Dependencies) without any output or user interaction related to Step 1.5.
