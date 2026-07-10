# Triage Outcome -- TC-8006: Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill detected this link and handled it idempotently by skipping link creation.

## Step 4.2 Detailed Analysis

### What Step 4.2 requires

Step 4.2 (Cross-stream coordination) requires linking different-stream siblings with a "Related" link type. However, before creating any link, the skill must perform an idempotency check:

1. Read the current issue's `issuelinks` array (already fetched in Step 1 via `jira.get_issue`).
2. Check if any existing link satisfies **all** of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
3. If a matching link exists, **skip link creation** and log the skip.
4. If no matching link exists, create the link.

### What happened for TC-8006

The `issuelinks` array from the Step 1 data extraction shows:

```
Issue Links:
- Related: TC-8001 (outward, Link ID: 1990401)
```

**Check performed**: Does any existing link have `type.name == "Related"` AND `outwardIssue.key == "TC-8001"`?

**Result**: Yes -- the existing outward Related link to TC-8001 (Link ID 1990401) matches both conditions.

**Action taken**: Link creation was **skipped**. The skill logged:
> "Related link to TC-8001 already exists -- skipping"

### Why this matters

The idempotency check in Step 4.2 prevents duplicate link creation. Without this check, re-triaging TC-8006 (or triaging it when the link was pre-populated by PSIRT or a previous partial triage) would create a second "Related" link to TC-8001, cluttering the issue's link list. The check ensures the skill is safe to run multiple times on the same issue.

### Remaining Step 4.2 actions completed

Even though link creation was skipped, Step 4.2 still performed:

1. **Affects Versions overlap check**: Verified no version overlap between TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1). Each issue carries versions from its own stream only -- no overlap.

2. **Sibling landscape presentation**: Presented the companion issue table showing both TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New) for engineer awareness.

## Overall Triage Outcome

Based on the full triage analysis:

- **Stream scope**: 2.1.x (from suffix [rhtpa-2.1])
- **Affected versions in scope**: RHTPA 2.1.0 (quinn-proto 0.11.9) and RHTPA 2.1.1 (quinn-proto 0.11.9) -- both ship vulnerable versions (< 0.11.14)
- **Cross-stream impact**: The 2.2.x stream is also partially affected (2.2.0 and 2.2.1), but that stream is already tracked by sibling TC-8001 (status: In Progress). No preemptive tasks needed for 2.2.x.
- **Sibling link**: Pre-existing Related link to TC-8001 was detected and preserved (no duplicate created).
- **Affects Versions correction needed**: PSIRT assigned only RHTPA 2.1.0 but lock file analysis shows RHTPA 2.1.1 is also affected. Step 3 would propose correction: `[RHTPA 2.1.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]`.
- **Recommended action**: Case A (Affected) -- create remediation tasks for the 2.1.x stream. Since quinn-proto is a Cargo (source) dependency, this means two tasks: an upstream backport task (bump quinn-proto to >= 0.11.14 on branch release/0.3.z in the backend repo) and a downstream propagation subtask (update the source reference in rhtpa-release.0.3.z).
