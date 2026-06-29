# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Data Source

Versions extracted from `rpms.lock.yaml` at each pinned tag in the Konflux release repo
(`rhtpa-release.0.4.z`), using command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

### Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

### Cross-stream Impact

The 2.1.x stream also ships vulnerable versions of openssl-libs:

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | |
| 2.1.1 | 3.0.7-24.el9 | YES | |

However, this issue is scoped to the 2.2.x stream only. Cross-stream impact
would be reported via comment on the Vulnerability issue for PSIRT awareness.
