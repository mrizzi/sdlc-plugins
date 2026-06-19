# Repository Impact Map — TC-9001

## Feature
**TC-9001**: Add advisory severity aggregation endpoint

## Workflow Mode
**direct-to-main** — Single-repo backend-only feature with no breaking changes. All tasks target `main` directly.

## Repository: trustify-backend

### Changes by Area

#### 1. Model Layer — Advisory Summary Response Struct
- **Create** `modules/fundamental/src/sbom/model/advisory_summary.rs` — New `AdvisorySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields
- **Modify** `modules/fundamental/src/sbom/model/mod.rs` — Re-export the new `advisory_summary` module

#### 2. Service Layer — Aggregation Query
- **Create** `modules/fundamental/src/sbom/service/advisory_summary.rs` — Service method to query severity counts from the `sbom_advisory` join table, deduplicating by advisory ID
- **Modify** `modules/fundamental/src/sbom/service/mod.rs` — Re-export the new service module

#### 3. Endpoint Layer — Handler and Route Registration
- **Create** `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — `GET /api/v2/sbom/{id}/advisory-summary` handler with optional `threshold` query param
- **Modify** `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route with 5-minute cache configuration

#### 4. Server — Route Mounting
- **Modify** `server/src/main.rs` — Verify SBOM module routes are mounted (should already include the new endpoint via `endpoints/mod.rs`)

#### 5. Integration Tests
- **Create** `tests/api/sbom_advisory_summary.rs` — Integration tests for the new endpoint (happy path, 404, threshold filter, caching)
- **Modify** `tests/Cargo.toml` — Add the new test file to the test suite if needed

## Task Dependency Graph

```
Task 1 (model) ──┐
                  ├── Task 3 (service) ── Task 4 (endpoint + routes) ── Task 5 (integration tests)
Task 2 (entity) ─┘
```

## Tasks

| # | Title | Dependencies |
|---|---|---|
| 1 | Create AdvisorySeveritySummary response model | None |
| 2 | Verify sbom_advisory entity supports severity aggregation | None |
| 3 | Add advisory summary aggregation service method | Task 1, Task 2 |
| 4 | Create advisory-summary endpoint with caching | Task 3 |
| 5 | Add integration tests for advisory-summary endpoint | Task 4 |
