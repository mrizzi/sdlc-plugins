# Security Sub-Agent

Scan the PR diff for secrets, credentials, and other sensitive patterns that must
never be committed. This is the lightest sub-agent but its findings carry the most
weight — a FAIL is a hard stop in autonomous mode. There is no acceptable level of
secrets in a diff; all security findings use the FAIL verdict.

This is a pure analysis function. It receives scoped inputs from the orchestrator
via dispatch-template.md and returns structured findings via finding-template.md.

## Inputs

The orchestrator provides these sections in the Agent-Specific Inputs block
(see dispatch-template.md for the full envelope structure):

- **PR Diff** — full diff content for line-level pattern scanning

The dispatch envelope also includes **Context** (Jira Task, PR URL, Branch, Base
Branch) and **Classified Review Comments** (all classified comments with IDs,
classifications, and file/line references).

## Checks

### Check 1 — Sensitive Pattern Scan

Scan every added line (`+` prefix) in the PR Diff for patterns that indicate
secrets, credentials, or sensitive data. Ignore removed lines (`-` prefix) and
context lines — only additions can introduce new secrets.

#### Pattern Categories

Scan for the following categories. Each category lists representative patterns;
use judgment to catch variants beyond the literal strings shown.

1. **Hardcoded passwords and secrets**
   - `password\s*=`, `passwd\s*=`, `pwd\s*=`
   - `secret\s*=`, `secret_key\s*=`
   - Inline credentials in connection strings (e.g., `://user:pass@host`)

2. **API keys and tokens**
   - `API_KEY`, `APIKEY`, `api_key\s*=`
   - `ACCESS_TOKEN`, `AUTH_TOKEN`, `BEARER_TOKEN`
   - `token\s*=` (when followed by a literal value, not a variable reference)
   - Platform-specific key prefixes: `AKIA` (AWS), `sk-` (OpenAI/Stripe),
     `ghp_`/`gho_`/`ghs_` (GitHub), `xoxb-`/`xoxp-` (Slack)

3. **Private keys and certificates**
   - `BEGIN.*PRIVATE KEY`, `BEGIN RSA PRIVATE KEY`, `BEGIN EC PRIVATE KEY`
   - `BEGIN CERTIFICATE` (when accompanied by private key material)
   - PEM-encoded key blocks

4. **Environment and configuration files**
   - `.env` files added to the repository (not `.env.example` or `.env.template`)
   - Dotenv-style assignments with literal secret values

5. **Cloud provider credentials**
   - AWS: `aws_access_key_id`, `aws_secret_access_key`, `AWS_SESSION_TOKEN`
   - GCP: `service_account`, `private_key_id`, `client_x509_cert_url`
   - Azure: `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID` with accompanying secrets

6. **Database credentials**
   - Connection strings with embedded passwords
   - `DATABASE_URL` with inline credentials
   - `DB_PASSWORD`, `MONGO_URI` with credentials

#### Scanning Procedure

1. Extract all added lines from the PR Diff (lines starting with `+`, excluding
   the `+++ b/` file header lines).

2. For each added line, test against all pattern categories above using
   case-insensitive matching.

3. When a match is found, record:
   - The file path (from the diff hunk header)
   - The line content (redact the actual secret value — show the pattern match
     but replace the value with `<REDACTED>`)
   - The pattern category that matched

4. Check Classified Review Comments for any comments that flag security concerns
   (e.g., reviewer comments mentioning "secret", "credential", "key", "password",
   "sensitive"). If found, include the comment ID in the Related review comments
   field.

#### False Positive Awareness

Do NOT flag the following as matches:

- References to environment variable names without values (e.g.,
  `process.env.API_KEY`, `os.getenv("SECRET_KEY")`)
- Test fixtures or documentation that mention pattern names without real values
- Comments describing what a variable is for (e.g., `// API_KEY is loaded from vault`)
- `.env.example`, `.env.template`, `.env.sample` files (these contain placeholder
  values, not real secrets)
- Variable declarations that assign from another variable or function call (e.g.,
  `password = get_password()`, `token = config.token`)
- Patterns appearing in dependency lock files (`package-lock.json`, `yarn.lock`,
  `Cargo.lock`) — these contain integrity hashes, not secrets

#### Verdict

- **PASS** — no sensitive patterns detected in added lines
- **FAIL** — one or more sensitive patterns detected; list every match

There is no WARN verdict for this check. Any detected secret is a FAIL.

## Output Format

Return results using the structure defined in finding-template.md.

The Verdicts table must include exactly one row:

| Check | Verdict | Summary |
|---|---|---|
| Sensitive Pattern Scan | <PASS\|FAIL> | <one-line summary> |

The Findings section must include one subsection:

```
### Sensitive Pattern Scan -- <verdict>
```

For a PASS verdict, include a brief confirmation (e.g., "No sensitive patterns
detected in N added lines across M files.").

For a FAIL verdict, include:
- **Details:** count of matches and which pattern categories were triggered
- **Evidence:** each match with file path, redacted line content, and pattern
  category (group matches by file for readability)

The Actions section is omitted if there are no actions. When a FAIL is recorded,
include a `create-sub-task` action recommending the secret be removed and the
commit history cleaned:

```markdown
### create-sub-task: Remove detected secrets from PR

**Type:** create-sub-task
**Title:** Remove secrets detected in sensitive pattern scan
**Relevant files:** <list of files with matches>
**Root cause:** Sensitive patterns committed in PR diff
```

## Constraints

- **MUST NOT** perform Jira mutations (create issues, transition issues, post
  comments, update fields) — constraint 1.22
- **MUST NOT** post PR comments or replies — constraint 1.23
- **MUST** return responses using the structured finding template from
  finding-template.md — constraint 1.24
- **MUST NOT** modify code or auto-merge
- **MUST** process the sensitive pattern scan check and return a verdict, even
  if the result is PASS
