# Task 3: Add API model types, REST client functions, and React Query hooks for remediation endpoints

**Epic**: TC-9006: trustify-ui

## Repository

trustify-ui

## Target Branch

main

## Description

Add TypeScript interfaces for remediation API response types, Axios-based REST client functions for the two new remediation endpoints, and React Query hooks for data fetching. This task establishes the data layer that the dashboard UI components will consume.

## Acceptance Criteria

- [ ] TypeScript interfaces defined for `RemediationSummary`, `RemediationSeverityCount`, and `ProductRemediationSummary`
- [ ] REST client functions `fetchRemediationSummary()` and `fetchRemediationByProduct()` added using the Axios client instance
- [ ] React Query hook `useRemediationSummary` wraps the summary fetch with proper query key
- [ ] React Query hook `useRemediationByProduct` wraps the by-product fetch with pagination support
- [ ] All types, functions, and hooks follow existing naming conventions (camelCase for hooks/utilities, PascalCase for types)

## Files to Modify

- `src/api/models.ts` -- add RemediationSummary, RemediationSeverityCount, and ProductRemediationSummary interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() functions

## Files to Create

- `src/hooks/useRemediationSummary.ts` -- React Query hook for remediation summary data
- `src/hooks/useRemediationByProduct.ts` -- React Query hook for by-product breakdown data

## Implementation Notes

- Add TypeScript interfaces to `src/api/models.ts` alongside existing API response types
- REST functions in `src/api/rest.ts` should use the Axios instance from `src/api/client.ts`, following the pattern of existing functions like `fetchSboms()` and `fetchAdvisories()`
- React Query hooks follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`: use `useQuery` with descriptive query keys
- The by-product hook should accept pagination parameters matching the backend's `PaginatedResults` response structure

## Convention-Aware Enrichment

- **API layer**: Applies: task modifies `src/api/models.ts` and `src/api/rest.ts` matching the convention's API layer scope.
- **Naming**: Applies: task creates `src/hooks/useRemediationSummary.ts` and `src/hooks/useRemediationByProduct.ts` matching the convention's camelCase hook naming scope.

## Test Requirements

- Unit test for `useRemediationSummary` hook verifying correct query key and data transformation
- Unit test for `useRemediationByProduct` hook verifying pagination parameter handling
- MSW handlers added to `tests/mocks/handlers.ts` for both remediation endpoints
- Mock fixtures added to `tests/mocks/fixtures/` for remediation response data
