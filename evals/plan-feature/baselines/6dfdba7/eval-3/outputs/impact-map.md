# Impact Map: TC-9003 SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view with a new backend diffing endpoint (`GET /api/v2/sbom/compare`) and a frontend comparison UI. Users select two SBOM versions and see structured diffs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Repositories Impacted

### trustify-backend

| Area | Files | Change Type | Description |
|---|---|---|---|
| Comparison model | `modules/fundamental/src/sbom/model/comparison.rs` | Create | New structs for the comparison response: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` |
| Comparison service | `modules/fundamental/src/sbom/service/compare.rs` | Create | Diff logic: load packages and advisories for two SBOMs, compute added/removed/changed sets |
| SBOM service module | `modules/fundamental/src/sbom/service/mod.rs` | Modify | Re-export the new `compare` submodule |
| SBOM model module | `modules/fundamental/src/sbom/model/mod.rs` | Modify | Re-export the new `comparison` submodule |
| Comparison endpoint | `modules/fundamental/src/sbom/endpoints/compare.rs` | Create | `GET /api/v2/sbom/compare?left={id}&right={id}` handler |
| Endpoint registration | `modules/fundamental/src/sbom/endpoints/mod.rs` | Modify | Register the comparison route |
| Integration tests | `tests/api/sbom_compare.rs` | Create | Integration tests for the comparison endpoint |
| Test module | `tests/api/mod.rs` or test config | Modify | Register the new test file |

### trustify-ui

| Area | Files | Change Type | Description |
|---|---|---|---|
| API types | `src/api/models.ts` | Modify | Add TypeScript interfaces for the comparison response shape |
| API client | `src/api/rest.ts` | Modify | Add `fetchSbomComparison(leftId, rightId)` function |
| Comparison hook | `src/hooks/useSbomComparison.ts` | Create | React Query hook wrapping the comparison API call |
| Comparison page | `src/pages/SbomComparePage/SbomComparePage.tsx` | Create | Main comparison page with SBOM selectors, compare button, and diff sections |
| Diff section components | `src/pages/SbomComparePage/components/DiffSection.tsx` | Create | Reusable expandable diff section with count badge and data table |
| Comparison empty state | `src/pages/SbomComparePage/components/ComparisonEmptyState.tsx` | Create | Empty state shown before comparison is performed |
| Route registration | `src/routes.tsx` | Modify | Add `/sbom/compare` route |
| SBOM list page | `src/pages/SbomListPage/SbomListPage.tsx` | Modify | Add checkbox selection and "Compare selected" button |
| Page tests | `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Create | Unit tests for the comparison page |
| Mock handlers | `tests/mocks/handlers.ts` | Modify | Add MSW handler for the comparison endpoint |
| Mock fixtures | `tests/mocks/fixtures/sbom-comparison.json` | Create | Mock comparison response data |

## Task Breakdown

| Task | Repository | Title | Dependencies |
|---|---|---|---|
| 1 | trustify-backend | Define SBOM comparison model types | None |
| 2 | trustify-backend | Implement SBOM comparison service logic | Task 1 |
| 3 | trustify-backend | Add comparison REST endpoint and integration tests | Task 2 |
| 4 | trustify-ui | Add comparison API types, client function, and React Query hook | Task 3 |
| 5 | trustify-ui | Build SBOM comparison page with diff sections | Task 4 |
| 6 | trustify-ui | Add SBOM selection and navigation from SBOM list page | Task 5 |

## Non-Functional Considerations

- **Performance**: Backend must compute diffs in <1s at p95 for SBOMs with up to 2000 packages. Frontend must use virtualized lists for diffs with >100 rows.
- **No new database tables**: Diff is computed on-the-fly from existing package, advisory, and license data.
- **URL-shareable**: Comparison page URL encodes both SBOM IDs as query params (`?left=...&right=...`).
