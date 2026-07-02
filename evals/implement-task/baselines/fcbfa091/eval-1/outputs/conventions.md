# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` at path `./` with Serena instance `serena_backend`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID present
- Code Intelligence: tool naming convention `mcp__serena_backend__<tool>` documented

## Step 1 -- Target Branch

Target Branch: `main`

## Step 1.5 -- Description Digest Check

No description digest comment found -- skipping integrity check. This task may have been created before digest tracking was introduced.

Proceeding with a warning rather than blocking execution, as specified by the digest protocol.

## CONVENTIONS.md Lookup

The repository contains a `CONVENTIONS.md` file at the root (`trustify-backend/CONVENTIONS.md`). Would read and follow its conventions throughout implementation. Any CI check commands found therein would be extracted for use in Step 9.

## Production Code Conventions (from sibling analysis)

### Module structure
- Every domain module follows a strict `model/ + service/ + endpoints/` directory structure
- Siblings examined: `sbom/`, `advisory/`, `package/` under `modules/fundamental/src/`
- Each sub-module has its own `mod.rs` that re-exports public items

### Error handling
- All endpoint handlers return `Result<T, AppError>` using the `AppError` enum from `common/src/error.rs`
- Errors are wrapped with `.context("descriptive message")` for contextual error chains
- Pattern is consistent across `sbom/endpoints/get.rs`, `advisory/endpoints/get.rs`, and `package/endpoints/list.rs`

### Naming conventions
- Service methods follow `verb_noun` pattern: `fetch`, `list`, `search` (seen in `AdvisoryService`, `SbomService`, `PackageService`)
- Model structs use domain noun suffixes: `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`
- Endpoint handler files are named after the HTTP verb or action: `get.rs`, `list.rs`
- New endpoint file should follow this pattern: `severity_summary.rs`

### Endpoint registration
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`
- Routes are mounted by `server/src/main.rs` which auto-discovers modules
- Path convention: `/api/v2/<resource>` for top-level, with `{id}` path parameters for item access

### Service method signatures
- Service methods take `&self` as receiver
- Methods that interact with the database accept `tx: &Transactional<'_>` as the final parameter
- Methods return `Result<T, Error>` where Error is the service-level error type
- Pattern observed in `AdvisoryService::fetch`, `AdvisoryService::list`, `SbomService::fetch`

### Handler pattern
- Path parameters extracted via Axum's `Path<Id>` extractor
- Service called with extracted params
- Response returned directly as the struct (Axum's `Json` extractor handles serialization)
- Pattern observed in `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`

### Response types
- Single-item endpoints return the domain struct directly (e.g., `AdvisoryDetails`)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new endpoint returns a summary struct, not a list, so it should return the struct directly

### Import organization
- Standard library imports first, then external crates, then local crate imports
- `use` statements grouped by source with blank lines between groups

### Database access
- SeaORM is used for database queries
- Join tables (e.g., `sbom_advisory`) are defined in `entity/src/` as dedicated entity files
- Queries use SeaORM's query builder API

## Test Conventions (from sibling test analysis)

### Test file location
- Integration tests reside in `tests/api/` directory
- Test files named after the resource being tested: `sbom.rs`, `advisory.rs`, `search.rs`
- New test file should follow: `advisory_summary.rs`

### Assertion style
- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for success responses
- Error case tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 responses
- Response body deserialized and fields validated with `assert_eq!` on specific values

### Response validation
- Tests validate the response body by deserializing into the expected struct type
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-item tests validate key fields of the returned struct

### Error case coverage
- All endpoint test files include at least one 404 test for non-existent resource IDs
- Tests verify both the status code and that the response body contains appropriate error info

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern
- Examples: `test_list_advisories_filtered`, `test_get_sbom_not_found`

### Test setup
- Tests hit a real PostgreSQL test database
- Test fixtures are created using service methods or direct database inserts
- Each test manages its own test data setup and does not rely on shared mutable state

### Parameterized tests
- Sibling tests do not appear to use `#[rstest]` or other parameterized test frameworks
- Follow the existing pattern of individual test functions per scenario
