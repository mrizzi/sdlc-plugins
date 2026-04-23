# Impact Map: TC-9003 SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view that lets users select two SBOM versions and see what changed: added/removed packages, new/resolved vulnerabilities, and license changes. Requires a new backend diffing endpoint and a frontend comparison UI.

## Repository Impact

### trustify-backend

| Area | Impact | Details |
|---|---|---|
| `modules/fundamental/src/sbom/model/` | NEW | Add `SbomComparison` response struct with diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes) |
| `modules/fundamental/src/sbom/service/` | MODIFY | Add comparison logic to `SbomService` that queries packages and advisories for two SBOMs and computes the diff |
| `modules/fundamental/src/sbom/endpoints/` | NEW | Add `compare.rs` endpoint handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}` and register the route |
| `entity/src/` | READ-ONLY | Reference existing `sbom.rs`, `sbom_package.rs`, `package.rs`, `package_license.rs`, `sbom_advisory.rs`, `advisory.rs` entities for join queries |
| `common/src/error.rs` | READ-ONLY | Reuse `AppError` for error handling in the new endpoint |
| `tests/api/` | NEW | Add `sbom_compare.rs` integration tests for the comparison endpoint |

### trustify-ui

| Area | Impact | Details |
|---|---|---|
| `src/api/models.ts` | MODIFY | Add TypeScript interfaces for the comparison response (`SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) |
| `src/api/rest.ts` | MODIFY | Add `fetchSbomComparison(leftId, rightId)` API client function |
| `src/hooks/` | NEW | Add `useSbomComparison.ts` React Query hook for the comparison endpoint |
| `src/pages/SbomComparePage/` | NEW | New page directory with `SbomComparePage.tsx` and page-specific components for diff sections |
| `src/routes.tsx` | MODIFY | Add `/sbom/compare` route pointing to `SbomComparePage` |
| `src/pages/SbomListPage/SbomListPage.tsx` | MODIFY | Add checkbox selection and "Compare selected" button to navigate to comparison page |
| `src/components/` | READ-ONLY | Reuse `SeverityBadge.tsx`, `EmptyStateCard.tsx`, `FilterToolbar.tsx`, `LoadingSpinner.tsx` |
| `tests/mocks/` | MODIFY | Add MSW handler and fixture for comparison endpoint |
| `tests/e2e/` | NEW | Add E2E test for comparison workflow |

## Task Dependency Graph

```
Task 1 (backend: comparison model)
  |
  v
Task 2 (backend: comparison service + endpoint)
  |
  v
Task 3 (backend: integration tests)
  |
  v
Task 4 (frontend: API layer + hook) --depends on--> Task 2
  |
  v
Task 5 (frontend: comparison page UI) --depends on--> Task 4
  |
  v
Task 6 (frontend: SBOM list page integration + E2E tests) --depends on--> Task 5
```

## Risk Areas

- **Performance**: Diffing two large SBOMs (2000+ packages) on-the-fly requires efficient queries; may need to batch package/advisory lookups rather than N+1 queries
- **Virtualization**: Frontend must handle large diffs (>100 rows) with virtualized lists to avoid browser freezing
- **Cross-repo contract**: Backend response shape must match frontend TypeScript interfaces exactly; the `SbomComparison` struct is the contract boundary
