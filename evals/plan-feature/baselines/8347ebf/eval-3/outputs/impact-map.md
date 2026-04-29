# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add comparison diff model structs (`SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
  - Add `SbomComparisonService` with `compare(left_id, right_id)` method in `modules/fundamental/src/sbom/service/` that computes the diff on-the-fly from existing package, advisory, and license data
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
  - Add integration tests for the comparison endpoint in `tests/api/`

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response shape in `src/api/models.ts`
  - Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
  - Add React Query hook `useSbomComparison` in `src/hooks/`
  - Add `SbomComparePage` at route `/sbom/compare` with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Register `/sbom/compare` route in `src/routes.tsx`
  - Add multi-select checkboxes and "Compare selected" button to `SbomListPage`
  - Add MSW handlers and test fixtures for the comparison endpoint in `tests/mocks/`
  - Add unit tests for `SbomComparePage` in `src/pages/SbomComparePage/`
