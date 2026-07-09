# Step 2.1.1 — Matrix Format Validation Results

## Stream: 2.2.x (rhtpa-release.0.4.z)

**Matrix file**: `security-matrix-wrong-columns-mock.md`
**Template**: `docs/templates/security-matrix.template.md`

### Section Headings

| Required Section | Present? | Status |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### Table Parsability

| Section | Header Row | Separator Row | Data Rows | Status |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 | PASS |
| Ecosystem Mappings | Yes | Yes | 1 | PASS |

### Ecosystem Mappings Column Validation

**Status: WARNING — column mismatch detected**

Expected (from template):

```
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
```

Actual (from matrix file):

```
| Ecosystem | Repo | Lock File Path | Command | Branch |
```

Diff:

| Position | Expected | Actual | Match? |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | YES |
| 2 | Repository | Repo | NO |
| 3 | Lock File | Lock File Path | NO |
| 4 | Check Command | Command | NO |
| 5 | Upstream Branch | Branch | NO |

> WARNING: Matrix file `security-matrix-wrong-columns-mock.md` has unexpected Ecosystem Mappings columns.
> Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
> Actual: `Ecosystem | Repo | Lock File Path | Command | Branch`

### Summary

Matrix validation found issues that cannot be auto-repaired.

1. Continue with partial data (skip streams with critical warnings)
2. Abort triage to fix the matrix files first

Choose (1/2):
