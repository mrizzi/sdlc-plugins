# Step 2.1.1 — Matrix Format Validation Results

## Template Reference

Canonical template: `docs/templates/security-matrix.template.md`

### Required Section Headings (extracted from template)

| # | Heading | Level | Required |
|---|---------|-------|----------|
| 1 | `## Supportability Matrix` | H2 | Yes |
| 2 | `### Source Pinning Method` | H3 | Yes |
| 3 | `## Ecosystem Mappings` | H2 | Yes |
| 4 | `## Forward Pointer` | H2 | Yes |

Note: `## Version Stream` is informational and not enforced.

### Ecosystem Mappings Expected Columns (from template)

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Matrix file**: `security-matrix-missing-section-mock.md`

### Section Presence Check

| Required Section | Present | Status |
|------------------|---------|--------|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | **No** | FAIL -- critical section missing |
| `## Forward Pointer` | Yes | PASS |

### Table Parsability Check

| Section | Header Row | Separator Row | Data Rows | Status |
|---------|-----------|---------------|-----------|--------|
| Supportability Matrix | Yes | Yes | 2 | PASS |
| Ecosystem Mappings | N/A | N/A | N/A | SKIP -- section missing |

### Ecosystem Mappings Column Check

Skipped -- section not present.

### Auto-Repairs Applied

None. No auto-repairable issues detected (Forward Pointer section is present).

---

## Validation Summary

| Stream | Result | Issues |
|--------|--------|--------|
| 2.2.x | **WARNING** | Missing required section: `## Ecosystem Mappings` |

### Warnings (non-repairable)

> **Warning:** Matrix file `security-matrix-missing-section-mock.md` is missing required section `## Ecosystem Mappings`.
> This stream cannot be processed.

Without the Ecosystem Mappings section, the skill cannot determine which lock files to inspect or which check commands to use for dependency version extraction (Step 2.3). Version impact analysis cannot proceed for this stream.

### User Decision Required

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
