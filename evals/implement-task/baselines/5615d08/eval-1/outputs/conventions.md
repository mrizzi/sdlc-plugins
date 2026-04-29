# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows a consistent `model/ + service/ + endpoints/` structure (observed in `sbom/`, `advisory/`, `package/`).
- Each sub-module has a `mod.rs` that re-exports child modules.

### Endpoint Patterns
- **Route registration**: Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`. Individual handlers live in separate files (e.g., `list.rs`, `get.rs`).
- **Path parameters**: Handlers extract path params via `Path<Id>` (observed in `get.rs` for both `sbom` and `advisory`).
- **Return types**: Handlers return `Result<Json<T>, AppError>` — Axum's `Json` extractor handles serialization. List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping for error messages, matching the pattern in `common/src/error.rs`.

### Service Patterns
- Services are structs with methods like `fetch`, `list`, and `search`.
- Service methods take `&self`, an entity ID or filter, and `tx: &Transactional<'_>` for database access.
- The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` follows this pattern with `fetch` and `list` methods.

### Model Patterns
- Response structs live in `model/` with one struct per file (e.g., `summary.rs`, `details.rs`).
- Models derive `Serialize`, `Deserialize`, and typically `Debug`, `Clone`.
- The `AdvisorySummary` struct in `model/summary.rs` includes a `severity` field used for severity classification.

### Naming Conventions
- **Files**: lowercase snake_case (e.g., `severity_summary.rs`).
- **Structs**: PascalCase (e.g., `SbomSummary`, `AdvisorySummary`, `PackageSummary`).
- **Service methods**: verb_noun pattern (e.g., `fetch`, `list`, `search`, `ingest`).
- **Endpoint handlers**: named by HTTP action (e.g., `get`, `list`).
- **Routes**: RESTful paths under `/api/v2/` prefix (e.g., `/api/v2/sbom`, `/api/v2/advisory`).

### Error Handling
- `AppError` enum in `common/src/error.rs` implements `IntoResponse`.
- All fallible operations use `.context("descriptive message")` for error wrapping.
- 404 errors are returned when entities are not found, consistent across `sbom` and `advisory` endpoints.

### Import Organization
- Framework imports (axum, serde) first, then crate-level imports, then module-local imports.

### Database Patterns
- Framework: SeaORM for database interaction.
- Join tables exist for many-to-many relationships (e.g., `sbom_advisory`, `sbom_package`).
- Entity definitions live in `entity/src/` with one file per entity.

## Test Conventions

### File Organization
- Integration tests live in `tests/api/` directory, one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database.

### Assertion Patterns
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and individual fields are checked.
- Error cases (404) follow `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` pattern.

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test Structure
- Non-trivial tests use setup (seed database), action (make HTTP request), assertion (check response) phases.
- No parameterized test patterns observed in sibling test files (standard `#[test]` or `#[tokio::test]` used).

### Documentation
- Per skill requirement: every test function gets a doc comment (`///`) regardless of sibling patterns.
- Non-trivial tests include given-when-then inline comments.
