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
