# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields configured
- **Code Intelligence**: Serena with rust-analyzer, tool naming convention documented

Configuration is valid. Proceeding.

## Production Code Conventions

### Module structure
- Each domain module (sbom, advisory, package) follows a strict `model/ + service/ + endpoints/` directory structure.
- Each sub-directory has a `mod.rs` that re-exports public items and registers sub-modules via `pub mod <name>;`.

### Model conventions (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)
- Model structs derive `Serialize, Deserialize, Debug, Clone`.
- Each model struct lives in its own file within the `model/` directory.
- The `model/mod.rs` file declares each sub-module with `pub mod <name>;` and re-exports the primary struct.
- Model structs represent API response shapes directly (no separate DTO layer).

### Service conventions (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)
- Service structs are named `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`).
- Methods follow `verb_noun` naming pattern (e.g., `fetch`, `list`, `search`).
- Method signatures take `&self`, domain-specific parameters, and `tx: &Transactional<'_>` as the last parameter for database transaction context.
- Methods return `Result<T, AppError>` where `T` is the domain model type.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` ecosystem, matching the pattern in `common/src/error.rs`.

### Endpoint conventions (from `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`)
- Handlers are async functions that extract path parameters via `Path<Id>`.
- Handlers call the corresponding service method and return the result as JSON via Axum's `Json` extractor.
- Return type is `Result<Json<T>, AppError>`.
- Route registration is done in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` chaining.
- Each handler lives in its own file within the `endpoints/` directory.

### Error handling
- All handlers and service methods return `Result<T, AppError>`.
- Errors are wrapped with `.context()` for descriptive messages.
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse` for Axum.
- 404 errors are returned when a requested entity does not exist, consistent across SBOM and advisory endpoints.

### Import organization
- Standard library imports first, then external crate imports, then internal module imports.
- Grouped by origin with blank lines between groups.

### Naming conventions
- Files: `snake_case.rs`
- Structs: `PascalCase` (e.g., `AdvisorySummary`, `SbomDetails`)
- Functions/methods: `snake_case` with `verb_noun` pattern
- Route paths: kebab-case with `/api/v2/` prefix

### Response types
- Single-entity endpoints return the struct directly wrapped in `Json<T>`.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new endpoint returns a summary (not a list), so it should return the struct directly.

## Test Conventions

### Test file conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)
- Integration tests live in `tests/api/` directory, one file per domain.
- Tests hit a real PostgreSQL test database (not mocked).
- Test functions are annotated with `#[test]` or `#[tokio::test]` for async tests.

### Assertion style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and individual fields are checked with `assert_eq!`.
- Error cases assert `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Response validation
- Tests validate both the HTTP status code and the response body structure.
- For summary/aggregate endpoints: validate each field individually.
- For error cases: validate the status code matches the expected error.

### Test organization
- Tests are grouped by endpoint within the file.
- Success cases come before error cases.
- Each test function is self-contained with its own setup.

### Documentation
- Per SKILL.md requirements, every test function must have a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
