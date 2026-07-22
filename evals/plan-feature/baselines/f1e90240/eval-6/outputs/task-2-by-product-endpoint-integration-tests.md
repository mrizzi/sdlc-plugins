# Task 2: Add by-product remediation endpoint and integration tests

**Epic**: TC-9006: trustify-backend

## Repository

trustify-backend

## Target Branch

main

## Description

Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. Also add comprehensive integration tests for both remediation endpoints (summary and by-product) following the project's integration testing pattern.

## Acceptance Criteria

- [ ] `GET /api/v2/remediation/by-product` endpoint returns per-product remediation breakdown
- [ ] Each product entry includes `product_name`, `total`, `open`, `in_progress`, and `resolved` counts
- [ ] Response supports pagination via `PaginatedResults<T>` wrapper
- [ ] Integration tests cover both `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`
- [ ] Integration tests verify correct status codes, response schemas, and aggregation accuracy
- [ ] Endpoint handles portfolios with >50 products via pagination
- [ ] All handlers return `Result<T, AppError>` with `.context()` wrapping

## Files to Modify

- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register the by-product route
- `modules/fundamental/src/remediation/service/mod.rs` -- add by-product aggregation query

## Files to Create

- `modules/fundamental/src/remediation/model/by_product.rs` -- ProductRemediationSummary struct
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints

## API Changes

- **New endpoint**: `GET /api/v2/remediation/by-product`
  - Response: `PaginatedResults<ProductRemediationSummary>` with each entry containing `product_name`, `total`, `open`, `in_progress`, `resolved`
  - Supports standard pagination query parameters

## Implementation Notes

- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for list endpoints returning `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Use `common/src/db/query.rs` for pagination and sorting helpers
- Integration tests follow the pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`: hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` assertions
- Error handling must use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`
- Large portfolios (>50 products) require proper pagination support, matching the existing `PaginatedResults<T>` convention

## Convention-Aware Enrichment

- **Module pattern**: Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's domain module structure scope.
- **Error handling**: Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's handler return type scope.
- **Response types**: Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's PaginatedResults response wrapper scope.
- **Query helpers**: Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's shared query builder scope.
- **Testing**: Applies: task creates `tests/api/remediation.rs` matching the convention's integration test scope.

## Test Requirements

- Integration test: `GET /api/v2/remediation/summary` returns 200 with correct severity-by-status breakdown
- Integration test: `GET /api/v2/remediation/by-product` returns 200 with per-product counts
- Integration test: by-product endpoint pagination works correctly
- Integration test: endpoints return empty results gracefully when no vulnerability data exists
