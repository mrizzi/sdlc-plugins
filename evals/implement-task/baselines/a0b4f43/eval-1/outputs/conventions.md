# Conventions Discovered from Sibling Analysis

The following conventions were identified by inspecting existing code in the `trustify-backend` repository, particularly within the `modules/fundamental/src/advisory/` and `modules/fundamental/src/sbom/` modules and the `common/` crate.

## 1. Error Handling: `Result<T, AppError>` with `.context()`

All service methods and endpoint handlers return `Result<T, AppError>`. Errors are propagated using the `.context()` method (from the `anyhow` or similar error-chaining crate) to add descriptive context strings. The `AppError` enum in `common/src/error.rs` implements Axum's `IntoResponse` trait, so errors are automatically converted to appropriate HTTP status codes (e.g., 404 for not-found, 500 for internal errors).

**Pattern observed in**: `advisory/service/advisory.rs` (fetch, list methods), `advisory/endpoints/get.rs`, `common/src/error.rs`

## 2. Module Structure: `model/` + `service/` + `endpoints/`

Each domain module (sbom, advisory, package) follows a consistent three-directory structure:
- `model/` — Data structures (DTOs/response types) with Serde derives
- `service/` — Business logic and database queries
- `endpoints/` — Axum HTTP handlers that delegate to the service layer

Sub-modules are registered via `pub mod` declarations in each directory's `mod.rs`.

**Pattern observed in**: `advisory/`, `sbom/`, `package/` modules

## 3. Endpoint Handler Pattern: Extract, Call Service, Return JSON

Endpoint handlers follow a consistent pattern:
1. Extract path parameters using Axum's `Path<Id>` extractor
2. Obtain the service from Axum shared state/extensions
3. Call the appropriate service method with the extracted parameters and a `Transactional` reference
4. Return `Ok(Json(result))` on success
5. Return `AppError` on failure (automatically converted to HTTP response)

**Pattern observed in**: `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`

## 4. Route Registration Pattern

Routes are registered in each module's `endpoints/mod.rs` using Axum's `Router::new().route("/path", get(handler))` builder pattern. The server's `main.rs` mounts all module routers, so individual modules only need to define their sub-routes.

**Pattern observed in**: `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs`

## 5. Model Struct Conventions

Model structs derive `Serialize`, `Deserialize`, `Debug`, and `Clone`. Response structs use flat field layouts with primitive types. List endpoints wrap results in `PaginatedResults<T>` from `common/src/model/paginated.rs`, while single-entity or aggregation endpoints return the struct directly.

**Pattern observed in**: `advisory/model/summary.rs` (AdvisorySummary), `sbom/model/summary.rs` (SbomSummary)

## 6. Service Method Signature Convention

Service methods take `&self` plus domain-specific parameters and a `tx: &Transactional<'_>` parameter for database transaction management. They return `Result<T, AppError>` where T is the appropriate model type.

**Pattern observed in**: `advisory/service/advisory.rs` (fetch, list, search methods), `sbom/service/sbom.rs` (fetch, list, ingest methods)

## 7. Integration Test Pattern

Integration tests in `tests/api/` make real HTTP requests against a test database. Assertions use `assert_eq!(resp.status(), StatusCode::OK)` and similar status code checks. Each domain has its own test file (e.g., `advisory.rs`, `sbom.rs`).

**Pattern observed in**: `tests/api/advisory.rs`, `tests/api/sbom.rs`

## 8. Entity Join Tables for Cross-Domain Queries

Cross-domain relationships are modeled via explicit join tables in the `entity/` crate (e.g., `sbom_advisory.rs` for SBOM-to-Advisory links, `sbom_package.rs` for SBOM-to-Package links). Service methods query these join tables using SeaORM.

**Pattern observed in**: `entity/src/sbom_advisory.rs`, `entity/src/sbom_package.rs`
