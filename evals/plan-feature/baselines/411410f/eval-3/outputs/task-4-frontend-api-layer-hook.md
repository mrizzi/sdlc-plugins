# Task 4: Add frontend API client and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
main

## Description
Extend the frontend API layer with TypeScript interfaces for the comparison response and a client function to call the new backend endpoint. Add a React Query hook that wraps the API call with proper caching, loading states, and error handling. This provides the data-fetching foundation for the comparison page UI.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that calls the comparison endpoint

## Implementation Notes
- **TypeScript interfaces** in `src/api/models.ts` — follow the naming and style of existing interfaces in that file:
  ```typescript
  export interface PackageDiff {
    name: string;
    version: string;
    license: string | null;
    advisory_count: number;
  }
  export interface VersionChange {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade" | "unknown";
  }
  export interface VulnerabilityDiff {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }
  export interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }
  export interface SbomComparison {
    added_packages: PackageDiff[];
    removed_packages: PackageDiff[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: VulnerabilityDiff[];
    license_changes: LicenseChange[];
  }
  ```
- **API function** in `src/api/rest.ts` — follow the pattern of existing functions like `fetchSboms()`:
  - Use the Axios instance from `src/api/client.ts`
  - Function signature: `export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparison>`
  - Endpoint: `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}`
- **React Query hook** in `src/hooks/useSbomComparison.ts` — follow the pattern of `src/hooks/useSbomById.ts`:
  - Use `useQuery` from TanStack Query
  - Query key: `["sbom-comparison", leftId, rightId]`
  - The query should be enabled only when both `leftId` and `rightId` are defined and non-empty (`enabled: !!leftId && !!rightId`)
  - Return the full `useQuery` result (data, isLoading, isError, error)

## Acceptance Criteria
- [ ] `SbomComparison` and all supporting interfaces are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts` and correctly calls the backend endpoint
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook is disabled when either SBOM ID is missing (does not fire a request)
- [ ] Hook uses a descriptive query key that includes both SBOM IDs for proper cache invalidation
- [ ] All types compile without TypeScript errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook verifying it does not fetch when IDs are missing
- [ ] Unit test verifying the hook returns comparison data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 2 — Implement SBOM comparison service and endpoint (defines the response contract and endpoint URL)
