# Repository Impact Map — TC-9003: SBOM comparison view

## trustify-backend

### Changes

- Add `SbomComparisonResult` model struct with sub-structs for added/removed packages, version changes, new/resolved vulnerabilities, and license changes in `modules/fundamental/src/sbom/model/`
- Add `compare` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that computes a structured diff between two SBOMs using existing package, advisory, and license data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
- Add integration tests for the comparison endpoint in `tests/api/`

## trustify-ui

### Changes

- Add TypeScript interfaces for the comparison API response and `compareSboms()` API client function in `src/api/`
- Add `useSbomComparison` React Query hook in `src/hooks/`
- Create `SbomComparePage` at `/sbom/compare` with PatternFly `Select` dropdowns for SBOM selection, `ExpandableSection` diff sections with `Badge` count indicators, `Table` components for each diff category, `EmptyState` for initial state, and `Skeleton` loading placeholders
- Add `SeverityBadge` usage for vulnerability severity display in comparison tables (reusing existing `src/components/SeverityBadge.tsx`)
- Update `SbomListPage` with row selection checkboxes and "Compare selected" button
- Register the `/sbom/compare` route in `src/routes.tsx`
