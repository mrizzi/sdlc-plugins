# Impact Map — TC-9003: SBOM Comparison View

## Repositories Affected

### 1. trustify-backend

| Area | Changes |
|---|---|
| **Models** | New `SbomComparisonResult` struct and sub-types (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) in `modules/fundamental/src/sbom/model/` |
| **Service** | New `compare` method on `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that computes on-the-fly diff between two SBOMs using existing package, advisory, and license data |
| **Endpoint** | New `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/` with route registered in `modules/fundamental/src/sbom/endpoints/mod.rs` |
| **Tests** | New integration test file `tests/api/sbom_compare.rs` covering comparison endpoint with various diff scenarios |

### 2. trustify-ui

| Area | Changes |
|---|---|
| **API types** | New TypeScript interfaces (`SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) in `src/api/models.ts` |
| **API client** | New `compareSboms(leftId, rightId)` function in `src/api/rest.ts` |
| **Hooks** | New `useSbomComparison` React Query hook in `src/hooks/` |
| **Pages** | New `SbomComparePage/` directory under `src/pages/` with main page component and sub-components for diff sections |
| **Routing** | New route `/sbom/compare` registered in `src/routes.tsx` |
| **Existing page** | Modified `SbomListPage.tsx` to add checkbox selection and "Compare selected" button |
| **Tests** | Unit tests for comparison page, MSW mock handler for comparison endpoint, E2E test for comparison flow |

## Cross-Repo Dependencies

```
trustify-backend Task 1 (model) ← Task 2 (service) ← Task 3 (endpoint) ← Task 4 (tests)
                                                            ↓
trustify-ui      Task 5 (API types) ← Task 6 (hook) ← Task 7 (page)
                                                        ↓         ↓
                                                   Task 8 (route + nav)  Task 9 (SbomListPage selection)
                                                        ↓
                                                   Task 10 (tests)
```

Frontend tasks 5-6 depend on backend task 3 (the endpoint definition) for API contract alignment. Frontend tasks 7-10 depend on tasks 5-6 for the client/hook layer.
