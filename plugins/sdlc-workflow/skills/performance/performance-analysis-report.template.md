# Performance Analysis Report

**Generated:** {iso-8601-timestamp}  
**Workflow:** {workflow-name}  
**Baseline Date:** {baseline-capture-date}

---

## Executive Summary

**Overall Performance Rating:** {rating} (Excellent / Good / Needs Improvement / Poor)

**Key Findings:**
- {summary-bullet-1}
- {summary-bullet-2}
- {summary-bullet-3}

**Top 3 Optimization Opportunities:**
1. {opportunity-1} — Estimated impact: {impact-1}
2. {opportunity-2} — Estimated impact: {impact-2}
3. {opportunity-3} — Estimated impact: {impact-3}

---

## Workflow Metrics

| Metric | Current (p95) | Target | Status |
|---|---|---|---|
| LCP (Largest Contentful Paint) | {lcp-p95} ms | 2500 ms | {status} |
| FCP (First Contentful Paint) | {fcp-p95} ms | 1800 ms | {status} |
| DOM Interactive | {domInteractive-p95} ms | 3500 ms | {status} |
| Total Load Time | {total-p95} ms | 4000 ms | {status} |

---

## Bundle Composition

**Total JavaScript Size:** {total-js-size} KB  
**Third-Party Libraries:** {third-party-size} KB ({third-party-percentage}%)  
**Application Code:** {application-code-size} KB ({application-code-percentage}%)

**Top Third-Party Libraries by Size:**

| Library | Size | Used In |
|---|---|---|
| {library-1} | {size-1} KB | {scenarios-1} |
| {library-2} | {size-2} KB | {scenarios-2} |
| ... | ... | ... |

---

## Anti-Pattern Analysis

### {Anti-Pattern-Name}

**Severity:** {High / Medium / Low}  
**Confidence:** {High (Serena MCP) / Medium (Grep — good pattern) / Low (Grep — requires manual verification)}  
**Instances Found:** {count}  
**Estimated Impact:** {quantified-impact}

**Description:**
{brief-explanation-of-anti-pattern}

**Detected Instances:**

1. **{file-path}:{line-number}**
   ```{language}
   {code-snippet}
   ```
   **Issue:** {specific-issue-description}
   **Recommended Fix:** {actionable-recommendation}
   **Verification Checklist:**
   - [ ] {verification-step-1 from detection step}
   - [ ] {verification-step-2 from detection step}

{... repeat for each anti-pattern ...}

---

## Backend Source Code Analysis

**Note:** This section is included only if backend repository is configured (`backend_available = true`). Otherwise, omit this section entirely.

**Backend Repository:** {backend-repo-name} ({backend-framework})  
**Analysis Coverage:** {endpoints-analyzed} endpoints analyzed  
**Serena Status:** {serena-instance-name or "Grep fallback"}

### Backend Anti-Patterns Detected

#### Database N+1 Queries

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Latency Impact:** {(n_queries - 1) * 10ms}

**Detected Instances:**

1. **{handler-file-path}:{line-number}**
   ```{language}
   {code-snippet-showing-loop-with-queries}
   ```
   **Issue:** {count} queries executed sequentially in loop  
   **Recommended Fix:**
   - **SQL:** Use batch query: `SELECT * FROM table WHERE id IN (...)`
   - **SeaORM:** Use `.find()` with `filter(column.is_in(ids))` or `.find_with_related()` for eager loading
   - **Diesel:** Use `.filter(id.eq_any(ids))` for batch query
   - **JPA/Hibernate:** Use `@EntityGraph`, `JOIN FETCH` in JPQL, or `findAllById(ids)`
   - **SQLAlchemy:** Use `.filter(Model.id.in_(ids))` for batch query
   - **Django ORM:** Use `Model.objects.filter(id__in=ids)` or `.select_related()`

{... repeat for each N+1 instance ...}

#### Missing Pagination

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Payload Waste:** {(total_items - 20) * avg_item_size}

**Detected Instances:**

