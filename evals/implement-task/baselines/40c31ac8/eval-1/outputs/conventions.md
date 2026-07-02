# Discovered Conventions

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: Serena MCP servers configured with `serena_backend` using `rust-analyzer`

## Step 1.5 -- Description Integrity Check

> No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## CONVENTIONS.md Lookup

A `CONVENTIONS.md` file exists at the repository root (`trustify-backend/CONVENTIONS.md`). Its contents would be read and followed throughout implementation. Verification commands from any CI checks section would be extracted and run in Step 9.

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

- **Module structure**: Each domain module follows the `model/ + service/ + endpoints/` tripartite structure. New domain features must place code in the corresponding subdirectory.
- **Error handling**: All endpoint handlers return `Result<T, AppError>` with `.context()` wrapping from the `AppError` enum in `common/src/error.rs`. No raw `unwrap()` or `expect()` in production code.
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`. The `server/src/main.rs` auto-mounts all module routers, so no change there is needed.
- **Endpoint handler pattern**: Handlers in `endpoints/get.rs` extract path parameters via `Path<Id>`, call the corresponding service method, and return JSON via Axum's `Json` extractor. The handler signature follows the Axum extractor pattern.
- **Service method pattern**: `AdvisoryService` methods in `service/advisory.rs` follow the pattern: take `&self`, entity ID, and `tx: &Transactional<'_>` as parameters. Methods like `fetch` and `list` use SeaORM queries and return `Result<T, AppError>`.
- **Model struct pattern**: Model structs in `model/summary.rs` and `model/details.rs` derive `Serialize`, `Deserialize`, and use `#[serde(rename_all = "camelCase")]` when appropriate. Each model has its own file and is re-exported via `model/mod.rs`.
- **Module registration**: New model files must be registered in `model/mod.rs` with `pub mod <name>;`.
- **Naming conventions**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`). Model structs use PascalCase descriptive names (e.g., `AdvisorySummary`, `AdvisoryDetails`).
- **Response types**: Single-entity endpoints return the struct directly (Axum handles serialization). List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Database access**: SeaORM is used for all database operations. Join tables (e.g., `sbom_advisory` in `entity/src/sbom_advisory.rs`) are used for many-to-many relationships.
- **Import organization**: External crate imports first, then internal module imports, grouped by crate.
- **Framework**: Axum for HTTP, SeaORM for database, tower-http for middleware.

### Test Conventions

- **Test location**: Integration tests live in `tests/api/` and are organized by domain (e.g., `advisory.rs`, `sbom.rs`, `search.rs`).
- **Test database**: Integration tests hit a real PostgreSQL test database (not mocked).
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization and field-level assertions.
- **Error case coverage**: Tests include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent resource IDs.
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Response validation**: Tests validate both the HTTP status code and specific fields in the response body, not just collection lengths.
- **Parameterized tests**: Would need to check sibling test files for `#[rstest]` usage. If not present, individual test functions should be used instead.

### Documentation Conventions

- **Doc comments**: All new public structs, enums, and functions must have `///` doc comments (Rust convention).
- **Test documentation**: Every test function must have a `///` doc comment explaining what it verifies. Non-trivial tests must include `// Given`, `// When`, `// Then` inline comments.
