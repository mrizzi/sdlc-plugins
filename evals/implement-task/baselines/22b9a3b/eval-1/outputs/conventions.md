# Conventions Discovered from Sibling Analysis

## Repository: trustify-backend

### Module Structure Convention

Each domain module under `modules/fundamental/src/` follows a strict tripartite structure:

```
<domain>/
  mod.rs
  model/
    mod.rs
    summary.rs       # Summary struct (list view)
    details.rs       # Details struct (detail view)
  service/
    mod.rs
    <domain>.rs      # <Domain>Service with fetch, list methods
  endpoints/
    mod.rs           # Route registration
    list.rs          # GET /api/v2/<domain> handler
    get.rs           # GET /api/v2/<domain>/{id} handler
```

Sibling modules observed: `sbom/`, `advisory/`, `package/` -- all follow this pattern consistently.

### Endpoint Conventions

1. **Route registration**: Each module's `endpoints/mod.rs` assembles routes using `Router::new().route("/path", get(handler))` pattern.
2. **Path parameter extraction**: Handlers extract path params via `Path<Id>` (Axum extractor).
3. **Service injection**: Services are passed into handlers via Axum state/extension extractors.
4. **Return types**: Handlers return `Result<Json<T>, AppError>` where `T` is the response struct.
5. **List endpoints**: Return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
6. **Single-resource endpoints**: Return the domain struct directly (e.g., `SbomDetails`, `AdvisoryDetails`).
7. **Route mounting**: `server/main.rs` mounts all module routers; individual modules do not need explicit registration there since routes auto-mount via module registration.

### Error Handling Convention

- All handlers return `Result<T, AppError>`.
- Errors are wrapped with `.context("descriptive message")` using the `AppError` pattern from `common/src/error.rs`.
- 404 responses use `AppError` variants for "not found" cases (consistent with existing SBOM/advisory endpoints).

### Service Method Convention

- Service structs follow naming: `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`, `PackageService`).
- Standard methods: `fetch`, `list`, and domain-specific methods like `search` or `ingest`.
- Method signatures take `&self`, domain-specific identifiers, and `tx: &Transactional<'_>` for database transaction context.
- Services use SeaORM for database access.

### Model/Struct Convention

- Model structs derive `Serialize`, `Deserialize` (serde), and typically `Clone`, `Debug`.
- Summary structs are used for list responses; Details structs for individual resource responses.
- New model types get their own file under `model/` and are registered via `pub mod <name>;` in `model/mod.rs`.

### Entity/ORM Convention

- SeaORM entities reside in `entity/src/`.
- Join tables follow `<table1>_<table2>.rs` naming (e.g., `sbom_advisory.rs`, `sbom_package.rs`).

### Testing Convention

- Integration tests live in `tests/api/` with one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database.
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`.
- Test functions are `async` and use the standard Rust `#[tokio::test]` attribute.

### Naming Conventions

- Files: `snake_case.rs`
- Structs: `PascalCase` (e.g., `SeveritySummary`, `AdvisorySummary`)
- Methods: `snake_case` (e.g., `severity_summary`, `fetch`, `list`)
- Routes: kebab-case in URLs (e.g., `/api/v2/sbom/{id}/advisory-summary`)
- API versioning: All routes under `/api/v2/`

### Framework Stack

- **HTTP framework**: Axum
- **ORM**: SeaORM
- **Middleware**: tower-http (caching)
- **Serialization**: serde (JSON)
- **Database**: PostgreSQL
