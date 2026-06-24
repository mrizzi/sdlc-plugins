## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response and a client function to call the comparison endpoint. This establishes the API contract on the frontend, matching the backend's `SbomComparisonResult` response shape.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function using the Axios client

## API Changes
- None (consuming existing backend endpoint)

## Implementation Notes
Add the following interfaces to `src/api/models.ts`, following the existing naming pattern used by other interfaces in that file:

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
  direction: "upgrade" | "downgrade";
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

export interface SbomComparisonResult {
  added_packages: PackageDiff[];
  removed_packages: PackageDiff[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityDiff[];
  resolved_vulnerabilities: VulnerabilityDiff[];
  license_changes: LicenseChange[];
}
```

In `src/api/rest.ts`, add the client function following the pattern of existing functions like `fetchSboms()`:

```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } })
    .then((res) => res.data);
```

Per Key Conventions (API layer): Typed API functions in `src/api/rest.ts`; TypeScript interfaces in `src/api/models.ts`. Applies: task modifies `src/api/models.ts` and `src/api/rest.ts` matching the convention's API layer scope.

## Acceptance Criteria
- [ ] All five interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms` function is exported from `src/api/rest.ts`
- [ ] Function calls `GET /api/v2/sbom/compare` with `left` and `right` query parameters
- [ ] TypeScript compiles without errors (`npx tsc --noEmit`)

## Test Requirements
- [ ] TypeScript type-checking passes with the new interfaces
- [ ] Verify `compareSboms` function signature matches expected API contract

## Dependencies
- Depends on: Task 3 — SBOM comparison endpoint (API contract)

[sdlc-workflow] Description digest: sha256-md:c68fb3e5c5b14c9715893edd3fb3aa05bff1104a79d7b1c8429ff84ecd917acd
