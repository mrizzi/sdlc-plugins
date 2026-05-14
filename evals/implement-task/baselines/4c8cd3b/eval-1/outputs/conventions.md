# Discovered Conventions (from Sibling Analysis)

## Production Code Conventions

### Module structure
- Each domain module follows a strict `model/ + service/ + endpoints/` directory layout.
- The `model/` directory contains one file per struct (e.g., `summary.rs`, `details.rs`) plus a `mod.rs` that re-exports them with `pub mod` declarations.
- The `service/` directory contains domain-specific service structs with methods following a `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- The `endpoints/` directory contains one file per route handler (e.g., `list.rs`, `get.rs`) plus a `mod.rs` for route registration.

### Endpoint handler pattern
- Handlers extract path parameters via `Path<Id>` (Axum extractor).
- Handlers call a service method, then return the result directly (Axum's `Json` extractor handles serialization).
- All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`.
- Route registration uses `Router::new().route("/path", get(handler))` pattern in each module's `endpoints/mod.rs`.

### Service method pattern
- Service methods take `&self` as the first parameter.
- Database-accessing methods take a transaction parameter: `tx: &Transactional<'_>`.
- Service methods follow the naming pattern: `fetch` (single item by ID), `list` (paginated collection), `search` (filtered query).

### Response types
- Single-item endpoints return the domain struct directly (e.g., `SbomDetails`, `AdvisoryDetails`).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Error handling
- All errors use the `AppError` enum from `common/src/error.rs`.
- Errors are wrapped with `.context()` to add human-readable context strings.
- 404 errors are returned when an entity is not found by ID, consistent across all `fetch`-style endpoints.

### Naming conventions
- Files: lowercase snake_case matching the primary struct or concept (e.g., `summary.rs` for `SbomSummary`).
- Structs: PascalCase with domain prefix (e.g., `AdvisorySummary`, `SbomDetails`).
- Service structs: `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`).
- Module registration: `pub mod <module_name>;` in parent `mod.rs`.

### Import organization
- Framework imports (Axum, SeaORM) first, then crate-internal imports, then local module imports.

### Database access
- SeaORM is used for all database operations.
- Join tables exist for many-to-many relationships (e.g., `sbom_advisory`, `sbom_package`).
- Entities are defined in the top-level `entity/` crate.

## Test Conventions

### Test location
- Integration tests live in `tests/api/` with one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).

### Assertion style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and fields are checked with `assert_eq!`.
- 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test setup
- Tests hit a real PostgreSQL test database.
- Test data is created via fixtures or direct database insertion before assertions.

### Error case coverage
- All endpoint test files include at least one 404 test for non-existent entity IDs.
