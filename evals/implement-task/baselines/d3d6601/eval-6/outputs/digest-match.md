# Step 1.5 -- Description Integrity Verification

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This is the exact marker prefix defined in `shared/description-digest-protocol.md`.

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker string, it is selected directly. If multiple comments had matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the `created` and `updated` timestamps are identical, which means the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the `sha256:<hex-digest>` value from the comment body:

```
a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 5. Compute the current digest

Compute SHA-256 of the current task description field text. The preferred method is to use the `scripts/sha256-digest.py` script:

- Write the description field content (as returned by the Jira API) to a temporary file
- If the description is ADF JSON (MCP path): the script parses as JSON and re-serializes with compact separators (`json.dumps(parsed, separators=(',', ':'))`) before hashing
- If the description is raw text (REST API path): strip leading and trailing whitespace before hashing
- Run: `python3 scripts/sha256-digest.py /tmp/desc.json`
- The script outputs the lowercase 64-character hexadecimal SHA-256 digest to stdout

### 6. Compare digests

Compare the stored digest (from the comment) with the computed digest (from the current description).

**In this scenario, the digests match.** The task description has not been modified since plan-feature created it.

### 7. Outcome: proceed silently

Per the protocol, when digests match: **proceed silently**. There is no user prompt, no warning, no additional output, and no added latency. Implementation continues directly to Step 2 (Verify Dependencies) without any interruption.

## Summary of behavior for this scenario

| Check | Result | Action |
|---|---|---|
| Digest comment found | Yes (1 comment with marker) | Proceed to comparison |
| Comment edited after posting | No (created == updated) | No warning needed |
| Digest comparison | Match | Proceed silently -- no user prompt |

The key point is that a matching digest means the description is verified as unmodified since planning, and the skill proceeds without alerting or prompting the user in any way. This is the "happy path" for integrity verification.
