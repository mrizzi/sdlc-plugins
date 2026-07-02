# Step 1.5 -- Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical. The digest computed from the current task description matches the stored digest.

## Verification Procedure

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments on the issue. In this scenario, there is exactly one comment.

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:` as defined in the shared description-digest-protocol.

In this scenario, the single comment matches the marker. If multiple comments had matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. Here, with only one matching comment, it is selected directly.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the two timestamps are identical, which means the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

If `updated` had been later than `created`, a warning would be logged: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." But the verification would still continue regardless.

If the timestamps were not available in the API response (e.g., MCP omits them), this check would be skipped silently.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md` (indicating the description was hashed as markdown text)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md`, not the legacy untagged format `sha256:`. No legacy format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (fetched in Step 1). Write it to a temporary file and compute the digest using the project's script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP), the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script had exited non-zero, a warning would be logged and the integrity check would be skipped without blocking execution.

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- they match. Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), a warning would be logged: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." Execution would proceed normally.

### 7. Compare Hex Digests

The stored hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` and the computed hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` -- they match.

## Outcome: Match -- Proceed Silently

When the digests match, the description has not been modified since plan-feature created it. The verification confirms the integrity of the task description.

**No user prompt is displayed. No warning is logged. No additional latency is introduced.** Execution proceeds directly to Step 2 (Verify Dependencies) without any pause or notification to the user.

This is the expected happy path: the digest protocol confirms that the description is exactly as plan-feature authored it, and the implementation can trust the task specification without interruption.

## Contrast: What Would Happen on Mismatch

For completeness, if the hex digests had not matched, the skill would:

1. Alert the user that the task description was modified after plan-feature created it
2. Display the expected digest (from the comment) and the actual digest (computed from current description)
3. Ask the user whether to: (a) Proceed with the current description as-is, or (b) Stop so they can re-run plan-feature to regenerate tasks
4. Stop execution immediately and wait for user response before continuing to any subsequent step
