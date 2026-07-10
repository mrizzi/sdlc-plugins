# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

After fetching the Jira issue TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Verification Process

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns a list of comment objects, each containing body text, `created` timestamp, and `updated` timestamp.

### 2. Locate the Digest Comment by Marker

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. Here, only one digest comment exists, so it is used directly.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. Per the eval scenario, these timestamps are identical -- the comment has not been edited since it was posted.

Result: the comment is unmodified. No warning is emitted. Proceed with digest comparison.

(If `updated` had been later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The comparison would still proceed, but the warning would be shown to the user alongside the result.)

### 4. Parse the Format Tag and Hex Digest

Extract the tagged digest value from the comment body:

- Full tagged digest: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `sha256-md` (indicating the description was hashed as markdown text)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not the legacy untagged format (`sha256:<hex>`) -- it uses the format-tagged format (`sha256-md:<hex>`), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the description). Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script:
1. Strips leading and trailing whitespace from the description
2. Computes SHA-256 of the normalized text
3. Outputs a tagged digest: `sha256-md:<64-char-hex>`

Per the eval scenario, the computed digest matches the stored digest. The script output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The stored format tag is `sha256-md`. The computed format tag is `sha256-md`. The tags match, so the hex digests can be compared directly.

(If the tags had differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." The skill would then proceed normally without blocking.)

### 7. Compare Hex Digests

- Stored hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

Result: **MATCH**.

## Outcome

The digests match. The description has not been modified since plan-feature created the task. Per the SKILL.md specification (Step 1.5, item 4e):

> **Match**: proceed silently -- no additional user prompt, no added latency.

The skill proceeds directly to Step 2 (Verify Dependencies) without any user interaction, warning, or delay. No message is displayed to the user about the digest verification. The integrity check is completely transparent when the digests match.

(If the digests had mismatched, the skill would have alerted the user, displayed the expected vs. actual digests, and asked whether to proceed with the current description or stop so the user can re-run plan-feature. Execution would halt until the user responded.)
