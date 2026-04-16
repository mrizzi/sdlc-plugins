---
generated_by: {{skill-name}}
timestamp: {{iso-8601-timestamp}}
repository: {{repository-name}}
module: {{module-name}}
---

# Module Analysis Report: {{module-name}}

## Module Overview

- **Module Name:** {{module-name}}
- **Entry Point:** `{{entry-point-path}}`
- **Analysis Date:** {{analysis-date}}
- **Baseline LCP:** {{baseline-lcp}} ms
- **Baseline Bundle Size:** {{baseline-bundle-size}} KB

## Bundle Analysis

### Bundle Composition

| Component | Size (KB) | % of Total | Type |
|---|---|---|---|
| {{bundle-component-1-name}} | {{bundle-component-1-size}} | {{bundle-component-1-percent}} | {{bundle-component-1-type}} |
| {{bundle-component-2-name}} | {{bundle-component-2-size}} | {{bundle-component-2-percent}} | {{bundle-component-2-type}} |
| {{bundle-component-3-name}} | {{bundle-component-3-size}} | {{bundle-component-3-percent}} | {{bundle-component-3-type}} |

**Total Bundle Size:** {{total-bundle-size}} KB

### Third-Party Libraries

| Library | Size (KB) | Version | Purpose |
|---|---|---|---|
| {{library-1-name}} | {{library-1-size}} | {{library-1-version}} | {{library-1-purpose}} |
| {{library-2-name}} | {{library-2-size}} | {{library-2-version}} | {{library-2-purpose}} |

### Module-Specific vs. Shared Code

- **Module-specific code:** {{module-specific-size}} KB ({{module-specific-percent}}%)
- **Shared code (from common chunks):** {{shared-code-size}} KB ({{shared-code-percent}}%)

## Component Analysis

### Component Hierarchy

```
{{component-tree-visualization}}
```

### Heavy Components

Components with large dependency trees or frequent re-renders:

| Component | Dependencies | Render Count | Issue |
|---|---|---|---|
| {{heavy-component-1-name}} | {{heavy-component-1-deps}} | {{heavy-component-1-renders}} | {{heavy-component-1-issue}} |
| {{heavy-component-2-name}} | {{heavy-component-2-deps}} | {{heavy-component-2-renders}} | {{heavy-component-2-issue}} |

## Backend Source Code Analysis

**Note:** This section appears only when backend repository is configured.

**Backend Repository:** {{backend-repo-name}}  
**Backend Framework:** {{backend-framework}}  
**Endpoints Analyzed:** {{endpoints-analyzed-count}}  
**Analysis Method:** {{serena-instance or "Grep fallback"}}

### Backend Anti-Patterns

| Anti-Pattern | Severity | Location | Impact |
|---|---|---|---|
| **Database N+1 Queries** | {{db-n-plus-1-severity}} | {{db-n-plus-1-location}} | {{db-n-plus-1-impact}} |
| **Missing Pagination** | {{missing-pagination-severity}} | {{missing-pagination-location}} | {{missing-pagination-impact}} |
| **Missing Caching** | {{missing-caching-severity}} | {{missing-caching-location}} | {{missing-caching-impact}} |
| **Inefficient Queries** | {{inefficient-queries-severity}} | {{inefficient-queries-location}} | {{inefficient-queries-impact}} |

#### Database N+1 Queries

