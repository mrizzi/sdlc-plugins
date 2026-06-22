# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Module structure

- Each domain module (sbom, advisory, package) follows the `model/ + service/ + endpoints/` structure
- Model modules have a `mod.rs` that re-exports submodules (`pub mod summary;`, `pub mod details;`)
- Service modules have a `mod.rs` that re-exports the service implementation file
- Endpoint modules have a `mod.rs` for route registration and individual handler files

### Sibling files analyzed

- **Model siblings**: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`, `modules/fundamental/src/sbom/model/summary.rs`
- **Service siblings**: `modules/fundamental/src/advisory/service/advisory.rs` (existing methods: fetch, list, search), `modules/fundamental/src/sbom/service/sbom.rs` (fetch, list, ingest)
- **Endpoint siblings**: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`

### Error handling

- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` pattern (from anyhow/similar)
- 404 errors are returned when an entity is not found, consistent across all GET-by-ID endpoints

### Naming conventions

- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- New method should be named `severity_summary` following the task description
- Model structs use PascalCase descriptive names (e.g., `SbomSummary`, `AdvisoryDetails`, `AdvisorySummary`)
- Endpoint handler files are named after the HTTP action or resource (e.g., `get.rs`, `list.rs`)

### Endpoint patterns

- Path parameters extracted via `Path<Id>` from Axum
- Service is obtained from application state (likely via Axum `State` or `Extension` extractor)
- Transaction context passed as `&Transactional<'_>` parameter to service methods
- Response types returned directly -- Axum's `Json<T>` wrapper handles serialization
- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern

### Response types

- Single-entity endpoints return the model struct directly (e.g., `AdvisoryDetails`)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new endpoint returns a summary (not paginated), so direct struct return is appropriate

### Import organization

- Standard library imports first
- External crate imports next
- Internal/project imports last
- Each group separated by a blank line

### Database patterns

- SeaORM is used for all database operations
- Join tables (e.g., `sbom_advisory`, `sbom_package`) are defined in `entity/src/`
- Queries use SeaORM's query builder pattern

## Test Conventions

### Sibling test files analyzed

- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/advisory.rs` -- Advisory endpoint integration tests
- `tests/api/search.rs` -- Search endpoint integration tests

### Assertion style

- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Body is deserialized from JSON and fields are checked individually
- Status code assertions come before body assertions

### Response validation

- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-entity tests validate specific field values after deserialization

### Error cases

- All endpoint test suites include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- 404 tests use a non-existent ID pattern

### Test naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Function names are snake_case and descriptive

### Test setup

- Integration tests hit a real PostgreSQL test database
- Test data is seeded before assertions
- Tests use a test HTTP client to make requests against the running test server

### Parameterized tests

- Would check siblings for `#[rstest]` usage. If not found in sibling test files, would not introduce parameterized tests and would use individual test functions instead.

### Test documentation

- Per SKILL.md requirements, every test function gets a `///` doc comment explaining what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments
