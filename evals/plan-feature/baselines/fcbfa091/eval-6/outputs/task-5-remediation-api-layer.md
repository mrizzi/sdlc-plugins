## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for remediation API response types, API client functions for fetching remediation data, and React Query hooks for consuming the remediation endpoints. This establishes the frontend data layer for the remediation dashboard.

## Files to Modify
- `src/api/models.ts` — Add `RemediationSummary`, `SeverityBreakdown`, `ProductRemediation`, and `PaginatedProductRemediation` TypeScript interfaces
- `src/api/rest.ts` — Add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for fetching remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for fetching per-product remediation data with pagination parameters

## Implementation Notes
Follow the existing API layer pattern:
1. Define interfaces in `src/api/models.ts` matching the backend response schemas
2. Add fetch functions in `src/api/rest.ts` using the Axios client from `src/api/client.ts`
3. Create React Query hooks in `src/hooks/` following the pattern from `src/hooks/useSboms.ts`

Per CONVENTIONS.md: API client functions go in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`; React Query hooks go in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

Per CONVENTIONS.md: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useRemediationSummary.ts` and `src/hooks/useRemediationByProduct.ts` matching the convention's `.ts` file scope.

The `RemediationSummary` interface should mirror the backend struct:
```typescript
interface SeverityBreakdown {
  severity: string;
  open: number;
  inProgress: number;
  resolved: number;
}

interface RemediationSummary {
  totalOpen: number;
  totalInProgress: number;
  totalResolved: number;
  bySeverity: SeverityBreakdown[];
}
```

The React Query hooks should use descriptive query keys (e.g., `["remediation", "summary"]` and `["remediation", "by-product", params]`) for proper cache management.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for all API calls
- `src/api/rest.ts::fetchSboms()` — Reference for API client function pattern with pagination parameters
- `src/hooks/useSboms.ts` — Reference for React Query hook pattern with query parameters
- `src/hooks/useAdvisories.ts` — Reference for list-type React Query hook with pagination

## Acceptance Criteria
- [ ] `RemediationSummary` and `ProductRemediation` TypeScript interfaces match the backend response schemas
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` and returns typed data
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` with pagination params
- [ ] `useRemediationSummary` hook provides loading, error, and data states
- [ ] `useRemediationByProduct` hook accepts pagination parameters and provides loading, error, and data states
- [ ] All new code passes TypeScript type checking without errors

## Test Requirements
- [ ] Type-check: `tsc --noEmit` passes with new interfaces and hooks
- [ ] Hook renders without error in a test component using React Testing Library

## Dependencies
- Depends on: Task 3 — Remediation endpoints (backend API must be defined)

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
