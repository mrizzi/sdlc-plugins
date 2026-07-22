# Impact Map: TC-9003 SBOM Comparison View

## Workflow Mode

Feature-branch (`TC-9003`). Backend and frontend changes are tightly coupled -- the new comparison UI page requires the new backend diffing endpoint. Bookend tasks (1 and 9) target `main`; all intermediate tasks target `TC-9003`.

## Task Dependency Graph

```
Task 1 (create feature branch)
  |
  +-- Task 2 (comparison model) [trustify-backend]
  |     |
  |     +-- Task 3 (comparison service) [trustify-backend]
  |           |
  |           +-- Task 4 (comparison endpoint + tests) [trustify-backend]
  |                 |
  |                 +-- Task 5 (API types + client) [trustify-ui] ** cross-repo dependency **
  |                       |
  |                       +-- Task 6 (comparison hook) [trustify-ui]
  |                             |
  |                             +-- Task 7 (comparison page) [trustify-ui]
  |                                   |
  |                                   +-- Task 8 (route + tests) [trustify-ui]
  |
  Task 9 (merge feature branch) -- depends on Task 4 and Task 8
```

## Repository: trustify-backend

### Files to Create

| File | Task | Purpose |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Task 2 | Comparison result structs (SbomComparisonResult, AddedPackage, etc.) |
| `modules/fundamental/src/sbom/service/comparison.rs` | Task 3 | Comparison business logic (diff computation) |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | Task 4 | REST handler for GET /api/v2/sbom/compare |
| `tests/api/sbom_compare.rs` | Task 4 | Integration tests for comparison endpoint |

### Files to Modify

| File | Task | Change |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Task 2 | Add `pub mod comparison;` |
| `modules/fundamental/src/sbom/service/mod.rs` | Task 3 | Add `pub mod comparison;` |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 4 | Register `/compare` route |

## Repository: trustify-ui

### Files to Create

| File | Task | Purpose |
|---|---|---|
| `src/hooks/useSbomComparison.ts` | Task 6 | React Query hook for comparison API |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Task 7 | Main comparison page component |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Task 7 | Reusable collapsible diff section |
| `src/pages/SbomComparePage/components/SbomSelector.tsx` | Task 7 | SBOM selector dropdown |
| `src/pages/SbomComparePage/components/ExportDropdown.tsx` | Task 7 | Export JSON/CSV dropdown |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Task 8 | Unit tests for comparison page |
| `tests/mocks/fixtures/sbom-comparison.json` | Task 8 | Mock comparison API response |
| `tests/e2e/sbom-compare.spec.ts` | Task 8 | Playwright E2E test |

### Files to Modify

| File | Task | Change |
|---|---|---|
| `src/api/models.ts` | Task 5 | Add comparison TypeScript interfaces |
| `src/api/rest.ts` | Task 5 | Add `fetchSbomComparison()` client function |
| `src/routes.tsx` | Task 8 | Add lazy-loaded route for `/sbom/compare` |
| `tests/mocks/handlers.ts` | Task 8 | Add MSW handler for comparison endpoint |

## Cross-Repository Dependencies

Task 5 (trustify-ui: API types + client) depends on Task 4 (trustify-backend: comparison endpoint). The frontend TypeScript interfaces must align with the backend Rust struct serialization. The API contract is defined by the `SbomComparisonResult` struct in Task 2 and serialized as JSON by the endpoint in Task 4.

## Existing Components Reused

- `src/components/SeverityBadge.tsx` -- Used in New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/hooks/useSboms.ts` -- Used by SbomSelector to populate SBOM dropdown options
- `src/api/client.ts` -- Shared Axios instance used by `fetchSbomComparison`
- `common/src/error.rs` -- `AppError` used for error handling in backend service and endpoint
- `entity/src/sbom_package.rs`, `entity/src/package.rs`, `entity/src/sbom_advisory.rs`, `entity/src/package_license.rs` -- Existing entities queried by comparison service