{{#if db-n-plus-1-detected}}

**Instances Found:** {{db-n-plus-1-count}}

##### {{db-n-plus-1-instance-1-name}}

**Handler:** `{{db-n-plus-1-instance-1-handler-path}}:{{db-n-plus-1-instance-1-line}}`

**Pattern:**
```{{db-n-plus-1-instance-1-language}}
{{db-n-plus-1-instance-1-code-snippet}}
```

**Issue:** {{db-n-plus-1-instance-1-query-count}} queries executed sequentially in loop

**Estimated Latency Impact:** {{db-n-plus-1-instance-1-latency-impact}} ms

**Recommended Fix:** {{db-n-plus-1-instance-1-recommendation}}

{{#each additional-n-plus-1-instances}}
{... repeat pattern ...}
{{/each}}

{{else}}
No database N+1 patterns detected.
{{/if}}

#### Missing Pagination

{{#if missing-pagination-detected}}

**Instances Found:** {{missing-pagination-count}}

##### Endpoint: {{missing-pagination-instance-1-endpoint}}

**Handler:** `{{missing-pagination-instance-1-handler-path}}`

**Issue:** Returns {{missing-pagination-instance-1-item-count}} items without pagination

**Estimated Payload Waste:** {{missing-pagination-instance-1-payload-waste}} KB

**Recommended Fix:** {{missing-pagination-instance-1-recommendation}}

{{#each additional-pagination-instances}}
{... repeat pattern ...}
{{/each}}

{{else}}
All collection endpoints implement pagination.
{{/if}}

#### Missing Caching

{{#if missing-caching-detected}}

**Instances Found:** {{missing-caching-count}}

##### Endpoint: {{missing-caching-instance-1-endpoint}}

**Handler:** `{{missing-caching-instance-1-handler-path}}`

**Issue:** {{missing-caching-instance-1-expensive-operation}} on every request (no cache detected)

**Data Change Frequency:** {{missing-caching-instance-1-change-frequency}}

**Estimated Latency Reduction:** {{missing-caching-instance-1-latency-reduction}} ms (with 80% cache hit rate)

**Recommended Fix:** {{missing-caching-instance-1-recommendation}}

{{#each additional-caching-instances}}
{... repeat pattern ...}
{{/each}}

{{else}}
Appropriate caching detected for expensive operations.
{{/if}}

#### Inefficient Queries

{{#if inefficient-queries-detected}}

**Instances Found:** {{inefficient-queries-count}}

##### Query: {{inefficient-query-instance-1-name}}

**Handler:** `{{inefficient-query-instance-1-handler-path}}:{{inefficient-query-instance-1-line}}`

**Query:**
```sql
{{inefficient-query-instance-1-query-snippet}}
```

**Issue:** {{inefficient-query-instance-1-issue-description}}

**Columns Fetched:** {{inefficient-query-instance-1-column-count}}  
**Columns Used:** {{inefficient-query-instance-1-used-column-count}}

**Estimated Impact:** {{inefficient-query-instance-1-impact}}

**Recommended Fix:** {{inefficient-query-instance-1-recommendation}}

{{#each additional-inefficient-query-instances}}
{... repeat pattern ...}
{{/each}}

{{else}}
Queries are efficiently fetching only required columns.
{{/if}}

### Cross-Repository Over-Fetching Analysis

**Note:** This analysis cross-references backend response schemas with frontend field usage.

#### Endpoint: {{cross-repo-endpoint-1-path}}

**Backend Handler:** `{{cross-repo-endpoint-1-handler-path}}`  
**Response Type:** `{{cross-repo-endpoint-1-response-type}}`  
**Call Pattern:** {{cross-repo-endpoint-1-call-pattern}}

| Field Category | Count | Details |
|---|---|---|
| **Total Backend Fields** | {{cross-repo-endpoint-1-total-fields}} | All fields in response schema |
| **Used by Frontend** | {{cross-repo-endpoint-1-used-fields}} | Fields accessed in components |
| **Unused Fields** | {{cross-repo-endpoint-1-unused-fields}} | {{cross-repo-endpoint-1-unused-field-list}} |

**Over-Fetching:** {{cross-repo-endpoint-1-waste-percent}}%  
**Payload Waste:** {{cross-repo-endpoint-1-payload-waste}} KB per request  
{{#if cross-repo-endpoint-1-is-n-plus-1}}
**N+1 Multiplier:** ×{{cross-repo-endpoint-1-call-count}} calls = {{cross-repo-endpoint-1-total-waste}} KB total  
{{/if}}

**Recommendation:** {{cross-repo-endpoint-1-recommendation}}

{{#each additional-endpoints}}
{... repeat pattern for each endpoint ...}
{{/each}}

## Over-Fetching Analysis

API calls made during module load with unused field analysis:

### {{api-endpoint-1}}

**Request:** `{{api-endpoint-1-method}} {{api-endpoint-1-path}}`

| Field | Fetched | Used | Status |
|---|---|---|---|
| {{api-field-1-name}} | ✓ | {{api-field-1-used}} | {{api-field-1-status}} |
| {{api-field-2-name}} | ✓ | {{api-field-2-used}} | {{api-field-2-status}} |
| {{api-field-3-name}} | ✓ | {{api-field-3-used}} | {{api-field-3-status}} |

**Over-fetching:** {{api-endpoint-1-unused-percent}}% of fields unused

### {{api-endpoint-2}}

**Request:** `{{api-endpoint-2-method}} {{api-endpoint-2-path}}`

| Field | Fetched | Used | Status |
|---|---|---|---|
| {{api-field-4-name}} | ✓ | {{api-field-4-used}} | {{api-field-4-status}} |
| {{api-field-5-name}} | ✓ | {{api-field-5-used}} | {{api-field-5-status}} |

**Over-fetching:** {{api-endpoint-2-unused-percent}}% of fields unused

## N+1 Query Detection

Potential N+1 query patterns detected:

### {{n-plus-1-pattern-1-name}}

**Location:** `{{n-plus-1-pattern-1-file}}:{{n-plus-1-pattern-1-line}}`

**Pattern:** {{n-plus-1-pattern-1-description}}

**Impact:** {{n-plus-1-pattern-1-impact}} sequential requests

**Recommendation:** {{n-plus-1-pattern-1-recommendation}}

## Performance Anti-Patterns

| Anti-Pattern | Severity | Location | Description |
|---|---|---|---|
| **Waterfall Loading** | {{waterfall-severity}} | {{waterfall-location}} | {{waterfall-description}} |
| **Render-Blocking Resources** | {{render-blocking-severity}} | {{render-blocking-location}} | {{render-blocking-description}} |
| **Unused Code** | {{unused-code-severity}} | {{unused-code-location}} | {{unused-code-description}} |
| **Expensive Re-renders** | {{expensive-rerender-severity}} | {{expensive-rerender-location}} | {{expensive-rerender-description}} |
| **Long Tasks** | {{long-task-severity}} | {{long-task-location}} | {{long-task-description}} |
| **Layout Thrashing** | {{layout-thrashing-severity}} | {{layout-thrashing-location}} | {{layout-thrashing-description}} |

**Severity Levels:**
- **CRITICAL:** LCP > 4s, bundle > 1MB, API > 2s (p95)
- **HIGH:** LCP > 2.5s, bundle > 500KB, API > 1s (p95)
- **MEDIUM:** LCP > 1.8s, bundle > 300KB, API > 500ms (p95)
- **LOW:** Below medium thresholds but above baseline targets

## Recommendations

### High-Priority Optimizations

1. **{{recommendation-1-title}}**
   - Impact: {{recommendation-1-impact}}
   - Effort: {{recommendation-1-effort}}
   - Approach: {{recommendation-1-approach}}

2. **{{recommendation-2-title}}**
   - Impact: {{recommendation-2-impact}}
   - Effort: {{recommendation-2-effort}}
   - Approach: {{recommendation-2-approach}}

### Medium-Priority Optimizations

3. **{{recommendation-3-title}}**
   - Impact: {{recommendation-3-impact}}
   - Effort: {{recommendation-3-effort}}
   - Approach: {{recommendation-3-approach}}

## Next Steps

1. Review high-priority recommendations with team
2. Create optimization plan: `/sdlc-workflow:performance-plan-optimization`
3. Prioritize by impact vs. effort trade-off
