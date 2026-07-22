# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Stream**: 2.2.x (rhtpa-release.0.4.z)
**Matrix file**: security-matrix.md (Stream 1: rhtpa-release.0.4.z)
**Template**: docs/templates/security-matrix.template.md

---

## Section Headings Check

| Required Section | Present? | Status |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

## Table Parsability Check

| Table | Header Row | Separator Row | Data Rows | Status |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 rows | PASS |
| Ecosystem Mappings | Yes | Yes | 1 row | PASS |

## Ecosystem Mappings Column Validation

**Result: WARNING — column mismatch detected**

> :warning: Matrix file `security-matrix.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Column Diff

| Position | Expected (template) | Actual (matrix) | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

4 of 5 columns have mismatched names. The column count is the same (5), but the column names differ from the canonical template.

## Auto-Repairs Applied

None. Column name mismatches cannot be auto-repaired — they require user decision.

## Summary

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

The Ecosystem Mappings column names do not match the canonical template defined in `docs/templates/security-matrix.template.md`. While the table is structurally parsable, the column name mismatches may cause downstream processing errors if column names are used for programmatic lookups. The matrix file should be updated to use the canonical column names: `Repository`, `Lock File`, `Check Command`, and `Upstream Branch`.
