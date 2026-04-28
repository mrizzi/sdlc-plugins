# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (`SbomComparisonDiff`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
  - Add comparison diffing service method to `SbomService` that computes the structured diff between two SBOMs using existing package, advisory, and license data
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler in `modules/fundamental/src/sbom/endpoints/`
  - Register comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs`
  - Add integration tests for the comparison endpoint in `tests/api/sbom.rs`

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response shape in `src/api/models.ts`
  - Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
  - Add React Query hook `useSbomComparison` in `src/hooks/`
  - Create `SbomComparePage` component with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per Figma design
  - Create page-specific sub-components: `DiffSection`, `PackageTable`, `VulnerabilityTable`, `LicenseChangeTable` under `src/pages/SbomComparePage/components/`
  - Register `/sbom/compare` route in `src/routes.tsx`
  - Add SBOM multi-select checkboxes and "Compare selected" button to `SbomListPage`
  - Add unit tests for `SbomComparePage` and sub-components
  - Add MSW mock handlers and fixtures for the comparison endpoint
