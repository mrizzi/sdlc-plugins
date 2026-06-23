# Step 7 -- Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug (Not Affected)

The version impact analysis (Step 2) shows that **no supported product version** ships a vulnerable version of serde_json. All versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested JSON input) was patched before any currently supported product version was built.

**No remediation tasks are needed.** There are zero affected versions, so no upstream backport or downstream propagation work is required.

## VEX Justification

The VEX Justification custom field (`customfield_12345`) is configured in the project's Security Configuration.

**Recommended VEX value**: `Component not Present`

**Rationale**: Lock file analysis confirms that the vulnerable package version (serde_json < 1.0.135) is not included in any supported product version. All shipped versions contain serde_json >= 1.0.137, which already includes the CVE-2026-28940 fix (recursion limit). Per skill guidance, "Component not Present" is the default when lock file analysis shows the vulnerable package version is not included.

## Proposed Jira Actions

The following actions are **proposals** requiring engineer confirmation before execution. No Jira mutations have been performed.

### 1. Add triage comment to TC-8002

**Proposed comment:**

> No supported versions ship a vulnerable version of serde_json. Version impact analysis:
>
> | Stream | Versions | serde_json Range | Affected? |
> |--------|----------|-----------------|-----------|
> | 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | NO |
> | 2.2.x | 2.2.0 -- 2.2.4 | 1.0.138 -- 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.137, which is above the affected range (versions before 1.0.135). The fix for CVE-2026-28940 (configurable recursion limit) has been present in serde_json since 1.0.135.
>
> Closing as Not a Bug (not affected).
>
> ---
> _This triage was performed by the `triage-security` skill._

### 2. Transition TC-8002 to Closed

- **Resolution**: Not a Bug

### 3. Set VEX Justification

- **Field**: `customfield_12345`
- **Value**: `Component not Present`

### 4. Add label `ai-cve-triaged`

Mark the issue as triaged to prevent re-triage and enable filtering in Jira dashboards.

### 5. Assign to current user

Assign TC-8002 to the engineer performing the triage.

### 6. Correct Affects Versions

The current Affects Versions on TC-8002 is `RHTPA 2.2.0`. Since no versions are actually affected, the Affects Versions field should be cleared (or left as-is depending on team convention, since the issue is being closed as Not a Bug). This is presented for the engineer's decision.

## Actions NOT Taken

- **No remediation tasks created** -- zero affected versions means no fix work is needed.
- **No cross-stream impact comment** -- no stream is affected, so there is no cross-stream impact to report.
- **No Vulnerability issues created** -- this skill never creates Vulnerability issues; PSIRT owns that process.
