# Step 1.5 -- Description Integrity Verification for TC-9201

## Locating the Digest Comment

After fetching the Jira issue TC-9201 in Step 1, retrieve all comments on the issue using:

```
jira.get_issue_comments("TC-9201")
```

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in the shared description digest protocol (`shared/description-digest-protocol.md`) and is used by plan-feature to record a content hash of the task description at creation time.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker string, it is selected directly. If multiple comments had matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected to ensure deterministic behavior.

## Comment Edit Detection

The digest comment's `created` and `updated` timestamps are compared. In this case, they are identical, which means the comment has not been edited since it was initially posted. No warning is needed -- the comment is unmodified and trustworthy. Proceed with digest comparison.

(If the timestamps had differed -- `updated` later than `created` -- a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." But comparison would still proceed. If the API response omitted timestamps, this check would be skipped silently.)

## Extracting the Stored Digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md` (indicates the description was hashed as markdown text)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:<hex>` (legacy untagged format), so no legacy-format warning is needed.

## Computing the Current Digest

Extract the description field from the fetched issue response for TC-9201. Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. The script would output:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

(If the script had exited non-zero, a warning would be logged and the integrity check skipped -- execution would not be blocked.)

## Comparing Format Tags

The stored format tag is `sha256-md` and the computed format tag is `sha256-md`. The tags match, so the hex digests can be compared directly.

(If the tags had differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." And execution would proceed normally.)

## Comparing Hex Digests

The stored hex digest and the computed hex digest are compared:

- Stored:   `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.** The digests are identical, confirming the task description has not been modified since plan-feature created it.

## Outcome

Per the protocol, when the hex digests match the skill proceeds silently -- no additional user prompt, no warning, no added latency. The description integrity is verified and execution continues directly to Step 2 (Verify Dependencies) without any user interaction or pause.
