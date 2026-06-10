# Version Impact Analysis

This companion file contains the detailed procedures for Step 2 of the
triage-security skill. It determines which supported product versions actually
ship the vulnerable dependency by reading lock files at pinned source commits.

## 2.1 – Load the supportability matrix

Read `security-matrix.md` from each Konflux release repo listed in the project's
Security Configuration. Each `security-matrix.md` covers one version stream and
contains:

- **Version stream** — which product versions this repo covers (e.g., `2.1.x`)
- **Supportability matrix** — a table mapping each version to source commits
  per repository, with build dates
- **Ecosystem mappings** — lock file paths and check commands per ecosystem
- **Forward pointer** — the next stream's Konflux release repo URL (if any)

**Follow forward pointers** to chain across all streams. Starting from the first
repo in Version Streams, read its `security-matrix.md`, then follow its forward
pointer to the next repo, and repeat until no more forward pointers exist. This
ensures full coverage of all supported version streams.

To follow a forward pointer, match the repo URL against the **Konflux Release Repo**
column in the Version Streams table to find the corresponding **Local Path**. If the
URL is not in the table, ask the user for the local path or skip that stream.

If the Version Streams table in Security Configuration is empty or incomplete, ask
the user which Konflux release repos to scan. Present any discovered repos (from
forward pointers) and let the user confirm or add to the list before proceeding.

Aggregate all versions from all streams into a single working matrix.

### On-demand matrix population

If a stream's Supportability Matrix is empty or missing rows (e.g., the template
was scaffolded but never populated), research and fill it in before proceeding:

1. Query the Konflux release repo's git history (tags, release branches) to discover
   released versions
2. For each version, extract image digest, build date, and source commits per
   repository from the repo's build metadata
3. Identify retags (versions with identical source commits)
4. Write the discovered rows into the `security-matrix.md` file
5. Present the populated matrix to the user for confirmation before writing

This is the **only** file the triage-security skill writes to — source code and
Jira are the only other output channels (Jira for mutations, source repos are
read-only).

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
   using the forward pointer chain (the development stream is typically the last
   stream, covered by the most recent Konflux release repo).

The development stream is checked at **branch HEAD** (not a pinned commit) since
there is no released version yet.

## 2.3 – Extract dependency versions

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

5. **Compare** each extracted dependency version against the CVE's affected range
   to determine whether that product version is affected.

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

3. **Base image reference** (when origin is base image) — extract the `FROM`
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

4. **Introduction point** — check if the package origin differs across versions
   (e.g., moved from explicit install to base image inheritance between streams).

Example output (RPM, base image origin):
```
Dependency chain for openssl (RPM):
  SBOM confirms: openssl-libs-3.0.7-27.el9.x86_64
  rpms.lock.yaml: NOT present → base image
  Dockerfile: FROM registry.access.redhat.com/ubi9/ubi-minimal:9.4-1227
  Origin: base image (openssl-libs inherited from ubi9-minimal)
  Pinning: version tag (9.4-1227)

Remediation: update base image tag to a version with patched openssl.
Check base image errata or container catalog for available updates.
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
