# Triage Outcome: TC-8002

## Decision: Close as "Not a Bug"

**Rationale:** CVE-2026-28940 affects serde_json versions before 1.0.135. Every supported version of RHTPA across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.137, which already includes the fix. No supported version has ever been affected by this vulnerability. This falls under Step 7 Case C: no supported versions are impacted.

## Proposed Jira Mutations

The following actions are **proposals** and have not been executed.

### 1. Transition TC-8002 to "Closed" with resolution "Not a Bug"

- **Field:** Status
- **Current value:** New
- **Proposed value:** Closed
- **Resolution:** Not a Bug

### 2. Set VEX Justification

- **Field:** customfield_12345 (VEX Justification)
- **Proposed value:** Component not Present
- **Rationale:** The vulnerable version of serde_json (< 1.0.135) was never present in any shipped build. All builds contain serde_json >= 1.0.137, which already incorporates the fix for CVE-2026-28940.

### 3. Add closing comment with version impact evidence

**Proposed comment body:**

> **Triage result: Not affected -- closing as Not a Bug.**
>
> CVE-2026-28940 affects serde_json versions prior to 1.0.135. Analysis of lock file data across all supported streams confirms that no shipped version contains a vulnerable copy of serde_json.
>
> **Version impact evidence:**
>
> *Stream: 2.1.x (rhtpa-release.0.3.z)*
> | Version | Build Tag | serde_json | Status |
> |---------|-----------|------------|--------|
> | 2.1.0   | v0.3.8    | 1.0.137    | Not affected |
> | 2.1.1   | v0.3.12   | 1.0.137    | Not affected |
>
> *Stream: 2.2.x (rhtpa-release.0.4.z)*
> | Version | Build Tag | serde_json | Status |
> |---------|-----------|------------|--------|
> | 2.2.0   | v0.4.5    | 1.0.138    | Not affected |
> | 2.2.1   | v0.4.8    | 1.0.138    | Not affected |
> | 2.2.2   | v0.4.9    | 1.0.138    | Not affected (retag of v0.4.8) |
> | 2.2.3   | v0.4.11   | 1.0.139    | Not affected |
> | 2.2.4   | v0.4.12   | 1.0.139    | Not affected |
>
> The lowest serde_json version across all builds is 1.0.137, which is above the fix threshold of 1.0.135. The vulnerable component was never present in any shipped release.
>
> Setting VEX Justification to "Component not Present".

## Actions NOT Taken (and why)

- **No upstream backport task created:** No fix is needed because all versions already ship the patched dependency.
- **No downstream propagation task created:** No remediation is required in any stream.
- **No Affects Version changes:** The issue is being closed outright; adjusting Affects Versions is unnecessary.

## Summary

| Aspect | Detail |
|--------|--------|
| CVE | CVE-2026-28940 |
| Package | serde_json |
| Vulnerable range | < 1.0.135 |
| Lowest version in any build | 1.0.137 |
| Streams checked | 2.1.x, 2.2.x |
| Total versions checked | 7 |
| Versions affected | 0 |
| Triage decision | Close as Not a Bug |
| VEX Justification | Component not Present |
| Remediation tasks | None required |
