# Step 2.1.1 — Matrix Format Validation Results

## Template Reference

Canonical template: `docs/templates/security-matrix.template.md`

### Required Section Headings (from template)

| # | Heading | Required |
|---|---------|----------|
| 1 | `## Supportability Matrix` | Yes |
| 2 | `### Source Pinning Method` | Yes |
| 3 | `## Ecosystem Mappings` | Yes |
| 4 | `## Forward Pointer` | Yes |

### Expected Ecosystem Mappings Columns (from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream: 2.2.x

**File:** `security-matrix.md` (rhtpa-release.0.4.z)

### Section Presence Check

| Required Section | Present? | Status |
|------------------|----------|--------|
| `## Supportability Matrix` | Yes | Pass |
| `### Source Pinning Method` | Yes | Pass |
| `## Ecosystem Mappings` | **No** | **CRITICAL WARNING** |
| `## Forward Pointer` | Yes | Pass |

### Table Parsability Check

| Section | Header Row | Separator Row | Data Rows | Status |
|---------|------------|---------------|-----------|--------|
| `## Supportability Matrix` | Yes | Yes | 2 | Pass |
| `## Ecosystem Mappings` | — | — | — | **Skipped (section missing)** |

### Ecosystem Mappings Column Check

Skipped — section is missing entirely.

---

## Warnings

> **WARNING:** Matrix file `security-matrix.md` (stream 2.2.x) is missing required section `## Ecosystem Mappings`. This stream cannot be processed.

The `## Ecosystem Mappings` section is required for version impact analysis (Step 2.3). Without it, the skill cannot determine which lock files to inspect or which check commands to use for dependency version extraction. This stream must be excluded from triage until the section is added.

## Auto-Repairs Applied

None — no auto-repairable issues found. (The `## Forward Pointer` section is present, so no auto-repair is needed.)

## Validation Summary

| Stream | Result | Issues |
|--------|--------|--------|
| 2.2.x | **Warning** | Missing required section: `## Ecosystem Mappings` |

**Overall result: Warnings (non-repairable issues found)**

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):
