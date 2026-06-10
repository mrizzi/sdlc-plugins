# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:
1. **Repository Registry** -- present, with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with `rust-analyzer`

Configuration is valid. Proceed.

## Step 1 -- Task Parsing

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none
- **GitHub Issue custom field**: customfield_10747 (not populated on this task)

## Step 4 -- Code Inspection and Convention Conformance Analysis

### CONVENTIONS.md Lookup

Would check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). The repo structure shows `CONVENTIONS.md` exists at the root. Would read it via `mcp__serena_backend__read_file` or direct Read. Would extract any CI check commands and code generation commands listed therein.

### Production Code Conventions (from sibling analysis)

#### Module Structure
- **Module pattern**: every domain module follows `model/ + service/ + endpoints/` directory structure (observed in `sbom/`, `advisory/`, `package/`)
- **Model sub-modules**: each model directory has a `mod.rs` that re-exports sub-modules; individual model structs live in their own files (e.g., `summary.rs`, `details.rs`)
- **Service sub-modules**: service logic lives in a file named after the domain entity (e.g., `sbom.rs`, `advisory.rs`) with a `mod.rs` re-export
- **Endpoint sub-modules**: each endpoint handler lives in its own file (e.g., `list.rs`, `get.rs`) with route registration in `endpoints/mod.rs`

#### Endpoint Patterns (siblings: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`)
- **Route registration**: `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- **Path extraction**: handlers use `Path<Id>` extractor for path parameters
- **Return type**: handlers return `Result<Json<T>, AppError>` where `T` is the response struct
- **Error handling**: all handlers use `Result<T, AppError>` with `.context()` wrapping for error propagation (pattern from `common/src/error.rs`)
- **List responses**: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Single-item responses**: get endpoints return the struct directly via `Json` (Axum handles serialization)

#### Service Patterns (siblings: `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)
- **Method signatures**: service methods take `&self`, entity-specific ID parameter, and `tx: &Transactional<'_>` as the last parameter
- **Naming**: service methods follow `verb_noun` pattern -- `fetch`, `list`, `search` (observed in AdvisoryService and SbomService)
- **Return type**: `Result<T, AppError>` with `.context()` wrapping

#### Model Patterns (siblings: `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)
- **Struct definition**: response structs derive `Serialize, Deserialize, Debug, Clone`
- **Field types**: use standard Rust types; severity fields exist on `AdvisorySummary`
- **Module registration**: each new model file must be registered as `pub mod <name>;` in the parent `mod.rs`

#### Error Handling
- **Error type**: `AppError` enum from `common/src/error.rs`, implements `IntoResponse`
- **Wrapping**: `.context("descriptive message")` from anyhow/thiserror pattern
- **404 pattern**: return appropriate error variant when entity not found, consistent with existing SBOM endpoints

#### Import Organization
- Framework imports (axum, serde) first, then crate imports, then local module imports

#### Database Patterns
- **ORM**: SeaORM for database operations
- **Join tables**: `sbom_advisory` join table in `entity/src/sbom_advisory.rs` links SBOMs to advisories
- **Query helpers**: shared filtering/pagination/sorting via `common/src/db/query.rs`

### Test Conventions (from sibling test analysis)

Sibling test files: `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization
- **Response validation**: endpoint tests validate response body structure and specific field values
- **Error cases**: all endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Test setup**: integration tests hit a real PostgreSQL test database
- **Test organization**: one file per domain area in `tests/api/`
- **Parameterized tests**: no evidence of `#[rstest]` usage in sibling tests -- would not introduce parameterized tests
- **No given-when-then comments observed in siblings**, but per SKILL.md Step 7, AI-generated tests must include doc comments and given-when-then section comments for non-trivial tests regardless

### Documentation Files Identified

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (relevant: new endpoint being added)
