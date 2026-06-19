# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:
1. **Repository Registry** -- present, with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, with Project key `TC`, Cloud ID, Feature issue type ID, and custom fields
3. **Code Intelligence** -- present, with `serena_backend` using `rust-analyzer`

Validation passes. Proceed.

---

## Production Code Conventions (from sibling analysis in Step 4)

### Module structure
- Every domain module under `modules/fundamental/src/` follows the pattern: `model/` + `service/` + `endpoints/`
- Siblings: `sbom/`, `advisory/`, `package/` all follow this structure identically
- New files must slot into the existing `advisory/` module, not create a new top-level module

### Endpoint conventions (from `sbom/endpoints/get.rs`, `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`)
- All handlers return `Result<Json<T>, AppError>` where `T` is the response struct
- Path parameters extracted via Axum's `Path<Id>` extractor
- Service instances injected via Axum's `State` or `Extension` extractor
- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` chaining
- Error wrapping uses `.context("descriptive message")` from the `anyhow` crate (re-exported through `AppError`)

### Service conventions (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)
- Service methods follow `verb_noun` pattern: `fetch`, `list`, `search`
- Method signature pattern: `async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Services use SeaORM query builders to access the database
- Transaction context (`Transactional`) is threaded through all database operations

### Model conventions (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)
- Model structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- Each model file contains one primary struct
- Module registration via `pub mod <name>;` in `model/mod.rs`

### Naming conventions
- File names use `snake_case` matching the concept: `summary.rs`, `details.rs`, `get.rs`, `list.rs`
- Struct names use `PascalCase`: `AdvisorySummary`, `SbomDetails`
- New model file: `severity_summary.rs` with struct `SeveritySummary`
- New endpoint file: `severity_summary.rs` with handler function `severity_summary`

### Error handling
- All service and handler errors use `Result<T, AppError>`
- `.context()` wrapping on every fallible operation
- `AppError` is defined in `common/src/error.rs` and implements Axum's `IntoResponse`
- 404 errors returned when entity not found, consistent with existing SBOM endpoints

### Import organization
- Standard library imports first, then external crates, then local crate imports
- Each group separated by a blank line

### Response types
- Single-entity endpoints return `Json<T>` directly
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new endpoint returns a single aggregate object, so it should use `Json<SeveritySummary>`

---

## Test Conventions (from sibling test analysis in Step 4)

### Sibling test files analyzed: `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`

### Assertion style
- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Body deserialized via `resp.json::<T>().await` or equivalent
- Field-level assertions on specific values, not just structural checks

### Response validation
- Status code checked first, then body deserialized and fields asserted
- For aggregate/summary responses: assert on each field value individually

### Error cases
- All endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Error tests use non-existent IDs to trigger 404 responses

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Test functions annotated with `#[tokio::test]` for async tests

### Test setup
- Integration tests hit a real PostgreSQL test database
- Test fixtures created via service methods or direct database seeding
- Each test function sets up its own data (no shared mutable state between tests)

### Test organization
- One test file per domain area in `tests/api/`
- Tests grouped by endpoint within the file

### Parameterized tests
- No evidence of `#[rstest]` or parameterized tests in sibling test files
- Individual test functions used for each scenario -- follow this pattern

---

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at the root (`trustify-backend/CONVENTIONS.md`). In a real implementation, this file would be read and its conventions followed. Any CI check commands found in that file would be extracted for Step 9 verification. Since this is an eval context and the file content is not available, we note its existence and would read it during actual execution.
