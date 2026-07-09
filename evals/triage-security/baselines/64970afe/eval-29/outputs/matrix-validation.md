# Step 2.1.1 — Matrix Format Validation Results

Canonical template: `docs/templates/security-matrix.template.md`

## Template Reference

**Required section headings** (extracted from template):
1. `## Supportability Matrix`
2. `### Source Pinning Method`
3. `## Ecosystem Mappings`
4. `## Forward Pointer`

**Ecosystem Mappings expected columns** (from template):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

**Source**: `/home/dev/repos/rhtpa-release.0.3.z/security-matrix.md`

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | PASS — present |
| `### Source Pinning Method` | PASS — present |
| `## Ecosystem Mappings` | PASS — present |
| `## Forward Pointer` | PASS — present |

### Table Column Structure (Ecosystem Mappings)

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — columns match template in name and order

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | `Version | Build | Build Date | backend | Notes` | Present (`---`) | 2 rows | PASS |
| Ecosystem Mappings | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` | Present (`---`) | 2 rows | PASS |

Note: Supportability Matrix column names (`Version`, `backend`) differ from the template placeholders (`RHTPA Version`, `trustify`, `trustify-ui`). This is expected — per the validation spec, Supportability Matrix columns are product-specific and vary across deployments. Only parsability is validated, not column name matching.

### Auto-Repairs

None required.

### Stream 1 Verdict: PASS

---

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

**Source**: `/home/dev/repos/rhtpa-release.0.4.z/security-matrix.md`

### Required Sections

| Section | Status |
|---------|--------|
| `## Supportability Matrix` | PASS — present |
| `### Source Pinning Method` | PASS — present |
| `## Ecosystem Mappings` | PASS — present |
| `## Forward Pointer` | PASS — present |

### Table Column Structure (Ecosystem Mappings)

- **Expected columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Actual columns**: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- **Result**: PASS — columns match template in name and order

### Table Parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|-------|------------|---------------|-----------|--------|
| Supportability Matrix | `Version | Build | Build Date | backend | Notes` | Present (`---`) | 5 rows | PASS |
| Ecosystem Mappings | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` | Present (`---`) | 2 rows | PASS |

Note: Supportability Matrix column names are product-specific (same as Stream 1). Parsability validated only.

### Auto-Repairs

None required.

### Stream 2 Verdict: PASS

---

## Overall Validation Summary

| Stream | File | Sections | Columns | Parsability | Auto-Repairs | Verdict |
|--------|------|----------|---------|-------------|--------------|---------|
| 2.1.x | rhtpa-release.0.3.z | 4/4 PASS | PASS | PASS | None | PASS |
| 2.2.x | rhtpa-release.0.4.z | 4/4 PASS | PASS | PASS | None | PASS |

**Overall result**: PASS — no issues found. Both matrix files conform to the canonical template structure. Proceeding silently (no user interruption required per Step 2.1.1 spec).
