# Discovered Conventions for TC-9201

## Conventions from CONVENTIONS.md

The repository root contains a `CONVENTIONS.md` file. Key conventions extracted:

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database
- **Caching**: Uses `tower-http` caching middleware

CI check commands would be extracted from the CONVENTIONS.md CI checks section for use in Step 9 verification.

---

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

**From sibling endpoint handlers** (`advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`):

- **Path extraction**: All GET-by-ID handlers use `Path<Id>` extractor from Axum
- **Service call pattern**: Handlers call a method on the corresponding service (e.g., `advisory_service.fetch(id, &tx)`) and return the result as JSON
- **Error handling**: All handlers return `Result<Json<T>, AppError>` and use `.context("description")` for error wrapping
- **Route registration**: Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` chaining
- **Naming**: Handler functions follow `get_<entity>`, `list_<entity>` naming (e.g., `get_advisory`, `list_advisories`)

**From sibling model files** (`advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`):

- **Derive macros**: Model structs derive `Serialize, Deserialize, Debug, Clone` (at minimum `Serialize` for response types)
- **Documentation**: Each struct has a doc comment describing what it represents
- **Field types**: Numeric counts use integer types; optional fields use `Option<T>`
- **Module registration**: Each model sub-module is registered in `model/mod.rs` via `pub mod <name>;`

**From sibling service methods** (`AdvisoryService.fetch`, `AdvisoryService.list`):

- **Method signature**: Service methods take `&self`, entity-specific parameters, and `tx: &Transactional<'_>` as the last parameter
- **Naming**: Service methods follow `verb_noun` or just `verb` pattern (e.g., `fetch`, `list`, `search`)
- **Error wrapping**: Service methods use `.context()` for error wrapping and return `Result<T, anyhow::Error>` or similar
- **Database access**: Services use SeaORM entity queries through the transaction handle

**From error handling** (`common/src/error.rs`):

- **AppError enum**: Centralized error type implementing `IntoResponse`
- **Context wrapping**: All error propagation uses `.context("descriptive message")` from anyhow
- **404 pattern**: Non-existent entity lookups return an appropriate AppError variant for 404

**From import organization**:

- Standard library imports first
- External crate imports second
- Internal crate imports third
- Each group separated by a blank line

### Test Conventions

**From sibling test files** (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

- **Assertion style**: All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for success cases followed by body deserialization via `resp.json::<T>().await`
- **Response validation**: Tests validate specific field values, not just counts. List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: All endpoint test files include a 404 test using `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` with a non-existent ID
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_sboms_filtered`)
- **Test setup**: Tests use a shared test database with fixtures; setup functions create necessary entities before assertions
- **Test organization**: Tests are grouped by endpoint, with success cases first, then error cases
- **Doc comments**: Following SKILL.md requirement, every test function will have a `///` doc comment explaining what it verifies (applied as a new standard even if siblings lack them)
- **Given-When-Then**: Non-trivial tests will include `// Given`, `// When`, `// Then` section comments

### Parameterized Tests

Sibling test files in `tests/api/` do not appear to use `#[rstest]` or other parameterized test mechanisms. Following the convention conformance rule, parameterized tests will NOT be introduced. Each test case will be a separate function.
