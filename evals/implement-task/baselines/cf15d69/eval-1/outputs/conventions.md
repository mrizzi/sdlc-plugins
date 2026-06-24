# Discovered Conventions

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) was validated. All required sections are present:

1. **Repository Registry** -- contains `trustify-backend` with Role `Rust backend service`, Serena Instance `serena_backend`, Path `./`
2. **Jira Configuration** -- contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>`

Configuration is valid. Proceeding.

## Step 1 -- Parsed Task Fields

- **Jira ID**: TC-9201
- **Summary**: Add advisory severity aggregation service and endpoint
- **Repository**: trustify-backend
- **Target Branch**: main
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Review Context**: not present
- **Dependencies**: None
- **Labels**: ai-generated-jira
- **Linked Issues**: is incorporated by TC-9001

### GitHub Issue extraction

GitHub Issue custom field ID: `customfield_10747`. This is a synthetic eval -- the field value would be read from the fetched issue's fields. Not present in the mock data, so skipped.

## Step 1.5 -- Description Digest Verification

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`. If found:

1. Check comment `created` vs `updated` timestamps for edit detection
2. Extract the tagged digest value (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`)
3. Write the current description to `/tmp/desc-TC-9201.txt` and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
4. Compare format tags -- if they differ, log a warning about format mismatch and proceed
5. Compare hex digests -- if they match, proceed silently; if they mismatch, alert the user and ask whether to proceed or stop

If no digest comment found, log: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 -- Dependencies

Dependencies section says "Depends on: None". No dependency verification needed.

## Conventions Discovered from Sibling Analysis (Step 4)

### Production code conventions

Based on analysis of sibling files in the `modules/fundamental/src/` module:

- **Module structure**: Every domain follows `model/ + service/ + endpoints/` trifecta. Each subdirectory has a `mod.rs` for module registration.
- **Framework**: Axum for HTTP routing, SeaORM for database ORM.
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`. No unwrap or panic in production code.
- **Naming (service methods)**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search` in `AdvisoryService`; `fetch`, `list`, `ingest` in `SbomService`).
- **Naming (files)**: Model files are named after the concept they represent (e.g., `summary.rs`, `details.rs`). Endpoint files are named after the HTTP operation (e.g., `get.rs`, `list.rs`).
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes via `Router::new().route("/path", get(handler))`. The `server/main.rs` mounts all modules but requires no changes for new routes within existing modules.
- **Service method signatures**: Methods take `&self`, a domain ID parameter, and `tx: &Transactional<'_>` for database transactional context.
- **Path extraction**: Endpoint handlers extract path parameters via `Path<Id>` (Axum extractor).
- **Response types**: Single-entity endpoints return the struct directly (Axum `Json` handles serialization). List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Model structs**: Use `#[derive(Serialize, Deserialize, Debug)]` at minimum. Structs in `model/` are response DTOs.
- **Import organization**: Standard Rust convention -- std first, external crates second, internal modules third.
- **Query helpers**: Filtering, pagination, and sorting via `common/src/db/query.rs`.
- **Join tables**: Cross-entity relationships use dedicated join-table entities in `entity/src/` (e.g., `sbom_advisory.rs` for SBOM-Advisory relationships).

### CONVENTIONS.md lookup

The repository has a `CONVENTIONS.md` at the root. In a real implementation, this would be read via `mcp__serena_backend__list_dir` or Read to extract:
- Naming rules, directory structure for new files, code patterns
- CI check commands (verification commands extraction)
- Code generation commands

### Test conventions (from sibling test analysis)

Based on analysis of sibling test files in `tests/api/`:

- **Test location**: Integration tests live in `tests/api/` directory, one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks followed by body deserialization.
- **Response validation**: Endpoint tests validate response body fields after deserializing from JSON.
- **Error cases**: Tests include 404 checks with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent entity IDs.
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Test database**: Integration tests hit a real PostgreSQL test database (not mocks).
- **Test organization**: One test file per domain module. New endpoint tests go in a new file in `tests/api/`.
- **Parameterized tests**: Not observed in the described sibling tests. Will not introduce `#[rstest]` unless seen in actual codebase analysis.

### Documentation files identified

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (relevant for new endpoint documentation)
