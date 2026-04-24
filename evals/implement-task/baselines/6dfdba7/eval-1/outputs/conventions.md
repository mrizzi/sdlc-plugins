# Conventions Discovered from Sibling Analysis

## Source: trustify-backend repository structure and task implementation notes

### Module Structure Convention

Every domain module under `modules/fundamental/src/` follows a strict three-directory pattern:

```
<domain>/
  mod.rs
  model/
    mod.rs
    summary.rs      # Summary struct for the domain entity
    details.rs      # Details struct (optional, for detailed views)
  service/
    mod.rs
    <domain>.rs     # Service struct with fetch, list, and other methods
  endpoints/
    mod.rs          # Route registration
    list.rs         # GET list endpoint
    get.rs          # GET single-entity endpoint
```

Siblings observed: `sbom/`, `advisory/`, `package/` all follow this pattern exactly.

### Endpoint Registration Convention

- Each module's `endpoints/mod.rs` registers routes using Axum's `Router::new().route("/path", get(handler))` pattern.
- Routes are grouped by module and mounted by `server/src/main.rs`.
- Route paths follow `/api/v2/<resource>` naming.

### Service Method Signature Convention

Service methods follow a consistent signature pattern:

```rust
pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>
```

Observed on `AdvisoryService` (fetch, list, search) and `SbomService` (fetch, list, ingest).

### Error Handling Convention

- All handlers return `Result<T, AppError>`.
- Errors use `.context()` wrapping from the `anyhow` / `AppError` pattern defined in `common/src/error.rs`.
- `AppError` implements `IntoResponse` for automatic HTTP status code mapping (e.g., not-found maps to 404).

### Endpoint Handler Convention

Endpoint handlers:

- Extract path parameters via Axum's `Path<Id>` extractor.
- Accept service state via Axum's `State` or `Extension` extractor.
- Call the corresponding service method.
- Return the result directly; Axum's `Json` extractor handles serialization via `serde::Serialize`.

Observed in `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`.

### Response Struct Convention

- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-entity endpoints return the domain struct directly (auto-serialized to JSON).
- Structs derive `serde::Serialize` and `serde::Deserialize`.

### Model Module Registration Convention

Each `model/mod.rs` registers sub-modules via `pub mod <name>;` declarations. Existing entries:

- `advisory/model/mod.rs` has `pub mod summary;` and `pub mod details;`
- `sbom/model/mod.rs` has `pub mod summary;` and `pub mod details;`

New model files must be registered in the parent `mod.rs`.

### Testing Convention

- Integration tests live in `tests/api/` at the workspace root.
- Test files are named after the domain entity (e.g., `sbom.rs`, `advisory.rs`).
- Tests hit a real PostgreSQL test database.
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for success cases.
- Each test function sets up test data, makes an HTTP request, and asserts on the response body/status.

### Entity Convention

- SeaORM entities live in `entity/src/`.
- Join tables follow the `<left>_<right>.rs` naming pattern (e.g., `sbom_advisory.rs`, `sbom_package.rs`).

### Dependency / Import Convention

- Cross-crate imports reference the workspace crate name (e.g., `use trustify_common::error::AppError;`).
- Entity imports: `use trustify_entity::sbom_advisory;`.
- Module-internal imports use `crate::` or `super::` paths.

### Commit Message Convention

Based on the project's Jira configuration (project key: TC) and Conventional Commits:

```
feat(advisory): add severity aggregation endpoint

TC-9201
```
