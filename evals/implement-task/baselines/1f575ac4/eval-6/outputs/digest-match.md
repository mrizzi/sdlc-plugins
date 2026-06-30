# Step 1.5 -- Description Integrity Verification

## Retrieving Issue Comments

After fetching the task TC-9201 in Step 1, retrieve all comments on the issue using:

```
jira.get_issue_comments("TC-9201")
```

## Locating the Digest Comment

Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This exact marker prefix is defined in `shared/description-digest-protocol.md` and is used by plan-feature to record a content digest at task creation time.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected. Only one matching comment exists here.

## Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the `created` and `updated` timestamps are identical, meaning the comment has not been edited since it was posted. No warning is needed -- the comment is unmodified and trustworthy.

## Extracting the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

## Computing the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest using the project's script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest, e.g. `sha256-md:<64-char-hex>`.

## Comparing Format Tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md` -- the tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (MCP, which returns markdown). Proceed to hex digest comparison.

## Comparing Hex Digests

Per the eval prompt, the computed digest matches the stored digest. The format-tagged digest from `scripts/sha256-digest.py` produces the same `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` value as the one stored in the comment.

**Result: MATCH.**

## Outcome

The digests match. Per Step 1.5 rule 4e of the SKILL.md: when the hex digests match, proceed silently -- no additional user prompt, no added latency. The description has not been modified since plan-feature created it.

No user alert is issued. No pause in execution. Proceeding directly to Step 2 (Verify Dependencies) and subsequent steps.
