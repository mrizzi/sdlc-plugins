## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the RemediationSummary model struct and add an aggregation service method that computes remediation status counts from existing advisory and vulnerability data. The model captures counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved). The service method queries existing entity tables using SQL GROUP BY aggregations for performance.

## Files to Create
- `modules/fundamental/src/advisory/model/remediation_summary.rs` — RemediationSummary struct with severity x status count fields, plus ProductRemediation struct for per-product breakdown

## Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` — Add `pub mod remediation_summary;` declaration and re-export
- `modules/fundamental/src/advisory/service/advisory.rs` — Add `get_remediation_summary()` and `get_remediation_by_product()` methods to the existing AdvisoryService

## Implementation Notes
The RemediationSummary model should contain:
- Counts grouped by severity (Critical/High/Medium/Low) and status (Open/InProgress/Resolved)
- A total count field for convenience
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone`

The ProductRemediation model should contain:
- Product identifier and name
- Total, open, in-progress, and resolved vulnerability counts
- Support wrapping in `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs`

Service implementation:
- Reuse `common/src/db/query.rs` for shared query builder helpers
- Reuse `common/src/model/paginated.rs::PaginatedResults<T>` for the by-product response
- Reuse `common/src/error.rs::AppError` for error types
- Query existing entities in `entity/src/advisory.rs` and related tables
- Use SQL GROUP BY for aggregation rather than in-memory computation

Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context(). Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's .rs scope.

Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ structure. Applies: task modifies modules/fundamental/src/advisory/model/mod.rs matching the convention's .rs module scope.

## Acceptance Criteria
- [ ] RemediationSummary struct contains severity x status count matrix with total
- [ ] ProductRemediation struct contains product identifier, name, total, open, in-progress, and resolved counts
- [ ] `get_remediation_summary()` returns aggregated counts from existing entity tables via SQL GROUP BY
- [ ] `get_remediation_by_product()` returns paginated per-product breakdown using PaginatedResults
- [ ] All service methods return `Result<T, AppError>` with contextual error wrapping via `.context()`
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test for RemediationSummary struct serialization round-trip
- [ ] Unit test for ProductRemediation struct serialization round-trip
- [ ] Service method returns correct aggregation for known test data

## Dependencies
None (first task in the chain)

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
