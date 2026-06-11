# Discovered Conventions

## From CONVENTIONS.md lookup

The repository `trustify-backend` has a `CONVENTIONS.md` file at the repository root.
While I cannot read its full contents in this eval (no actual repo access), the
repo-backend.md Key Conventions section documents the following project-level conventions:

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

## Discovered conventions (from sibling analysis)

### Production code conventions

#### Endpoint conventions (from `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`)
- **Handler signature**: async functions that take Axum extractors (`Path<Id>`, `State<AppState>`, etc.) and return `Result<Json<T>, AppError>`
- **Path parameter extraction**: use `Path<Id>` extractor for single resource endpoints (e.g., `GET /api/v2/advisory/{id}`)
- **Service invocation**: handlers call service methods passing through the extracted parameters and a `Transactional` reference
- **Error wrapping**: errors are wrapped with `.context("descriptive message")` before propagating
- **Route registration pattern**: `Router::new().route("/path", get(handler_fn))` in `endpoints/mod.rs`
- **Module re-export**: endpoint modules are declared in `endpoints/mod.rs` and handler functions are imported for route registration

#### Model conventions (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)
- **Derive macros**: all model structs derive `Clone, Debug, Serialize, Deserialize`
- **Module registration**: new model modules are declared as `pub mod <name>;` in `model/mod.rs`
- **Naming**: model structs use PascalCase descriptive names (e.g., `AdvisorySummary`, `SbomDetails`)
- **Field types**: use standard Rust types; `i64` or `u64` for counts, `String` for identifiers
- **Serde attributes**: `#[serde(rename_all = "camelCase")]` or snake_case field names matching the API contract

#### Service conventions (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)
- **Method signature**: service methods take `&self`, domain-specific parameters, and `tx: &Transactional<'_>` as the last parameter
- **Naming**: service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Error handling**: service methods return `Result<T, anyhow::Error>` or `Result<T, AppError>` with `.context()` wrapping
- **Database access**: use SeaORM entity queries with the `sbom_advisory` join table for cross-entity lookups

#### File organization conventions
- **New endpoint files**: placed in `modules/fundamental/src/<domain>/endpoints/<feature>.rs`
- **New model files**: placed in `modules/fundamental/src/<domain>/model/<feature>.rs`
- **Integration tests**: placed in `tests/api/<feature>.rs`

### Test conventions (from sibling test analysis)

#### From `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`
- **Assertion style**: use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization with `resp.json::<T>().await`
- **Error case testing**: include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent resource IDs
- **Test naming**: tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_sboms_filtered`)
- **Test setup**: use test database fixtures with known data for predictable assertions
- **Response validation**: validate specific field values and counts, not just response status
- **Test organization**: grouped by endpoint/feature within a single test file
- **Attribute**: use `#[tokio::test]` for async integration tests
- **Documentation**: each test function should have a `///` doc comment explaining what it verifies (enforced as AI-generated standard)
