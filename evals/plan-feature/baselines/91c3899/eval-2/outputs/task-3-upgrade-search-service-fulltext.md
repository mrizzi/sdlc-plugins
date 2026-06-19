## Repository
trustify-backend

## Target Branch
main

## Description
Upgrade the `SearchService` in the search module to use PostgreSQL full-text search instead of the current text matching approach. This replaces basic string matching with weighted `ts_rank_cd` ranking, making search results more relevant by prioritizing matches in important fields (e.g., title matches rank higher than description matches).

**ASSUMPTION pending clarification:** "More relevant results" is interpreted as implementing ranked full-text search with field weighting. Without explicit relevance criteria from the product owner, the weighting scheme (title > description > metadata) is a best-effort assumption.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor `SearchService` full-text search method to use `build_tsquery` and `apply_fulltext_rank` helpers from `common/src/db/query.rs` instead of current text matching; add entity-specific weight configurations
- `modules/search/Cargo.toml` — Add dependency on `common` crate if not already present

## Implementation Notes
- The current `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Replace the existing search query construction with calls to the new `build_tsquery` and `apply_fulltext_rank` helpers from `common/src/db/query.rs`
- Configure per-entity weight maps:
  - SBOM: name (weight A=1.0), description (weight B=0.4)
  - Advisory: title (weight A=1.0), description (weight B=0.4), severity (weight C=0.2)
  - Package: name (weight A=1.0), license (weight B=0.2)
- The search should query each entity table's `search_vector` column (added by the migration in Task 1)
- Results should be ordered by `ts_rank_cd` score descending, then by existing sort criteria as tiebreaker
- Maintain backward compatibility: the search endpoint should still return the same response shape, just with better-ordered results
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure when modifying the search module. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module structure scope.
- Per Key Conventions §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs::build_tsquery` — Query builder helper (from Task 2) for converting user input to tsquery
- `common/src/db/query.rs::apply_fulltext_rank` — Query builder helper (from Task 2) for adding rank-based ordering
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` as a reference for service method patterns (fetch, list, search)
- `common/src/error.rs::AppError` — Error type for `.context()` wrapping pattern

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL `ts_rank_cd` for result ordering instead of basic text matching
- [ ] Search results are ranked by relevance with title/name matches weighted higher than description matches
- [ ] Search queries use `tsquery` for proper lexeme matching (stemming, normalization)
- [ ] Response shape is unchanged — existing consumers are not broken
- [ ] Empty search queries return results in default sort order (no ranking)
- [ ] Service methods use `Result<T, AppError>` with `.context()` wrapping

## Test Requirements
- [ ] Integration test: search for a term that appears in an SBOM name returns that SBOM ranked first
- [ ] Integration test: search for a term in an advisory description ranks it lower than a title match
- [ ] Integration test: search with no matches returns empty results (not an error)
- [ ] Integration test: empty search query returns results without error

## Dependencies
- Depends on: Task 1 — Add full-text search migration (tsvector columns and indexes must exist)
- Depends on: Task 2 — Add full-text query helpers (build_tsquery and apply_fulltext_rank must be available)