1. **Endpoint:** GET {endpoint-path}
   **Handler:** {handler-file-path}  
   **Issue:** Returns {item-count} items without pagination  
   **Recommended Fix:** Add `page` and `limit` query parameters, implement `.limit()` and `.offset()` in query

{... repeat for each pagination issue ...}

#### Missing Caching

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Latency Reduction:** {operation_time × analysis_cache_hit_rate}

**Detected Instances:**

1. **Endpoint:** GET {endpoint-path}
   **Handler:** {handler-file-path}  
   **Issue:** {expensive-operation-description} on every request (no cache detected)  
   **Data Change Frequency:** {static / slow-changing / fast-changing}  
   **Recommended Fix:** Implement cache layer (Redis, in-memory) with appropriate TTL

{... repeat for each caching issue ...}

#### Inefficient Queries

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Impact:** 30-50% query time reduction

**Detected Instances:**

1. **Query:** {query-snippet}
   **Handler:** {handler-file-path}:{line-number}  
   **Issue:** SELECT * fetches {column-count} columns but only {used-count} used in response  
   **Recommended Fix:** Specify exact columns: `SELECT id, name, price FROM products WHERE ...`

{... repeat for each inefficient query ...}

#### Unused Table Joins

**Severity:** {Critical / High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Impact:** {total_latency_saved}ms saved per request

**Description:** Database queries that JOIN tables but never access fields from the joined tables, wasting database CPU, I/O, and memory resources.

**Detected Instances:**

1. **Endpoint:** {endpoint_method} {endpoint_path}
   **Handler:** {handler-file-path}:{line-number}  
   **Query:**
   ```{language}
   {full_query_with_highlighted_join}
   ```
   **Unused Join:** `{joined_table}` (alias: `{alias}`)  
   **Reason:** No fields from `{joined_table}` accessed in SELECT, WHERE, or response schema  
   **Join Type:** {INNER/LEFT/RIGHT JOIN}  
   **Table Size:** {estimated_row_count} rows  
   **Index Status:** {Indexed/Not Indexed} on foreign key  
   **Estimated Overhead:** {overhead_ms}ms per query  
   **Call Frequency:** {single/N+1 with count calls}  
   **Total Impact:** {total_impact}ms per request  
   **Recommended Fix:**
   ```{language}
   {optimized_query_without_unused_join}
   ```

{... repeat for each unused join instance ...}

**Total Estimated Impact:** {sum_of_all_impacts}ms reduction across {count} endpoints

#### Service Chain Analysis (Deep Call Graph)

**Depth Analyzed:** {chain_depth} levels  
**Total Handlers Traced:** {handler_count}  
**Analysis Method:** {Serena MCP (High Confidence) / Grep (Fallback - Medium Confidence)}

{... for each handler with call chain findings ...}

##### Endpoint: {endpoint_method} {endpoint_path}

**Call Graph:**
```
{endpoint_method} {endpoint_path}
  └─ {callee_1}          [{file}:{line}]
       ├─ {callee_2}     [{file}:{line}]    ← {query_annotation}
       └─ {callee_3}     [{file}:{line}]
            ├─ {callee_4}  [{file}:{line}]  ← {query_annotation}
            └─ {callee_5}  [{file}:{line}]  ← {query_annotation}
```

**Query Ledger:**

| # | Query | Source | Depth | Loop Mult. | Effective Count |
|---|---|---|---|---|---|
| {n} | {description} | {file:line} | {depth} | {multiplier} | {effective} |
| **Total** | | | | | **{total_queries}** |

**Estimated Total DB Latency:** {total_queries * analysis_db_latency_ms}ms  

**Anti-Patterns Found at Depth:**
- Depth {N}: {anti-pattern-description} in `{symbol_name}` ({file}:{line})

{... end for each handler ...}

---

#### Wasted Computation

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}

**Description:** Handlers that call service methods returning substantial data but only use a subset of the result. The unused portion may involve database queries that execute needlessly.

**Detected Instances:**

