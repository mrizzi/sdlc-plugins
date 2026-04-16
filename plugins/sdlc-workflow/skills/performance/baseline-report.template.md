---
generated_by: {{skill-name}}
timestamp: {{iso-8601-timestamp}}
repository: {{repository-name}}
---

# Performance Baseline Report

## Configuration Summary

- **Capture Date:** {{capture-date}}
- **Iterations:** {{iterations}}
- **Warmup Runs:** {{warmup-runs}}
- **Scenarios Measured:** {{scenario-count}}

## Aggregate Metrics

Overall performance across all scenarios.

| Metric | Mean | p50 (Median) | p95 | p99 | Unit |
|---|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | {{lcp-mean}} | {{lcp-p50}} | {{lcp-p95}} | {{lcp-p99}} | ms |
| **FCP** (First Contentful Paint) | {{fcp-mean}} | {{fcp-p50}} | {{fcp-p95}} | {{fcp-p99}} | ms |
| **TTI** (Time to Interactive) | {{tti-mean}} | {{tti-p50}} | {{tti-p95}} | {{tti-p99}} | ms |
| **Total Load Time** | {{total-mean}} | {{total-p50}} | {{total-p95}} | {{total-p99}} | ms |

## Per-Scenario Metrics

### {{scenario-1-name}}

**URL:** `{{scenario-1-url}}`

| Metric | Mean | p50 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| LCP | {{scenario-1-lcp-mean}} | {{scenario-1-lcp-p50}} | {{scenario-1-lcp-p95}} | {{scenario-1-lcp-p99}} | ms |
| FCP | {{scenario-1-fcp-mean}} | {{scenario-1-fcp-p50}} | {{scenario-1-fcp-p95}} | {{scenario-1-fcp-p99}} | ms |
| TTI | {{scenario-1-tti-mean}} | {{scenario-1-tti-p50}} | {{scenario-1-tti-p95}} | {{scenario-1-tti-p99}} | ms |
| Total Load Time | {{scenario-1-total-mean}} | {{scenario-1-total-p50}} | {{scenario-1-total-p95}} | {{scenario-1-total-p99}} | ms |

**Resource Summary:**
- Scripts: {{scenario-1-scripts-count}}
- Stylesheets: {{scenario-1-stylesheets-count}}
- Images: {{scenario-1-images-count}}
- Fetch/XHR: {{scenario-1-fetch-count}}
- Total Resources: {{scenario-1-total-resources}}

### {{scenario-2-name}}

**URL:** `{{scenario-2-url}}`

| Metric | Mean | p50 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| LCP | {{scenario-2-lcp-mean}} | {{scenario-2-lcp-p50}} | {{scenario-2-lcp-p95}} | {{scenario-2-lcp-p99}} | ms |
| FCP | {{scenario-2-fcp-mean}} | {{scenario-2-fcp-p50}} | {{scenario-2-fcp-p95}} | {{scenario-2-fcp-p99}} | ms |
| TTI | {{scenario-2-tti-mean}} | {{scenario-2-tti-p50}} | {{scenario-2-tti-p95}} | {{scenario-2-tti-p99}} | ms |
| Total Load Time | {{scenario-2-total-mean}} | {{scenario-2-total-p50}} | {{scenario-2-total-p95}} | {{scenario-2-total-p99}} | ms |

**Resource Summary:**
- Scripts: {{scenario-2-scripts-count}}
- Stylesheets: {{scenario-2-stylesheets-count}}
- Images: {{scenario-2-images-count}}
- Fetch/XHR: {{scenario-2-fetch-count}}
- Total Resources: {{scenario-2-total-resources}}

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

1. Review scenarios with LCP > 2.5s or TTI > 3.5s
2. Identify heavy resources (> 500KB scripts, > 200KB stylesheets)
3. Run application-wide analysis: `/sdlc-workflow:performance-analyze-app`
4. Run module-level analysis for specific pages: `/sdlc-workflow:performance-analyze-module`
