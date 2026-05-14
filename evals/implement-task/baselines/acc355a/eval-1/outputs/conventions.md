# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows a `model/ + service/ + endpoints/` tripartite structure (observed in `advisory/`, `sbom/`, `package/` modules)
- Module registration via `mod.rs` files: each subdirectory has a `mod.rs` that re-exports public items
- New model files must be registered in the parent `model/mod.rs` with `pub mod <name>;`
- New endpoint files must be registered in the parent `endpoints/mod.rs` with `mod <name>;`

### Error Handling with Result<T, AppError> and .context()
- All handlers and service methods return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- `AppError` implements `IntoResponse` for Axum compatibility, mapping error variants to HTTP status codes
- Error wrapping uses `.context("descriptive message")` pattern from `anyhow` for error chaining
- 404 errors are returned when entity lookup fails (consistent across all SBOM and advisory endpoints)
- Pattern: `service_call().await.context("description")?.ok_or_else(|| AppError::not_found(...))?`

### Endpoint Patterns (from `endpoints/get.rs`, `endpoints/list.rs` siblings)
- All endpoint handlers extract path parameters via `Path<Id>` (Axum extractor)
- Handlers call the corresponding service method, passing `&self`, the entity ID, and `tx: &Transactional<'_>`
- Return type: `Result<Json<T>, AppError>` -- Axum's `Json` extractor handles serialization
- Route registration in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the model struct directly wrapped in `Json`

### Service Patterns (from `advisory.rs`, `sbom.rs` service siblings)
- Service structs (e.g., `AdvisoryService`, `SbomService`) contain methods like `fetch`, `list`, `search`
- Method signatures follow: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Methods use `.context()` wrapping from `anyhow` for error chaining
- Service methods follow `verb_noun` naming (e.g., `fetch`, `list`, `search`)

### Model Patterns (from `summary.rs`, `details.rs` siblings)
- Models are plain Rust structs deriving `Serialize`, `Deserialize`, and likely `Debug`, `Clone`
- Each model file defines a single primary struct
- Model structs represent API response shapes
- Module registration: parent `mod.rs` contains `pub mod <name>;` for each model file

### Database / ORM Patterns
- SeaORM is used for database access
- Join tables (e.g., `sbom_advisory.rs`, `sbom_package.rs`) are defined in the `entity/` crate
- Queries use SeaORM's query builder with shared helpers from `common/src/db/query.rs`
- Entity access pattern: `entity::<table>::Entity::find().filter(...).all(connection).await`

### Naming Conventions
- Files: snake_case (e.g., `severity_summary.rs`, `sbom_advisory.rs`)
- Structs: PascalCase (e.g., `SeveritySummary`, `AdvisorySummary`)
- Methods: snake_case following `verb_noun` pattern
- Routes: kebab-case in URL paths (e.g., `/api/v2/sbom/{id}/advisory-summary`)
- API versioning: `/api/v2/` prefix on all endpoints

### Import Organization
- Standard library imports first, then external crates, then internal modules
- `use` statements grouped by crate origin

## Test Conventions

### Test Structure (from `tests/api/` siblings: `sbom.rs`, `advisory.rs`, `search.rs`)
- Integration tests live in `tests/api/` directory
- Tests hit a real PostgreSQL test database (not mocked)
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks, followed by body deserialization
- Error case tests verify `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for missing entities

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`, `test_advisory_summary_not_found`)

### Test Organization
- One test file per endpoint group (e.g., `advisory.rs` for advisory endpoints, `sbom.rs` for SBOM endpoints)
- Tests grouped by endpoint within each file

### Assertion Patterns
- Status code assertions first: `assert_eq!(resp.status(), StatusCode::OK)`
- Body deserialization into the expected response struct
- Field-level value assertions (not just length checks or status-only checks)
- 404 tests for non-existent entity IDs

### Test Documentation
- Doc comments on every test function (constraint 5.11)
- Given-When-Then inline comments in non-trivial tests (constraint 5.12)
