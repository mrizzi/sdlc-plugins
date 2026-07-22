# Setup Skill Eval Results

## Per-Eval Results

| Eval | Name | Passed | Total | Pass Rate |
|------|------|--------|-------|-----------|
| 1 | Greenfield setup | 9 | 9 | 1.00 |
| 2 | Incremental update | 8 | 8 | 1.00 |
| 3 | No-Serena/no-MCP | 8 | 8 | 1.00 |
| 4 | Adversarial | 7 | 7 | 1.00 |
| 5 | Security Config opt-in | 8 | 8 | 1.00 |
| 6 | Idempotency (all configured) | 7 | 7 | 1.00 |

## Aggregate

| Metric | Current | Baseline (1dab64e0) | Delta |
|--------|---------|---------------------|-------|
| Pass Rate (mean) | 1.00 | 1.00 | unchanged |
| Pass Rate (stddev) | 0.00 | 0.00 | unchanged |

## Failed Assertions

None — all 47 assertions passed across 6 evals.

## Notes

- Timing and token metrics not captured in this run (agents ran via Agent tool, not the run-evals skill).
- Baseline comparison: pass rate matches the latest baseline at `evals/setup/baselines/1dab64e0/`.
