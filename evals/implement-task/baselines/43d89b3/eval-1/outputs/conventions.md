# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module structure
- Each domain module follows the `model/ + service/ + endpoints/` directory structure.
- `model/mod.rs` re-exports submodules (`pub mod summary;`, `pub mod details;`).
- `service/mod.rs` re-exports the service implementation file (e.g., `pub mod advisory;`).
- `endpoints/mod.rs` registers routes and re-exports handler submodules.

### Naming conventions
- Model structs use PascalCase nouns: `AdvisorySummary`, `SbomDetails`, `PackageSummary`.
- Service structs use PascalCase `<Domain>Service`: `AdvisoryService`, `SbomService`, `PackageService`.
- Service methods use `verb_noun` or short verb names: `fetch`, `list`, `search`, `ingest`.
- Endpoint handler files are named after their HTTP action: `get.rs`, `list.rs`.
- Endpoint handler functions follow the file name (e.g., `get` in `get.rs`, `list` in `list.rs`).

### Error handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`.
- Error wrapping uses `.context("descriptive message")` from the anyhow/error chain pattern.
- 404 responses are returned via `AppError` when an entity is not found, consistent across SBOM and advisory endpoints.

### Endpoint registration
- Each module's `endpoints/mod.rs` builds a `Router` using `Router::new().route("/path", get(handler))`.
- `server/main.rs` mounts all module routers; individual modules do not touch `main.rs` for route registration (auto-mount pattern).

### Response types
- Single-entity endpoints return the struct directly (Axum's `Json` extractor handles serialization).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Non-list aggregate endpoints (like the new severity summary) return a dedicated response struct.

### Import organization
- Framework imports (axum, serde) come first, followed by crate-internal imports.
- `use` statements are grouped by crate.

### Service method signatures
- Service methods take `&self` as the first parameter.
- Entity identifiers are passed as typed `Id` parameters.
- Transaction context is passed as `tx: &Transactional<'_>`.
- Pattern: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.

### Endpoint handler signatures
- Path parameters extracted via `Path<Id>` (from axum).
- Service accessed through shared state / extension.
- Handlers are `async fn` returning `Result<Json<T>, AppError>`.

### Serialization
- Response structs derive `Serialize` (from serde) for JSON serialization.
- Fields use snake_case naming in Rust; serde default serialization produces snake_case JSON keys.

## Test Conventions

### Assertion style
- Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` for success checks.
- Body is deserialized from JSON into the expected response struct for field-level assertions.
- 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test organization
- Integration tests live in `tests/api/` with one file per domain entity (e.g., `sbom.rs`, `advisory.rs`).
- Tests hit a real PostgreSQL test database (not mocked).

### Test setup
- Test fixtures are created via the service layer or direct database seeding before assertions.
- Each test manages its own setup/teardown within the test function.

### Response validation
- Success tests validate both status code and deserialized body fields.
- List tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Error tests validate status code and may check error message body.

## CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root. Its conventions (framework choices, module pattern, error handling, endpoint registration, response types, query helpers, testing, caching) align with the sibling analysis above.
