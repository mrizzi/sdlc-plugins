# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, there is exactly one matching comment with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, it is selected directly. If multiple had matched, the most recent by `created` timestamp would be selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical, which confirms the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Parse the stored digest

Extract the format-tagged digest value from the comment body after the marker prefix:

- **Full tagged value:** `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag:** `sha256-md` (indicates the digest was computed from a markdown representation of the description)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The tag is not the legacy untagged format (`sha256:<hex>`), so no legacy-format warning is needed. Proceed with full comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (as returned by `jira.get_issue`). Write it to a temporary file `/tmp/desc-TC-9201.txt`. Then compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (from MCP), it outputs a tagged digest in the form `sha256-md:<64-char-hex>`.

### 6. Compare format tags

The stored tag is `sha256-md`. The computed tag is also `sha256-md`. The tags match, meaning both the producer (plan-feature) and the consumer (implement-task) used the same API access method (MCP, which returns markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

The stored hex digest and the computed hex digest are compared. Per the eval scenario, the digests match -- the description has not been modified since plan-feature created the task.

### 8. Outcome: match -- proceed silently

Per the protocol specification (SKILL.md Step 1.5, section 4e): when the format tags match and the hex digests match, **proceed silently**. This means:

- No user prompt or confirmation is displayed
- No warning message is logged
- No additional latency is introduced
- Execution continues directly to Step 2 (Verify Dependencies) without interruption

The silent continuation is the correct behavior for a matching digest. The integrity check has confirmed that the task description is unchanged since planning, so there is no reason to involve the user or delay execution.
