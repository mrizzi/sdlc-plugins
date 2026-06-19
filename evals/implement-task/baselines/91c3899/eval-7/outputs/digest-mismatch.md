# Step 1.5 — Description Integrity Verification (MISMATCH Case)

## Context

Task TC-9201 has been fetched and parsed in Step 1. Before proceeding to Step 2 (Verify Dependencies), I must verify the description integrity per the digest protocol defined in `shared/description-digest-protocol.md`.

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Scan the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This is the exact fixed marker defined in the protocol. In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, I would select the most recent one by `created` timestamp. Here, only one comment matches.

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, meaning the comment has not been edited after initial posting. No warning is needed for comment tampering. Proceed to digest comparison.

(If `updated` were later than `created`, I would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed," but still proceed with the comparison.)

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged `sha256:<hex>` format, so no legacy warning applies. The full stored digest is `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP), the script outputs a tagged digest in the form:

```
sha256-md:abc123...def456
```

(A full 64-character hex digest, freshly computed from the current description content.)

## 6. Compare Format Tags

The stored tag is `sha256-md`. The computed tag is `sha256-md`. The tags match, so I proceed to compare the hex digests directly.

(If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- I would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.)

## 7. Compare Hex Digests — MISMATCH Detected

The stored hex digest is `0000000000000000000000000000000000000000000000000000000000000000`.
The computed hex digest is a different value (e.g., `abc123...def456`).

The format tags match (`sha256-md`) but the hex hashes differ. This is a **MISMATCH** -- the task description was modified after plan-feature created it.

## 8. Alert the User and Stop Execution

I would present the following to the user:

---

**Description integrity check: MISMATCH**

The task description for TC-9201 has been modified since plan-feature created it. The digest recorded at planning time does not match the current description content.

- **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<the-actual-64-char-hex-digest-computed-from-current-description>`

This means someone (or an automated process) edited the Jira task description after plan-feature generated it. The implementation plan may no longer align with the current description.

**How would you like to proceed?**

1. **Proceed** -- implement using the current description as-is, accepting that it differs from what was originally planned
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks based on the updated description

Please choose (1 or 2):

---

**EXECUTION STOPPED.** I will not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps until the user responds with their choice.

This follows the same pause-and-ask pattern used when a task description is incomplete -- execution halts completely, no branches are created, no code is inspected or modified, and no Jira transitions occur. The user's explicit decision is required before any further action.

### If the user chooses "Proceed" (option 1)

Continue with Step 2 (Verify Dependencies) using the current description content as the specification. The mismatch is acknowledged but accepted.

### If the user chooses "Stop" (option 2)

Terminate the implement-task execution entirely. The user should re-run plan-feature to regenerate the task descriptions, which will post a new digest comment reflecting the updated content. After that, implement-task can be re-invoked on the task.
