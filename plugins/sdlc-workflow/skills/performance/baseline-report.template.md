---
generated_by: {{skill-name}}
timestamp: {{iso-8601-timestamp}}
repository: {{repository-name}}
capture_mode: {{capture-mode}}
---

# Performance Baseline Report

## Configuration Summary

- **Capture Date:** {{capture-date}}
- **Iterations:** {{iterations}}
- **Warmup Runs:** {{warmup-runs}}
- **Scenarios Measured:** {{scenario-count}}

## Capture Mode

**Mode:** {{capture-mode}}

{{mode-description}}

**Mode descriptions:**
- **cold-start:** Direct URL navigation with cold cache. Measures worst-case/first-visit performance.

---

## Aggregate Metrics

Overall performance across all scenarios.

| Metric | Mean | p50 (Median) | p95 | p99 | Unit |
|---|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | {{lcp-mean}} | {{lcp-p50}} | {{lcp-p95}} | {{lcp-p99}} | ms |
| **FCP** (First Contentful Paint) | {{fcp-mean}} | {{fcp-p50}} | {{fcp-p95}} | {{fcp-p99}} | ms |
| **DOM Interactive** | {{domInteractive-mean}} | {{domInteractive-p50}} | {{domInteractive-p95}} | {{domInteractive-p99}} | ms |
| **Total Load Time** | {{total-mean}} | {{total-p50}} | {{total-p95}} | {{total-p99}} | ms |

## Per-Scenario Metrics

{{per-scenario-sections}}

## Resource Timing Breakdown

Top resources by load duration across all scenarios:

| Resource | Type | Duration (ms) | Size (KB) | Scenario |
|---|---|---|---|---|
| {{resource-1-name}} | {{resource-1-type}} | {{resource-1-duration}} | {{resource-1-size}} | {{resource-1-scenario}} |
| {{resource-2-name}} | {{resource-2-type}} | {{resource-2-duration}} | {{resource-2-size}} | {{resource-2-scenario}} |
| {{resource-3-name}} | {{resource-3-type}} | {{resource-3-duration}} | {{resource-3-size}} | {{resource-3-scenario}} |

## Waterfall Visualization

Resource load timeline for {{waterfall-scenario-name}}:

```
{{waterfall-ascii-chart}}
```

**Legend:**
- `[====]` Script
- `[----]` Stylesheet
- `[****]` Image
- `[++++]` Fetch/XHR

## Comparison with Previous Baseline

{{comparison-section}}

## Next Steps

1. Review scenarios with LCP > 2.5s or DOM Interactive > 3.5s
2. Identify heavy resources (> 500KB scripts, > 200KB stylesheets)
3. Run module-level analysis for your selected workflow: `/sdlc-workflow:performance-analyze-module`
