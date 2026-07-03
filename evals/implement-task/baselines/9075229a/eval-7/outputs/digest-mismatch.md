# Step 1.5 -- Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment posted by a previous `plan-feature` run:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

The comment's `created` and `updated` timestamps are identical. The current task
description, when hashed with `scripts/sha256-digest.py`, produces a different
`sha256-md` digest. The format tags match (both `sha256-md`) but the hex hashes
differ, indicating the description was modified after `plan-feature` created the
task.

## How Step 1.5 Would Handle This

### Sub-step 1: Retrieve issue comments

Fetch all comments on TC-9201 via `jira.get_issue_comments(TC-9201)`.

### Sub-step 2: Locate the digest comment

Scan all returned comments for bodies starting with the marker string
`[sdlc-workflow] Description digest:`. In this scenario, exactly one comment
matches. If multiple had matched, the most recent by `created` timestamp would
be selected.

### Sub-step 3: Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario they
are identical, so the comment was **not** edited after initial posting. No warning
is emitted. Proceed to digest comparison.

(If `updated` were later than `created`, the skill would warn: "Digest comment was
edited after initial posting -- integrity cannot be fully guaranteed." It would
still proceed with digest comparison regardless.)

### Sub-step 4: Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed.

### Sub-step 5: Compute the current digest

Extract the description field from the Jira issue response. Write it to a
temporary file `/tmp/desc-TC-9201.txt` and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs
a tagged digest, e.g.:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would depend on the current description content.)

If the script exits non-zero, the skill would warn and skip the integrity check
without blocking execution.

### Sub-step 6: Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags
**match**, so the skill proceeds to hex digest comparison.

(If the tags had differed -- e.g., stored `sha256-adf` vs computed `sha256-md` --
the skill would log: "Digest format mismatch (stored: sha256-adf, current:
sha256-md) -- producer and consumer used different API access methods. Skipping
integrity check." and proceed normally without blocking.)

### Sub-step 7: Compare hex digests -- MISMATCH

The stored hex digest (`0000...0000`) does **not** match the computed hex digest.
This is the critical decision point. The skill takes the following actions:

1. **Alert the user** that the task description was modified after `plan-feature`
   created it.

2. **Display both digests** so the user can see the discrepancy:
   - Expected (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
   - Actual (computed from current description): `sha256-md:<current-hex-digest>`

3. **Ask the user** to choose one of two options:
   - **(1) Proceed** -- continue with the current description as-is, accepting
     that it may differ from what was originally planned.
   - **(2) Stop** -- halt execution so the user can re-run `plan-feature` to
     regenerate tasks based on the updated feature description.

4. **Stop execution immediately** -- the skill does **not** proceed with any
   subsequent steps (Step 2 onward) until the user responds. This is a blocking
   prompt, not a non-blocking warning.

## Summary of Outcome

Because the format tags match (`sha256-md` on both sides) but the hex digests
differ, Step 1.5 surfaces a **blocking mismatch alert**. The skill halts and
waits for explicit user confirmation before continuing. This guards against
implementing a task whose description was silently modified between the planning
and implementation phases -- the user must consciously decide whether the current
description is acceptable or whether re-planning is needed.

## Key Design Points

- **Comment edit detection** (created vs updated) passed cleanly in this scenario
  (timestamps identical), so no additional warning was emitted. This is a
  defense-in-depth check against an attacker modifying both the description and
  the digest comment to match.
- **Format tag comparison** happened before hex comparison. Had the tags differed,
  the check would have been skipped entirely with a non-blocking warning, since
  cross-format digest comparison is meaningless (ADF JSON and markdown text
  produce different hashes for the same content).
- **The mismatch is blocking**, unlike missing-digest or format-mismatch
  scenarios which are non-blocking warnings. This is the only path in Step 1.5
  that halts execution and requires user input.
- **The digest script** (`scripts/sha256-digest.py`) is always used for
  computation -- never manual SHA-256 hashing -- to ensure consistent
  normalization (strip leading/trailing whitespace for markdown).
