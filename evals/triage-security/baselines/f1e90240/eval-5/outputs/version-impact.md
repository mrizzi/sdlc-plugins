# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact Table

CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4):

### Stream 2.2.x (scoped -- primary analysis)

| Version | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|-------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before fix threshold |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before fix threshold |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fixed version |

### Stream 2.1.x (cross-stream impact)

| Version | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|-------------------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before fix threshold |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before fix threshold |

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in `rpms.lock.yaml` at each pinned tag, confirming
it is an explicitly installed RPM (not inherited from the base image). SBOM cross-validation
via cosign was not performed because cosign is not available in this environment.
Classification relies on rpms.lock.yaml evidence only.

## Fix Status in Scoped Stream

The fix (openssl-libs 3.0.7-28.el9_4) is already present in the 2.2.x stream
starting from version 2.2.3 (build tag v0.4.11). The latest release 2.2.4
(v0.4.12) also ships the fixed version. Versions 2.2.0 through 2.2.2 are
affected and were shipped with vulnerable openssl-libs versions.

## Cross-Stream Summary

- **2.2.x**: partially affected (2.2.0--2.2.2 affected; 2.2.3--2.2.4 fixed)
- **2.1.x**: fully affected (all versions ship vulnerable openssl-libs)
