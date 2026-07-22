# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Module Structure

- **Domain module pattern**: Each domain module (sbom, advisory, package) follows a consistent `model/ + service/ + endpoints/` structure within `modules/fundamental/src/`.
- **Model sub-modules**: Each model directory contains a `mod.rs` that re-exports sub-modules. Models are split by purpose: `summary.rs` for list/overview responses, `details.rs` for full-detail responses.
- **Service files**: Service implementations live in dedicated files named after the domain entity (e.g., `sbom.rs` for SbomService, `advisory.rs` for AdvisoryService). The `mod.rs` in the service directory re-exports them.
- **Endpoint files**: Each endpoint action gets its own file (e.g., `list.rs`, `get.rs`). The `mod.rs` in the endpoints directory registers all routes.

### Naming Conventions

- **Structs**: PascalCase domain noun + role suffix (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`).
- **Service methods**: Follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`). The new method should be named `severity_summary` to describe its action.
- **Endpoint handler functions**: Named after the action (e.g., `list`, `get`). The new handler should be named `severity_summary` or `get_severity_summary`.
- **File naming**: Snake_case matching the primary concept (e.g., `severity_summary.rs` for the SeveritySummary struct/handler).
- **Route paths**: RESTful, lowercase with hyphens (e.g., `/api/v2/sbom/{id}/advisory-summary`).

### Error Handling

- All endpoint handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`.
- Error wrapping uses `.context()` method for adding context to errors before returning.
- 404 errors for missing entities follow the pattern used by existing SBOM and advisory endpoints.

### Response Types

- Single-entity endpoints return the struct directly (Axum's `Json` extractor handles serialization).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new endpoint returns a single aggregate object, so it should return the struct directly (not paginated).

### Framework Patterns

- **HTTP Framework**: Axum -- path parameters extracted via `Path<Id>` extractor.
- **ORM**: SeaORM for database queries.
- **Route registration**: Each module's `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern. Routes are auto-mounted by `server/src/main.rs` via module registration.
- **Caching**: Uses `tower-http` caching middleware configured in endpoint route builders.

### Import Organization

- Standard library imports first, then external crate imports, then internal module imports.
- Use statements grouped by crate with blank lines between groups.

### Service Method Signatures

- Service methods take `&self` as the first parameter.
- Entity ID parameters use the `Id` type.
- Transaction context passed as `tx: &Transactional<'_>` parameter.
- Pattern from existing methods: `async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.

### Database Patterns

- Join tables follow `<entity1>_<entity2>` naming (e.g., `sbom_advisory`, `sbom_package`).
- Entity definitions live in `entity/src/` as SeaORM entities.
- Queries use SeaORM's query builder with shared helpers from `common/src/db/query.rs`.

### Endpoint Registration Pattern

- Routes registered in `endpoints/mod.rs` using:
  ```rust
  Router::new()
      .route("/path", get(handler_function))
  ```
- Each handler imported from its own file in the endpoints directory.

## Test Conventions

### Test File Organization

- Integration tests live in `tests/api/` directory, one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database (not mocked).

### Assertion Style

- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and fields checked individually.
- For error cases: `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Response Validation

- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Single-entity tests validate specific field values after deserialization.

### Error Case Coverage

- All endpoint tests include a 404 test for non-existent entity IDs.
- Error tests verify both the status code and (where applicable) the error response body.

### Test Naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`, `test_get_sbom_not_found`).

### Test Documentation

- Per skill requirements, every test function must have a `///` doc comment explaining what it verifies (this is an AI-generated standard applied regardless of sibling patterns).
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

### Test Structure

- Tests use setup helpers to create test data (SBOMs, advisories) in the test database.
- Each test is independent -- does not rely on state from other tests.
- Cleanup happens automatically via test database transaction rollback.

### Parameterized Tests

- Would check siblings for `#[rstest]` or `#[case]` usage. If siblings do not use parameterized tests, follow their pattern and use individual test functions instead.

## Conventions from CONVENTIONS.md

- Would read `CONVENTIONS.md` at repository root for explicit project-level conventions.
- Would extract CI check commands (e.g., formatting, linting, type checking, compilation).
- Would extract code generation commands if any.
- These would be recorded for use in Step 9 verification.

## Convention Conflicts

No conflicts detected between the task description's Implementation Notes and the discovered conventions. The Implementation Notes align with all observed patterns:
- Path<Id> extraction matches the sibling endpoint pattern
- Service method signature matches existing fetch/list methods
- AppError with .context() matches error handling convention
- Route registration matches Router::new().route() pattern
