# Feature Preview

**Summary (title):** Add advisory notification email service

**Assignee:** Unassigned

**Labels:** `ai-generated-jira`

---

## Feature Overview

Add an email notification service that alerts subscribed users when new security advisories are published that affect their tracked SBOMs.

## Background and Strategic Fit

Advisory notification is a common feature in vulnerability management platforms. Currently users must manually check for new advisories.

## Goals

- **Who benefits**: Security operations teams and developers
- **Current state**: Users manually check the advisory feed page
- **Target state**: Automatic email notifications for relevant advisories
- **Goal statements**:
  - Reduce time-to-awareness for new vulnerabilities from days to minutes

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Send email when a new advisory matches a tracked SBOM | Match by CPE or PURL | Yes |
| Allow users to configure notification preferences | Email frequency: immediate, daily digest, weekly | Yes |
| Include advisory severity and affected package list in email body | Use existing email template system | Yes |

## Non-Functional Requirements

- Email delivery latency: < 5 minutes from advisory publication
- Support up to 10,000 subscribed users without performance degradation

## Use Cases (User Experience & Workflow)

### UC-1: Receive advisory notification

**Persona**: Security engineer
**Pre-conditions**: User has email notifications enabled and tracks at least one SBOM
**Steps**:
1. New advisory is published that affects a package in the user's SBOM
2. System matches advisory to affected SBOMs
3. System sends email to subscribed users

**Expected outcome**: User receives email with advisory details

## Customer Considerations

- Organizations may have email security policies that require allowlisting
- Some customers use internal mail relays

## Customer Information/Supportability

- Monitor email delivery success rate in Grafana
- Track notification matching accuracy (advisory-to-SBOM matching)

## Documentation Considerations

- **Doc Impact**: New Content -- document notification setup and email configuration
- **User purpose**: Admins need to configure SMTP settings and users need to manage their notification preferences
