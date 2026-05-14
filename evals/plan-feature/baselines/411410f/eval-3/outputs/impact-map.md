# Impact Map: TC-9003 — SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view that lets users select two SBOM versions and see what changed: added/removed packages, new/resolved vulnerabilities, and license changes. This requires a new backend diffing endpoint and a frontend comparison UI.

## Repository Impact

### trustify-backend

| Area | Files / Directories | Impact | Notes |
|---|---|---|---|
| Comparison model | `modules/fundamental/src/sbom/model/` | **New file**: `compare.rs` | New structs for the comparison response: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` |
| Comparison service | `modules/fundamental/src/sbom/service/` | **New file**: `compare.rs` | Diff logic that fetches packages/advisories/licenses for two SBOMs and computes the structured diff. Uses `PackageService` and `AdvisoryService` |
| Comparison service module | `modules/fundamental/src/sbom/service/mod.rs` | **Modify** | Register the new `compare` submodule |
| Comparison endpoint | `modules/fundamental/src/sbom/endpoints/` | **New file**: `compare.rs` | `GET /api/v2/sbom/compare?left={id}&right={id}` handler. Query-param extraction, validation, delegates to comparison service |
| Endpoint registration | `modules/fundamental/src/sbom/endpoints/mod.rs` | **Modify** | Register the `/compare` route in the SBOM endpoint router |
| SBOM model module | `modules/fundamental/src/sbom/model/mod.rs` | **Modify** | Re-export comparison model types |
| Entity layer | `entity/src/sbom_package.rs`, `entity/src/package_license.rs`, `entity/src/sbom_advisory.rs` | **Read only** | Queried by comparison service; no modifications needed |
| Integration tests | `tests/api/` | **New file**: `sbom_compare.rs` | Tests for the comparison endpoint covering happy-path, missing IDs, identical SBOMs, and large diffs |
| Test module | `tests/api/mod.rs` (if exists) or `Cargo.toml` | **Modify** | Register the new test file |

### trustify-ui

| Area | Files / Directories | Impact | Notes |
|---|---|---|---|
| API models | `src/api/models.ts` | **Modify** | Add TypeScript interfaces: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` |
| API client functions | `src/api/rest.ts` | **Modify** | Add `fetchSbomComparison(leftId, rightId)` function |
| React Query hook | `src/hooks/` | **New file**: `useSbomComparison.ts` | `useSbomComparison(leftId, rightId)` hook wrapping the API call |
| Comparison page | `src/pages/SbomComparePage/` | **New directory** | `SbomComparePage.tsx` — main page component with SBOM selectors and diff sections |
| Comparison page components | `src/pages/SbomComparePage/components/` | **New directory** | `DiffSection.tsx` (reusable expandable section with badge), `SbomSelector.tsx` (typeahead select), `ExportDropdown.tsx` |
| Routes | `src/routes.tsx` | **Modify** | Add `/sbom/compare` route pointing to `SbomComparePage` |
| SBOM list page | `src/pages/SbomListPage/SbomListPage.tsx` | **Modify** | Add checkbox selection and "Compare selected" button to navigate to comparison page |
| Unit tests | `src/pages/SbomComparePage/SbomComparePage.test.tsx` | **New file** | Tests for the comparison page |
| MSW mock handlers | `tests/mocks/handlers.ts` | **Modify** | Add mock handler for `GET /api/v2/sbom/compare` |
| Mock fixtures | `tests/mocks/fixtures/` | **New file**: `sbom-comparison.json` | Mock comparison response data |
| E2E tests | `tests/e2e/` | **New file**: `sbom-compare.spec.ts` | Playwright E2E test for the comparison workflow |

## Cross-Repository Dependencies

```
trustify-backend                         trustify-ui
─────────────────                        ───────────
Task 1: Comparison model        
Task 2: Comparison service/endpoint ───> Task 4: API layer + hook (depends on response shape)
Task 3: Backend integration tests        Task 5: Comparison page UI (depends on Task 2 endpoint)
                                         Task 6: SBOM list page integration
                                         Task 7: Frontend tests (depends on Tasks 5, 6)
```

Frontend work on the API client, hook, and page components depends on the backend endpoint being defined (at minimum the response contract from Task 1/2). Frontend tasks reference the backend's response shape and endpoint URL.

## Risk Assessment

| Risk | Likelihood | Mitigation |
|---|---|---|
| Large SBOM diffs cause slow responses (>1s p95) | Medium | Add database query optimization; consider parallel fetching of left/right SBOM data |
| Large diffs freeze the browser | Medium | Use virtualized table rendering for sections with >100 rows (PatternFly Table supports this) |
| Mismatched SBOM comparison (different products) | Low | Add validation in the backend to warn or reject comparisons of SBOMs from different products |
