# Task 6 — Add frontend API layer for SBOM comparison

**Summary:** Add frontend API types, client function, and React Query hook for SBOM comparison

**Labels:** ai-generated-jira

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This provides the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- **TypeScript interfaces** in `src/api/models.ts` — add interfaces matching the backend response contract:
  - `SbomComparisonResult` with fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: NewVulnerability[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`
  - `AddedPackage` — fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `RemovedPackage` — same fields as AddedPackage
  - `VersionChange` — fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `NewVulnerability` — fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `ResolvedVulnerability` — fields: `advisory_id: string`, `severity: string`, `title: string`, `previously_affected_package: string`
  - `LicenseChange` — fields: `name: string`, `left_license: string`, `right_license: string`
- **API function** in `src/api/rest.ts` — follow the existing pattern used by `fetchSboms()` and other functions: use the Axios instance from `src/api/client.ts`, call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`, and return typed `SbomComparisonResult`.
- **React Query hook** in `src/hooks/useSbomComparison.ts` — follow the pattern in `src/hooks/useSbomById.ts`: use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`, call the API function, and only enable the query when both IDs are provided (use `enabled: !!leftId && !!rightId`).

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- `GET /api/v2/sbom` — existing endpoint for SBOM list, used by SBOM selectors (see `modules/fundamental/src/sbom/endpoints/list.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API function pattern with Axios client
- `src/api/models.ts` — reference for existing TypeScript interface style and naming
- `src/hooks/useSbomById.ts` — reference for React Query hook pattern with useQuery
- `src/hooks/useSboms.ts` — reference for list-fetching hook pattern
- `src/api/client.ts` — Axios instance to reuse for API calls

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in models.ts
- [ ] `compareSboms` function in rest.ts calls the correct endpoint with left/right params
- [ ] `useSbomComparison` hook uses React Query with correct query key and enabled condition
- [ ] Types are exported and importable by the comparison page component

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook makes the correct API call with both IDs provided
- [ ] Unit test: `useSbomComparison` hook does not fire when either ID is missing (enabled: false)
- [ ] MSW handler added for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
