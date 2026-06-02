# Step 1.5 -- Description Integrity Verification for TC-9201

## 1. Retrieve Issue Comments

Fetch all comments on the Jira issue TC-9201 using:

```
jira.get_issue_comments(TC-9201)
```

This returns the full list of comments on the issue, each with body text, `created` timestamp, and `updated` timestamp.

## 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. (If multiple comments matched, the most recent one by `created` timestamp would be selected, per the protocol for handling plan-feature re-runs.)

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical -- the comment has not been edited since it was posted. This means the digest value is trustworthy and has not been tampered with after initial posting. No warning is needed; proceed with digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag `sha256-md` indicates the digest was computed from the markdown representation of the description. This is not a legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

## 5. Compute the Current Digest

Extract the description field from the fetched TC-9201 issue response. Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. The computed output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, meaning both the producer (plan-feature) and the consumer (implement-task) used the same Jira API access method (both received markdown). No format mismatch warning is needed. Proceed to hex digest comparison.

## 7. Compare Hex Digests

- **Stored hex:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hex:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests match exactly. This confirms that the task description has not been modified since plan-feature created it.

## 8. Outcome: Proceed Silently

Because the digests match, the integrity check passes. Per the protocol:

> **Match**: proceed silently -- no additional user prompt, no added latency.

No warning is displayed. No confirmation is requested from the user. No message is logged about the integrity check result. The skill proceeds directly and without interruption to Step 2 (Verify Dependencies), adding zero latency or friction to the workflow.

This silent-proceed behavior is the expected happy path -- the description is verified as unmodified, and implementation can begin with confidence that the task specification matches what was planned.
