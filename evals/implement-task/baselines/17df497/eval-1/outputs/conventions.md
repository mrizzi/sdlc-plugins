# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows a `model/ + service/ + endpoints/` tripartite structure
- Module registration via `mod.rs` files: each subdirectory has a `mod.rs` that re-exports public items
- New model files must be registered in the parent `model/mod.rs` with `pub mod <name>;`

### Endpoint Patterns (from `endpoints/get.rs`, `endpoints/list.rs` siblings)
- All endpoint handlers extract path parameters via `Path<Id>` (Axum extractor)
- Handlers call the corresponding service method, passing `&self`, the entity ID, and `tx: &Transactional<'_>`
- Return type: `Result<Json<T>, AppError>` — Axum's `Json` extractor handles serialization
- Route registration in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the model struct directly wrapped in `Json`

### Service Patterns (from `advisory.rs`, `sbom.rs` service siblings)
- Service structs (e.g., `AdvisoryService`, `SbomService`) contain methods like `fetch`, `list`, `search`
- Method signatures follow: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Methods use `.context()` wrapping from `anyhow` for error chaining
- Service methods follow `verb_noun` naming (e.g., `fetch`, `list`, `search`, `severity_summary`)

### Model Patterns (from `summary.rs`, `details.rs` siblings)
- Models are plain Rust structs deriving `Serialize`, `Deserialize`, and likely `Debug`, `Clone`
- Each model file defines a single primary struct
- Model structs represent API response shapes
- Module registration: parent `mod.rs` contains `pub mod <name>;` for each model file

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- `AppError` implements `IntoResponse` for Axum compatibility
- Error wrapping uses `.context("descriptive message")` pattern from `anyhow`
- 404 errors returned when entity lookup fails (consistent with existing SBOM/advisory endpoints)

### Database / ORM Patterns
- SeaORM is used for database access
- Join tables (e.g., `sbom_advisory.rs`, `sbom_package.rs`) are defined in the `entity/` crate
- Queries use SeaORM's query builder with shared helpers from `common/src/db/query.rs`

### Naming Conventions
- Files: snake_case (e.g., `severity_summary.rs`, `sbom_advisory.rs`)
- Structs: PascalCase (e.g., `SeveritySummary`, `AdvisorySummary`)
- Methods: snake_case following `verb_noun` pattern
- Routes: kebab-case in URL paths (e.g., `/api/v2/sbom/{id}/advisory-summary`)

### Import Organization
- Standard library imports first, then external crates, then internal modules
- `use` statements grouped by crate origin

## Test Conventions

### Test Structure (from `tests/api/` siblings: `sbom.rs`, `advisory.rs`, `search.rs`)
- Integration tests live in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks, followed by body deserialization
- Error case tests verify `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for missing entities

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`, `test_advisory_summary_not_found`)

### Test Organization
- One test file per endpoint group (e.g., `advisory.rs` for all advisory endpoints)
- Tests grouped by endpoint within each file

### Assertion Patterns
- Status code assertions first: `assert_eq!(resp.status(), StatusCode::OK)`
- Body deserialization into the expected response struct
- Field-level value assertions (not just length checks)
- 404 tests for non-existent entity IDs
