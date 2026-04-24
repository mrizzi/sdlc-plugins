# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

**Changes:**

1. **New comparison diff model** — Create `SbomComparisonResult` struct containing `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, and `license_changes` fields with their respective item structs
2. **New comparison service method** — Add `compare(left_id, right_id)` method to `SbomService` that fetches packages and advisories for both SBOMs and computes a structured diff on-the-fly (no new database tables)
3. **New comparison endpoint** — Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that accepts two SBOM IDs via query params and returns the `SbomComparisonResult` JSON response
4. **Route registration** — Register the comparison endpoint in `modules/fundamental/src/sbom/endpoints/mod.rs`
5. **Integration tests** — Add integration tests for the comparison endpoint in `tests/api/sbom.rs` covering: valid comparison, missing SBOM ID, same SBOM comparison, large SBOM performance

## trustify-ui

**Changes:**

1. **API types** — Add `SbomComparisonResult` and related TypeScript interfaces to `src/api/models.ts`
2. **API client function** — Add `compareSboms(leftId, rightId)` function to `src/api/rest.ts`
3. **React Query hook** — Create `useSbomComparison` hook in `src/hooks/useSbomComparison.ts`
4. **Comparison page** — Create `SbomComparePage` page directory under `src/pages/SbomComparePage/` with the main comparison page component, header toolbar (SBOM selectors, Compare button, Export dropdown), and collapsible diff sections using PatternFly `ExpandableSection` and `Table` components
5. **Diff section components** — Create page-specific components for each diff section: `AddedPackagesSection`, `RemovedPackagesSection`, `VersionChangesSection`, `NewVulnerabilitiesSection`, `ResolvedVulnerabilitiesSection`, `LicenseChangesSection`
6. **Route registration** — Add `/sbom/compare` route to `src/routes.tsx` pointing to `SbomComparePage`
7. **SBOM list page enhancement** — Add multi-select checkboxes and "Compare selected" button to `SbomListPage` that navigates to `/sbom/compare?left={id1}&right={id2}`
8. **URL-shareable state** — Pre-populate SBOM selectors from `left` and `right` URL query params and auto-trigger comparison when both are present
9. **Virtualized lists** — Use virtualization for diff section tables when row count exceeds 100 items
10. **Unit and E2E tests** — Add tests for comparison page, SBOM selection flow, and MSW handlers for the comparison endpoint
