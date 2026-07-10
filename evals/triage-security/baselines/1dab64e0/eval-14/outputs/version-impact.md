# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream rhtpa-release.0.4.z (2.2.x)
Last-Updated: 2026-06-28T10:00:00Z (12 days ago -- within 14-day threshold)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Ecosystem Mappings (2.2.x stream)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

CVE-2026-40215 affects openssl-libs versions before **3.0.7-28.el9_4**.
Fixed version: **3.0.7-28.el9_4**.

### rpms.lock.yaml inspection results

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** -- before 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** -- before 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ | **YES** -- same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** -- matches fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** -- matches fixed version |

## 2.3.5 -- Dependency Chain Context

### Dependency chain for openssl-libs (RPM):

**Version 2.2.0 (v0.4.5) -- openssl-libs 3.0.7-25.el9_3:**

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
    Lock file classification: explicit install (present in rpms.lock.yaml)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install
    SBOM comparison says: base image
    Investigate manually.

  Origin: CONFLICTING -- rpms.lock.yaml lists openssl-libs (explicit install),
    but SBOM comparison shows package in both final and base image SBOMs (base image origin).
```

**Version 2.2.1 (v0.4.8) -- openssl-libs 3.0.7-27.el9_4:**

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
    Lock file classification: explicit install (present in rpms.lock.yaml)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install
    SBOM comparison says: base image
    Investigate manually.

  Origin: CONFLICTING -- rpms.lock.yaml lists openssl-libs (explicit install),
    but SBOM comparison shows package in both final and base image SBOMs (base image origin).
```

**Version 2.2.2 (v0.4.9) -- retag of 2.2.1:**

```
Dependency chain for openssl-libs (RPM):
  Retag of v0.4.8 -- same as 2.2.1

  rpms.lock.yaml: present --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
    Lock file classification: explicit install (present in rpms.lock.yaml)

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install
    SBOM comparison says: base image
    Investigate manually.

  Origin: CONFLICTING -- same disagreement as 2.2.1 (retag).
```

**Versions 2.2.3 and 2.2.4 -- NOT AFFECTED (openssl-libs 3.0.7-28.el9_4 matches fixed version). No dependency chain trace needed.**

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | fixed version |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### SBOM Verification Summary

cosign is available at `/usr/bin/cosign`. SBOM verification was performed for all
affected versions.

For versions 2.2.0 through 2.2.2, there is a classification disagreement:

| Version | rpms.lock.yaml | SBOM (final vs base) | Agreement? |
|---------|----------------|----------------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (present in both SBOMs) | **DISAGREE** |
| 2.2.1 | explicit install (present in lock file) | base image (present in both SBOMs) | **DISAGREE** |
| 2.2.2 | explicit install (retag of 2.2.1) | base image (retag of 2.2.1) | **DISAGREE** |

The rpms.lock.yaml lists openssl-libs as an explicitly installed package, but the
SBOM comparison shows the package present in both the final image SBOM and the base
image SBOM, indicating base image origin. This disagreement should be investigated
manually to determine the correct remediation path (base image update vs. lock file
update).

## 2.5 -- Cross-Stream Impact (informational)

Since the issue is scoped to the 2.2.x stream via `[rhtpa-2.2]`, triage actions
(Affects Versions, remediation) are scoped to 2.2.x only. However, version impact
analysis across all configured streams shows:

| Stream | Version | openssl-libs | Affected? |
|--------|---------|-------------|-----------|
| 2.1.x | 2.1.0 | 3.0.7-24.el9 | **YES** |
| 2.1.x | 2.1.1 | 3.0.7-24.el9 | **YES** |
| 2.2.x | 2.2.0 | 3.0.7-25.el9_3 | **YES** |
| 2.2.x | 2.2.1 | 3.0.7-27.el9_4 | **YES** |
| 2.2.x | 2.2.2 | -- (retag) | **YES** |
| 2.2.x | 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.x | 2.2.4 | 3.0.7-28.el9_4 | NO |

The 2.1.x stream is also affected. Per Case B (cross-stream impact), a comment
would be posted to TC-8005 noting that stream 2.1.x is also affected, and
proactive remediation tasks would be evaluated for that stream.