1. **Endpoint:** {endpoint_method} {endpoint_path}
   **Handler:** {handler-file-path}:{line-number}  
   **Service Call:** `{service.method_name(...)}`  
   **Returns:** `{ReturnType}` with {total_field_count} fields  
   **Handler Uses:** {used_field_count} fields ({used_field_list})  
   **Wasted Fields:** {unused_field_list}  
   **Wasted Queries:** {count} queries ({wasted_query_latency}ms estimated)  
   **Recommended Fix:** Create `{optimized_method_name}()` that returns only needed data, or add a field projection parameter

{... repeat for each wasted computation instance ...}

---

#### Conditional Query Patterns (Memo/Option)

**Severity:** {High / Medium / Low}
**Instances Found:** {count}
**Estimated Impact:** {total_conditional_queries} additional queries per request

**Description:** Functions that accept lazy-load parameters (`Memo<T>`, `Option<T>`) and fire
database queries when callers pass the un-provided variant instead of pre-loading the data.

**Detected Instances:**

1. **Function:** `{function_name}` ({file}:{line})
   **Parameter:** `{param_name}: Memo<{Type}>`
   **Conditional Query:** `{query_description}` — fires when `Memo::NotProvided` is passed
   **Callers passing NotProvided:**
   - `{caller_1}` ({file}:{line}) — inside loop (×{iterations}) = {effective_count} queries
   - `{caller_2}` ({file}:{line}) — single call = 1 query
   **Total Impact:** {sum_effective} conditional queries per request
   **Recommended Fix:** Pre-load `{Type}` in batch at the caller level and pass via `Memo::Provided`

{... repeat for each instance ...}

---

#### Inter-Query SQL Duplication

**Severity:** {High / Medium / Low}
**Instances Found:** {count}
**Estimated Impact:** {redundant_executions} redundant CTE/subquery executions per request

**Description:** Multiple queries within the same handler chain that contain identical or
semantically equivalent CTEs/subqueries, causing the database to compute the same intermediate
results multiple times.

**Detected Instances:**

1. **Duplicated CTE:** `{cte_name}`
   **Appears in:** {count} queries within handler for {endpoint}
   **Queries:**
   - Query #{n1}: {description_1} ({source_1})
   - Query #{n2}: {description_2} ({source_2})
   **Shared SQL:**
   ```sql
   {shared_sql_fragment}
   ```
   **Estimated Overhead:** {(count-1)} redundant executions × {est_time}ms = {total_overhead}ms
   **Recommended Fix:** {Extract to materialized temp table / Refactor to single query}

{... repeat for each instance ...}

---

#### Missing Database Indexes

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Migration Directory:** {migration_path}

**Description:** Query WHERE/JOIN columns (found at any depth in the call chain) that lack database indexes, causing sequential scans instead of index lookups.

**Detected Instances:**

1. **Table:** `{table_name}`  
   **Column:** `{column_name}`  
   **Used In:** {query_description} (`{source_file}:{line}`)  
   **Query Type:** {WHERE filter / JOIN condition / ORDER BY}  
   **Loop Multiplier:** {from query_ledger — how many times this query fires per request}  
   **Estimated Impact:** Sequential scan on {estimated_rows} rows vs. index lookup  
   **Recommended Fix:**
   ```sql
   CREATE INDEX idx_{table}_{column} ON {table}({column});
   ```

{... repeat for each missing index ...}

---

### Cross-Repository Over-Fetching Analysis

**Note:** This analysis cross-references backend response schemas with frontend field usage.

#### Per-Endpoint Analysis

##### Endpoint: GET {endpoint-path}

**Backend Handler:** {handler-file-path}  
**Response Type:** {ResponseStructName}  
**Total Fields:** {total-field-count}  
**Used by Frontend:** {used-field-count}  
**Unused Fields:** {unused-field-list}  
**Over-Fetching Percentage:** {waste-percentage}%  
**Call Pattern:** {Single call / N+1 (count calls)}  
**Payload Waste:** {waste-bytes} KB per request × {call-count if N+1} calls = {total-waste} KB  
**Recommendation:** {Create specialized DTO / Use GraphQL / Field projection}

{... repeat for each endpoint ...}

