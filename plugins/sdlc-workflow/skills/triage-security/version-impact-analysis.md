# Version Impact Analysis

This companion file contains the detailed procedures for Step 2 of the
triage-security skill. It determines which supported product versions actually
ship the vulnerable dependency by reading lock files at pinned source commits.

## 2.1 – Load the supportability matrix

For each row in the **Version Streams** table in Security Configuration, read the
`security-matrix.md` file at the path given in the **Security Matrix Path** column,
resolved relative to the project's working directory. Step 0.3 already verified
that each matrix file's `Last-Updated` timestamp is recent — if staleness was
detected, the user chose to refresh or proceed before reaching this step.

Each `security-matrix.md` covers one version stream and contains:

- **Version stream** — which product versions this repo covers (e.g., `2.1.x`)
- **Supportability matrix** — a table mapping each version to source commits
  per repository, with build dates
- **Ecosystem mappings** — lock file paths and check commands per ecosystem

Enumerate all rows in the Version Streams table directly — each row already
identifies a stream, so no chaining is needed.

### Fallback to Konflux repos

When a local `security-matrix.md` file does not exist at the configured path,
fall back to reading from the Konflux release repo via `git show`:

```bash
git -C <konflux-release-repo-local-path> show main:<Security Matrix Path>
```

Where `<konflux-release-repo-local-path>` is the **Local Path** for that stream's
Konflux Release Repo from the Version Streams table, and `<Security Matrix Path>`
is the path from the same row.

After a successful fallback read, offer to write the content to the local path for
future use:

> "Local matrix file `<Security Matrix Path>` not found. Read from Konflux repo
> instead. Would you like me to save it locally for future triages?"

If the user confirms, write the file to the local path using the Write tool.

If the Version Streams table in Security Configuration is empty or incomplete, ask
the user which streams to configure before proceeding.

Aggregate all versions from all streams into a single working matrix.

### On-demand matrix population

If a stream's Supportability Matrix is empty or missing rows (e.g., the template
was scaffolded but never populated), research and fill it in before proceeding:

1. Query the Konflux release repo's git history (tags, release branches) to discover
   released versions
2. For each version, extract image digest, build date, and source commits per
   repository from the repo's build metadata
3. Identify retags (versions with identical source commits)
4. Write the discovered rows into the local `security-matrix.md` file at the
   **Security Matrix Path** from the Version Streams table (relative to the
   project working directory)
5. Present the populated matrix to the user for confirmation before writing

This is the **only** local file the triage-security skill writes to — source code
repositories are read-only, and Jira is the only other output channel.

## 2.2 – Detect the development stream

Query Jira for unreleased versions to identify the current development stream:

