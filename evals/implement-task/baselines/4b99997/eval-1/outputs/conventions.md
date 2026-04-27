# Conventions Discovered from Sibling Analysis

## Project Configuration Validation

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: Tool naming convention `mcp__serena_backend__<tool>`, rust-analyzer

## Production Code Conventions (from sibling analysis)

### Module Structure
- Every domain module follows a strict `model/ + service/ + endpoints/` structure
- Each sub-directory has a `mod.rs` that re-exports public items
- New model files are registered in their parent `model/mod.rs` via `pub mod <name>;`

### Framework Patterns
- **HTTP framework**: Axum with typed extractors (`Path<Id>`, `Json<T>`)
- **ORM**: SeaORM for database access
- **Route registration**: Each module's `endpoints/mod.rs` builds a `Router` with `.route("/path", get(handler))` calls; `server/main.rs` mounts all module routers

### Endpoint Conventions (from `endpoints/get.rs`, `endpoints/list.rs` siblings)
- Handlers are `async fn` returning `Result<Json<T>, AppError>`
- Path parameters extracted via `Path<Id>` from Axum
- Service method called with `(&self, id, tx)` pattern where `tx: &Transactional<'_>`
- Single-item endpoints return the struct directly wrapped in `Json`
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Service Conventions (from `service/advisory.rs`, `service/sbom.rs` siblings)
- Service structs hold database connection pool references
- Methods follow `verb_noun` naming pattern (e.g., `fetch`, `list`, `search`)
- Method signature: `async fn method_name(&self, param: Type, tx: &Transactional<'_>) -> Result<T, AppError>`
- Error handling uses `.context("descriptive message")` wrapping (from `anyhow` or similar)
- Database queries use SeaORM query builders

### Model Conventions (from `model/summary.rs`, `model/details.rs` siblings)
- Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- Structs are plain data containers (no business logic)
- Each model variant (summary, details) lives in its own file
- Parent `mod.rs` uses `pub mod <name>;` to register each sub-module

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- `AppError` implements `IntoResponse` for Axum
- Errors are wrapped with `.context()` to add descriptive context at each call site
- 404 errors for missing entities are consistent across all endpoints

### Naming Conventions
- **Files**: snake_case (e.g., `severity_summary.rs`)
- **Structs**: PascalCase (e.g., `SeveritySummary`)
- **Functions/methods**: snake_case with `verb_noun` pattern (e.g., `severity_summary`)
- **Modules**: snake_case matching the file name
- **Endpoints**: RESTful paths under `/api/v2/`

### Import Organization
- Standard library imports first
- External crate imports second
- Internal module imports last
- Grouped by category with blank line separators

## Test Conventions (from sibling test analysis)

### Test File Structure (from `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`)
- Integration tests live in `tests/api/` directory
- Each test file covers one domain module's endpoints
- Tests hit a real PostgreSQL test database (not mocked)

### Assertion Patterns
- Status code checks use `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::NOT_FOUND`
- Response bodies are deserialized and individual fields are asserted
- Value-based assertions preferred over length-only checks

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Test functions are annotated with `#[tokio::test]` for async tests

### Error Case Coverage
- All endpoint test files include 404 tests for non-existent resources
- Error responses validated with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test Organization
- Tests grouped by feature/endpoint within a single test file
- Each test function is self-contained with its own setup

## CONVENTIONS.md Lookup

The repository tree shows a `CONVENTIONS.md` at the root. Since this is a simulated environment, I note that:
- The file should be checked for CI verification commands
- Any listed CI checks (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`) should be extracted and run during Step 9
- Code generation commands should also be extracted if present

## Cross-Section Reference Consistency

Checked the task description for entity-path consistency:
- **AdvisoryService**: Referenced in both "Files to Modify" (`modules/fundamental/src/advisory/service/advisory.rs`) and "Implementation Notes" (same path) -- CONSISTENT
- **SeveritySummary model**: "Files to Create" (`modules/fundamental/src/advisory/model/severity_summary.rs`) and "Implementation Notes" reference to `AdvisorySummary` in `model/summary.rs` as a related struct -- CONSISTENT (different structs, no conflict)
- **Route registration**: "Files to Modify" (`modules/fundamental/src/advisory/endpoints/mod.rs`) and "Implementation Notes" (same path) -- CONSISTENT
- **Model module registration**: "Files to Modify" (`modules/fundamental/src/advisory/model/mod.rs`) -- CONSISTENT with convention of registering modules
