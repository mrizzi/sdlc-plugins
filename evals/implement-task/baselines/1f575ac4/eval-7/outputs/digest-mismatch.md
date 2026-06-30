# Step 1.5 — Verify Description Integrity: Digest Mismatch Handling

## 1. Locate the Digest Comment

Retrieve all comments on TC-9201 from the Jira API and search for the comment whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## 2. Comment Edit Detection

The comment's `created` and `updated` timestamps are identical, so the comment has not been edited after posting. No timestamp warning is necessary. Proceed to digest comparison.

## 3. Compute the Current Description Digest

Fetch the current description of TC-9201 from the Jira API, write it to a temporary file, and compute its digest using `scripts/sha256-digest.py`. The script auto-detects the input format and outputs a format-tagged digest. Since the stored digest uses the `sha256-md` tag, and the computed digest also uses `sha256-md` (both are markdown format), the format tags match and direct hex comparison is valid.

## 4. Detect the Mismatch

Compare the stored and computed digests:

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:<computed-64-char-hex>` (a different hash)

The format tags match (both `sha256-md`), but the hex digests differ. This means the task description was modified after plan-feature originally created it.

## 5. Alert the User

Present the following warning to the user:

> **Description integrity check failed.** The description of TC-9201 has been modified since plan-feature created this task.
>
> - **Expected digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest:** `sha256-md:<computed-64-char-hex>`
>
> The task description no longer matches what was originally planned. Someone (or another process) changed the description after plan-feature generated it.
>
> **How would you like to proceed?**
>
> 1. **Proceed anyway** — use the current (modified) description as-is for implementation
> 2. **Stop** — halt implementation so you can re-run plan-feature to regenerate tasks with a fresh plan

## 6. Stop and Wait for User Response

Execution halts here. I do NOT proceed to Step 2 (implementation planning) or any subsequent steps. No files are created or modified, no branches are created, no code is written. This follows the same pause-and-ask pattern used when a task description is incomplete — the skill blocks until the user explicitly chooses an option.

- If the user chooses **(1) Proceed anyway**: continue to Step 2 using the current description content as the implementation spec, accepting that it differs from the original plan.
- If the user chooses **(2) Stop**: end the implement-task invocation entirely. The user should re-run plan-feature to regenerate the task descriptions, which will post a new digest comment reflecting the updated content.
