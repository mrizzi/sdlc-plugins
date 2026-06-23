# Task 4: Add SBOM comparison TypeScript types and API client function

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Define the TypeScript interfaces for the SBOM comparison API response and add the API client function that calls the backend comparison endpoint. These types and the client function form the contract between the frontend and the new backend endpoint, and are consumed by the React Query hook and page components in subsequent tasks.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` API client function

## Implementation Notes
- The interfaces in `src/api/models.ts` must match the backend response shape:
  ```typescript
  interface SbomComparison {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }

  interface AddedPackage {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface RemovedPackage {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface VersionChange {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade";
  }

  interface NewVulnerability {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  interface ResolvedVulnerability {
    advisory_id: string;
    severity: string;
    title: string;
    previously_affected_package: string;
  }

  interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }
  ```
- The `fetchSbomComparison` function in `src/api/rest.ts` should follow the existing patterns (e.g., `fetchSboms()`) using the Axios client from `src/api/client.ts`.
- The function should call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` and return the typed `SbomComparison` response.
- Export all new interfaces from `src/api/models.ts` so they are available to hooks and components.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts` — existing API client functions (e.g., `fetchSboms`) as pattern reference
- `src/api/models.ts` — existing interfaces as pattern reference for naming and export style

## Acceptance Criteria
- [ ] All seven TypeScript interfaces are defined and exported from `src/api/models.ts`
- [ ] Interface field names and types match the backend response contract
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts`
- [ ] `fetchSbomComparison` calls the correct endpoint with query parameters
- [ ] TypeScript compilation passes with no errors

## Test Requirements
- [ ] Type-level verification: TypeScript compilation confirms interfaces match expected shapes
- [ ] The API client function is tested via MSW integration in Task 8

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Implement SBOM comparison endpoint handler and route (endpoint must exist for frontend integration)

`[sdlc-workflow] Description digest: sha256-md:d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6`
