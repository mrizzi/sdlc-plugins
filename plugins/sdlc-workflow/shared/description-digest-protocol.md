# Description Digest Protocol

Skills that create Jira tasks (plan-feature, verify-pr) record a content digest of
the task description at creation time. Skills that consume tasks (implement-task)
use this digest to detect whether the description was modified after creation,
guarding against silent tampering between planning and implementation phases.

## Marker String

The digest comment uses this exact marker prefix so consumers can locate it among
all issue comments:

```
[sdlc-workflow] Description digest:
```

The full comment body is a single line:

```
[sdlc-workflow] Description digest: sha256:<hex-digest>
```

## Hashing

- **Algorithm:** SHA-256
- **Input:** The full Jira description field text as returned by the API (ADF JSON
  string when using MCP, or the raw text when using REST API). Normalize the input
  by stripping leading/trailing whitespace before hashing.
- **Output:** Lowercase hexadecimal digest (64 characters)

The producer computes the hash from the description content it wrote to the issue,
immediately after creating it. This ensures the digest reflects exactly what was
persisted.

## Jira Comment Format

Post a comment on the created issue using ADF `contentFormat`. The comment body is
a single paragraph containing the marker and digest:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "[sdlc-workflow] Description digest: sha256:<hex-digest>"
        }
      ]
    }
  ]
}
```

This comment is separate from the skill's standard footnote comment. Post it as an
independent comment — do not append it to the plan summary comment or any other
comment.

## Consumer Verification

The consumer (implement-task) retrieves issue comments and searches for one whose
body starts with the marker string `[sdlc-workflow] Description digest:`. If found:

1. Extract the `sha256:<hex-digest>` value
2. Compute SHA-256 of the current description field (same normalization as producer)
3. Compare digests

**Match:** Proceed normally — description is unmodified since planning.

**Mismatch:** Warn the user that the task description was modified after planning.
Display the expected vs actual digest and ask whether to proceed or abort. Do not
silently continue.

### Comment Edit Detection

After locating the digest comment, check whether it was edited after posting by
comparing the comment's `created` and `updated` timestamps (both are returned by
the Jira REST API on every comment object):

1. If `updated` equals `created` — the comment is unmodified; proceed with digest
   comparison as above
2. If `updated` is later than `created` — the comment was edited after initial
   posting. Warn: "Digest comment was edited after initial posting — integrity
   cannot be fully guaranteed." Proceed with digest comparison but surface the
   warning to the user alongside any match/mismatch result
3. If the API response does not include `created`/`updated` fields (e.g., the MCP
   tool omits them) — skip this check silently and proceed with digest comparison
   only

This is a defense-in-depth measure. It detects the case where an attacker modifies
both the task description and the digest comment to match. Timestamp manipulation
by a Jira admin would bypass this check, but it raises the bar for casual tampering.

## Backward Compatibility

Tasks created before this protocol was introduced will not have a digest comment.
When the consumer finds no comment matching the marker string:

- Log a warning: "No description digest found — skipping integrity check. This task
  may have been created before digest tracking was introduced."
- Proceed with implementation normally — do not block execution.

## Rules

- Producers must post the digest comment immediately after creating the task issue,
  before creating issue links or other comments
- The digest comment must be a standalone comment, not embedded in other comments
- Consumers must treat a missing digest as a non-blocking warning, not an error
- Consumers should check digest comment `created` vs `updated` timestamps when
  available, and warn if the comment was edited — but proceed regardless
- The marker string is fixed — do not vary it per skill or per invocation

## Common Mistakes — Do NOT

The following mistakes have been observed in practice and must be avoided:

- **Do NOT use placeholder text.** The `<hex-digest>` in the marker template is a
  placeholder — replace it with the actual computed hash. Never post a comment
  containing the literal string `<hex-digest>`, `<hex>`, `sha256:placeholder`, or
  any other stand-in text.
- **Do NOT use abbreviated hashes.** A SHA-256 digest is exactly 64 lowercase
  hexadecimal characters. Values like `sha256:a1b2c3d4e5f6` (12 chars) or
  `sha256:abc123` (6 chars) are wrong. Always output the full 64-character digest.
- **Do NOT use example or hardcoded hashes.** Every digest must be freshly computed
  from the actual description content. Never copy a hash from documentation,
  examples, or a previous task.
- **Do NOT add extra text to the marker line.** The comment body must be exactly
  one line: `[sdlc-workflow] Description digest: sha256:<64-char-hex>`. Do not
  append explanations, timestamps, or metadata after the hash.
