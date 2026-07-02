# Triage Outcome: TC-8011 (CVE-2026-45678)

## Summary

**Decision: Case A -- Affected. Create NEW remediation tasks.**

CVE-2026-45678 affects webpack (versions before 5.98.0) with an Arbitrary Code Execution vulnerability (CVSS 7.8 High). The issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix.

## Rationale

### Version Impact

The issue is scoped to stream 2.2.x. The vulnerability affects all webpack versions before 5.98.0. Version impact analysis against the security matrix for the 2.2.x stream would determine which specific product versions ship a vulnerable webpack version.

### Cross-CVE Overlap (Step 4.3) -- Not Covered

A related CVE Jira (TC-8012 / CVE-2026-43210) was found affecting the same upstream component (webpack), same PS Component (pscomponent:org/rhtpa-ui), and same Stream (rhtpa-2.2). TC-8012 has a linked remediation task TC-8013 that bumps webpack to 5.96.1.

However, the current CVE requires webpack >= 5.98.0 to be fixed. Since 5.96.1 < 5.98.0, the existing remediation does **not** cover CVE-2026-45678.

### Why New Tasks Are Needed

1. **No covering remediation exists.** The only related remediation (TC-8013) bumps webpack to 5.96.1, which is below the fix threshold of 5.98.0.
2. **The vulnerability is in a supported stream.** Stream 2.2.x is the latest stream and is actively supported.
3. **The ecosystem is npm (source dependency).** Per the skill's remediation rules, source dependency ecosystems require two tasks.

## Remediation Plan

Since webpack is an npm package (source dependency ecosystem), create **two** remediation tasks:

### Task 1: Upstream Backport Task
- **Action**: Bump webpack to >= 5.98.0 in the source repository (rhtpa-ui or rhtpa-backend)
- **Stream**: rhtpa-2.2
- **Labels**: CVE-2026-45678, pscomponent:org/rhtpa-ui, security
- **Link**: Depend link from TC-8011 to this task
- **Description**: Must follow `task-description-template.md` format so `/implement-task` can parse it

### Task 2: Downstream Propagation Subtask
- **Action**: Update the webpack reference in the Konflux release repo (rhtpa-release.0.4.z) after the upstream fix lands
- **Stream**: rhtpa-2.2
- **Labels**: CVE-2026-45678, pscomponent:org/rhtpa-ui, security
- **Blocked by**: Task 1 (upstream backport must complete first)
- **Description**: Must follow `task-description-template.md` format so `/implement-task` can parse it

## Cross-CVE Overlap Table (for reference)

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

## Key Facts

- **CVE**: CVE-2026-45678
- **Library**: webpack
- **Fix threshold**: 5.98.0
- **Existing remediation (TC-8013) bump target**: 5.96.1
- **Coverage**: NOT covered (5.96.1 < 5.98.0)
- **Triage decision**: Create new remediation tasks
- **Number of tasks**: 2 (upstream backport + downstream propagation)
- **Ecosystem**: npm (source dependency)
