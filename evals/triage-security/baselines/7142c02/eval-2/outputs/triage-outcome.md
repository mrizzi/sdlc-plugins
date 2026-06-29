# Step 7 -- Triage Outcome for TC-8002

## Decision: Case C -- No Supported Versions Affected

The version impact analysis shows that **no supported versions** ship a vulnerable
version of serde_json. All versions across both streams (2.1.x and 2.2.x) include
serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

**Recommendation: Close as Not a Bug (not affected).**

## Evidence Summary

- **CVE**: CVE-2026-28940 (serde_json stack overflow on deeply nested input)
- **Affected range**: serde_json < 1.0.135
- **Fix version**: 1.0.135
- **Lowest version shipped**: 1.0.137 (in versions 2.1.0 and 2.1.1)
- **All versions ship patched dependency**: Yes

No version in either supported stream ships serde_json below 1.0.135. The
vulnerability was already fixed before any supported product version was built.

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Add triage comment to TC-8002

Post a comment documenting the version impact analysis and close rationale:

> No supported versions ship a vulnerable version of serde_json.
> Version impact analysis:
>
> | Version | serde_json | Affected? |
> |---------|------------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | -- | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.137, which is outside the affected
> range (< 1.0.135). Closing as Not a Bug.

### 2. Transition TC-8002 to Closed

- **Resolution**: Not a Bug
- **Rationale**: The vulnerable version of serde_json (< 1.0.135) is not present
  in any supported product version. All versions ship 1.0.137 or later.

### 3. Set VEX Justification field

- **Field**: customfield_12345 (VEX Justification)
- **Value**: Component not Present
- **Rationale**: The vulnerable version of serde_json (< 1.0.135) is not included
  in any supported product version. All shipped versions contain serde_json >= 1.0.137,
  which includes the fix.

Note: "Component not Present" is the appropriate VEX justification because the
*vulnerable version* of the component is not present -- all shipped versions contain
the patched version.

### 4. Add ai-cve-triaged label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent
re-triage.

### 5. Assign to current user

Assign TC-8002 to the current user as part of the close workflow.

## Remediation Tasks

**None required.** Since no supported versions are affected, no remediation tasks
need to be created. This is a pure close-as-not-affected scenario.

## Affects Versions Correction

The current Affects Versions on TC-8002 is "RHTPA 2.2.0". Since no versions are
actually affected by this CVE (the vulnerability was already fixed before any
supported version was built), the Affects Versions field would ideally be cleared.
However, since the issue is being closed as Not a Bug, the Affects Versions
correction is moot -- the close action with VEX justification sufficiently
documents that no versions are impacted.
