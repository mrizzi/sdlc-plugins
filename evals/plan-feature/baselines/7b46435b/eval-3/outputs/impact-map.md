# Impact Map: TC-9003 -- SBOM comparison view

## Feature
Add a side-by-side SBOM comparison view that lets users select two SBOM versions and see what changed: added/removed packages, new/resolved vulnerabilities, and license changes. The comparison requires a new backend diffing endpoint and a frontend comparison UI built from Figma mockups.

## Repositories Affected

| Repository | Role |
|---|---|
| trustify-backend | Backend -- new comparison diff model, service, REST endpoint, and integration tests |
| trustify-ui | Frontend -- comparison API types, React Query hook, comparison page UI, and list page compare action |

## Specific Changes Needed

### trustify-backend

#### Model Layer
- Create `SbomComparisonResult` struct with fields for each diff category: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- Create supporting sub-structs: `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- Register the new model module in `modules/fundamental/src/sbom/model/mod.rs`

#### Service Layer
- Add `compare_sboms` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`
- Diff computation joins `sbom_package` with `package` and `package_license` entities for both SBOMs, computes set differences
- Cross-reference with `sbom_advisory` and `advisory` entities for vulnerability diff
- No new database tables -- compute diff on-the-fly from existing data

#### Endpoint Layer
- Create `GET /api/v2/sbom/compare?left={id1}&right={id2}` handler in `modules/fundamental/src/sbom/endpoints/compare.rs`
- Return 400 if either query parameter is missing
- Return 404 if either SBOM ID does not exist
- Register route in `modules/fundamental/src/sbom/endpoints/mod.rs`

#### Integration Tests
- Create `tests/api/sbom_compare.rs` with test cases covering: valid comparison, 404 for missing SBOM, 400 for missing params, empty diff for identical SBOMs, deduplication verification

### trustify-ui

#### API Layer
- Add TypeScript interfaces for comparison response types in `src/api/models.ts`
- Add `compareSboms(leftId, rightId)` function in `src/api/rest.ts`
- Create `useSbomCompare` React Query hook in `src/hooks/useSbomCompare.ts`

#### Comparison Page
- Create `SbomComparePage` at `/sbom/compare` with PatternFly components
- Header toolbar with SBOM selectors (PatternFly `Select`), Compare button, Export `Dropdown`
- Six collapsible diff sections (PatternFly `ExpandableSection`) with data tables (PatternFly `Table`)
- Empty state (PatternFly `EmptyState`) when no comparison performed
- Loading state with PatternFly `Skeleton` placeholders
- Virtualized lists for >100 changed packages
- URL-shareable via query parameters

#### List Page Compare Action
- Add checkbox selection to `SbomListPage` for selecting two SBOMs
- Add "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

### Documentation
- Document the comparison endpoint in API reference (path, parameters, response schema, status codes)
- Document the comparison UI workflow for end users

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export diff as JSON or CSV | Marked as non-MVP in the feature requirements. The Export dropdown UI element is rendered per the Figma design but the actual export logic is deferred to a follow-up iteration. |

## Workflow Mode Decision

**Mode**: direct-to-main

**Rationale**: Although this feature spans two repositories (trustify-backend and trustify-ui), no atomicity indicator requires coordinated delivery:

1. **No coordinated schema migrations** -- no new database tables are created; the diff is computed on-the-fly from existing data.
2. **No breaking API changes** -- the backend adds a purely additive new endpoint (`GET /api/v2/sbom/compare`). Existing endpoints are unchanged.
3. **No cross-cutting refactors** -- changes in each repository are self-contained; no shared types or modules are modified.
4. **Independent deployability** -- the backend endpoint can be merged and deployed first. The frontend page, while it depends on the backend endpoint being available, does not break `main` if merged before the backend is deployed (the new page shows an error state until the API is available, but all existing pages are unaffected).

Cross-repo dependency ordering is enforced via explicit Dependencies sections: frontend tasks depend on backend tasks. Backend tasks must be merged first.
