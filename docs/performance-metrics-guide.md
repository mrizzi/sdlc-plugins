# Performance Metrics Guide

Quick reference for performance metrics, thresholds, and severity classification.

---

## Core Web Vitals

| Metric | Definition | Good | Needs Improvement | Poor | Default Target |
|---|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Time until largest content visible | ≤ 2.5s | 2.5 - 4.0s | > 4.0s | 2500 ms |
| **FCP** (First Contentful Paint) | Time until any content visible | ≤ 1.8s | 1.8 - 3.0s | > 3.0s | 1800 ms |
| **DOM Interactive** (Time to Interactive) | Time until page fully interactive | ≤ 3.8s | 3.8 - 7.3s | > 7.3s | 3500 ms |
| **Total Load Time** | Time until all resources loaded | ≤ 4.0s | 4.0 - 7.0s | > 7.0s | 4000 ms |

**Thresholds:** p75 for Web Vitals standard, p95 for internal targets (default in skills)

---

## Industry Benchmarks by Application Type

| Application Type | LCP Target | FCP Target | DOM Interactive Target |
|---|---|---|---|
| Simple dashboard | 2000 ms | 1200 ms | 2500 ms |
| Data-heavy admin | 2500 ms | 1800 ms | 3500 ms |
| Public-facing SPA | 1500 ms | 1000 ms | 2000 ms |
| E-commerce site | 1800 ms | 1200 ms | 2500 ms |

---

## Anti-Pattern Severity Thresholds

### Over-Fetching

| Severity | Unused Fields % | Payload Increase | Impact |
|---|---|---|---|
| High | > 70% | > 100 KB | > 300 ms |
| Medium | 40-70% | 30-100 KB | 100-300 ms |
| Low | < 40% | < 30 KB | < 100 ms |

**Detection:** Compare API response fields with frontend code usage

---

### N+1 Queries

| Severity | Sequential Calls | Time Impact |
|---|---|---|
| High | > 10 | > 1000 ms |
| Medium | 5-10 | 300-1000 ms |
| Low | 2-4 | < 300 ms |

**Impact formula:** `Sequential time = N × avg latency`, `Parallel time = 1 × avg latency`

---

### Waterfall Loading

| Severity | Sequential Depth | Time Impact |
|---|---|---|
| High | > 5 levels | > 800 ms |
| Medium | 3-5 levels | 300-800 ms |
| Low | 2 levels | < 300 ms |

**Detection:** Count sequential dependency chains in resource timing

---

### Render-Blocking Resources

| Severity | Blocking Resources | LCP Impact |
|---|---|---|
| High | > 3 | > 500 ms |
| Medium | 2-3 | 200-500 ms |
| Low | 1 | < 200 ms |

**Detection:** `<script>` without `async`/`defer` or `<link rel="stylesheet">` without `media`/`preload`

---

### Unused Code

| Severity | Unused Code % | Bundle Size Impact |
|---|---|---|
| High | > 30% | > 100 KB |
| Medium | 15-30% | 50-100 KB |
| Low | < 15% | < 50 KB |

**Impact formula:** `Parse time ≈ bundle KB × 3ms/KB`

---

### Expensive Re-Renders

| Severity | Re-Render Count | Time Impact |
|---|---|---|
| High | > 20 | > 300 ms |
| Medium | 10-20 | 100-300 ms |
| Low | 5-10 | < 100 ms |

**Impact formula:** `Wasted time = render time × unnecessary re-renders`

---

### Long Tasks

| Severity | Task Duration | Occurrence |
|---|---|---|
| High | > 250 ms | Multiple |
| Medium | 100-250 ms | Multiple |
| Low | 50-100 ms | Few |

**Threshold:** Tasks > 50ms block user interaction

**Impact formula:** `DOM Interactive delay = sum(task durations > 50ms)`

---

### Layout Thrashing

| Severity | Forced Reflows | Time Impact |
|---|---|---|
| High | > 20 | > 200 ms |
| Medium | 10-20 | 80-200 ms |
| Low | 5-10 | < 80 ms |

**Detection:** Read-write-read pattern (e.g., `offsetHeight` → `style.height = X`)

**Impact formula:** `Reflow time ≈ 10ms × reflow count`

---

### Missing Lazy Loading

| Severity | Component Size | LCP Impact |
|---|---|---|
| High | > 150 KB | > 600 ms |
| Medium | 80-150 KB | 300-600 ms |
| Low | 40-80 KB | < 300 ms |

**Detection:** Large components in main bundle used below-the-fold

---

## Resource Timing

| Resource Type | Typical Size | Optimization |
|---|---|---|
| Scripts (`.js`) | 10-500 KB | Code splitting, tree shaking, minification |
| Stylesheets (`.css`) | 5-100 KB | Critical CSS inlining, unused CSS removal |
| Images (`.png`, `.jpg`) | 10-500 KB | Compression, WebP format, lazy loading |
| API calls (JSON) | 1-100 KB | Reduce payload, caching, batching |

**Good compression ratio:** > 70% for text resources (HTML, CSS, JS, JSON)

---

## Metrics Aggregation

| Percentile | Use Case |
|---|---|
| **p50** (median) | Quick sanity checks, typical user experience |
| **p75** | Google Web Vitals standard, public monitoring |
| **p95** (default) | Internal targets, regression detection, worst-case typical |
| **p99** | Identifying outliers, debugging edge cases |

**Default in skills:** p95 across 5 iterations

---

## Regression Threshold

**5% degradation** in non-target scenarios triggers investigation

**Example:**
```
Optimization target: SBOM List
Non-target: Home Dashboard baseline 2000ms

After optimization:
- 2120ms (6% regression) → ⚠️ Flagged
- 2090ms (4.5% regression) → ✅ Acceptable drift
```

---

## Optimization Impact Formulas

| Optimization | Impact Formula |
|---|---|
| Over-fetching | `KB saved / bandwidth × 1000 = ms saved` |
| N+1 queries | `(N - 1) × avg latency = ms saved` |
| Waterfall loading | `Sequential time - max(parallel) = ms saved` |
| Render-blocking | `Resource load time = ms saved` |
| Unused code | `KB removed × 3ms/KB = parse time saved` |
| Long tasks | `sum(task > 50ms) = DOM Interactive delay reduced` |
| Layout thrashing | `reflow count × 10ms = ms saved` |
| Lazy loading | `Component KB × 3ms/KB = LCP improvement` |

---

## Navigation Timing Metrics

| Metric | Typical Range | Optimization |
|---|---|---|
| DNS Lookup | 20-120 ms | DNS prefetching, fast DNS provider |
| TCP Connection | 50-200 ms | HTTP/2, connection keep-alive, CDN |
| TLS Handshake | 50-300 ms | TLS 1.3, session resumption |
| TTFB (Time to First Byte) | 100-600 ms | CDN, server caching, query optimization |
| DOM Processing | 100-500 ms | Minimize DOM size, avoid deep nesting |

---

## See Also

- [Performance Workflow Guide](performance-workflow-guide.md) - End-to-end workflow
- [Performance Skills Reference](performance-skills-reference.md) - Skill documentation
- [Workflow Documentation](workflow.md) - Full skill catalog
