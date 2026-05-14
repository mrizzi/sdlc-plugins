# Conventions Discovered from Sibling Analysis

## Module Structure Convention

Every domain module under `modules/fundamental/src/` follows a strict tri-directory pattern:

```
<domain>/
  mod.rs
  model/
    mod.rs
    summary.rs
    details.rs       (optional, for detail views)
  service/
    mod.rs            (or <domain>.rs)
  endpoints/
    mod.rs            (route registration)
    list.rs           (GET collection)
    get.rs            (GET single resource)
```

Observed in: `sbom/`, `advisory/`, `package/`.

New files for advisory severity summary should follow this same layout, adding files inside the existing `advisory/` module rather than creating a new top-level module.

## Error Handling Pattern

- All endpoint handlers return `Result<T, AppError>`.
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`.
- Errors are wrapped with `.context("descriptive message")` (anyhow-style) before being propagated with `?`.
- 404 cases: when a resource lookup returns `None`, the convention is to return an `AppError` not-found variant with context describing which resource was missing.

## Endpoint Registration Pattern

- Each module's `endpoints/mod.rs` builds a `Router` using `Router::new().route("/path", get(handler))` chaining.
- The server's `main.rs` mounts all module routers -- no manual registration needed in `main.rs` when adding routes within an existing module.
- Path parameters use Axum's `Path<Id>` extractor.
- Handlers are async functions that take extractors as arguments and return `Result<Json<T>, AppError>`.

## Service Method Pattern

- Services are structs with methods like `fetch`, `list`, `search`.
- Methods accept `&self`, the resource identifier, and a `tx: &Transactional<'_>` parameter for database transaction context.
- Database queries use SeaORM entities and the join tables in `entity/src/`.
- The `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) links SBOMs to advisories.

## Response Type Conventions

- Single-resource endpoints return `Json<T>` directly (the struct derives `Serialize`).
- Collection endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new severity summary endpoint is a single-resource aggregation, so it should return `Json<SeveritySummary>` directly (not paginated).

## Model Struct Conventions

- Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`.
- Fields use snake_case naming (Rust convention; serde serializes to snake_case by default).
- The `AdvisorySummary` struct in `model/summary.rs` includes a `severity` field -- this is the field to aggregate over.

## Testing Conventions

- Integration tests live in `tests/api/<domain>.rs`.
- Tests use a real PostgreSQL test database (not mocks).
- Assertions follow the pattern: `assert_eq!(resp.status(), StatusCode::OK)`.
- Test function naming: `test_<action>_<scenario>` (e.g., `test_get_sbom`, `test_list_advisories`).
- Tests set up fixtures, make HTTP requests against the test server, and assert on status codes and response bodies.

## Naming Conventions

- File names: snake_case, matching the concept (e.g., `severity_summary.rs`).
- Struct names: PascalCase (e.g., `SeveritySummary`).
- Route paths: kebab-case (e.g., `/api/v2/sbom/{id}/advisory-summary`).
- Module re-exports: each `mod.rs` declares `pub mod <submodule>;` for every file in the directory.

## Deduplication Convention

- When aggregating across join tables, unique counts should deduplicate by the entity's primary key (advisory ID in this case) to avoid inflated counts from many-to-many relationships.
