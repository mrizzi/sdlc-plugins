# Task 5: Add SBOM comparison API types and client function

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 4 (cross-repo: trustify-backend comparison endpoint must be defined to ensure type alignment)

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Define TypeScript interfaces for the SBOM comparison API response and add a typed client function that calls the new `GET /api/v2/sbom/compare` endpoint. These types and client function form the frontend contract with the backend comparison endpoint.

## Files to Modify

- `src/api/models.ts` -- Add interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Acceptance Criteria

- [ ] `SbomComparisonResult` interface matches the backend JSON contract with all six diff category arrays
- [ ] Each sub-interface has correctly typed fields (e.g., `advisory_count: number`, `direction: "upgrade" | "downgrade"`)
- [ ] `fetchSbomComparison()` calls `GET /api/v2/sbom/compare` with `left` and `right` query parameters using the shared Axios client
- [ ] Function is exported and available for use by React Query hooks
- [ ] TypeScript compilation passes with no errors

## Test Requirements

- Type-level verification: ensure the interfaces compile and are structurally compatible with expected API responses.
- Optional unit test: mock Axios to verify `fetchSbomComparison` constructs the correct URL with query parameters.

## Implementation Notes

Add the interfaces to `src/api/models.ts` following the naming and style of existing interfaces like `SbomSummary` and `AdvisorySummary`.

In `src/api/rest.ts`, add the client function following the pattern of `fetchSboms()`:

```typescript
export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get("/api/v2/sbom/compare", { params: { left: leftId, right: rightId } }).then((res) => res.data);
```

Use the existing `client` Axios instance from `src/api/client.ts` which already has the base URL and auth interceptors configured.

## Applicable Conventions

- **API layer** (Axios client in client.ts, typed functions in rest.ts): Applies: task modifies `src/api/models.ts` and `src/api/rest.ts` matching the convention's API layer scope.
