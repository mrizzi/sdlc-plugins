# Step 1.5 -- Verify Description Integrity

## Context

Task: TC-9201 (Add advisory severity aggregation service and endpoint)

The Jira issue has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## Verification Process

### 1. Retrieve issue comments

Fetch all comments on the Jira issue using:

```
jira.get_issue_comments(TC-9201)
```

This returns the list of comments on the issue. In this case, there is exactly one comment.

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. The marker string is defined in `shared/description-digest-protocol.md` and is fixed across all skills.

**Result:** One comment matches the marker string. Since there is only one matching comment, there is no need to select among multiple candidates by `created` timestamp. This single comment is used as the digest comment.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps to detect post-creation editing.

**Result:** The `created` and `updated` timestamps are identical. This means the comment has not been edited since it was originally posted. No warning is needed. Proceed with digest comparison.

This check is a defense-in-depth measure described in the protocol's "Comment Edit Detection" section. If `updated` were later than `created`, a warning would be emitted: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." But in this case, timestamps match, so no such warning applies.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md` (indicates the description was hashed as markdown text)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:<hex>` (legacy untagged format), so there is no need to log a legacy format warning and skip the check. The tagged format (`sha256-md`) is the current format and proceeds to full verification.

### 5. Compute the current digest

Extract the description field from the Jira issue response (fetched in Step 1). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description retrieved via Jira is markdown text, the script:
1. Strips leading and trailing whitespace from the content
2. Computes SHA-256 of the normalized text
3. Outputs a format-tagged digest: `sha256-md:<64-char-hex>`

If the script exits non-zero, the integrity check would be skipped with a warning -- but in this scenario, the script succeeds.

**Result:** The script outputs `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

**Result:** Tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method, producing the same description format (markdown). Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs computed `sha256-md`), a warning would be logged ("Digest format mismatch -- skipping integrity check") and the skill would proceed normally without comparing hex digests.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result:** The hex digests match. The task description has not been modified since plan-feature created it.

### 8. Outcome

Per the SKILL.md Step 1.5 specification, section 4e:

> **Match**: proceed silently -- no additional user prompt, no added latency.

The integrity check passes. No warning is displayed to the user. No user interaction is required. Execution continues directly to Step 2 (Verify Dependencies) without pause.

## Summary of Decision Path

```
Fetch comments
  --> Found 1 digest comment (marker match)
    --> created == updated (no edit warning)
      --> Format: sha256-md (not legacy untagged)
        --> Compute current digest via scripts/sha256-digest.py
          --> Tags match (both sha256-md)
            --> Hex digests match
              --> PROCEED SILENTLY (no user prompt)
```
