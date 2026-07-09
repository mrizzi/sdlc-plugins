# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Current date**: 2026-07-09
- **Staleness threshold**: 14 days

## Version Streams Checked

The Security Configuration defines two version streams, both served by a single `security-matrix.md` file:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Analysis

### Matrix Timestamp

- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 11 days (from 2026-06-28 to 2026-07-09)
- **Threshold**: 14 days

### Result: FRESH -- Proceed

The security matrix was last updated 11 days ago, which is within the 14-day staleness threshold. No refresh is required.

Both stream 2.1.x and stream 2.2.x matrix data are covered by this timestamp and are considered current.

### Decision

Proceed with triage using the current matrix data. No user intervention required.
