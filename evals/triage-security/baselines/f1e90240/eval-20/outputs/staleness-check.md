# Step 0.3 -- Matrix Staleness Check

## Configuration

Checked against the Version Streams table from Security Configuration:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Staleness threshold: **14 days**

## Matrix File Inspection

Both streams share the security matrix data provided in the mock file.

### Timestamp Extraction

Found HTML comment timestamp at the top of the matrix file:

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

- **Last-Updated**: 2026-06-28T10:00:00Z
- **Current date**: 2026-07-22
- **Age**: 24 days

## Staleness Assessment

### Stream 2.1.x (rhtpa-release.0.3.z)

| Check | Result |
|-------|--------|
| Last-Updated timestamp present | YES |
| Timestamp value | 2026-06-28T10:00:00Z |
| Age (days) | 24 |
| Threshold (days) | 14 |
| **Status** | **STALE** (24 days > 14-day threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Check | Result |
|-------|--------|
| Last-Updated timestamp present | YES |
| Timestamp value | 2026-06-28T10:00:00Z |
| Age (days) | 24 |
| Threshold (days) | 14 |
| **Status** | **STALE** (24 days > 14-day threshold) |

## Result

The security matrix was last updated on **2026-06-28** (24 days ago), which **exceeds** the 14-day staleness threshold for both streams.

Per the skill's Step 0.3 protocol, the following warning would be presented to the engineer:

> Security matrix for stream **2.1.x** was last updated on 2026-06-28
> (24 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-06-28
> (24 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Recommendation

The staleness warning should be acknowledged before proceeding to Step 1. For this eval (no external tool calls), we assume the engineer chooses **Option 2: Proceed anyway** and continue triage with the current matrix data.

## Matrix Content Summary

The matrix contains valid data for both streams:

- **Stream 2.1.x**: 2 released versions (2.1.0, 2.1.1)
- **Stream 2.2.x**: 5 released versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4), with 2.2.2 identified as a retag of 2.2.1

Ecosystem Mappings are configured for:
- **Cargo**: lock file `Cargo.lock`, check command `git show <tag>:Cargo.lock`
- **RPM**: lock file `rpms.lock.yaml`, check command `git show <tag>:rpms.lock.yaml`
