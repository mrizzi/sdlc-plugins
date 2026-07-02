## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The rpms.lock.yaml classification remains the primary signal — the SBOM result supplements but does not override it (Step 2.3.5 non-MVP enhancement)"
  **Evidence:** "In version-impact.md line 28, the dependency chain output states 'Origin: **disputed** -- rpms.lock.yaml classifies as explicit install, SBOM classifies as base image'. If rpms.lock.yaml were maintained as the primary signal, the origin would remain 'explicit install' with a supplementary note about the SBOM disagreement. Instead, the 'disputed' classification treats both signals as co-equal, effectively allowing the SBOM result to change the origin determination from what rpms.lock.yaml alone would produce. The sbom-verification.md 'Engineer Action Required' section also presents both classification paths equally without stating that rpms.lock.yaml takes precedence."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The eval run only tests a CVSS 7.5 (High) CVE, which triggers the gate. While embargo-check.md defines the threshold as 'CVSS &gt;= 7.0', there is no output demonstrating what happens when a CVE with CVSS &lt; 7.0 is processed. No output file shows the gate being skipped silently for a low or moderate severity CVE. The threshold rule is stated but the skip behavior is not demonstrated or explicitly documented in any output."

</details>

**Pass rate:** 98% · **Tokens:** 54,987 · **Duration:** 132s

**Baseline** (`d573976e`): 99% · 0 tokens · 0s

