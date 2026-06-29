## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook to manage comparison data fetching. This establishes the data layer that the comparison page UI will consume.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId, rightId)` that calls the comparison API function

## Implementation Notes
- Follow the existing API layer pattern: types in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- The `SbomComparison` interface must match the backend response shape:
  ```typescript
  interface SbomComparison {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- The Axios client function should call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` using the existing Axios instance from `src/api/client.ts`.
- The React Query hook should use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]` and be enabled only when both IDs are provided (`enabled: !!leftId && !!rightId`).
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` and `src/api/models.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's API layer scope.
- Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's naming scope.

## Reuse Candidates
- `src/api/models.ts` — Existing TypeScript interfaces for SBOM and advisory types to follow as patterns
- `src/api/rest.ts::fetchSboms()` — Pattern for Axios API function with typed return
- `src/api/client.ts` — Axios instance to use for the API call
- `src/hooks/useSboms.ts` — Pattern for React Query `useQuery` hook with proper query key structure
- `src/hooks/useSbomById.ts` — Pattern for hook with parameter-based query key and conditional enabling

## Acceptance Criteria
- [ ] `SbomComparison` and all sub-interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms()` function is exported from `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook is disabled when either SBOM ID is not provided
- [ ] Hook returns proper loading, error, and data states

## Test Requirements
- [ ] Unit test for `compareSboms()` — mock Axios and verify correct URL construction with query parameters
- [ ] Unit test for `useSbomComparison` hook — verify it calls the API function with correct parameters
- [ ] Unit test for `useSbomComparison` hook — verify it is disabled when leftId or rightId is undefined
- [ ] Type-check passes with `tsc --noEmit`

## Dependencies
- Depends on: Task 5 — Create feature branch for trustify-ui
- Cross-repo dependency: Task 3 — Backend comparison endpoint must exist for integration testing

[sdlc-workflow] Description digest: sha256-md:3a53e723949fe1df25119c700066cebc3325895311dc863252861b7ce4274550
