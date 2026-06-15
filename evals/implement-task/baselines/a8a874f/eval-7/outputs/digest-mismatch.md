# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") has been fetched from Jira in Step 1. Before proceeding to Step 2 (Verify Dependencies), the implement-task skill must verify that the task description has not been modified since plan-feature created it.

This document describes the Step 1.5 verification process for this specific scenario, where a digest comment exists but the hex digest does not match the current description.

## Step 1.5 Execution Walkthrough

### Sub-step 1: Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

The API returns at least one comment. Among the returned comments, one has a body starting with the marker string `[sdlc-workflow] Description digest:`.

### Sub-step 2: Locate the digest comment

Search all returned comments for bodies starting with `[sdlc-workflow] Description digest:`. In this scenario, exactly one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker string, it is selected as the digest comment. (If multiple comments matched, the most recent one by `created` timestamp would be selected per the protocol's "Multiple Digest Comments" rule.)

### Sub-step 3: Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, which means the comment was not edited after initial posting. No warning is needed -- proceed to digest comparison.

(If `updated` were later than `created`, the skill would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." and still proceed with the comparison.)

### Sub-step 4: Extract the stored digest

Parse the tagged digest from the comment body:

- **Full value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md` (indicating the producer hashed the markdown representation)
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged format (`sha256:<hex>`) -- it uses the current `sha256-md` tag. No legacy format warning is needed.

### Sub-step 5: Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest, for example:

```
sha256-md:e4a3b7c1d9f2a5b8c3d6e7f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

The script exits with status 0 (success), so the check proceeds.

### Sub-step 6: Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same API access method (MCP, which returns markdown). Proceed to hex digest comparison.

(If tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- the skill would log a warning: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.)

### Sub-step 7: Compare hex digests -- MISMATCH

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `e4a3b7c1d9f2a5b8c3d6e7f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0`

The hex digests do NOT match. This means the task description was modified after plan-feature originally created it.

## Action: Alert the User and Stop

The skill alerts the user with the following message:

> **Description integrity check FAILED**
>
> The task description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:e4a3b7c1d9f2a5b8c3d6e7f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0`
>
> The format tags match (`sha256-md`), but the hex hashes differ, confirming the description content was changed.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- continue implementing with the current (modified) description as-is
> 2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate tasks with a fresh digest

**Execution stops immediately.** The skill does not proceed with any subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code, or any later step) until the user responds.

## Rationale

The description digest protocol is a defense-in-depth measure that guards against silent tampering between the planning and implementation phases. When plan-feature creates a task, it records a SHA-256 hash of the description. If someone (or something) modifies the description after planning -- whether intentionally or accidentally -- the implement-task skill detects this through the digest mismatch and surfaces it to the user rather than silently implementing a potentially altered specification.

The user is given explicit control: they can choose to proceed if the modification was intentional and acceptable, or stop to re-plan if the modification was unintended or introduces risk. The skill never silently continues past a confirmed mismatch.

## Summary of Verification Decision Points

| Check | Result in this scenario | Action |
|---|---|---|
| Digest comment found? | Yes (one comment matches marker) | Proceed to verification |
| Comment edited after posting? | No (created == updated) | No warning needed |
| Digest format (legacy untagged)? | No (uses `sha256-md` tag) | No legacy warning |
| Script exit code? | 0 (success) | Proceed to comparison |
| Format tags match? | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match? | No (hashes differ) | Alert user and STOP |
