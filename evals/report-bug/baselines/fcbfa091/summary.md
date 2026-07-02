# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 13/13 | 100% | 36.3 | 20007 |
| eval-2 | Interactive Partial | 9/9 | 100% | 34.0 | 19416 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 18.3 | 17057 |
| eval-4 | Programmatic Mode | 12/12 | 100% | 39.0 | 19864 |
| eval-5 | Adversarial | 7/7 | 100% | 62.0 | 21558 |
| **Aggregate** | | **47/47** | **100%** | **37.92** | **19580.4** |

## Comparison Against Baseline (7329d480)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 52.38 | 37.92 | -14.46 | ↓ improved |
| Time (stddev, s) | 20.83 | 14.03 | -6.80 | ↓ improved |
| Tokens (mean) | 25002.2 | 19580.4 | -5421.8 | ↓ improved |
| Tokens (stddev) | 1838.54 | 1453.82 | -384.72 | ↓ improved |

## Summary

- **Pass rate** is unchanged at 100% — all 47 assertions across 5 evals passed.
- **Time** improved by 27.6% (52.38s → 37.92s mean), with lower variance (stddev 20.83 → 14.03).
- **Tokens** improved by 21.7% (25002.2 → 19580.4 mean), with lower variance (stddev 1838.54 → 1453.82).
