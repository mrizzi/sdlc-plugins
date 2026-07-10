# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### 2.2.x Stream (issue scope)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### 2.1.x Stream (cross-stream assessment)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (versions listed per tag) --> explicit install
  SBOM verification: skipped -- cosign not available in this environment
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

Note: SBOM comparison via cosign was not performed because cosign is not
available in this eval environment. The rpms.lock.yaml classification
(explicit install) is used as the sole classification source.

## Summary

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship
openssl-libs versions prior to the fix threshold (3.0.7-28.el9_4) and
are affected. Versions 2.2.3 and 2.2.4 ship the fixed version and are
not affected.

The 2.1.x stream is also fully affected (all versions ship
openssl-libs 3.0.7-24.el9). This cross-stream impact is handled
in Step 8 Case B.
