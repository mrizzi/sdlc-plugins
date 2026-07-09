## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Extend the remediation module to add a `GET /api/v2/remediation/by-product` endpoint that returns a per-product remediation breakdown. Each product entry includes total vulnerability count, open count, and resolved count. This endpoint supports the frontend's product filtering capability on the remediation dashboard.

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` -- ProductRemediation struct with total/open/resolved counts per product
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` -- add `pub mod by_product;` declaration
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register by-product route
- `modules/fundamental/src/remediation/service/remediation.rs` -- add by-product aggregation method to RemediationService

## API Changes
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown with total, open, and resolved counts per product

## Implementation Notes
- Per CONVENTIONS.md $Module Pattern: add model and endpoint files following the established pattern in the remediation module created in Task 2. See `modules/fundamental/src/sbom/model/summary.rs` for a reference model struct.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md $Error Handling: return `Result<T, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/endpoints/list.rs` for a reference handler.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's .rs endpoint scope.
- Per CONVENTIONS.md $Response Types: use `PaginatedResults<ProductRemediation>` for the response wrapper to support pagination for large portfolios (>50 products). See `common/src/model/paginated.rs` for the wrapper definition.
  Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's Rust response type scope.
- The aggregation query joins SBOM-Package and SBOM-Advisory relationships to compute per-product remediation counts from existing tables.
- Support pagination for large portfolios as noted in Customer Considerations.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for paginated product lists
- `common/src/db/query.rs` -- pagination and sorting helpers
- `modules/fundamental/src/remediation/service/remediation.rs::RemediationService` -- extend with by-product aggregation method

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with per-product breakdown
- [ ] Each product entry includes total, open, and resolved counts
- [ ] Response supports pagination for large product portfolios
- [ ] No new database tables or migrations are created

## Test Requirements
- [ ] Verify the by-product endpoint returns correct per-product counts with known test data
- [ ] Verify the endpoint returns an empty list when no products have remediation data
- [ ] Verify pagination works correctly for large product sets

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation module with summary aggregation service and endpoint
