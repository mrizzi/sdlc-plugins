# Implementation Plan: TC-9201 — Add Advisory Severity Aggregation Service and Endpoint

## Branch

```
TC-9201/add-advisory-severity-aggregation
```

## Pre-Implementation Inspection

Before making any changes, the following files must be read and analyzed to understand existing conventions, types, and patterns:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Understand the existing GET handler pattern: how path parameters are extracted (via `Path<Id>`), how the service is called, how errors are returned, and how JSON responses are structured. This is the primary sibling to model the new endpoint after.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Understand the `AdvisoryService` struct, its constructor, the signatures of `fetch` and `list` methods, how `Transactional` is threaded through, and the return types used. The new `severity_summary` method must follow this exact pattern.

3. **`modules/fundamental/src/advisory/model/summary.rs`** — Understand the `AdvisorySummary` struct and its `severity` field. This tells us what severity representation is already in use (likely a string or enum) and how advisories are modeled at the domain layer.

4. **`modules/fundamental/src/advisory/model/mod.rs`** — Understand how model sub-modules are registered (the `pub mod` declarations) so the new `severity_summary` module is added consistently.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Understand how routes are composed via `Router::new().route(...)` so the new route is registered in the correct location and style.

6. **`common/src/error.rs`** — Understand the `AppError` enum, its variants, how `.context()` wrapping works, and how 404 responses are produced for missing entities.

7. **`entity/src/sbom_advisory.rs`** — Understand the `sbom_advisory` join table entity: its columns (especially `sbom_id` and `advisory_id`), relations, and how to query it with SeaORM.

8. **`common/src/model/paginated.rs`** — Understand `PaginatedResults<T>` to confirm the new endpoint does NOT use pagination (it returns a single summary object, not a list).

9. **`tests/api/`** — Read at least one existing integration test file to understand the test harness setup, how the test database is provisioned, how HTTP requests are made, and how responses are asserted.

10. **`server/src/main.rs`** — Confirm that routes auto-mount via module registration and no changes are needed here.

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`

**Change**: Add `pub mod severity_summary;` declaration to register the new model module.

**Details**: Insert a new line `pub mod severity_summary;` alongside the existing module declarations (e.g., next to `pub mod summary;`). This makes the `SeveritySummary` struct importable from the model layer.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`

**Change**: Add a `severity_summary` method to `AdvisoryService`.

**Details**: The new method follows the same signature pattern as `fetch` and `list`:
- Takes `&self, sbom_id: Id, tx: &Transactional<'_>`
- Queries the `sbom_advisory` join table to find all advisories linked to the given SBOM
- For each linked advisory, loads the `AdvisorySummary` to access its `severity` field
- Deduplicates by advisory ID (using a `HashSet` or `SELECT DISTINCT`)
- Counts advisories per severity level (Critical, High, Medium, Low)
- Returns `Result<SeveritySummary, AppError>`
- Returns 404 (via `AppError`) if the SBOM ID does not exist

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`

**Change**: Register the new route for the severity summary endpoint.

**Details**: Add:
- `mod severity_summary;` declaration at the top
- A new `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))` call in the router chain, following the pattern of existing route registrations.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

**Contents**: A new `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    pub critical: u32,
    pub high: u32,
    pub medium: u32,
    pub low: u32,
    pub total: u32,
}
```

Key design decisions:
- `Default` derive ensures all fields start at 0
- `ToSchema` for OpenAPI documentation
- `u32` for counts (non-negative integers, sufficient range)
- `total` is the sum of all severity counts for convenience

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Contents**: A GET handler following the pattern in `get.rs`:

```rust
use actix_web::{web, HttpResponse};
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::db::Transactional;
use trustify_common::error::AppError;
use trustify_common::id::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    responses(
        (status = 200, description = "Advisory severity summary for the SBOM", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
)]
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("Error fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Key design decisions:
- Follows the exact pattern from `get.rs`: `Path<Id>` extraction, `State<AdvisoryService>`, `Result<Json<T>, AppError>`
- Uses `.context()` for error wrapping per `common/src/error.rs` pattern
- Includes utoipa annotations for OpenAPI spec generation
- Note: The exact imports and framework types (Axum vs Actix) will be confirmed during pre-implementation inspection. The code above assumes Axum based on the task description.

### 6. `tests/api/advisory_summary.rs`

**Contents**: Integration tests covering all acceptance criteria:

```rust
// Test 1: Valid SBOM with known advisories returns correct severity counts
// - Set up test DB with an SBOM linked to advisories of known severities
// - Call GET /api/v2/sbom/{id}/advisory-summary
// - Assert response status is 200
// - Assert JSON body has correct counts for each severity level
// - Assert total equals sum of all severity counts

// Test 2: Non-existent SBOM ID returns 404
// - Call GET /api/v2/sbom/{nonexistent-id}/advisory-summary
// - Assert response status is 404

// Test 3: SBOM with no advisories returns all zeros
// - Set up test DB with an SBOM that has no linked advisories
// - Call GET /api/v2/sbom/{id}/advisory-summary
// - Assert response status is 200
// - Assert JSON body: { critical: 0, high: 0, medium: 0, low: 0, total: 0 }

// Test 4: Duplicate advisory links are deduplicated
// - Set up test DB with an SBOM linked to the same advisory multiple times
// - Call GET /api/v2/sbom/{id}/advisory-summary
// - Assert the advisory is counted only once in the severity summary
```

The test file will follow the existing integration test patterns discovered during pre-implementation inspection (test harness setup, DB provisioning, HTTP client usage, assertion style).

## Files NOT Modified

### `server/src/main.rs`

No changes needed. The task description confirms that routes auto-mount via module registration. The new route registered in `modules/fundamental/src/advisory/endpoints/mod.rs` will be automatically picked up by the server's router composition.

## Commit

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated counts of advisory severities (critical, high, medium, low)
for a given SBOM. This enables dashboard widgets to render severity
breakdowns without client-side counting.

Changes:
- Add SeveritySummary response model
- Add severity_summary method to AdvisoryService
- Add GET handler and route registration
- Add integration tests for the new endpoint

Refs: TC-9201
```

### Git Commit Command

```bash
git add \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  modules/fundamental/src/advisory/model/mod.rs \
  modules/fundamental/src/advisory/service/advisory.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  tests/api/advisory_summary.rs

git commit -m "$(cat <<'EOF'
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated counts of advisory severities (critical, high, medium, low)
for a given SBOM. This enables dashboard widgets to render severity
breakdowns without client-side counting.

Changes:
- Add SeveritySummary response model
- Add severity_summary method to AdvisoryService
- Add GET handler and route registration
- Add integration tests for the new endpoint

Refs: TC-9201
EOF
)" --trailer="Assisted-by: Claude Code"
```
