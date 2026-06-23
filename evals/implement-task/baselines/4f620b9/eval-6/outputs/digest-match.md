# Description Integrity Verification -- Step 1.5

## Scenario

Task TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical. The format-tagged digest matches the digest computed from the current task description using `scripts/sha256-digest.py`.

## Step-by-Step Verification Process

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this scenario, exactly one comment matches. Since there is only one matching comment, it is selected directly (no need to compare `created` timestamps across multiple candidates).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, which means the comment has not been edited since it was posted. No warning is emitted. Proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md`
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the current tagged format (`sha256-md:`), not the legacy untagged format (`sha256:`), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (markdown text in this case) and outputs a tagged digest. Per the scenario, the output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0, indicating success.

### 6. Compare format tags

The stored tag is `md` and the computed tag is `md`. Tags match, so we proceed to hex digest comparison. No format-mismatch warning is needed.

### 7. Compare hex digests

Stored hex:   `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digests match.

## Outcome

**MATCH -- proceed silently.** Per the SKILL.md specification (Step 1.5, section 4e):

> Match: proceed silently -- no additional user prompt, no added latency.

The description has not been modified since plan-feature created it. No warnings are displayed to the user. No user interaction is required. Implementation proceeds directly to Step 2 (Verify Dependencies) without any interruption or delay.

## Summary of Checks Performed

| Check | Result | Action |
|---|---|---|
| Digest comment found | Yes (1 comment) | Proceed to verification |
| Legacy format? | No (uses `sha256-md:` tagged format) | No warning needed |
| Comment edited? | No (`created` == `updated`) | No warning needed |
| Format tags match? | Yes (both `md`) | Proceed to hex comparison |
| Hex digests match? | Yes | Proceed silently |
