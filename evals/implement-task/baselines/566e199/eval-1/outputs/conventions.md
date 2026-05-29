# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Error handling
- All handlers in `modules/fundamental/src/*/endpoints/` return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` or similar error-context pattern, matching the style in `common/src/error.rs`.
- 404 errors use `AppError::NotFound` or equivalent variant for missing resources.

### Naming
- Service methods follow `verb_noun` pattern: `fetch`, `list`, `search` in `AdvisoryService`; `fetch`, `list`, `ingest` in `SbomService`.
- New method follows this pattern: `severity_summary` (noun compound describing the returned data).
- Endpoint handler files are named after the HTTP action or resource: `get.rs`, `list.rs`. New file: `severity_summary.rs`.
- Model struct files match the concept: `summary.rs`, `details.rs`. New file: `severity_summary.rs`.

### Module structure
- Each domain module follows the three-part pattern: `model/` + `service/` + `endpoints/`.
- `model/mod.rs` declares submodules with `pub mod <name>;`.
- `endpoints/mod.rs` contains route registration using `Router::new().route("/path", get(handler))`.
- `service/` contains the business logic with methods that accept `&self`, entity ID, and `&Transactional<'_>`.

### Endpoint patterns
- Path parameters extracted via Axum's `Path<Id>` extractor.
- Service is injected via Axum state or extension.
- Handler calls service method, then returns `Json(result)`.
- Route registration in `endpoints/mod.rs` follows `Router::new().route("/path", get(handler_fn))` chaining.

### Response types
- Single-entity responses return the model struct directly wrapped in `Json<T>`.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new endpoint returns a single summary, so it should return `Json<SeveritySummary>` directly (not paginated).

### Struct derive macros
- Model structs use `#[derive(Serialize, Deserialize, Debug, Clone)]` based on sibling model files (`summary.rs`, `details.rs`).
- Some structs may additionally derive `utoipa::ToSchema` for OpenAPI spec generation.

### Import organization
- Standard library imports first, then external crates, then internal modules -- following Rust conventions observed in sibling files.

### Options and parameter propagation
- Service methods consistently receive a transaction reference `tx: &Transactional<'_>` as their last parameter for database operations.
- Entity IDs are passed as the `Id` type (likely a UUID or domain-specific ID wrapper).

## Test Conventions

### Assertion style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` for success cases.
- Response body is deserialized with `resp.json::<T>()` or equivalent, then individual fields are asserted.

### Response validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Single-entity tests validate the returned struct's key fields directly.
- Tests assert on specific values, not just collection lengths.

### Error cases
- All endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Error tests use a non-existent ID to trigger the 404 path.

### Test naming
- Tests follow `test_<endpoint_or_action>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_sboms_filtered`).

### Test setup and teardown
- Integration tests hit a real PostgreSQL test database.
- Tests use a test server setup function that initializes the app with a test database.
- Test data is seeded before assertions.

### Test organization
- Tests are grouped by endpoint/feature in separate files under `tests/api/`.
- Each file covers success and error paths for its endpoint.

### Parameterized tests
- Need to verify from sibling test files whether `#[rstest]` with `#[case]` is used. If siblings do not use parameterized tests, individual test functions are written instead.

### Test documentation
- Per SKILL.md requirements, every test function gets a `///` doc comment regardless of sibling patterns.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` file at the root. Its contents would provide:
- Explicit naming rules
- Directory structure requirements
- Code patterns
- CI check commands (to be extracted for Step 9 verification)
- Code generation commands (if any)

These explicit conventions supplement the implicit conventions discovered above. In case of conflict, `CONVENTIONS.md` takes precedence over implicit sibling patterns.
