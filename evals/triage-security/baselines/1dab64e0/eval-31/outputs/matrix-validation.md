# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Source**: local security-matrix.md

### Section Headings

| Required Section | Present? |
|---|---|
| `## Supportability Matrix` | YES |
| `### Source Pinning Method` | YES |
| `## Ecosystem Mappings` | YES |
| `## Forward Pointer` | YES |

### Table Parsability

| Section | Header Row | Separator Row | Data Rows | Parsable? |
|---|---|---|---|---|
| Supportability Matrix | YES | YES | 2 | YES |
| Ecosystem Mappings | YES | YES | 1 | YES |

### Ecosystem Mappings Column Validation

**Result: WARNING -- column name mismatch**

> WARNING: Matrix file `security-matrix.md` (stream 2.2.x) has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual:   `Ecosystem | Repo | Lock File Path | Command | Branch`

**Column diff:**

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

This is a non-auto-repairable warning. The column names do not match the canonical template at `docs/templates/security-matrix.template.md`. While the column count is the same (5), four of five column names differ from the expected names. The skill cannot reliably map columns by name when they deviate from the template.

### Auto-Repairs Applied

None.

### Summary

- Sections: all required sections present (PASS)
- Table parsability: all tables parsable (PASS)
- Ecosystem Mappings columns: column names do not match template (WARNING)

> Matrix validation found issues that cannot be auto-repaired.
>
> 1. Continue with partial data (skip streams with critical warnings)
> 2. Abort triage to fix the matrix files first
>
> Choose (1/2):
