# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

Data source: `rpms.lock.yaml` at each pinned tag in the 2.2.x supportability matrix.

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Summary

- **Affected**: 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1)
- **Not affected**: 2.2.3, 2.2.4
- Versions 2.2.0 through 2.2.2 ship openssl-libs versions older than the fix threshold (3.0.7-28.el9_4).
- Versions 2.2.3 and 2.2.4 ship the patched version 3.0.7-28.el9_4.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: skipped -- cosign not available in eval environment
  Origin: explicit install (openssl-libs is listed in rpms.lock.yaml)

  Remediation: update openssl-libs version spec in rpms.in.yaml / regenerate rpms.lock.yaml.
```

openssl-libs is classified as an **explicit install** because it is present in `rpms.lock.yaml`. It is not inherited solely from the base image -- it is explicitly pinned in the RPM lock file. Remediation involves updating the package specification and regenerating the lock file.

## Cross-Stream Impact

The 2.1.x stream also ships vulnerable openssl-libs versions:

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

However, this issue is scoped to 2.2.x. Cross-stream impact for 2.1.x would be handled via Case B (cross-stream impact comment) or through the 2.1.x stream's own CVE Jira.
