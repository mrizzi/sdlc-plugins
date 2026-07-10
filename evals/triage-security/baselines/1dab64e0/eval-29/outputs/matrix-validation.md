# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Date**: 2026-07-10

## Template Reference

Required section headings extracted from the canonical template:

1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

Required Ecosystem Mappings columns (from template):

`| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |`

Note: `## Version Stream` is informational and not enforced per Step 2.1.1.
Note: Supportability Matrix columns are product-specific and vary across deployments — only table parsability is validated, not column names.

---

## Stream 1: rhtpa-release.0.3.z (2.1.x stream)

**Source**: `security-matrix-mock.md` (Stream 1 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings Column Structure

- **Expected**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — column names and order match the template exactly.

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 2 rows (2.1.0, 2.1.1) | PASS |
| Ecosystem Mappings | Yes | Yes | 2 rows (Cargo, RPM) | PASS |

### Auto-Repairs Applied

None required.

### Warnings

None.

### Stream 1 Overall Result: PASS

No issues found. Proceed without user interruption.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x stream)

**Source**: `security-matrix-mock.md` (Stream 2 section)

### 1. Required Sections Present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings Column Structure

- **Expected**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — column names and order match the template exactly.

### 3. Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes (`Version \| Build \| Build Date \| backend \| Notes`) | Yes | 5 rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | PASS |
| Ecosystem Mappings | Yes | Yes | 2 rows (Cargo, RPM) | PASS |

### Auto-Repairs Applied

None required.

### Warnings

None.

### Stream 2 Overall Result: PASS

No issues found. Proceed without user interruption.

---

## Validation Summary

| Stream | Matrix File | Sections | Columns | Parsability | Auto-Repairs | Warnings | Overall |
|---|---|---|---|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | security-matrix-mock.md | 4/4 PASS | PASS | PASS | None | None | PASS |
| 2.2.x (rhtpa-release.0.4.z) | security-matrix-mock.md | 4/4 PASS | PASS | PASS | None | None | PASS |

**Overall validation result**: PASS — all matrix files conform to the canonical template. Both streams are valid and ready for version impact analysis aggregation. No auto-repairs were needed and no warnings were raised. Proceeding silently per Step 2.1.1 rules.
