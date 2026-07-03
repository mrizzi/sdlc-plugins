# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") has been
fetched and parsed in Step 1. The structured description is complete and contains
all required sections (Repository, Target Branch, Description, Files to Modify,
Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test
Requirements, Dependencies). Step 1 parsing succeeds with no gaps.

Before proceeding to Step 2 (Verify Dependencies), Step 1.5 performs description
integrity verification using the digest protocol defined in
`plugins/sdlc-workflow/shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple
comments had matched, the most recent one by `created` timestamp would be selected,
per the protocol's Multiple Digest Comments rule.)

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
two timestamps are identical, meaning the comment has not been edited after initial
posting. No warning is emitted. Proceed to digest comparison.

(If `updated` had been later than `created`, a warning would be emitted: "Digest
comment was edited after initial posting -- integrity cannot be fully guaranteed."
The digest comparison would still proceed, but the warning would be surfaced to the
user.)

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text
of the description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a
format-tagged digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would be computed from the current description content.)

The script exits with status 0, so we proceed with comparison. (If the script had
exited non-zero, we would warn and skip the integrity check without blocking
execution.)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer
(implement-task) used the same Jira access method (MCP, which returns markdown).
Proceed to hex digest comparison.

(If the tags had differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` --
a warning would be logged: "Digest format mismatch (stored: sha256-adf, current:
sha256-md) -- producer and consumer used different API access methods. Skipping
integrity check." Execution would proceed normally without blocking.)

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected (from comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The format tags match (`sha256-md` == `sha256-md`) but the hex hashes differ.
This means the task description was modified after plan-feature created it.

## Action Taken: Alert User and Stop

Per the SKILL.md Step 1.5 rule 4e (mismatch case), execution stops immediately.
The following alert is presented to the user:

---

> **Description integrity check FAILED for TC-9201.**
>
> The task description has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):**
>   `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):**
>   `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> The description was changed after planning. Implementing against a modified
> description may produce results that diverge from the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks from the
>    updated feature description
>
> Choose (1/2):

---

**Execution is halted.** No subsequent steps (Step 2 through Step 11) are executed
until the user responds.

- If the user chooses **1 (Proceed)**: implementation continues with the current
  description. Steps 2-11 execute normally using the parsed task data from Step 1.
  The mismatch is noted but does not alter the implementation workflow.

- If the user chooses **2 (Stop)**: execution terminates. The user is expected to
  re-run plan-feature against the parent feature (TC-9001) to regenerate task
  descriptions that reflect the current state of the feature, producing new digest
  comments that will match on the next implement-task run.

## Why This Matters

The description digest protocol guards against silent tampering between the
planning and implementation phases. When plan-feature creates a task, it records a
cryptographic fingerprint of the description. If someone (or an automated process)
modifies the task description in Jira after planning -- changing acceptance
criteria, implementation notes, file targets, or scope -- implement-task detects
the change before writing any code.

In this specific scenario:
- The format tags match (`sha256-md` == `sha256-md`), confirming both producer and
  consumer used the same Jira access method, so the comparison is valid.
- The comment was not edited (created == updated), so the stored digest is
  trustworthy.
- The hex hashes differ, which is the definitive signal that the description
  content changed.

The human-in-the-loop decision ensures that the user explicitly acknowledges the
modification before implementation proceeds, preventing divergence between the
planned and implemented behavior.
