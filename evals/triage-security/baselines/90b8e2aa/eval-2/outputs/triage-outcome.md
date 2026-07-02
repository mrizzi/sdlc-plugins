# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

**Recommendation: Close as Not a Bug (not affected).**

All supported product versions ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. No version in either the 2.2.x stream (issue-scoped) or the 2.1.x stream (cross-stream) is vulnerable. The vulnerability was already fixed in the dependency before the earliest shipped product version was built.

## Evidence

- Fix threshold: serde_json >= 1.0.135
- Lowest shipped version: serde_json 1.0.137 (in 2.1.0 and 2.1.1, build tags v0.3.8 and v0.3.12)
- Issue-scoped stream (2.2.x): all versions ship serde_json 1.0.138 or 1.0.139
- Cross-stream (2.1.x): all versions ship serde_json 1.0.137

## Proposed Jira Actions

The following Jira mutations would be performed after engineer confirmation:

### 1. Correct Affects Versions

The PSIRT-assigned Affects Version "RHTPA 2.2.0" is incorrect -- version 2.2.0 ships serde_json 1.0.138, which is not within the affected range (< 1.0.135).

- Current: `[RHTPA 2.2.0]`
- Proposed: `[]` (empty -- no versions are affected)

### 2. Post triage comment

Add comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
> Version impact analysis shows all versions across both streams ship
> serde_json >= 1.0.137, which is outside the affected range (< 1.0.135).
>
> | Version | serde_json | Affected? |
> |---------|------------|-----------|
> | 2.2.0   | 1.0.138    | NO        |
> | 2.2.1   | 1.0.138    | NO        |
> | 2.2.2   | (retag)    | NO        |
> | 2.2.3   | 1.0.139    | NO        |
> | 2.2.4   | 1.0.139    | NO        |
> | 2.1.0   | 1.0.137    | NO        |
> | 2.1.1   | 1.0.137    | NO        |

### 3. Set VEX Justification

Since the VEX Justification custom field is configured (`customfield_12345`), set it to **"Component not Present"** -- the vulnerable version of the package (serde_json < 1.0.135) is not shipped in any supported version. All versions ship a patched version.

Note: Strictly speaking, the component IS present but at a non-vulnerable version. The most accurate VEX justification is "Component not Present" in the sense that the *vulnerable component version* is not present. An alternative justification could be "Vulnerable Code not Present" if the team prefers to distinguish between "package absent" and "package present but at a fixed version."

### 4. Transition to Closed

- Resolution: **Not a Bug**
- Assign to current user

### 5. Add label

Add `ai-cve-triaged` label to TC-8002 to mark it as triaged.

## No Remediation Tasks Needed

Since no supported versions are affected, no remediation tasks are created. This is a clean close -- the vulnerability was already fixed in the dependency before it was incorporated into any shipped product version.
