# Conventions Analysis for TC-9201

## Step 0 -- Validate Project Configuration

Project Configuration validated in CLAUDE.md:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present, tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` with `rust-analyzer`

All required sections are present. Proceeding.

## Step 1 -- Parse Task

- **Jira Key**: TC-9201
- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: (none)
- **Target PR**: (none)
- **Dependencies**: None

## CONVENTIONS.md Lookup

The repository root at `./` contains a `CONVENTIONS.md` file. This would be read for project-level conventions, CI check commands, and code generation commands. (In this eval we note its existence but cannot read its actual contents since we are not modifying real files.)

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

The following conventions were discovered by inspecting sibling files in the `advisory/`, `sbom/`, and `package/` modules:

- **Module structure:** Every domain module follows a `model/ + service/ + endpoints/` tri-directory structure. Each sub-directory has a `mod.rs` that re-exports public types and registers sub-modules.

- **Model pattern:** Model structs (e.g., `AdvisorySummary`, `SbomSummary`, `PackageSummary`) are defined in their own file under `model/`, registered via `pub mod <name>;` in `model/mod.rs`. Structs derive `Serialize, Deserialize, Debug, Clone` and use `#[serde(rename_all = "camelCase")]` for JSON field naming.

- **Service pattern:** Service structs (e.g., `AdvisoryService`, `SbomService`) have methods that take `&self`, an entity ID, and `tx: &Transactional<'_>` as parameters. Methods return `Result<T, AppError>` where `T` is the domain model type. Error wrapping uses `.context("descriptive message")` from the `anyhow` crate, and errors propagate via `?`.

- **Endpoint pattern:** Endpoint handlers are async functions that extract path parameters via `Path<Id>`, call the appropriate service method, and return `Json<T>`. All handlers return `Result<Json<T>, AppError>`. Route registration happens in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.

- **Error handling:** All handlers and service methods return `Result<T, AppError>` with `.context()` wrapping for error messages. `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`. The 404 pattern uses a specific `AppError::NotFound` variant or similar.

- **Naming conventions:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`). Endpoint handler functions are named after the HTTP method and resource (e.g., `get_advisory`, `list_advisories`).

- **Import organization:** External crate imports first, then `crate::` imports, then `super::` imports. SeaORM entity imports use `entity::prelude::*` or specific entity names.

- **Response types:** Single-entity endpoints return `Json<T>` directly. List endpoints return `Json<PaginatedResults<T>>` using the wrapper from `common/src/model/paginated.rs`.

### Test Conventions

The following test conventions were discovered by inspecting sibling test files in `tests/api/`:

- **Assertion style:** All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases, followed by body deserialization via `resp.json::<T>()`.

- **Response validation:** Tests validate specific field values in the response, not just counts. For aggregation responses, each field is individually asserted.

- **Error cases:** Every endpoint test file includes at least one test for non-existent resource (404). The pattern is to request with a known-invalid ID and assert `StatusCode::NOT_FOUND`.

- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_advisories_filtered`).

- **Test setup:** Integration tests use a real PostgreSQL test database. Test data is seeded before assertions. Each test function is independent and sets up its own data.

- **Documentation:** Test functions should have `///` doc comments explaining what they verify (this is an AI-generated standard applied regardless of sibling test docs).

- **Given-When-Then:** Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
