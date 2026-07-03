# Description Integrity Verification (Step 1.5) for TC-9201

## Scenario

The Jira issue TC-9201 has one comment with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical. The digest uses the format-tagged format (`sha256-md:...`) and the computed digest from the current task description matches.

## Step-by-Step Verification Process

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the digest comment

Search returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, it is selected directly (no need to resolve multiple matches by `created` timestamp).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, meaning the comment has not been edited after initial posting. This is the clean case -- no warning is needed. Proceed to digest comparison.

If `updated` had been later than `created`, we would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed" but still proceed with the comparison.

### 4. Extract the stored digest

Parse the comment body to extract:
- **Format tag**: `md` (from `sha256-md:`)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the format-tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temporary file:

```bash
# Write description to temp file
cat > /tmp/desc-TC-9201.txt << 'EOF'
Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity
breakdowns without client-side counting.
EOF

# Compute digest using the project script
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs: `sha256-md:<64-char-hex>`.

Check the exit code -- if non-zero, warn and skip the integrity check (do not block execution).

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md`. Tags match, so we proceed to hex digest comparison.

If tags had differed (e.g., stored `sha256-adf` vs computed `sha256-md`), we would log: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally.

### 7. Compare hex digests

The stored hex digest matches the computed hex digest (as stated in the scenario).

**Result: MATCH -- proceed silently.** No user prompt, no warning, no added latency. The description has not been modified since plan-feature created it.

## Summary of Outcome

| Check | Result | Action |
|---|---|---|
| Digest comment found | Yes (1 comment) | Proceed to verification |
| Comment edited | No (created == updated) | No warning needed |
| Digest format | Tagged (`sha256-md`) | Not legacy; proceed |
| Format tag comparison | Match (both `md`) | Proceed to hex comparison |
| Hex digest comparison | Match | Proceed silently |

The integrity verification passes cleanly. Implementation proceeds to Step 2 (Verify Dependencies) without any user interaction or warnings.
