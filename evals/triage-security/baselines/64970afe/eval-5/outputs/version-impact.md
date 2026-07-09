# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### 2.2.x Stream (issue scope)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|-------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 0.4.9 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### 2.1.x Stream (cross-stream check)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|-------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | 0.3.12 | v0.3.12 | 3.0.7-24.el9 | YES | |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4).
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected. This stream is outside the issue's scope but is noted for cross-stream impact (Case B).

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification: skipped -- cosign not available in this environment
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in `rpms.lock.yaml` for the 2.2.x stream, confirming it is an explicitly installed package (not inherited from the base image). SBOM cross-validation via cosign was not performed because cosign is not available in this environment. The rpms.lock.yaml classification is used as the sole basis for the package origin determination.

## Upstream Fix Status

No upstream branch is configured for the RPM ecosystem in the Ecosystem Mappings table (Upstream Branch column is `--`). Upstream fix status check is not applicable for system packages -- the fix is delivered via RPM package updates from the distribution vendor (Red Hat).

The fix is available as RHSA-2026:4021 (openssl-libs-3.0.7-28.el9_4), and has already been picked up in builds v0.4.11 and v0.4.12 (versions 2.2.3 and 2.2.4).
