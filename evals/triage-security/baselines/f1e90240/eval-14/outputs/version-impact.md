# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from: rhtpa-release.0.4.z security-matrix.md (Last-Updated: 2026-06-28T10:00:00Z -- 24 days ago, within 14-day threshold).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Extracted openssl-libs versions from rpms.lock.yaml at each pinned tag:

| Tag | openssl-libs version | Comparison to fix (3.0.7-28.el9_4) |
|-----|----------------------|------------------------------------|
| `v0.4.5` | 3.0.7-25.el9_3 | BELOW fix threshold |
| `v0.4.8` | 3.0.7-27.el9_4 | BELOW fix threshold |
| `v0.4.9` | _(retag of v0.4.8)_ | same as v0.4.8 |
| `v0.4.11` | 3.0.7-28.el9_4 | AT fix threshold (fixed) |
| `v0.4.12` | 3.0.7-28.el9_4 | AT fix threshold (fixed) |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fix threshold |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fix threshold |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### Cross-stream impact (out of scope for this issue)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in versions 2.1.0 and 2.1.1, both below fix threshold). This will be reported via Case B cross-stream impact notice.

## 2.3.5 -- Dependency Chain and SBOM Verification

### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml:
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml indicates explicit install but SBOM
    indicates base image origin. Manual investigation required to determine
    whether openssl-libs is intentionally pinned in rpms.lock.yaml or
    inherited from the base image and redundantly listed.
```

### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml:
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    Investigate manually.
  Origin: CONFLICTING -- rpms.lock.yaml indicates explicit install but SBOM
    indicates base image origin. Manual investigation required to determine
    whether openssl-libs is intentionally pinned in rpms.lock.yaml or
    inherited from the base image and redundantly listed.
```

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1)
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image (same as 2.2.1)
  WARNING: SBOM classification DISAGREES with rpms.lock.yaml:
    rpms.lock.yaml says: explicit install (package is listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    Investigate manually.
  Origin: CONFLICTING -- same as 2.2.1 (retag)
```

### Versions 2.2.3 and 2.2.4

Not affected (openssl-libs 3.0.7-28.el9_4 is at the fix threshold). Dependency chain analysis is not required for non-affected versions.

### SBOM Disagreement Summary

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the SBOM classification disagrees with the rpms.lock.yaml classification:

| Version | rpms.lock.yaml | SBOM (final vs base) | Agreement? |
|---------|---------------|----------------------|------------|
| 2.2.0 | present (explicit install) | in both SBOMs (base image) | DISAGREE |
| 2.2.1 | present (explicit install) | in both SBOMs (base image) | DISAGREE |
| 2.2.2 | present (explicit install) | in both SBOMs (base image) | DISAGREE |

This discrepancy suggests that openssl-libs may be both present in the base image AND explicitly listed in rpms.lock.yaml (possibly as an override or version pin). The engineer should investigate whether the rpms.lock.yaml entry is intentional (to pin a specific version of an otherwise base-image-provided package) or redundant.

Remediation path depends on resolution of the discrepancy:
- If the lock file entry is an intentional pin: update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4 (explicit install remediation path).
- If the lock file entry is redundant and the package comes from the base image: update the base image reference to a version that ships the patched openssl-libs, and optionally remove the redundant lock file entry.
