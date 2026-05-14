# External API Claim Verification — Fallback

## Detected Claim

While processing **Section 4 — Requirements**, the following claim about an external API was detected:

> **Claim:** "PR reviews cannot be updated after initial submission so always create a new review — The GitHub API does not support modifying a submitted review."

This claim asserts that the GitHub REST API does not support updating or modifying a pull request review after it has been submitted.

## Verification Attempt

Web tools (WebSearch and WebFetch) are **unavailable** in this session. Automated verification against the official GitHub REST API documentation could not be performed.

## Fallback Result

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support modifying a submitted review."** Would you like to proceed as-is, or verify it manually before continuing?

**Status:** UNVERIFIED — Claim was flagged to the user for manual verification.

**Recommendation:** Before finalizing this requirement, verify against the official GitHub REST API documentation whether the `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint exists. If it does, the requirement should be revised to allow updating existing reviews rather than always creating new ones.
