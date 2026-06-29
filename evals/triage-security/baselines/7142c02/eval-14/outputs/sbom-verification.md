# Step 2.3.5 -- SBOM Verification and Dependency Chain

## Tool Availability

cosign is available at `/usr/bin/cosign`.

## SBOM Verification Method

For each affected version (2.2.0 through 2.2.2), two signals were compared:

1. **rpms.lock.yaml** -- checked via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
2. **SBOM comparison** -- final image SBOM vs base image SBOM via `cosign download sbom`

## SBOM Verification Results

| Version | Tag | openssl-libs in rpms.lock.yaml | rpms.lock.yaml classification | openssl-libs in final SBOM | openssl-libs in base SBOM | SBOM classification | Agreement? |
|---------|-----|-------------------------------|------------------------------|---------------------------|--------------------------|---------------------|------------|
| 2.2.0 | v0.4.5 | YES (3.0.7-25.el9_3) | explicit install | YES | YES | base image | NO -- DISCREPANCY |
| 2.2.1 | v0.4.8 | YES (3.0.7-27.el9_4) | explicit install | YES | YES | base image | NO -- DISCREPANCY |
| 2.2.2 | v0.4.9 | YES (3.0.7-27.el9_4) | explicit install (same as 2.2.1) | YES | YES | base image | NO -- DISCREPANCY |

## Discrepancy Analysis

For all affected versions (2.2.0, 2.2.1, 2.2.2), the two classification signals **disagree**:

- **rpms.lock.yaml says**: openssl-libs IS listed in the lock file --> **explicit install**
- **SBOM comparison says**: openssl-libs appears in BOTH the final image SBOM AND the base image SBOM --> **base image origin**

WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

This discrepancy likely means the package is present in the base image AND is also explicitly pinned/reinstalled via rpms.lock.yaml. The package may be overlaid on top of the base image version, or the lock file may be pinning the same package that the base image already provides.

## Classification Decision

Per the skill specification, **rpms.lock.yaml remains the primary signal**. SBOM verification supplements but does not override the lock file classification.

**Final classification: explicit install** (based on rpms.lock.yaml as primary signal, with SBOM discrepancy flagged for manual investigation).

## Dependency Chain Output

```
Dependency chain for openssl-libs (RPM):

Version 2.2.0 (v0.4.5):
  rpms.lock.yaml: present (3.0.7-25.el9_3) --> explicit install
  SBOM verification: present in both final and base image SBOMs --> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Primary classification (rpms.lock.yaml): explicit install
  Affected: YES (3.0.7-25.el9_3 < 3.0.7-28.el9_4)

Version 2.2.1 (v0.4.8):
  rpms.lock.yaml: present (3.0.7-27.el9_4) --> explicit install
  SBOM verification: present in both final and base image SBOMs --> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Primary classification (rpms.lock.yaml): explicit install
  Affected: YES (3.0.7-27.el9_4 < 3.0.7-28.el9_4)

Version 2.2.2 (v0.4.9, retag of 2.2.1):
  rpms.lock.yaml: present (3.0.7-27.el9_4) --> explicit install (same as 2.2.1)
  SBOM verification: present in both final and base image SBOMs --> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Primary classification (rpms.lock.yaml): explicit install
  Affected: YES (3.0.7-27.el9_4 < 3.0.7-28.el9_4)

Version 2.2.3 (v0.4.11):
  rpms.lock.yaml: present (3.0.7-28.el9_4) --> explicit install
  Not affected (at fix threshold). SBOM verification not required for unaffected versions.

Version 2.2.4 (v0.4.12):
  rpms.lock.yaml: present (3.0.7-28.el9_4) --> explicit install
  Not affected (at fix threshold). SBOM verification not required for unaffected versions.
```

## Remediation Implication

Since rpms.lock.yaml classification (primary signal) indicates **explicit install**, the remediation path is:

- Update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml in the Konflux release repo to version 3.0.7-28.el9_4 or later.
- This is a single-task remediation (RPM ecosystem, no upstream backport needed).
- The SBOM discrepancy should be investigated to determine whether the explicit pin in rpms.lock.yaml is intentional or redundant with the base image package.
