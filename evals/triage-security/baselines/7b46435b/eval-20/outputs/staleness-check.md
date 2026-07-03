# Step 0.3 -- Matrix Staleness Check

## Configuration

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Evaluation

Both version streams share a single security-matrix.md file in this eval configuration.

**Matrix timestamp:** `2026-06-28T10:00:00Z`
**Current date:** 2026-07-03
**Age:** 5 days
**Staleness threshold:** 14 days

## Result: FRESH -- Proceed

The security matrix was last updated on 2026-06-28 (5 days ago), which is within the 14-day staleness threshold. No staleness warning is triggered.

### Per-Stream Detail

| Stream | Last-Updated | Age (days) | Status |
|--------|-------------|------------|--------|
| 2.1.x (rhtpa-release.0.3.z) | 2026-06-28T10:00:00Z | 5 | Fresh |
| 2.2.x (rhtpa-release.0.4.z) | 2026-06-28T10:00:00Z | 5 | Fresh |

Both streams pass the staleness check. Proceeding to Step 1 (Data Extraction) without user intervention.