1. Call `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type in the
   project (see Step 3 for the full call pattern).
2. From the returned `versions` field's `allowedValues`, find versions where
   `released: false`.
3. Filter by the Jira version prefix (e.g., `MYPRODUCT`).
4. Among the unreleased versions, select the one with the **earliest `releaseDate`**
   — this is the current development version.
5. Identify which stream's repo and branch correspond to this development version
   using the Version Streams table (match the development version to the stream
   that covers it).

The development stream is checked at **branch HEAD** (not a pinned commit) since
there is no released version yet.

## 2.3 – Extract dependency versions

**Environment variable resolution:** Paths in the Version Streams table may contain
environment variable references (e.g., `${TRUSTIFY_GL_PATH}`) in the **Konflux
Release Repo** and **Local Path** columns. These must be expanded before using the
paths for `git show` commands or lock file inspection. The **Security Matrix Path**
column does not use env vars — it is relative to the project working directory.

For each version in the aggregated matrix (plus the development stream):

1. **Identify the investigation method** from the ecosystem mappings in the
   relevant stream's `security-matrix.md`. The method is determined by the
   **configuration**, not by search results:
   - If `Lock File` is configured → use the lock file. **The lock file is the
     source of truth.** If the package is not found in the lock file, it is not a
     dependency — mark as NOT affected.
   - If `Lock File` is empty → the ecosystem has no lock file (e.g., RPM). Check
     the Source Pinning Method section for alternative investigation approaches,
     or report to the engineer that the dependency version cannot be determined.

2. **Lock file path** — run the check command via `git show`, substituting the
   pinned commit and package name. The exact command comes from the `Check Command`
   column in the stream's Ecosystem Mappings table.

   Example commands for common ecosystems:

   **Cargo (Cargo.lock — TOML):**
   ```bash
   git show <commit>:Cargo.lock | grep -A2 'name = "<library>"'
   ```
   Output: version line from the TOML block.

   **npm (package-lock.json — JSON):**
   ```bash
   git show <commit>:package-lock.json | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   pkgs = d.get('packages', d.get('dependencies', {}))
   for path, info in pkgs.items():
       if '<library>' in path.split('/')[-1]:
           print(f\"{path}: {info.get('version', '?')}\")
   "
   ```

   **RPM (rpms.lock.yaml — YAML):**
   ```bash
   git show <commit>:rpms.lock.yaml | grep '<library>'
   ```

   **For the development stream**, use branch HEAD instead of a pinned commit:
   ```bash
   git show HEAD:<lock-file> | <check-command-for-ecosystem>
   ```
   Run this in the source repository directory for the development stream.

3. **SBOM fallback** — when no lock file is configured for an ecosystem (the
   `Lock File` column is empty), the image SBOM may still contain dependency
   information. If `cosign` is available, try querying the container image SBOM:

   ```bash
   cosign download sbom <image-reference>@<image-digest> | grep '<library>'
   ```

   This requires `cosign` to be installed and registry access to the container image.
   If SBOM is not available, report to the engineer that the dependency version cannot
   be determined for this ecosystem/stream and ask for guidance.

4. **Handle retags**: if a version is marked as a retag in the supportability matrix
   (e.g., `2.2.2 = retag of 2.2.1`), **skip** the version check and carry forward
   the result from the retagged version. Note in the output: "same as [version]".

5. **Compare** each extracted dependency version against the enriched fix threshold
   from Step 1.5. When Step 1.5 produced a cross-validated fix threshold (from MITRE
   CVE API or OSV.dev), use that value instead of the Jira description's affected
   range. If Step 1.5 was skipped or both external APIs were unavailable, fall back
   to the Jira description's affected range.

### 2.3.5 – Dependency chain context

For affected versions (where the vulnerable dependency is in the lock file and
within the affected range), trace the dependency chain to give the engineer context
about how the vulnerable package entered the tree. This information helps assess
remediation complexity — a direct dependency is a simple bump, while a deep
transitive dependency may require coordinating updates across intermediate packages.

For each affected version, trace how the vulnerable dependency entered the build
to give the engineer remediation context.

The investigation method depends on the ecosystem:

#### Source-level dependencies (Cargo, npm, Go)

Inspect the lock file and manifest files to determine:

1. **Direct vs transitive** — is the vulnerable package a direct dependency of a
   workspace member, or pulled in transitively?
2. **Dependency path** — the chain from a workspace root to the vulnerable package
   (e.g., `workspace-root → reqwest → hyper → h2 → vulnerable-lib`)
3. **Profile/scope** — whether the dependency is included in all build profiles or
   only specific ones:
   - **Cargo**: `[dev-dependencies]` (test/bench only, not shipped),
     `[build-dependencies]` (build scripts only), feature-gated optional deps
   - **npm**: `devDependencies` (build/test only), `optionalDependencies`

   If the dependency is only present in a non-production profile (e.g., dev-only),
   note this — it changes the risk assessment.
4. **Introduction point** — if a dependency is present in one version but not
   another, note when it was introduced (helps identify which upgrade or feature
   addition brought it in)

Example output:
```
Dependency chain for quinn-proto:
  backend (workspace) → reqwest [features: http3] → h3 → quinn → quinn-proto
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.2.0 (commit 05a3af91 added reqwest http3 feature)
Not present in: 2.1.x (reqwest used without http3 feature)
```

#### Container-level dependencies (RPM, system packages)

For RPM and system-level packages, classify origin to determine the remediation
path. The classification method depends on whether an RPM lock file is configured
for the stream.

1. **Confirm presence** — the SBOM or rpms.lock.yaml from Step 2.3 already confirms
   the package is in the image and at what version.

2. **Classify the package origin**:

   **When an RPM lock file exists** (rpms.lock.yaml or equivalent):
   - **In lock file** → **explicit install**. Remediation: update the package spec
     in the lock file (or rpms.in.yaml).
   - **Not in lock file but in SBOM** → **base image**. The package is inherited
     from the `FROM` image.

   **When no RPM lock file exists** (SBOM-only streams):
   - Check the Dockerfile to classify:
     ```bash
     git show <commit>:Dockerfile | grep -i '<package-name>\|FROM\|dnf\|yum\|microdnf'
     ```
   - **In a `dnf install` / `yum install` command** → **explicit install**.
   - **Not in any install command** → **base image**.

3. **Optional SBOM verification** (requires cosign CLI) — when available, compare
   the final container image SBOM against the base image SBOM to cross-check the
   rpms.lock.yaml classification. This step supplements but does not replace the
   lock file classification above.

   1. Check if `cosign` is available:
      ```bash
      which cosign
      ```
   2. If available, download the final image SBOM using the image reference and
      digest from the supportability matrix:
      ```bash
      cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json
      ```
   3. Extract the base image reference from the Dockerfile's `FROM` line (already
      available from the classification step above).
   4. Download the base image SBOM:
      ```bash
      cosign download sbom <base-image-reference> > /tmp/base-sbom.json
      ```
   5. Compare the package presence in both SBOMs:
      - **In final SBOM but NOT in base SBOM** → explicit install (confirms
        rpms.lock.yaml classification of "in lock file")
      - **In both SBOMs** → base image package (confirms rpms.lock.yaml
        classification of "not in lock file")
      - **If SBOM result disagrees with rpms.lock.yaml classification**, flag the
        discrepancy to the engineer:
        > "⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says
        > [explicit install / base image] but SBOM comparison says [base image /
        > explicit install]. Investigate manually."
   6. Present the SBOM classification result alongside the rpms.lock.yaml result
      in the dependency chain output (see example output below).

   If `cosign` is not available or any SBOM download fails, skip with a warning
   and use the rpms.lock.yaml classification alone:
   > "⚠️ SBOM verification skipped — cosign not available / SBOM download failed.
   > Using rpms.lock.yaml classification only."

   **Output requirement:** the dependency chain output for RPM packages MUST
   always include an SBOM verification status line — either the comparison
   result (sub-step 6) or the skip notice above. This line is mandatory even
   though the cosign verification itself is optional; omitting it leaves the
   engineer without visibility into whether SBOM cross-validation was attempted.

4. **Base image reference** (when origin is base image) — extract the `FROM`
   reference from the Dockerfile to identify the update path:
   ```bash
   git show <commit>:Dockerfile | grep -i '^FROM'
   ```
   Record:
   - **Image reference** — the full registry/repository path
     (e.g., `registry.access.redhat.com/ubi9/ubi-minimal`)
   - **Tag or digest** — how the image is pinned
     (e.g., `9.4-1227`, `@sha256:abc123`, or `latest`)
   - **Pinning method** — `digest` (immutable), `version tag` (mutable but specific),
     or `floating tag` (e.g., `latest` — rebuilding may pick up the fix automatically)

   This determines the remediation path:
   - **Floating tag** → a Konflux rebuild may pick up the fix if the base image was
     already updated upstream. Verify by checking the base image's errata or SBOM.
   - **Version tag** → update the tag to a version that includes the fix. Check the
     base image's container catalog or errata for available versions.
   - **Digest** → update the digest to a build that includes the fix.

   The skill does **not** resolve which specific base image version has the fix — that
   depends on the base image vendor's errata pipeline. Include the current reference
   in the remediation task so the engineer or `/implement-task` can research it.

5. **Introduction point** — check if the package origin differs across versions
   (e.g., moved from explicit install to base image inheritance between streams).

Example output (RPM, base image origin with SBOM verification):
```
Dependency chain for openssl (RPM):
  SBOM confirms: openssl-libs-3.0.7-27.el9.x86_64
  rpms.lock.yaml: NOT present → base image
  SBOM verification: present in both final and base image SBOMs → base image (confirms lock file)
  Dockerfile: FROM registry.access.redhat.com/ubi9/ubi-minimal:9.4-1227
  Origin: base image (openssl-libs inherited from ubi9-minimal)
  Pinning: version tag (9.4-1227)

Remediation: update base image tag to a version with patched openssl.
Check base image errata or container catalog for available updates.
```

Example output (RPM, explicit install with SBOM verification):
```
Dependency chain for custom-rpm (RPM):
  rpms.lock.yaml: present → explicit install
  SBOM verification: present in final SBOM but NOT in base image SBOM → explicit install (confirms lock file)
  Origin: explicit install (custom-rpm specified in rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml.
```

Example output (RPM, SBOM verification skipped):
```
Dependency chain for openssl (RPM):
  rpms.lock.yaml: NOT present → base image
  SBOM verification: ⚠️ skipped — cosign not available
  Origin: base image (openssl-libs inherited from ubi9-minimal)
```

Note that the lock file contents and base image can differ across streams — always
check at the specific stream's pinned commit.

## 2.4 – Present the version impact table

Build and present the version impact table to the engineer:

```
Version Impact for CVE-YYYY-XXXXX (<library> <affected-range>):

| Version | <library> | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0   | 0.11.9    | YES       |       |
| 2.1.1   | 0.11.9    | YES       |       |
| 2.2.0   | 0.11.9    | YES       |       |
| 2.2.1   | 0.11.12   | YES       |       |
| 2.2.2   | —         | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14   | NO        |       |
| 2.2.4   | 0.11.14   | NO        |       |
| 3.0 (dev) | 0.11.14 | NO        | branch HEAD |
```

Include the dependency chain context from Step 2.3.5 below the table so the
engineer can see both the impact and the remediation path at a glance.

## 2.5 – Upstream fix check

For each affected stream, check whether the upstream source repository has
already fixed the vulnerability on the branch that feeds that stream. Read the
**Upstream Branch** column from the stream's Ecosystem Mappings table.

For each affected ecosystem with an Upstream Branch configured:

1. Check the dependency version at the upstream branch HEAD. Use the **Repository**
   column from the Ecosystem Mappings row to determine which source repo to inspect:
   ```bash
   git -C <source-repo-local-path> show <upstream-branch>:<lock-file> | grep -A2 '<library>'
   ```
2. Compare against the affected version range from the CVE.

Present the upstream fix status below the version impact table:

```
Upstream fix status:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | 0.11.14         | YES    |
| 3.0.x  | Cargo     | main            | 0.11.14         | YES    |
```

This determines the remediation path for each stream:
- **Fixed upstream** → remediation is a Konflux release repo change: bump the
  source tag/commit reference to pick up the fix. Include the upstream commit
  or tag in the remediation task.
- **Not fixed upstream** → remediation requires an upstream PR first to bump
  the dependency, then a Konflux release repo update. Note this in the
  remediation task.

Wait for the engineer to review and confirm the table before proceeding to Step 3.
