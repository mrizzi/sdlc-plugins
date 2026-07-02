# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | before fix threshold |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | before fix threshold |
| 2.2.2 | 0.4.9 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fix threshold |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fix threshold |

Fix threshold: **3.0.7-28.el9_4** (from Jira description, cross-validated with advisory RHSA-2026:4021).

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs. Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4). The vulnerability was remediated starting with build 0.4.11 (version 2.2.3).

## Cross-stream Impact

The 2.1.x stream (rhtpa-release.0.3.z) is also affected:

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before fix threshold |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before fix threshold |

All versions in the 2.1.x stream ship a vulnerable openssl-libs. This cross-stream impact is noted for Case B handling in Step 8 but is outside the scope of this issue's triage (scoped to 2.2.x only).

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT (3.0.7-27.el9_4 at v0.4.8) -> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4 and regenerate the lock file.
```

openssl-libs is present in `rpms.lock.yaml` across all tags in both streams, confirming it is an **explicitly installed** RPM package (not inherited from the base image). The remediation path is to update the package specification in the Konflux release repo.

SBOM verification via cosign was not performed because the `cosign` CLI tool is not available in this environment. The rpms.lock.yaml classification alone is used to determine the package origin.

## Upstream Fix Status

RPM ecosystem does not have an Upstream Branch configured in the Ecosystem Mappings table (Upstream Branch column is empty). Upstream fix status check is not applicable -- the fix comes from Red Hat's RPM repositories via RHSA-2026:4021, not from an upstream source branch. The advisory confirms the fix is available in openssl-libs 3.0.7-28.el9_4.
