# Conventions Discovered from Sibling Analysis

## Repository-Level Conventions (from repo-backend.md Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

## Production Code Conventions (from sibling analysis)

### Model layer (`modules/fundamental/src/advisory/model/`)

- **Sibling files inspected**: `summary.rs` (AdvisorySummary), `details.rs` (AdvisoryDetails)
- **Naming**: Model structs use PascalCase with domain-descriptive names (e.g., `AdvisorySummary`, `AdvisoryDetails`)
- **Module registration**: Each model is declared in `model/mod.rs` with `pub mod <name>;`
- **Derive macros**: Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone` (for API response types)
- **Fields**: Use standard Rust types; severity is a string-based field on `AdvisorySummary`

### Service layer (`modules/fundamental/src/advisory/service/`)

- **Sibling files inspected**: `advisory.rs` (AdvisoryService with `fetch`, `list`, `search` methods)
- **Method signature pattern**: `pub async fn method_name(&self, id_or_params: Type, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Error handling**: Uses `.context("description")` for wrapping errors, returns `Result<T, AppError>`
- **Transaction support**: All service methods accept `&Transactional<'_>` as a parameter
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)

### Endpoint layer (`modules/fundamental/src/advisory/endpoints/`)

- **Sibling files inspected**: `get.rs` (GET /api/v2/advisory/{id}), `list.rs` (GET /api/v2/advisory)
- **Path extraction**: Uses Axum's `Path<Id>` extractor for path parameters
- **Handler return type**: Returns `Result<Json<T>, AppError>` where T is the response model
- **Route registration**: Routes registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`
- **Handler pattern**: Extract params -> call service method -> return Json-wrapped result
- **Error propagation**: Uses `?` operator with `.context()` wrapping for descriptive errors

### Cross-module patterns (SBOM module as reference)

- **Sibling module inspected**: `modules/fundamental/src/sbom/` (parallel domain module)
- **Directory structure**: Identical `model/ + service/ + endpoints/` structure
- **Endpoint paths**: Follow `/api/v2/<resource>` and `/api/v2/<resource>/{id}` pattern
- **Model organization**: `summary.rs` and `details.rs` as separate files within `model/`

### Entity layer (`entity/src/`)

- **Join tables**: `sbom_advisory.rs` defines the SBOM-Advisory join table entity
- **SeaORM pattern**: Entities follow SeaORM conventions with `Entity`, `Model`, `Column`, `Relation` definitions

## Test Conventions (from sibling test analysis)

- **Sibling test files inspected**: `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization
- **Response validation**: Tests validate response body structure by deserializing and checking key fields
- **Error cases**: All endpoint test files include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`)
- **Test setup**: Tests use a real PostgreSQL test database with fixture data
- **Test organization**: One test file per domain area in `tests/api/`
- **Given-When-Then**: Not explicitly used in existing tests, but will be added per SKILL.md requirement for AI-generated tests
- **Parameterized tests**: No evidence of `rstest` usage in sibling tests; will use individual test functions per existing convention
- **Doc comments**: SKILL.md mandates doc comments on all test functions regardless of sibling convention

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` at the root. Its contents were not directly readable in this eval (synthetic repo), but the Key Conventions section in repo-backend.md captures the equivalent project-level conventions. No CI check commands were extracted from a CONVENTIONS.md section, so Step 9 would fall back to standard `cargo build` / `cargo test` / `cargo clippy` checks.
