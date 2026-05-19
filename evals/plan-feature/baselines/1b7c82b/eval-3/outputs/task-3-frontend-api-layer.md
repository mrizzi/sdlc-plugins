## Repository
trustify-ui

## Target Branch
main

## Description
Add the TypeScript types, API client function, and React Query hook for the SBOM comparison endpoint. This establishes the data-fetching layer that the comparison page UI (Task 4) will consume.

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook that calls the comparison endpoint with left and right SBOM IDs

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityDiff`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` function

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- CONSUMED: New endpoint created in backend Task 2

## Implementation Notes
- In `src/api/models.ts`, define interfaces matching the backend response shape. Follow the naming conventions used by existing interfaces in that file (e.g., `SbomSummary`, `AdvisorySummary`). The `SbomComparison` interface should have fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`.
- In `src/api/rest.ts`, add `fetchSbomComparison` using the Axios instance from `src/api/client.ts`, following the pattern of existing functions like `fetchSboms()`. The function should accept two string IDs and pass them as `left` and `right` query params.
- In `src/hooks/useSbomComparison.ts`, create a React Query hook following the pattern in `src/hooks/useSbomById.ts`. Use a query key like `["sbom-comparison", leftId, rightId]`. The hook should accept `leftId` and `rightId` parameters and only enable the query when both values are non-empty (use `enabled: !!leftId && !!rightId`).
- The `VulnerabilityDiff` interface should include a `severity` field typed as a string union matching the existing severity levels used by `SeverityBadge` in `src/components/SeverityBadge.tsx` and `src/utils/severityUtils.ts`.

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms` -- Pattern for API client functions using the shared Axios instance
- `src/hooks/useSbomById.ts` -- Pattern for single-resource React Query hooks with conditional enabling
- `src/api/models.ts` -- Existing interface naming conventions and structure
- `src/utils/severityUtils.ts` -- Severity level definitions to align the `VulnerabilityDiff.severity` type

## Acceptance Criteria
- [ ] `SbomComparison` interface and all sub-interfaces are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison()` function makes a GET request to `/api/v2/sbom/compare` with correct query params
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError }` matching React Query conventions
- [ ] Hook does not fire the API call until both SBOM IDs are provided
- [ ] All new types are exported from their respective modules

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns comparison data when both IDs are provided (mock with MSW)
- [ ] Unit test: `useSbomComparison` hook does not fetch when one ID is missing
- [ ] Unit test: `useSbomComparison` hook handles error responses correctly

## Verification Commands
- `npx vitest run src/hooks/useSbomComparison` -- Hook tests pass
- `npx tsc --noEmit` -- No TypeScript compilation errors

## Dependencies
- Depends on: Task 2 -- Backend comparison endpoint (API contract must be finalized)
