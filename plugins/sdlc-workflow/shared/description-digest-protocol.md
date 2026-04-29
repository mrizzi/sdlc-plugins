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
- The marker string is fixed — do not vary it per skill or per invocation
