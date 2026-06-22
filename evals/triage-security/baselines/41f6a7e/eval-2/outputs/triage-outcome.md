# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision

**Not Affected** -- all shipped versions already include the fix.

## Rationale

CVE-2026-28940 affects serde_json versions prior to 1.0.135. Analysis of the Cargo.lock files across all supported version streams shows that every shipped RHTPA release includes serde_json >= 1.0.137, which is above the fixed version threshold. The fix (a configurable recursion limit for JSON deserialization) was incorporated upstream before any RHTPA version was released.

Specifically:
- **Stream 2.1.x**: Both versions (2.1.0 and 2.1.1) ship serde_json 1.0.137
- **Stream 2.2.x**: All five versions (2.2.0 through 2.2.4) ship serde_json 1.0.138 or 1.0.139

No version in any stream ships a vulnerable serde_json version. The product was never exposed to this vulnerability.

## VEX Justification

**fixed_already** -- The vulnerable component was updated to the fixed version before any affected product version was released.

## Proposed Jira Actions

### 1. Update Issue Status

Transition TC-8002 from **New** to **Closed** (or the equivalent terminal status in the workflow, e.g., "Won't Fix" / "Not a Bug" / "Closed - Not Affected").

### 2. Set VEX Justification

Set custom field `customfield_12345` (VEX Justification) to: **fixed_already**

### 3. Add Triage Comment

Add the following comment to TC-8002:

> **Security Triage Result: Not Affected**
>
> CVE-2026-28940 affects serde_json versions before 1.0.135. Analysis of Cargo.lock across all supported version streams confirms that no shipped RHTPA version contains a vulnerable serde_json version:
>
> - Stream 2.1.x (2.1.0, 2.1.1): serde_json 1.0.137
> - Stream 2.2.x (2.2.0 through 2.2.4): serde_json 1.0.138 - 1.0.139
>
> All versions ship serde_json >= 1.0.135 (the fix version). The vulnerability was patched upstream before any RHTPA release.
>
> **VEX Justification**: fixed_already
> **Resolution**: Closing as Not Affected.

### 4. Remove Affects Versions

Clear the "Affects Versions" field (currently set to "RHTPA 2.2.0") since no version is actually affected.

### 5. Resolution Summary

| Action | Field / Transition | Value |
|--------|--------------------|-------|
| Transition | Status | Closed (Not Affected) |
| Set | VEX Justification (customfield_12345) | fixed_already |
| Clear | Affects Versions | (remove RHTPA 2.2.0) |
| Add | Comment | Triage analysis with version-by-version evidence |
