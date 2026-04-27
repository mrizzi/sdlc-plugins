# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Clarifications Needed

The feature description TC-9002 contains significant ambiguities that must be resolved before implementation. The following items require clarification from the product owner:

### Critical Ambiguities

1. **"Search should be faster" — no performance target defined.**
   - What is the current search latency? What is the target latency?
   - **Assumption (if not clarified):** Target p95 response time of <500ms for full-text search queries. Current baseline must be measured before optimization.

2. **"Results should be more relevant" — no relevance criteria defined.**
   - What does "relevant" mean in the context of SBOMs, advisories, and packages? Is it keyword matching, semantic relevance, or ranking by recency/severity?
   - Are there specific user complaints or examples of irrelevant results?
   - **Assumption (if not clarified):** Improve relevance by adding field-weighted scoring (e.g., title matches rank higher than description matches) and supporting phrase matching.

3. **"Add filters" — no filter specification.**
   - Which entity types should be filterable (SBOMs, advisories, packages, or all)?
   - Which fields should be filterable (e.g., severity, date range, license type, package name)?
   - Should filters be combinable (AND logic)?
   - **Assumption (if not clarified):** Add filters for entity type (SBOM, advisory, package), severity (for advisories), and date range. Filters are combinable via AND logic.

4. **"Better UI" — no design provided, marked as non-MVP.**
   - No Figma mockup or design specification provided.
   - This requirement is excluded from MVP scope per the feature description.
   - **Action:** Excluded from this implementation plan. Will require a separate feature with design specifications.

5. **"Should be fast enough" (NFR) — no quantitative target.**
   - See ambiguity #1 above; same clarification applies.

6. **"Don't break existing functionality" — no regression test baseline mentioned.**
   - **Assumption:** Existing integration tests in `tests/api/search.rs` define the current behavioral contract. All existing tests must continue to pass.

7. **Search scope is undefined.**
   - The current `SearchService` provides "full-text search across entities." It is unclear whether the improvements should cover all entity types equally or prioritize specific ones.
   - **Assumption:** Improvements apply to all entity types (SBOMs, advisories, packages) served by the existing `SearchService`.

8. **No pagination/sorting requirements for search results.**
   - The existing list endpoints use `PaginatedResults<T>`, but it is unclear whether search results already support pagination or if this is a gap.
   - **Assumption:** Search results should use the existing `PaginatedResults<T>` pattern from `common/src/model/paginated.rs` if not already doing so.

---

## Impact Map

```
trustify-backend:
  changes:
    - Optimize SearchService full-text search query for performance (add database indexes, optimize query construction)
    - Add field-weighted relevance scoring to search results (title > description > content)
    - Add search filter parameters: entity type, severity (advisories), date range
    - Add filter parsing and query construction to search endpoint
    - Extend GET /api/v2/search endpoint to accept filter query parameters
    - Ensure search results use PaginatedResults<T> with proper pagination and sorting
    - Add integration tests for search filters, relevance ordering, and performance
    - Add database migration for search-related indexes if needed
```

---

## Assumptions Summary

All assumptions above are provisional and should be confirmed with the product owner before implementation begins. Tasks are written against these assumptions but tagged so that scope can be adjusted after clarification.
