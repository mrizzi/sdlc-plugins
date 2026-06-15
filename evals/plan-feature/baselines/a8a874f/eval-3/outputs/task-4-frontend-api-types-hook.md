# TC-9003-4: Frontend API types, client function, and React Query hook

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Add TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This establishes the data layer that the comparison UI components will consume.

## Files to Modify

- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function using the Axios client

## Files to Create

- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId, rightId)` that calls the comparison endpoint

## Dependencies

- TC-9003-3 (backend comparison endpoint must be defined for API contract alignment)

## Implementation Notes

- Add interfaces to `src/api/models.ts` following the existing pattern (e.g., adjacent to SBOM-related types). The `SbomComparison` interface should match the backend response shape:
  ```typescript
  interface SbomComparison {
    added_packages: PackageDiff[];
    removed_packages: PackageDiff[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: VulnerabilityDiff[];
    license_changes: LicenseChange[];
  }
  ```
- Add the `fetchSbomComparison` function in `src/api/rest.ts` following the existing pattern of `fetchSboms()` and `fetchAdvisories()`: use the Axios instance from `src/api/client.ts`, call `GET /api/v2/sbom/compare` with `left` and `right` query params, and return typed `SbomComparison`.
- The React Query hook in `src/hooks/useSbomComparison.ts` should follow the pattern in `src/hooks/useSboms.ts`: use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`, and set `enabled: !!leftId && !!rightId` so the query only fires when both IDs are provided.
- The hook should return the standard React Query result object (`data`, `isLoading`, `isError`, `error`).

## Acceptance Criteria

- [ ] `SbomComparison` and related interfaces are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison` correctly calls `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- [ ] `useSbomComparison` hook returns comparison data, loading state, and error state
- [ ] Hook is disabled (does not fire) when either SBOM ID is missing

## Test Requirements

- [ ] Unit test for `useSbomComparison` hook: mock API response via MSW handler in `tests/mocks/handlers.ts`, verify the hook returns the expected data shape
- [ ] Unit test for disabled state: verify hook does not fire when `leftId` or `rightId` is undefined

## Reuse Candidates

- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — Pattern reference for React Query hook structure
- `tests/mocks/handlers.ts` — Add MSW handler for the comparison endpoint

## Convention Compliance

- `Applies: task modifies src/api/models.ts and src/api/rest.ts matching the convention's API layer scope.`
- `Applies: task creates src/hooks/useSbomComparison.ts matching the convention's hooks naming scope (camelCase for hooks).`

[Description digest: sha256-md:d6a0f4b2c9e5a1d7b3f8c4e0a6d2f8b4c0e7a3d9f5b1c8e4a0d6f2b9c5e1a7d3]
