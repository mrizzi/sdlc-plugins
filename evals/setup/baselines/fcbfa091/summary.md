# setup Eval Results

## Run Summary

| Metric | Current | Baseline (7329d480) | Delta |
|--------|---------|---------------------|-------|
| **Pass rate** | 1.00 (0.00) | 1.00 (0.00) | -- |
| **Time (s)** | 57.44 (18.30) | 70.74 (23.80) | -13.30 (18.8% faster) |
| **Tokens** | 20,474 (1,032) | 31,301 (2,013) | -10,827 (34.6% fewer) |

## Per-Eval Results

| Eval | Name | Assertions | Pass Rate | Time (s) | Tokens |
|------|------|------------|-----------|----------|--------|
| 1 | Greenfield setup | 9/9 | 1.00 | 45.36 | 20,105 |
| 2 | Incremental update | 8/8 | 1.00 | 46.69 | 19,635 |
| 3 | No-Serena/no-MCP | 8/8 | 1.00 | 63.06 | 20,042 |
| 4 | Adversarial | 7/7 | 1.00 | 95.90 | 22,624 |
| 5 | Security config opt-in | 8/8 | 1.00 | 44.61 | 20,771 |
| 6 | Fully configured idempotent | 7/7 | 1.00 | 49.00 | 19,666 |

## Verdict

**All 47 assertions passed across 6 evals.** Pass rate matches baseline (1.00).
Execution was 18.8% faster and used 34.6% fewer tokens than the baseline.
