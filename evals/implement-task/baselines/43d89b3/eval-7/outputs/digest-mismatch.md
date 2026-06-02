# Step 1.5 — Description Integrity Verification (Digest Mismatch Scenario)

## 1. Locate the Digest Comment

After fetching the Jira issue TC-9201 in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

Search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in `shared/description-digest-protocol.md` and is the fixed prefix used by plan-feature when posting digest comments.

In this scenario, one matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. If multiple comments matched, the most recent one by `created` timestamp would be selected per the protocol's "Multiple Digest Comments" rule.

## 2. Comment Edit Detection

Before comparing digests, check whether the digest comment was edited after it was originally posted by comparing the `created` and `updated` timestamps on the comment object.

In this scenario, the `created` and `updated` timestamps are identical. This means the comment has not been edited since it was posted — it is unmodified. Proceed with digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." If the timestamps were unavailable in the API response, this check would be skipped silently.)

## 3. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full tagged digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format tag is not `sha256:` (untagged/legacy format), so legacy handling does not apply. Proceed with full digest comparison.

## 4. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest using the canonical script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. Suppose the output is:

```
sha256-md:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
```

(This is an illustrative value representing the actual hash of the current description content.)

## 5. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match — both are `sha256-md`. This means the producer (plan-feature) and consumer (implement-task) used the same API access method (both markdown). Proceed to hex digest comparison.

(If the tags differed, e.g. stored `sha256-adf` vs computed `sha256-md`, a warning would be logged and the integrity check would be skipped: "Digest format mismatch (stored: sha256-adf, current: sha256-md) — producer and consumer used different API access methods. Skipping integrity check.")

## 6. Compare Hex Digests — MISMATCH DETECTED

- **Expected (stored in comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069`

The hex digests do NOT match. The format tags are identical (`sha256-md`), confirming both values were computed using the same method. The difference in hex hashes means the task description content has been modified after plan-feature originally created the task.

## 7. Alert the User

The following alert is presented to the user:

> **Warning: Task description modified after planning**
>
> The description for TC-9201 has been modified since plan-feature created this task. The description digest recorded at planning time does not match the current description content.
>
> - **Expected digest (from plan-feature):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (from current description):** `sha256-md:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069`
>
> This could mean someone manually edited the task description in Jira after plan-feature generated it, or plan-feature was re-run and the digest comment was not updated.
>
> How would you like to proceed?
>
> 1. **Proceed** — continue implementing with the current (modified) description as-is
> 2. **Stop** — halt implementation so you can re-run plan-feature to regenerate the task with a fresh digest
>
> Please choose (1 or 2):

## 8. Stop Execution — Await User Response

**Execution is halted immediately.** No subsequent steps are performed — Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), Step 5 (Create Branch), Step 6 (Implement Changes), and all later steps are NOT started.

This follows the same pause-and-ask pattern used for incomplete description handling in Step 1: when the task description is missing required sections, the skill stops and asks the user for clarification before proceeding. The digest mismatch scenario applies the same principle — the description integrity cannot be confirmed, so the user must make an explicit decision before any implementation work begins.

If the user chooses option 1 (Proceed), implementation continues from Step 2 with the current description content, accepting the risk that the description may have been modified in ways that diverge from the original plan.

If the user chooses option 2 (Stop), the skill terminates. The user can re-run plan-feature to regenerate the task description and digest, then re-invoke implement-task.
