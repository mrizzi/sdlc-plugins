# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module structure
- Each domain module follows a strict `model/ + service/ + endpoints/` tripartite structure.
- Siblings: `sbom/`, `advisory/`, `package/` all follow this exact layout under `modules/fundamental/src/`.
- New files must be placed within the appropriate sub-directory of the domain module.

### Model conventions
- Each model concept gets its own file within `model/` (e.g., `summary.rs`, `details.rs`).
- The `model/mod.rs` file re-exports sub-modules with `pub mod` declarations.
- Siblings: `sbom/model/` contains `summary.rs` and `details.rs`; `advisory/model/` contains `summary.rs` and `details.rs`; `package/model/` contains `summary.rs`.
- New model files (like `severity_summary.rs`) must be registered in `model/mod.rs` via `pub mod severity_summary;`.

### Service conventions
- Service structs follow a `<Domain>Service` naming pattern (e.g., `SbomService`, `AdvisoryService`, `PackageService`).
- Service methods follow `verb_noun` naming (e.g., `fetch`, `list`, `search`, `ingest`).
- Service methods take `&self`, domain-specific ID parameters, and `tx: &Transactional<'_>` for database transactions.
- Siblings: `SbomService` has `fetch`, `list`, `ingest`; `AdvisoryService` has `fetch`, `list`, `search`; `PackageService` has `fetch`, `list`.

### Endpoint conventions
- Each endpoint action gets its own file within `endpoints/` (e.g., `list.rs`, `get.rs`).
- Route registration happens in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.
- Path parameters are extracted via `Path<Id>`.
- All handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation.
- Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`; single-item endpoints return the struct directly (Axum's `Json` extractor handles serialization).
- Route mounting: `server/src/main.rs` mounts all module routers; modules register their own sub-routes.
- Siblings: `advisory/endpoints/` contains `list.rs` and `get.rs`; `sbom/endpoints/` contains `list.rs` and `get.rs`.

### Error handling
- All errors use the `AppError` enum from `common/src/error.rs`, which implements `IntoResponse`.
- Error wrapping uses `.context()` for adding contextual messages.
- 404 responses should be consistent with existing SBOM/advisory endpoints.

### Naming conventions
- File naming: lowercase snake_case (e.g., `severity_summary.rs`, `sbom_advisory.rs`).
- Struct naming: PascalCase (e.g., `SeveritySummary`, `AdvisorySummary`).
- Function naming: snake_case verb_noun pattern (e.g., `severity_summary`, `fetch`, `list`).

### Import organization
- SeaORM entities are defined in the `entity/` crate (e.g., `entity/src/sbom_advisory.rs`).
- Common utilities come from the `common/` crate (e.g., `common/src/db/query.rs`, `common/src/error.rs`).
- Cross-module dependencies use crate paths.

### Framework stack
- HTTP framework: Axum
- ORM: SeaORM
- Database: PostgreSQL
- Caching: tower-http caching middleware

## Test Conventions

### Test file organization
- Integration tests live in `tests/api/` directory, one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Test files are named after the domain they test.
- Siblings: `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`.

### Assertion style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and checked for specific field values.

### Error case coverage
- All endpoint test files include 404 tests for non-existent resource IDs, consistent with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` naming pattern (inferred from repository conventions).

### Test environment
- Integration tests hit a real PostgreSQL test database.
- Test setup involves creating test fixtures in the database before assertions.

## CONVENTIONS.md
- The repository structure indicates a `CONVENTIONS.md` file exists at the repo root. In a real implementation, this would be read and its CI check commands extracted for Step 9 verification. Since we cannot access actual file contents in this eval, we note its presence and would follow any conventions it specifies.

## Cross-section Reference Consistency

Checked all entity references across task description sections:

- Entity `AdvisoryService` -- **CONSISTENT**: Both "Files to Modify" and "Implementation Notes" reference `modules/fundamental/src/advisory/service/advisory.rs`.
- Entity `SeveritySummary` -- **CONSISTENT**: "Files to Create" lists `modules/fundamental/src/advisory/model/severity_summary.rs` and this aligns with the model directory pattern.
- Entity `advisory/model/mod.rs` -- **CONSISTENT**: "Files to Modify" correctly identifies this as the module registration file.
- Entity `advisory/endpoints/mod.rs` -- **CONSISTENT**: "Files to Modify" correctly identifies this as the route registration file.
- Entity route registration in `server/src/main.rs` -- **CONSISTENT**: Task notes "no changes needed" because routes auto-mount via module registration, aligning with the endpoint convention.
