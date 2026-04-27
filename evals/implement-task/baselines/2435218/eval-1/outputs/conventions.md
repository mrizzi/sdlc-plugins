# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module structure

Every domain module under `modules/fundamental/src/` follows a strict three-directory layout:
- `model/` -- data structures (DTOs, response types)
- `service/` -- business logic (database queries, aggregation)
- `endpoints/` -- HTTP handlers and route registration

Each directory contains a `mod.rs` that re-exports public symbols and registers sub-modules. New files must be registered via `pub mod <name>;` in the corresponding `mod.rs`.

### Endpoint patterns (from `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`)

- **Path extraction**: handlers use `Path<Id>` from Axum to extract path parameters (e.g., `Path(id): Path<Id>` for a single resource lookup).
- **Return type**: all handlers return `Result<Json<T>, AppError>` where `T` is the response struct.
- **Service invocation**: handlers call a method on the corresponding service (e.g., `AdvisoryService::fetch(&self, id, &tx)`) and propagate errors with `.context("descriptive message")`.
- **JSON response**: the struct is returned directly wrapped in `Json(...)` -- Axum handles serialization via `serde::Serialize`.
- **List endpoints**: list handlers return `Result<Json<PaginatedResults<T>>, AppError>` using the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs`.

### Service patterns (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)

- **Method signature**: service methods take `&self`, an identifier (e.g., `sbom_id: Id`), and a `tx: &Transactional<'_>` parameter for database transaction context.
- **Naming**: methods follow `verb_noun` pattern -- `fetch`, `list`, `search`, `ingest`.
- **Error handling**: methods return `Result<T, anyhow::Error>` and use `.context()` wrapping for all fallible operations.
- **Database access**: queries are built using SeaORM's query builder; join tables (e.g., `sbom_advisory`) are used for many-to-many relationships.

### Model patterns (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)

- **Derive macros**: all model structs derive `Debug, Clone, Serialize, Deserialize` (serde).
- **Documentation**: each struct has a doc comment describing what it represents.
- **Field types**: fields use Rust standard types (`String`, `i64`, `Option<T>`) and domain-specific ID types.
- **Module registration**: each new model file must be added as `pub mod <name>;` in the parent `model/mod.rs`.

### Error handling (from `common/src/error.rs`, sibling handlers)

- **Error type**: `AppError` enum implements Axum's `IntoResponse` trait.
- **Wrapping**: all errors are wrapped with `.context("human-readable description")` at each layer boundary.
- **404 pattern**: when a resource is not found, return `AppError::NotFound("resource description")` or equivalent.

### Route registration (from `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs`)

- Routes are registered in the module's `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.
- Each handler function is imported from its own sub-module file.
- The `server/main.rs` mounts all module routers -- no changes needed there for new routes within an existing module.

### Import organization

- Standard library imports first, then external crate imports, then local/crate imports.
- Grouped by category with blank lines between groups.

### Naming conventions

- **Files**: snake_case for all Rust source files (e.g., `severity_summary.rs`).
- **Types**: PascalCase for structs and enums (e.g., `SeveritySummary`, `AdvisoryDetails`).
- **Functions**: snake_case for functions and methods (e.g., `severity_summary`, `fetch`).
- **Constants**: SCREAMING_SNAKE_CASE.

## Test Conventions (from sibling test analysis)

### Test file organization (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)

- Integration tests live in `tests/api/` and are named after the domain entity they test.
- Tests hit a real PostgreSQL test database (not mocks).
- Each test file covers one module's endpoints.

### Assertion style

- **Status code checks**: `assert_eq!(resp.status(), StatusCode::OK)` for success cases, `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases.
- **Body deserialization**: response body is deserialized into the expected struct type, then individual fields are asserted with `assert_eq!`.
- **Value-based assertions**: tests assert on specific field values, not just collection lengths.

### Test naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_sboms_filtered`).

### Error case coverage

- Every endpoint test file includes at least one 404 test for non-existent resource IDs.
- Error responses are checked for correct status code.

### Test structure

- Non-trivial tests use given-when-then section comments (`// Given`, `// When`, `// Then`).
- Each test function has a doc comment (`///`) explaining what it verifies.

### Test setup

- Tests use shared test database setup utilities.
- Test data fixtures are created within each test or via shared helper functions.

### Parameterized tests

- No evidence of `#[rstest]` or parameterized test usage in sibling test files; tests are written as individual functions. New tests should follow this pattern.
