# Step 2 -- Version Impact Analysis

## PROPOSAL: Version Impact Table for CVE-2026-40215

Scope: 2.2.x stream only (per issue stream suffix `[rhtpa-2.2]`).

Dependency versions extracted from `rpms.lock.yaml` at each pinned tag in the supportability matrix. Fix threshold: openssl-libs >= 3.0.7-28.el9_4.

| Version | Build | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|-----|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs. Versions 2.2.3 and 2.2.4 already include the fixed version (3.0.7-28.el9_4). The fix was picked up in build 0.4.11 (version 2.2.3, released 2026-03-23).

## Cross-Stream Observation

Although triage is scoped to the 2.2.x stream, the security matrix also shows the 2.1.x stream (rhtpa-release.0.3.z). Both 2.1.x versions (2.1.0 at 3.0.7-24.el9, 2.1.1 at 3.0.7-24.el9) ship a vulnerable openssl-libs. This would be reported as a cross-stream impact comment (Case B) on TC-8005 if a companion CVE Jira does not already exist for the 2.1.x stream.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation path: update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4. Note: versions 2.2.3+ already have this version pinned.
```

The package `openssl-libs` is present in `rpms.lock.yaml` at each inspected tag, confirming it is an explicitly installed RPM (not inherited from the base image). SBOM cross-verification via `cosign` was not performed because `cosign` is not available in this environment. The rpms.lock.yaml classification is used as the sole source of truth.

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (the Upstream Branch column is `--` in the Ecosystem Mappings table). Upstream fix status check is not applicable for system packages -- the fix is tracked via the Red Hat advisory (RHSA-2026:4021) and the updated RPM version in rpms.lock.yaml.
