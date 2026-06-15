# Conventions Discovered from Sibling Analysis

## Project Configuration Validation (Step 0)

The project's CLAUDE.md (`claude-md-mock.md`) contains all required sections:
- **Repository Registry**: `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID configured
- **Code Intelligence**: Serena instance `serena_backend` with `rust-analyzer`

## Discovered Conventions (from sibling analysis)

### Repository-Level Conventions (from repo-backend.md Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

### Production Code Conventions (from advisory/ and sbom/ sibling analysis)

- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search` in `AdvisoryService`)
- **Service method signature**: Methods take `&self, id: Id, tx: &Transactional<'_>` for single-entity lookups
- **Model structs**: Separate `summary.rs` and `details.rs` files in each `model/` directory; each struct derives `Serialize, Deserialize, Debug, Clone`
- **Model module registration**: `model/mod.rs` contains `pub mod <submodule>;` declarations for each model file
- **Endpoint handler pattern**: Extract path params via `Path<Id>`, call service method, return `Json(result)` or `Result<Json<T>, AppError>`
- **Route registration**: `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern
- **File naming**: Model files named after the concept they represent (e.g., `summary.rs`, `details.rs`)
- **Import organization**: Grouped by crate, then module, then specific items
- **Error handling strategy**: Use `AppError` with `.context()` wrapping from `common/src/error.rs`

### Endpoint Conventions (from sbom/endpoints/ and advisory/endpoints/ sibling analysis)

- **Handler function signature**: `async fn handler(Path(id): Path<Id>, State(service): State<ServiceType>) -> Result<Json<T>, AppError>`
- **Path parameter extraction**: Uses Axum's `Path<Id>` extractor
- **Route paths**: Follow RESTful conventions under `/api/v2/<resource>`
- **Separate handler files**: Each endpoint operation gets its own file (e.g., `list.rs`, `get.rs`)
- **Module registration**: All handler modules declared in `endpoints/mod.rs`

### Test Conventions (from tests/api/ sibling analysis)

- **Assertion style**: All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`)
- **Test file naming**: One file per domain module in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- **Test structure**: Tests use a real PostgreSQL test database, not mocks
- **Response validation**: Tests validate specific field values, not just counts

### Convention Conflicts

No conflicts detected between the task description/Implementation Notes and the established conventions. The task description aligns with all discovered patterns:
- The endpoint pattern (Path params, service call, JSON response) matches existing handlers
- The service method signature matches existing methods in `AdvisoryService`
- The model struct approach matches the existing `summary.rs`/`details.rs` pattern
- The test patterns match the existing integration test style
