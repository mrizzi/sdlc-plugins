# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 (CVE-2026-31812 quinn-proto)
**Validated against**: `docs/templates/security-matrix.template.md`

## Template Reference

Required section headings extracted from the canonical template:
- `## Supportability Matrix`
- `### Source Pinning Method`
- `## Ecosystem Mappings`
- `## Forward Pointer`

Note: `## Version Stream` is informational and not enforced.

Required Ecosystem Mappings columns (in order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

---

## Stream 1: rhtpa-release.0.3.z (2.1.x)

**Source**: security-matrix-mock.md (Stream 1 section)

### 1. Required sections present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings column structure

Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **PASS** — columns match the template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 2 rows (2.1.0, 2.1.1) | PASS |
| Ecosystem Mappings | Yes | Yes | 2 rows (Cargo, RPM) | PASS |

Note: Supportability Matrix columns (`Version | Build | Build Date | backend | Notes`) differ from the template (`RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes`). Per the validation spec, Supportability Matrix columns are product-specific and vary across deployments — only parsability is validated, not column names. **No warning issued.**

### Stream 1 overall: PASS

No issues found. No auto-repairs needed.

---

## Stream 2: rhtpa-release.0.4.z (2.2.x)

**Source**: security-matrix-mock.md (Stream 2 section)

### 1. Required sections present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `## Forward Pointer` | Yes | PASS |

### 2. Ecosystem Mappings column structure

Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Result: **PASS** — columns match the template in name and order.

### 3. Table parsability

| Table | Header Row | Separator Row | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | Yes | Yes | 5 rows (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | PASS |
| Ecosystem Mappings | Yes | Yes | 2 rows (Cargo, RPM) | PASS |

Note: Supportability Matrix columns (`Version | Build | Build Date | backend | Notes`) differ from the template — product-specific columns, parsability validated only. **No warning issued.**

### Stream 2 overall: PASS

No issues found. No auto-repairs needed.

---

## Validation Summary

| Stream | Sections | Columns | Parsability | Auto-repairs | Warnings | Result |
|---|---|---|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | 4/4 | Match | All tables valid | None | None | PASS |
| 2.2.x (rhtpa-release.0.4.z) | 4/4 | Match | All tables valid | None | None | PASS |

**Overall result: PASS** — both matrix files pass validation with no issues. Proceeding silently (no user interruption required per the validation protocol).
