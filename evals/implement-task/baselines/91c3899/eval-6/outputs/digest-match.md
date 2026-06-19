# Step 1.5 -- Verify Description Integrity

## Locating the Digest Comment

After fetching the Jira issue TC-9201 in Step 1, I retrieve all comments on the issue using `jira.get_issue_comments("TC-9201")`. I search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in the shared description-digest-protocol and is the fixed prefix used by all sdlc-workflow skills.

One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, there is no need for recency disambiguation (though if multiple existed, I would select the most recent one by `created` timestamp).

## Comment Edit Detection

I compare the digest comment's `created` and `updated` timestamps. They are identical, which means the comment has not been edited since it was posted. No edit warning is needed -- the comment is unmodified and its integrity is intact.

## Computing the Current Digest

I extract the format tag and hex digest from the stored comment:

- **Format tag:** `sha256-md`
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

Next, I extract the description field from the issue response (the markdown text of the task description), write it to a temp file (`/tmp/desc-TC-9201.txt`), and compute the current digest using:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain text / markdown) and outputs a format-tagged digest: `sha256-md:<64-char-hex>`.

## Comparing Format Tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md`. Tags match, so I proceed to compare the hex digests directly. No format mismatch warning is needed.

## Comparing Hex Digests

The stored hex digest matches the computed hex digest exactly. The digests are identical.

## Outcome

**Digests match.** The task description has not been modified since plan-feature created it. Per the protocol, I proceed silently -- no user prompt, no alert, no added latency. Execution continues directly to Step 2 (Verify Dependencies).
