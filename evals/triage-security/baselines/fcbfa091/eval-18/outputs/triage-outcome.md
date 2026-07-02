# Triage Outcome -- Re-run Produces No New Mutations

## Conclusion

The second run of triage-security on TC-8001 produces **no new Jira mutations**.
Every artifact that the triage workflow would normally create already exists from
the prior run executed on 2026-07-01. The skill's idempotency guarantees ensure
that re-running triage on an already-triaged issue is safe and side-effect-free.

## Why No Mutations Occur

The triage-security skill follows an 8-step sequential workflow. At each step that
would normally produce a Jira mutation, the re-run detects the pre-existing artifact
and skips the write operation. The table below maps each mutation point to its
idempotency guard:

| Step | Normal Mutation | Idempotency Guard | Outcome on Re-run |
|------|----------------|--------------------|--------------------|
| 0.7 | Assign issue and transition to Assigned | Status check: issue is already `In Progress` (past Assigned) | **Skipped** -- no transition needed |
| 3 | Correct Affects Versions | Affects Versions already set to RHTPA 2.2.0, RHTPA 2.2.1 (matches lock file evidence from prior analysis) | **Skipped** -- values already correct |
| 8 (Case A) | Create upstream backport task | Depend link to TC-8100 already exists with matching summary, labels, and CVE ID | **Skipped** -- task already exists |
| 8 (Case A) | Create downstream propagation task | Depend link to TC-8101 already exists with matching summary, labels, CVE ID, and Blocks link to TC-8100 | **Skipped** -- task already exists |
| 8 (Case A) | Post description digest on remediation tasks | Remediation tasks already have their own digest comments from prior run | **Skipped** -- digests already posted |
| Post-Triage | Add `ai-cve-triaged` label | Label already present in issue labels array | **Skipped** -- label already applied |
| Post-Triage | Post description digest comment | Digest comment with prefix `[sdlc-workflow] Description digest:` already exists (Comment #1) | **Skipped** -- digest already posted |
| Post-Triage | Post triage summary comment | Summary comment with `sdlc-workflow/triage-security` footer already exists (Comment #2) | **Skipped** -- summary already posted |
| Post-Triage | Transition to In Progress | Issue status is already `In Progress` | **Skipped** -- already in target state |

## Read-Only Steps Still Execute

While no mutations occur, the following read-only analysis steps still execute
during the re-run to validate the current state:

1. **Step 0 -- Validate Configuration**: Reads CLAUDE.md and confirms Security
   Configuration is present and complete. This is stateless and always runs.

2. **Step 0.3 -- Matrix Staleness Check**: Reads `security-matrix.md` timestamps.
   The matrix was last updated 2026-06-28 (4 days before the re-run date of
   2026-07-02), which is within the 14-day freshness threshold. No warning issued.

3. **Step 1 -- Data Extraction**: Fetches the issue from Jira and parses CVE
   metadata. This is read-only and produces the data table used by subsequent
   steps. The extracted data is unchanged from the prior run.

4. **Step 1.5 -- External CVE Data Enrichment**: Queries MITRE and OSV.dev APIs
   for structured version ranges. Read-only external lookups.

5. **Step 2 -- Version Impact Analysis**: Reads lock files via `git show` at
   pinned commits from the supportability matrix. The version impact table
   is recomputed and matches the prior run's findings:
   - RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- **AFFECTED** (< 0.11.14)
   - RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- **AFFECTED** (< 0.11.14)
   - RHTPA 2.2.2 (v0.4.9): retag of v0.4.8 -- **AFFECTED** (same as 2.2.1)
   - RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- **NOT AFFECTED** (>= 0.11.14)
   - RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- **NOT AFFECTED** (>= 0.11.14)

6. **Step 4 -- Duplicate/Sibling Check**: JQL search for sibling Vulnerability
   issues with the same CVE. Read-only search.

7. **Step 5 -- Version Lifecycle Check**: Reads product lifecycle page. Read-only.

8. **Step 6 -- Already Fixed Check**: Checks resolved sibling issues. Read-only.

9. **Step 7 -- Concurrent Triage Detection**: JQL search for concurrent triages
   on the same upstream component. Read-only.

## Design Rationale

The triage-security skill achieves idempotency through **artifact presence checks**
rather than explicit "already triaged" short-circuiting. This design is intentional:

1. **Partial triage recovery**: If a prior run failed partway through (e.g., created
   tasks but crashed before posting the summary), a re-run completes only the missing
   steps rather than either (a) refusing to run or (b) duplicating everything.

2. **State verification**: Re-running triage re-validates the version impact analysis
   against current lock file data. If a new release occurred between runs, the
   re-run would detect updated dependency versions and flag any discrepancies.

3. **Granular skip decisions**: Each artifact is checked independently. The label
   check is separate from the task creation check, which is separate from the
   comment check. This means a re-run correctly handles edge cases like "label
   exists but summary comment is missing."

In the case of TC-8001, all six artifact checks find pre-existing results, so
the complete re-run is mutation-free. The only observable effect is the read-only
analysis output presented to the engineer for verification.
