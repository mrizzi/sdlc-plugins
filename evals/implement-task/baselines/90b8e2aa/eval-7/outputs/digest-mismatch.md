# Step 1.5 — Description Integrity Verification for TC-9201

## 1. Retrieve Issue Comments

After fetching TC-9201 in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in `shared/description-digest-protocol.md`.

In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple comments matched, the most recent one by `created` timestamp would be selected.)

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case they are identical, which means the comment has not been edited after initial posting. No edit-detection warning is needed. Proceed to digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so the integrity check proceeds normally.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the description), write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown and outputs a tagged digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would be whatever SHA-256 produces from the current description content.)

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so a direct hex digest comparison is performed. (If the tags differed — e.g., stored `sha256-adf` vs computed `sha256-md` — we would log a format mismatch warning and skip the integrity check.)

## 7. Compare Hex Digests — Mismatch Detected

The stored hex digest (`0000000000000000000000000000000000000000000000000000000000000000`) does not match the computed hex digest (e.g., `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). This means the task description was modified after plan-feature created it.

## 8. Alert the User and Stop Execution

Present the following alert to the user:

---

**Warning: Task description integrity check failed for TC-9201.**

The task description has been modified since plan-feature created it. The description digest recorded at planning time does not match the current description content.

- **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

Please choose how to proceed:

1. **Proceed** — continue implementation using the current (modified) description as-is
2. **Stop** — halt execution so you can review the changes and re-run plan-feature to regenerate tasks if needed

---

**Execution is stopped immediately.** No subsequent steps are performed — Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), implementation planning, branching, code changes, and all later steps are blocked until the user responds.

This follows the same pause-and-ask pattern used when the structured description is incomplete: present the issue, offer explicit choices, and wait for the user's decision before taking any further action.

### If the user chooses "Proceed"

Resume execution at Step 2 (Verify Dependencies) using the current description content. The mismatch is acknowledged but does not block further work.

### If the user chooses "Stop"

End the skill invocation entirely. The user can investigate what changed in the description and re-run plan-feature to regenerate tasks with a fresh digest before re-invoking implement-task.
