# Impact Map: TC-9003 — SBOM Comparison View

## Workflow Mode

**Mode**: `feature-branch`

**Rationale**: The frontend comparison page depends on a new backend endpoint (`GET /api/v2/sbom/compare`) that does not exist yet. Without the backend, the frontend comparison page is non-functional — this is tight coupling. Both repositories must be coordinated under a single feature branch to ensure atomicity.

**Feature branch name**: `TC-9003`

## trustify-backend

### New Files

| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | `SbomComparison` response struct and diff sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) |
| `modules/fundamental/src/sbom/service/compare.rs` | Comparison logic: load two SBOMs' packages and advisories, compute structured diff |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | `GET /api/v2/sbom/compare?left={id1}&right={id2}` handler |
| `tests/api/sbom_compare.rs` | Integration tests for the comparison endpoint |

### Modified Files

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod comparison;` |
| `modules/fundamental/src/sbom/service/mod.rs` | Add `pub mod compare;` |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register comparison route |
| `tests/api/mod.rs` (or test entry point) | Include `sbom_compare` test module |

## trustify-ui

### New Files

| File | Purpose |
|---|---|
| `src/hooks/useSbomComparison.ts` | React Query hook for `GET /api/v2/sbom/compare` |
| `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` | Comparison page with SBOM selectors, diff sections, export dropdown |
| `src/pages/SbomComparisonPage/components/DiffSection.tsx` | Reusable ExpandableSection wrapper for each diff category |
| `src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` | Unit tests for comparison page |
| `tests/mocks/fixtures/sbom-comparison.json` | Mock comparison response data |

### Modified Files

| File | Change |
|---|---|
| `src/api/models.ts` | Add TypeScript interfaces for comparison response types |
| `src/api/rest.ts` | Add `fetchSbomComparison()` client function |
| `src/routes.tsx` | Add `/sbom/compare` route |
| `tests/mocks/handlers.ts` | Add MSW handler for comparison endpoint |

## Task Summary

| Task | Repository | Summary |
|---|---|---|
| 1 | trustify-backend | Bookend: create feature branch `TC-9003` |
| 2 | trustify-backend | SBOM comparison model and diff service |
| 3 | trustify-backend | Comparison REST endpoint and integration tests |
| 4 | trustify-ui | API types, client function, and React Query hook |
| 5 | trustify-ui | Comparison page UI with Figma design mapping |
| 6 | trustify-ui | Comparison page tests and MSW mocks |
| 7 | trustify-ui | Bookend: merge feature branch `TC-9003` |
