# Conventions Discovered from Sibling Analysis

## Module Structure Convention

Every domain module under `modules/fundamental/src/` follows a strict tripartite structure:

```
<domain>/
  mod.rs
  model/
    mod.rs
    summary.rs
    details.rs        (optional)
  service/
    mod.rs            (or <domain>.rs re-exported from mod.rs)
  endpoints/
    mod.rs            (route registration)
    list.rs           (GET collection)
    get.rs            (GET single resource)
```

The `advisory` module already has `model/`, `service/`, and `endpoints/` sub-modules. New files must slot into this existing structure.

## Model Conventions

- Model structs live in individual files inside `model/`.
- Each model file is registered via `pub mod <name>;` in `model/mod.rs`.
- Sibling reference: `AdvisorySummary` in `model/summary.rs` contains a `severity` field. `SbomSummary` and `PackageSummary` follow the same single-struct-per-file pattern.
- Structs derive `Serialize`, `Deserialize`, `Debug`, and `Clone`.
- Response structs that are not paginated collections are returned directly (no `PaginatedResults<T>` wrapper).

## Service Conventions

- Service structs are named `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`).
- Methods take `&self` plus domain-specific parameters and a `tx: &Transactional<'_>` for database transaction scoping.
- Pattern from `AdvisoryService`: `fetch`, `list`, `search` methods. New methods follow the same signature style.
- Error handling: methods return `Result<T, anyhow::Error>` (or equivalent), using `.context("descriptive message")` for error wrapping.

## Endpoint Conventions

- Handler functions are async, extract path parameters via `Path<Id>` (Axum extractor).
- Handlers call the service layer, then return `Json(result)` or the struct directly (Axum `IntoResponse`).
- Return type: `Result<Json<T>, AppError>` or `Result<impl IntoResponse, AppError>`.
- Error mapping: service errors are converted to `AppError` using `.context()`.
- Route registration happens in `endpoints/mod.rs` via `Router::new().route("/path", get(handler))` chaining.
- Each endpoint handler lives in its own file (e.g., `get.rs`, `list.rs`).
- Sibling pattern from `endpoints/get.rs`: extracts `Path(id)`, calls service method, maps errors, returns JSON.

## Route Registration Convention

- Each module's `endpoints/mod.rs` builds a `Router` with all routes for that domain.
- `server/main.rs` mounts each module's router. The task notes say "routes auto-mount via module registration," so no changes to `main.rs` are needed.

## Error Handling Convention

- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- `AppError` implements `IntoResponse`, converting errors to appropriate HTTP status codes.
- Context wrapping uses `.context("operation description")` from `anyhow`.
- 404 errors are returned when a resource is not found, consistent across SBOM and advisory endpoints.

## Testing Conventions

- Integration tests live in `tests/api/<domain>.rs`.
- Tests hit a real PostgreSQL test database (not mocked).
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test functions are `#[tokio::test]` async functions.
- Tests use a shared test harness/setup to provision test data and obtain an HTTP client.

## Naming Conventions

- File names: `snake_case.rs` matching the module/struct concept (e.g., `severity_summary.rs` for `SeveritySummary`).
- Struct names: `PascalCase` (e.g., `SeveritySummary`).
- Method names: `snake_case` (e.g., `severity_summary`).
- Endpoint paths: kebab-case with hyphens (e.g., `/api/v2/sbom/{id}/advisory-summary`).

## Dependency/Import Conventions

- Entity references use `entity::` crate imports (e.g., `entity::sbom_advisory`).
- Common utilities imported from `common::` (e.g., `common::error::AppError`, `common::db::query`).
- Cross-module references within `fundamental` use relative paths or `crate::` imports.
