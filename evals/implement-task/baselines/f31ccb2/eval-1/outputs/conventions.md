# Conventions Discovered from Sibling Analysis

## Source Files Inspected

The following sibling files were analyzed (from repository structure and task implementation notes) to extract conventions:

- `modules/fundamental/src/advisory/endpoints/mod.rs` — route registration pattern
- `modules/fundamental/src/advisory/endpoints/get.rs` — endpoint handler pattern (path params, service call, JSON response)
- `modules/fundamental/src/advisory/endpoints/list.rs` — list endpoint pattern
- `modules/fundamental/src/advisory/service/advisory.rs` — service method pattern (`fetch`, `list` methods)
- `modules/fundamental/src/advisory/model/mod.rs` — model module registration pattern
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field
- `modules/fundamental/src/advisory/model/details.rs` — model struct patterns
- `modules/fundamental/src/sbom/endpoints/get.rs` — SBOM endpoint pattern for comparison
- `modules/fundamental/src/sbom/service/sbom.rs` — SBOM service pattern
- `common/src/error.rs` — `AppError` enum and `IntoResponse` implementation
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response type
- `entity/src/sbom_advisory.rs` — join table entity for SBOM-advisory relationships
- `tests/api/advisory.rs` — integration test patterns
- `tests/api/sbom.rs` — SBOM integration test patterns

## Conventions Extracted

### 1. Module Structure (from `modules/fundamental/src/advisory/`)

Each domain concept follows a three-directory pattern:
- `model/` — data structs (DTOs/response types), with `mod.rs` re-exporting submodules
- `service/` — business logic, database queries via SeaORM
- `endpoints/` — Axum HTTP handlers, with `mod.rs` assembling the router

New features within an existing domain add files to these directories rather than creating new top-level modules.

### 2. Endpoint Handler Pattern (from `advisory/endpoints/get.rs`)

```rust
use axum::{extract::Path, Json};
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

pub async fn handler_name(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,  // or State-based injection
    tx: Transactional<'_>,
) -> Result<Json<ResponseType>, AppError> {
    let result = service.method_name(id, &tx).await?;
    Ok(Json(result))
}
```

Key observations:
- Path parameters extracted via `Path<Id>`
- Service injected via Axum extractors (Extension or State)
- Returns `Result<Json<T>, AppError>`
- Errors propagated with `?` operator and `.context()` wrapping

### 3. Route Registration Pattern (from `advisory/endpoints/mod.rs`)

```rust
use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/path", get(handler))
        .route("/other", get(other_handler))
}
```

New routes are added by chaining `.route()` calls on the existing `Router::new()` builder.

### 4. Service Method Pattern (from `advisory/service/advisory.rs`)

```rust
impl AdvisoryService {
    pub async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<Option<AdvisorySummary>, AppError> {
        // SeaORM query
    }

    pub async fn list(&self, /* params */, tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, AppError> {
        // SeaORM query with pagination
    }
}
```

Key observations:
- Methods take `&self`, domain-specific params, and `tx: &Transactional<'_>`
- Return `Result<T, AppError>`
- Use SeaORM entities and query builders
- Error wrapping via `.context("descriptive message")`

### 5. Model/Response Struct Pattern (from `advisory/model/summary.rs`, `advisory/model/details.rs`)

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]
pub struct StructName {
    pub field: Type,
}
```

Key observations:
- Derive `Serialize`, `Deserialize`, `ToSchema` (for OpenAPI)
- Also typically `Clone` and `Debug`
- Fields are `pub`
- `utoipa::ToSchema` used for API documentation generation

### 6. Model Module Registration (from `advisory/model/mod.rs`)

```rust
pub mod summary;
pub mod details;
```

New model submodules are registered by adding `pub mod module_name;` lines.

### 7. Error Handling Pattern (from `common/src/error.rs`)

- `AppError` is an enum implementing `IntoResponse`
- Variants map to HTTP status codes (e.g., NotFound -> 404)
- Service methods use `.context("message")` from anyhow-style error chaining
- Endpoints return `Result<T, AppError>` where AppError auto-converts to HTTP responses

### 8. Entity/Join Table Pattern (from `entity/src/sbom_advisory.rs`)

- SeaORM entities define the database schema
- Join tables like `sbom_advisory` link SBOMs to advisories
- Used in service queries with SeaORM's `find_with_related()` or manual joins

### 9. Integration Test Pattern (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)

- Tests live in `tests/api/` directory
- Each test file corresponds to an API domain
- Tests use a real PostgreSQL database (test fixtures)
- HTTP requests made via test client (likely `reqwest` or Axum's test utilities)
- Tests verify status codes and JSON response bodies
- Pattern: set up test data -> make HTTP request -> assert response

### 10. API Path Convention

- Base path: `/api/v2/`
- Resource-oriented: `/api/v2/sbom/{id}/...`
- Nested resources use the parent resource path as prefix
- Consistent with REST conventions

### 11. Rust/Cargo Convention

- Workspace-based Cargo project with multiple crates
- Each module (`common`, `entity`, `modules/fundamental`, `server`) is a separate crate
- Cross-crate dependencies managed via Cargo workspace
