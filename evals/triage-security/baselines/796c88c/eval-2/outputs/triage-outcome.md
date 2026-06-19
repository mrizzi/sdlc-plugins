# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

No supported versions ship a vulnerable version of serde_json. All versions across both the 2.1.x and 2.2.x streams include serde_json >= 1.0.137, which is above the fixed version threshold of 1.0.135. The vulnerability was already resolved before any supported release was built.

## Version Impact Evidence

| Version | serde_json | Vulnerable? |
|---------|-----------|-------------|
| 2.1.0 | 1.0.137 | No |
| 2.1.1 | 1.0.137 | No |
| 2.2.0 | 1.0.138 | No |
| 2.2.1 | 1.0.138 | No |
| 2.2.2 | 1.0.138 (retag of 2.2.1) | No |
| 2.2.3 | 1.0.139 | No |
| 2.2.4 | 1.0.139 | No |

## Proposed Jira Mutations

The following mutations are **proposals** and have not been executed:

### 1. Transition Issue to Closed

- **Action**: Transition TC-8002 to **Closed**
- **Resolution**: Not a Bug
- **Reason**: The vulnerable component (serde_json < 1.0.135) is not present in any supported product version. All supported versions ship serde_json >= 1.0.137.

### 2. Add Triage Comment

- **Action**: Add comment to TC-8002
- **Content**:

> **Security Triage -- Not Affected**
>
> CVE-2026-28940 affects serde_json versions < 1.0.135. All supported product versions ship serde_json >= 1.0.137, which includes the fix.
>
> **Version impact analysis:**
> - 2.1.0 (v0.3.8): serde_json 1.0.137 -- not affected
> - 2.1.1 (v0.3.12): serde_json 1.0.137 -- not affected
> - 2.2.0 (v0.4.5): serde_json 1.0.138 -- not affected
> - 2.2.1 (v0.4.8): serde_json 1.0.138 -- not affected
> - 2.2.2 (v0.4.8, retag of 2.2.1): serde_json 1.0.138 -- not affected
> - 2.2.3 (v0.4.11): serde_json 1.0.139 -- not affected
> - 2.2.4 (v0.4.12): serde_json 1.0.139 -- not affected
>
> Closing as Not a Bug. No remediation required.

### 3. Set VEX Justification

- **Action**: Set custom field `customfield_12345` (VEX Justification)
- **Value**: "Component not Present"
- **Reason**: The vulnerable version of serde_json (< 1.0.135) is not present in any supported product version.

### 4. No Remediation Tasks

Per Case C procedure, no remediation tasks are created since no supported versions are affected.
