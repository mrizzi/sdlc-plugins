# Step 0.3 -- Matrix Staleness Check

## Triage Target

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812 quinn-proto
- **Issue Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Staleness Check Procedure

Step 0.3 executes **before** Step 0.5 (JIRA Access Initialization). No Jira
operations have been attempted at this point -- the staleness check is a
pre-triage gate that operates solely on local matrix files.

### Configured Version Streams

From Security Configuration in CLAUDE.md:

| Stream | Konflux Release Repo | Security Matrix Path |
|--------|----------------------|----------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z/security-matrix.md |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z/security-matrix.md |

### Timestamp Extraction

Read the `<!-- Last-Updated: <ISO-8601> -->` HTML comment from the security matrix file.

- **Extracted timestamp**: `2026-05-01T10:00:00Z`
- **Parsed date**: 2026-05-01
- **Current date**: 2026-07-03
- **Days since last update**: 63 days
- **Staleness threshold**: 14 days (default)
- **Result**: **STALE** (63 days > 14-day threshold)

The same matrix file covers both configured streams (2.1.x and 2.2.x), and
the single `Last-Updated` timestamp applies to both.

## Staleness Warning

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (63 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (63 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

**Awaiting user choice before proceeding.** No further triage steps (including
Step 0.5 JIRA Access Initialization) will execute until the user responds to
the staleness warning for each stream.

## Step Ordering Verification

| Step | Name | Status |
|------|------|--------|
| 0 | Validate Configuration | Completed -- Security Configuration present and valid |
| 0.3 | Matrix Staleness Check | **Blocked -- awaiting user choice** |
| 0.5 | JIRA Access Initialization | Not started -- depends on Step 0.3 resolution |
| 0.7 | Assign and Transition | Not started -- depends on Step 0.5 |
| 1 | Data Extraction | Not started -- depends on Step 0.7 |

Step 0.3 is a blocking gate. The triage pipeline is paused here until the user
selects an option for each stale stream. If the user chooses "Refresh now", the
matrix population logic from setup Step 10.6 runs for the selected stream,
which writes an updated `Last-Updated` timestamp. After refresh completes (or
if the user chooses "Proceed anyway"), triage continues to Step 0.5.
