## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response types and a client function `compareSboms` in the API layer. This provides the typed API foundation that the React Query hook and comparison page will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Implementation Notes
Follow the existing API layer pattern:
- Interfaces go in `src/api/models.ts` alongside existing `SbomSummary`, `AdvisorySummary`, etc. Use the same naming convention (PascalCase for types).
- The `compareSboms` function goes in `src/api/rest.ts` alongside existing `fetchSboms()`, `fetchAdvisories()`, etc. It should use the Axios instance from `src/api/client.ts`.
- Use query parameters for the endpoint call: `client.get('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } })`.
- The TypeScript interfaces must match the backend response shape exactly:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- Field naming uses snake_case to match the Rust/JSON serialization from the backend.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces showing naming and structure conventions
- `src/api/rest.ts` — existing API client functions (e.g., `fetchSboms`) showing the Axios call pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function exists in `src/api/rest.ts`
- [ ] Function calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] Return type is `Promise<SbomComparisonResult>`
- [ ] TypeScript interfaces match the backend response shape

## Test Requirements
- [ ] Unit test: verify `compareSboms` calls the correct endpoint with correct query parameters (using MSW or Axios mock)
- [ ] Type check: verify TypeScript compilation succeeds with the new interfaces

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 4 — Add SBOM comparison endpoint (trustify-backend)

[sdlc-workflow] Description digest: sha256:38b271fef003fed048e44766f10db8560fb14c62f252174849e3738ae4bec246
