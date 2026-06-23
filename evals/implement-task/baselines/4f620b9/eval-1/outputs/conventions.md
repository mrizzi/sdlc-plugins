# Discovered Conventions

## From CONVENTIONS.md (repository root)

The task mentions a `CONVENTIONS.md` at the repository root. Per the repo structure document, this file exists at `trustify-backend/CONVENTIONS.md`. The following conventions would be extracted from it during Step 4.

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

**Module structure:**
- Every domain module follows the `model/ + service/ + endpoints/` tripartite structure
- Each subdirectory has a `mod.rs` that re-exports or registers its children
- Model files define response structs (e.g., `summary.rs`, `details.rs`)
- Service files define the service struct with methods like `fetch`, `list`, `search`
- Endpoint files define individual route handlers (e.g., `list.rs`, `get.rs`)

**Framework patterns:**
- HTTP framework: Axum
- ORM: SeaORM
- Caching: tower-http middleware

**Error handling:**
- All endpoint handlers return `Result<T, AppError>`
- Errors are wrapped with `.context()` from the `AppError` enum in `common/src/error.rs`
- `AppError` implements `IntoResponse` for automatic HTTP error mapping

**Endpoint registration:**
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern
- `server/main.rs` mounts all module routers — no changes needed in main.rs when adding routes within an existing module

**Response types:**
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the struct directly via Axum's `Json` extractor
- New aggregate/summary endpoints (like this one) return a custom struct directly

**Naming conventions:**
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- Model structs use PascalCase with a descriptive suffix (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- Endpoint handler files are named after the HTTP action (e.g., `get.rs`, `list.rs`)
- Endpoint handler functions match the file name (e.g., `get()` in `get.rs`, `list()` in `list.rs`)

**Path parameter extraction:**
- Endpoint handlers extract path parameters via `Path<Id>` (Axum extractor)
- The `Id` type is used for entity identifiers

**Import organization:**
- Model modules use `pub mod` declarations in their `mod.rs` to register submodules
- Service modules re-export through `mod.rs`

**Database patterns:**
- SeaORM entities are defined in the `entity/` crate
- Join tables exist for many-to-many relationships (e.g., `sbom_advisory.rs`, `sbom_package.rs`)
- Query helpers (filtering, pagination, sorting) come from `common/src/db/query.rs`

### Test Conventions

**Test location:**
- Integration tests live in `tests/api/` directory
- Test files are named after the domain entity being tested (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)

**Test infrastructure:**
- Integration tests hit a real PostgreSQL test database
- Tests use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status verification

**Assertion style:**
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` or `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response body is deserialized and specific field values are checked
- Value-based assertions are preferred over length-only checks

**Test naming:**
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

**Error case coverage:**
- All endpoint test files include 404 tests for non-existent entity IDs
- Error responses are validated by status code

**No parameterized tests observed:**
- Sibling test files (`sbom.rs`, `advisory.rs`, `search.rs`) do not appear to use `#[rstest]` or parameterized patterns
- Individual test functions should be used rather than introducing parameterized tests
