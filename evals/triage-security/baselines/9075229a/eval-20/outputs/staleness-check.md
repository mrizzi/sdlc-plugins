# Step 0.3 -- Matrix Staleness Check

## Configuration

Two version streams are configured in Security Configuration:

| Stream | Konflux Release Repo | Security Matrix Path |
|--------|----------------------|----------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Evaluation

### Stream 2.1.x (rhtpa-release.0.3.z)

- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Current date**: 2026-07-03
- **Age**: 5 days
- **Threshold**: 14 days
- **Result**: **Fresh** -- matrix is within the 14-day staleness threshold.

No staleness warning displayed. Check passed silently.

### Stream 2.2.x (rhtpa-release.0.4.z)

- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Current date**: 2026-07-03
- **Age**: 5 days
- **Threshold**: 14 days
- **Result**: **Fresh** -- matrix is within the 14-day staleness threshold.

No staleness warning displayed. Check passed silently.

## Outcome

Both version streams have security matrices updated within the 14-day threshold (5 days ago). No staleness warning is required. No user prompt or options are presented -- the staleness check is silent on success.

Triage proceeds to Step 0.5 (JIRA Access Initialization) without interruption from the staleness check.
