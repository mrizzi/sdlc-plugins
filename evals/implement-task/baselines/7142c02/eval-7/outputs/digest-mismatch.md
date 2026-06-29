# Step 1.5 -- Description Integrity Verification for TC-9201

## Retrieving Issue Comments

After fetching the task description in Step 1, I proceed to Step 1.5 to verify description integrity per the digest protocol defined in `shared/description-digest-protocol.md`.

I would retrieve all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

## Locating the Digest Comment

I search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`, as defined in `shared/description-digest-protocol.md`. This exact marker prefix is the canonical way to locate digest comments among all issue comments.

One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, there is no need to apply the "most recent by `created` timestamp" tiebreaker rule (which would apply if multiple digest comments existed from plan-feature re-runs).

## Comment Edit Detection

Per the protocol, I compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical, meaning the comment has not been edited after initial posting. No edit warning is needed. Proceeding to digest comparison.

## Extracting the Stored Digest

From the comment body, I parse the tagged digest value:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

This is not a legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged convention (`sha256-md:<hex>`), so I proceed with full verification.

## Computing the Current Digest

I would extract the description field from the issue response obtained in Step 1, write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (in this case, markdown text from the MCP response) and outputs a tagged digest. For this scenario, the script would output something like:

```
sha256-md:b7e4f2a1c9d8e3f5a6b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2
```

(The exact hex value would be computed from the actual current description content.)

## Comparing Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method (MCP, which returns markdown). I proceed to compare the hex digests directly.

## Comparing Hex Digests -- MISMATCH DETECTED

The hex digests do not match:

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:b7e4f2a1c9d8e3f5a6b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2`

## Alert to User

I would present the following alert to the user:

---

> **Warning: Task description modified after planning**
>
> The description of TC-9201 has been modified since plan-feature created this task. The description integrity check failed:
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:b7e4f2a1c9d8e3f5a6b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2`
>
> Someone modified the task description after plan-feature generated it. The implementation may not match the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Please choose (1 or 2):

---

## Execution Halted

**Execution stops here.** I do not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps. No branch is created, no code is modified, and no Jira transitions are made. The skill waits for the user's explicit response before taking any further action.

- If the user chooses **1 (Proceed)**: I would continue to Step 2 and proceed with implementation using the current description content.
- If the user chooses **2 (Stop)**: I would terminate execution entirely, informing the user that they should re-run plan-feature to regenerate the task descriptions based on the current feature specification.
