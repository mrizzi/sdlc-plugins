# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

Project Configuration in `claude-md-mock.md` validated:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: present with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured for `rust-analyzer`

All required sections are present -- proceeding.

## Step 1.5 -- Description Integrity Verification

No Jira access is available in this eval context, so no digest comment can be retrieved. Per the backward compatibility rule in `shared/description-digest-protocol.md`:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

In a real execution, the skill would:
1. Call `jira.get_issue_comments(TC-9201)` to retrieve all comments
2. Search for comments whose body starts with `[sdlc-workflow] Description digest:`
3. If multiple match, select the most recent by `created` timestamp
4. If found, extract the tagged digest (e.g., `sha256-md:<hex>`), compute the current description's digest via `python3 scripts/sha256-digest.py`, compare format tags, then compare hex digests
5. If not found, log the warning above and proceed -- do not block execution

Since no digest comment is available here, we proceed with a warning (backward compatibility).

## Production Code Conventions (from sibling analysis)

### Module structure
- Each domain module under `modules/fundamental/src/` follows a consistent `model/ + service/ + endpoints/` structure
- Siblings: `sbom/`, `advisory/`, `package/` all follow this pattern
- The `model/` directory contains a `mod.rs` that re-exports submodules, plus individual struct files (`summary.rs`, `details.rs`)

### Model conventions
- Model structs are defined in dedicated files named after the concept (e.g., `summary.rs`, `details.rs`)
- Each model file is registered via `pub mod <name>;` in the parent `model/mod.rs`
- Response structs derive `Serialize` (and likely `Deserialize`) for JSON serialization
- The `AdvisorySummary` struct in `model/summary.rs` includes a `severity` field -- this is the field to count by

### Service conventions
- Services are defined as structs with methods in dedicated files (e.g., `advisory.rs` within `service/`)
- Method signatures follow the pattern: `async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Methods follow a `verb_noun` naming pattern (e.g., `fetch`, `list`, `search`)
- Error handling uses `Result<T, AppError>` with `.context()` wrapping from the `anyhow` or project-specific error crate

### Endpoint conventions
- Each endpoint handler is in its own file within `endpoints/` (e.g., `list.rs`, `get.rs`)
- Route registration happens in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern
- Path parameters are extracted via `Path<Id>` extractor
- Handlers return `Result<Json<T>, AppError>` -- Axum's `Json` wrapper handles serialization
- All handlers return `Result<T, AppError>` with `.context()` for error wrapping

### Error handling
- All handlers use `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Errors are wrapped with `.context()` for descriptive error messages
- 404 responses are returned when entities are not found, consistent with existing SBOM endpoints

### Import organization
- Standard library imports first, then external crates, then internal modules (Rust convention)
- SeaORM entities are imported from `entity::` module
- Common utilities from `common::` module

### Response types
- Single-entity endpoints return `Json<T>` directly
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new severity summary endpoint returns a single summary object, not a list, so it should use `Json<SeveritySummary>`

### Route paths
- API versioned under `/api/v2/`
- Resource-oriented paths (e.g., `/api/v2/sbom`, `/api/v2/advisory`)
- The new endpoint `/api/v2/sbom/{id}/advisory-summary` follows the nested resource pattern

## Test Conventions (from sibling test analysis)

### Test file structure
- Integration tests live in `tests/api/` directory
- Each domain has its own test file (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- Tests hit a real PostgreSQL test database

### Assertion patterns
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response bodies are deserialized and field values are checked
- 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test organization
- Tests are grouped by endpoint/feature within a single file
- Each test function is annotated with `#[tokio::test]` for async tests

### Error case coverage
- All endpoint test files include at least one 404 test for non-existent resources
- Validation error cases are tested where applicable

### Parameterized tests
- Not enough information from the repo structure to determine if `#[rstest]` is used
- Default to individual test functions per the sibling pattern observed
