# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review — The GitHub API does not support modifying a submitted review"

**Verification Status:** UNVERIFIED (fallback)

## Fallback Reason

Web tools (WebSearch and WebFetch) are unavailable. Unable to verify this claim against official GitHub REST API documentation.

## Fallback Notice Presented to User

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"PR reviews cannot be updated after
> initial submission — The GitHub API does not support modifying a submitted
> review."** Would you like to proceed as-is, or verify it manually before
> continuing?

## Recommendation

This claim should be manually verified before finalizing the Feature. The GitHub REST API documentation for pull request reviews should be consulted to confirm whether an endpoint exists to update or modify a submitted review (e.g., `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`). If such an endpoint exists, the requirement should be revised to allow updating existing reviews instead of always creating new ones.

## Impact on Feature Description

If the claim is incorrect, the following requirement should be revised:

| Original Requirement | Suggested Revision |
|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | Update existing PR review if one already exists; create a new review only on first posting |
