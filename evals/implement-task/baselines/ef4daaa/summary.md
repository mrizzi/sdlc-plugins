## Eval Results

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 8/8 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 6/6 | 0 | 100% |
| eval-4 | 5/6 | 1 | 83% |

**Pass rate:** 96% · **Tokens:** 40,626 · **Duration:** 152s

**Baseline** (`24a6e77`): 96% · 24,493 tokens · 74s

### Eval-4 Failure Detail

**Assertion 6** (scope containment): The plan mentions modifying `modules/fundamental/src/sbom/model/mod.rs` to add `pub mod export;` for module registration. While this is a mechanical `mod.rs` update necessary in Rust to register new modules, it is a file outside the explicitly listed Files to Modify scope — same failure mode as the previous baseline.

### Baseline Comparison

| Metric | Current | Baseline | Delta |
|--------|---------|----------|-------|
| Pass rate | 96% | 96% | 0% |
| Tokens | 40,626 | 24,493 | +66% |
| Duration | 152s | 74s | +105% |

Pass rate is unchanged from baseline. Token usage and duration increased — eval-1 (standard task) took 344s and 51k tokens, significantly more than the baseline's mean. This is likely due to the eval agent writing 8 detailed output files (plan.md + 6 file descriptions + conventions.md), which is more verbose than the baseline's approach.
