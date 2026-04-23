## Repository
trustify-ui

## Description
Add the TypeScript API types, REST client function, and React Query hook for the SBOM comparison endpoint. This task establishes the data-fetching layer that the comparison page UI will consume. The types match the backend `SbomComparison` response shape defined in the Figma design context.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `fetchSbomComparison`

## Implementation Notes
- **TypeScript interfaces** in `src/api/models.ts`: Add these interfaces matching the backend contract and Figma design context response shape:
  - `SbomComparison` with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
  - `PackageDiff` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` with fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `VulnerabilityDiff` with fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `LicenseChange` with fields: `name: string`, `left_license: string`, `right_license: string`
- **REST function** in `src/api/rest.ts`: Follow the pattern of existing functions like `fetchSboms()`. Use the Axios client from `src/api/client.ts` to call `GET /api/v2/sbom/compare` with `left` and `right` query parameters. Return type should be `SbomComparison`.
- **React Query hook** in `src/hooks/useSbomComparison.ts`: Follow the pattern in `src/hooks/useSbomById.ts`. Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should be `enabled` only when both `leftId` and `rightId` are truthy. This enables the Figma-specified behavior where the Compare button triggers the query.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — pattern for API client function using Axios
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSbomById.ts` — pattern for single-resource React Query hook with parameters
- `src/hooks/useSboms.ts` — pattern for React Query hook setup

## Acceptance Criteria
- [ ] `SbomComparison` and all sub-interfaces are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function exists in `src/api/rest.ts` and calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook exists and returns React Query result with `data`, `isLoading`, `isError`
- [ ] Hook is disabled when either SBOM ID is missing (does not fire a request)
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns loading state initially when both IDs are provided
- [ ] Unit test: `useSbomComparison` hook does not fetch when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` hook does not fetch when `rightId` is undefined
- [ ] Unit test: verify `fetchSbomComparison` calls the correct URL with query parameters (mock Axios)

## Verification Commands
- `npx tsc --noEmit` — TypeScript compiles without errors
- `npx vitest run --grep "useSbomComparison"` — hook tests pass

## Dependencies
- Depends on: Task 2 — SBOM comparison service and endpoint (backend must define the API contract)
