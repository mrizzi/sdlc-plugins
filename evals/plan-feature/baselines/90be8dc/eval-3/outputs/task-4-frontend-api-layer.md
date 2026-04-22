## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response and a React Query hook to fetch comparison data. This task builds the data layer that the comparison page will consume.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId, rightId)` that calls the comparison endpoint and returns typed data

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` using the Axios client

## Implementation Notes
- The TypeScript interfaces must match the backend response shape from the Figma design context:
  - `SbomComparison` with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`.
  - `PackageDiff`: `name: string`, `version: string`, `license: string`, `advisory_count: number`.
  - `VersionChange`: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`.
  - `VulnerabilityDiff`: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`.
  - `LicenseChange`: `name: string`, `left_license: string`, `right_license: string`.
- The API function in `src/api/rest.ts` should follow the pattern of existing functions like `fetchSboms()` — use the Axios instance from `src/api/client.ts`.
- The React Query hook in `src/hooks/useSbomComparison.ts` should follow the pattern in `src/hooks/useSbomById.ts`:
  - Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`.
  - The query should be `enabled` only when both `leftId` and `rightId` are defined and non-empty.
  - Return the full `useQuery` result (data, isLoading, isError, etc.).

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — pattern for API client function using Axios
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSbomById.ts` — pattern for single-resource React Query hook with `enabled` guard
- `src/api/models.ts` — existing interface definitions to follow naming conventions

## Acceptance Criteria
- [ ] All five TypeScript interfaces are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison()` calls `GET /api/v2/sbom/compare?left={id}&right={id}` and returns typed `SbomComparison`
- [ ] `useSbomComparison` hook is disabled when either ID is missing
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook verifying it calls the correct endpoint and returns typed data (use MSW mock)

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds

## Dependencies
- Depends on: Task 2 — Backend comparison service and endpoint (API contract must be finalized)