---

### Cross-Layer Computation Waste

**Note:** This section is included only when `analysis_scope` is `full-stack` or `full-stack-monorepo`
AND backend chain analysis (Step 7.6.2) completed successfully.

**Severity:** {Critical / High / Medium / Low}
**Instances Found:** {count}
**Estimated Impact:** {total_wasted_queries} wasted queries per dashboard load

**Description:** Backend endpoints compute expensive response fields (requiring database queries)
that the frontend never reads. Unlike handler-level waste (Wasted Computation section above),
this detects waste at the HTTP API boundary — where the backend serves fields the frontend discards.

**Detected Instances:**

1. **Endpoint:** {method} {path}
   **Total Backend Query Cost:** {total_queries} queries ({total_latency}ms)
   **Frontend-Used Fields:** {field_list} — Cost: {used_queries} queries
   **Frontend-Unused Fields:** {field_list} — Cost: {wasted_queries} queries
   **Cross-Layer Waste:** {waste_pct}% of backend computation serves no frontend purpose
   **Call Pattern:** {single / N+1 (×count)}
   **Total Wasted Queries:** {wasted × call_count}
   **Recommended Fix:** {recommendation}

{... repeat for each instance ...}

---

## Dynamic Performance Testing

**Note:** This section is included only if dynamic testing was executed (backend running + test data manifest exists).

**Status:** Service running on localhost:{port}  
**Methodology:** curl loop — cold-cache first request + {iterations} warm-cache requests for p50/p95/p99 percentiles  
**Iterations:** {iterations} requests per endpoint

### Endpoint Performance Metrics

{... for each endpoint in dynamic_results ...}

#### Endpoint: {endpoint_method} {endpoint_path}

**Test URL:** {test_url}

**Response Time (milliseconds)**:
| Metric | Value |
|---|---|
| p50 (Median) | {p50}ms |
| p95 | {p95}ms |
| p99 | {p99}ms |
| Mean | {mean}ms |

**Cache Effectiveness**:
- First request: {first_request_ms}ms (cache miss)
- Subsequent mean: {mean}ms (cache hits)
- Improvement: {cache_improvement_pct}% faster
- **Status**: {cache_status} ✅/⚠️

**Dynamic vs Static Comparison**:
| Source | Estimate | Notes |
|---|---|---|
| Static Analysis | **[Manual: See Backend Source Code Analysis section]** | Check N+1 query findings, estimated overhead |
| Dynamic Actual | {p95}ms (p95) | Measured with curl loop |
| Variance | **[Manual: Calculate]** | If >200ms: Database profiling needed |

**Recommendation**: Review static analysis estimates. If variance >200ms, database query optimization is critical priority.

{... end for each endpoint ...}

### Summary

**Total Endpoints Tested:** {count}  
**Cache-Effective Endpoints:** {count with "Effective" status}  
**Slow Endpoints (p95 > 500ms):** {count}  
**Recommended Actions:**
- Endpoints with >200ms variance: Profile with database query analyzer
- Minimal cache effectiveness: Review caching strategy
- Slow endpoints: Prioritize for optimization

---

## Recommended Optimizations

**Note:** Optimizations are categorized by layer (Frontend / Backend / Integration) when backend analysis is available.

Optimizations are prioritized by estimated impact (time or size savings).

| Priority | Optimization | Estimated Impact | Effort |
|---|---|---|---|
| 1 | {optimization-1} | {impact-1} | {effort-1} |
| 2 | {optimization-2} | {impact-2} | {effort-2} |
| 3 | {optimization-3} | {impact-3} | {effort-3} |
| ... | ... | ... | ... |

**Effort Legend:**
- **Low:** < 1 day of work
- **Medium:** 1-3 days of work
- **High:** > 3 days of work

---

## Next Steps

1. Review this report with the team and prioritize optimizations
2. Create optimization plan and Jira Epic/Tasks using `/sdlc-workflow:performance-plan-optimization`
3. After implementing optimizations, re-run `/sdlc-workflow:performance-baseline` to capture new baseline and measure improvements
