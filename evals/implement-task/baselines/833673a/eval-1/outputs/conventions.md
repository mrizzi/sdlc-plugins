# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Endpoint Handler Conventions (from `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`)

- **Path extraction**: All single-resource GET handlers extract path parameters via `Path<Id>` from Axum
- **Service invocation**: Handlers call the corresponding service method, passing the extracted ID and a `Transactional` reference
- **Return type**: All handlers return `Result<Json<T>, AppError>` where `T` is the response model
- **Error handling**: All handlers use `.context("descriptive message")` wrapping on error paths, producing `AppError` responses
- **Route registration**: Each handler module is declared with `mod <name>;` in `endpoints/mod.rs`, and routes are registered via `Router::new().route("/path", get(<module>::handler))`

### Model Conventions (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)

- **Derive macros**: All model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- **Module registration**: Each model file is registered in `model/mod.rs` with `pub mod <name>;`
- **Field types**: Numeric count fields use `i64` or `u64`; IDs use the `Id` type from common
- **Naming**: Model structs use PascalCase descriptive names (e.g., `AdvisorySummary`, `SbomDetails`)

### Service Conventions (from `advisory/service/advisory.rs` -- `fetch` and `list` methods)

- **Method signature**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Parameters**: Methods take `&self`, relevant identifier(s), and `tx: &Transactional<'_>` as the last parameter
- **Return type**: Methods return `Result<T, AppError>` using the common error type
- **Error wrapping**: Internal errors are wrapped with `.context()` before returning
- **Query pattern**: Methods use SeaORM entity queries with the entity types from `entity/src/`

### Module Structure Conventions

- **Domain modules**: Each domain (sbom, advisory, package) follows the `model/ + service/ + endpoints/` directory structure
- **Module registration**: Parent `mod.rs` files register child modules with `pub mod <name>;`
- **Route mounting**: Each module's `endpoints/mod.rs` builds a `Router` that is mounted by `server/main.rs`

### Error Handling Conventions (from `common/src/error.rs`)

- **Error type**: All public-facing functions return `Result<T, AppError>`
- **Context wrapping**: Errors are wrapped with `.context("human-readable description")` from the anyhow/context pattern
- **HTTP mapping**: `AppError` implements `IntoResponse` for Axum, mapping to appropriate HTTP status codes

### Import Organization

- Standard library imports first
- External crate imports second
- Internal crate imports third (from `common`, `entity`, etc.)
- Local module imports last

## Test Conventions

### Test Structure (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)

- **Location**: Integration tests live in `tests/api/` directory, one file per domain area
- **Database**: Tests hit a real PostgreSQL test database (not mocked)
- **Naming**: Test functions follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Assertion style**: Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Tests validate response body fields after deserializing from JSON
- **Error cases**: All endpoint test files include at least one 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Uses `#[test]` or `#[tokio::test]` attributes for async handlers

### Test Patterns

- **Setup**: Tests create test data (SBOMs, advisories) before making HTTP requests
- **HTTP client**: Tests use an HTTP client to make requests to the test server
- **Cleanup**: Test database is typically rolled back or cleaned up after each test
- **Field-level checks**: Tests verify specific field values in response JSON, not just status codes

### Parameterized Tests

- Would check sibling test files for `#[rstest]` or `#[case]` usage
- If not found in sibling tests, would not introduce parameterized testing -- follow existing patterns
