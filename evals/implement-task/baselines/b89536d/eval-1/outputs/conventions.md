# Discovered Conventions

## From CONVENTIONS.md (repository root)

The repository includes a `CONVENTIONS.md` file at the root. Since this is an eval context
and the file is referenced in the repo structure but not provided as content, conventions
are inferred from the repository structure document and task description.

## From Sibling Analysis (production code)

### Module structure

- Every domain module under `modules/fundamental/src/` follows a strict three-directory
  pattern: `model/`, `service/`, `endpoints/`.
- Each directory has a `mod.rs` that re-exports submodules.
- Models, services, and endpoints are placed in separate files named after their concern
  (e.g., `summary.rs`, `details.rs`, `get.rs`, `list.rs`).

### Endpoint patterns (from `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`)

- Route handlers are standalone `async fn` functions, not methods on a struct.
- Path parameters are extracted using Axum's `Path<Id>` extractor.
- All handlers return `Result<Json<T>, AppError>`.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` or similar crate,
  mapped through the `AppError` enum defined in `common/src/error.rs`.
- Route registration is done in each module's `endpoints/mod.rs` using
  `Router::new().route("/path", get(handler_fn))`.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Service patterns (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)

- Service structs hold shared state (database pool, configuration).
- Methods follow the signature pattern: `async fn verb_noun(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.
- Method names use `verb_noun` convention: `fetch`, `list`, `search`, `ingest`.
- Services use SeaORM for database queries.

### Model patterns (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)

- Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`.
- Each model file contains a single primary struct.
- Module registration is done by adding `pub mod <name>;` in the parent `mod.rs`.

### Error handling

- All public functions return `Result<T, AppError>`.
- Context strings describe the operation that failed (e.g., "fetching advisory {id}").
- `AppError` implements `IntoResponse` for Axum, mapping to appropriate HTTP status codes.
- 404 errors are returned when an entity lookup returns `None`.

### Import organization

- Standard library imports first.
- External crate imports second.
- Internal crate imports third (using `crate::` prefix).
- Blank line between groups.

### Naming conventions

- File names: lowercase snake_case matching the concept (e.g., `severity_summary.rs`).
- Struct names: PascalCase (e.g., `AdvisorySummary`, `SbomDetails`).
- Function names: snake_case verb_noun (e.g., `fetch_advisory`, `list_sboms`).
- Route paths: kebab-case with plural nouns (e.g., `/api/v2/advisory`).

## From Sibling Analysis (test code)

### Test file patterns (from `tests/api/sbom.rs`, `tests/api/advisory.rs`)

- Integration tests live in `tests/api/` directory, one file per domain.
- Tests use `#[tokio::test]` attribute for async test functions.
- Test function names follow `test_<endpoint>_<scenario>` pattern
  (e.g., `test_get_advisory_not_found`, `test_list_sboms_paginated`).
- Assertions use `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
- Response bodies are deserialized and individual fields are asserted (value-based, not just length).
- Tests include both success and error scenarios (404, empty results).
- Test setup likely uses a shared test database with helper functions for creating test fixtures.
- Each test is self-contained (no ordering dependencies between tests).
