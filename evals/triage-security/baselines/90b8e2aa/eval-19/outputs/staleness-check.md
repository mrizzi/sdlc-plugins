# Step 0.3 -- Matrix Staleness Check

## Configuration Extracted (Step 0)

From the project CLAUDE.md Security Configuration:

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Check Execution

Step 0.3 runs **after** Step 0 (Validate Project Configuration) and **before** Step 0.5 (JIRA Access Initialization). No Jira operations are attempted before the staleness check completes.

### Matrix file read

Read the `security-matrix-stale-mock.md` file used for both configured Version Streams (2.1.x and 2.2.x).

### Timestamp extraction

Extracted the `Last-Updated` timestamp from the HTML comment at the top of the matrix file:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

Parsed ISO 8601 value: **2026-05-01T10:00:00Z**

### Staleness evaluation

- **Current date**: 2026-07-02
- **Last updated**: 2026-05-01
- **Age**: 62 days
- **Threshold**: 14 days (default)
- **Result**: **STALE** -- the matrix is 62 days old, exceeding the 14-day threshold by 48 days.

### Staleness Warning -- Stream 2.1.x

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (62 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

### Staleness Warning -- Stream 2.2.x

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (62 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

## Step Sequencing Note

This check (Step 0.3) executes after Step 0 (Validate Project Configuration) and before Step 0.5 (JIRA Access Initialization). No Jira API calls, MCP operations, or external tool invocations have been made at this point. The staleness check is a local-only operation that reads the matrix file timestamp and compares it against the current date.

If the user selects **Refresh now** for either stream, the skill would invoke the matrix population logic from setup Step 10.6 for the selected stream. After population completes (which writes an updated `Last-Updated` timestamp), triage continues with the refreshed matrix.

If the user selects **Proceed anyway**, triage continues with the current (stale) matrix data. Version impact analysis in Step 2 would use the existing supportability matrix rows, which may not include recently released versions.

If the user selects **Stop**, triage execution halts immediately. The user can investigate the matrix staleness and re-run triage after updating the matrix.
