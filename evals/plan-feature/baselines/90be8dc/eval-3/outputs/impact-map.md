# Impact Map: TC-9003 — SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view that lets users select two SBOM versions and see what changed: added/removed packages, new/resolved vulnerabilities, and license changes. Requires a new backend diffing endpoint and a frontend comparison UI.

## Repositories Impacted

### trustify-backend

| Area | Change Type | Details |
|---|---|---|
| `modules/fundamental/src/sbom/model/` | New file | `compare.rs` — structs for comparison response: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` |
| `modules/fundamental/src/sbom/service/` | New file | `compare.rs` — `SbomService::compare()` method implementing on-the-fly diff logic |
| `modules/fundamental/src/sbom/endpoints/` | New file | `compare.rs` — `GET /api/v2/sbom/compare` handler with `left` and `right` query params |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Modify | Register the new `/compare` route |
| `modules/fundamental/src/sbom/model/mod.rs` | Modify | Re-export comparison model types |
| `modules/fundamental/src/sbom/service/mod.rs` | Modify | Re-export comparison service logic |
| `tests/api/` | New file | `sbom_compare.rs` — integration tests for the comparison endpoint |

### trustify-ui

| Area | Change Type | Details |
|---|---|---|
| `src/api/models.ts` | Modify | Add TypeScript interfaces for `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` |
| `src/api/rest.ts` | Modify | Add `fetchSbomComparison(leftId, rightId)` API client function |
| `src/hooks/` | New file | `useSbomComparison.ts` — React Query hook wrapping the comparison API call |
| `src/pages/SbomComparePage/` | New directory | Comparison page with main component and sub-components |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | New file | Main comparison page component with SBOM selectors and diff sections |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | New file | Reusable collapsible diff section using PatternFly `ExpandableSection`, `Badge`, and `Table` |
| `src/pages/SbomComparePage/components/CompareToolbar.tsx` | New file | Header toolbar with SBOM selectors, Compare button, and Export dropdown |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | New file | Unit tests for comparison page |
| `src/routes.tsx` | Modify | Add `/sbom/compare` route pointing to `SbomComparePage` |
| `src/pages/SbomListPage/SbomListPage.tsx` | Modify | Add multi-select checkboxes and "Compare selected" button |
| `tests/mocks/handlers.ts` | Modify | Add MSW handler for `GET /api/v2/sbom/compare` |
| `tests/mocks/fixtures/` | New file | `sbom-comparison.json` — mock comparison response data |

## Task Dependency Graph

```
Task 1: Backend comparison models
Task 2: Backend comparison service + endpoint  (depends on Task 1)
Task 3: Backend integration tests              (depends on Task 2)
Task 4: Frontend API layer + hook              (depends on Task 2)
Task 5: Frontend comparison page               (depends on Task 4)
Task 6: Frontend SBOM list page enhancements   (depends on Task 5)
```
