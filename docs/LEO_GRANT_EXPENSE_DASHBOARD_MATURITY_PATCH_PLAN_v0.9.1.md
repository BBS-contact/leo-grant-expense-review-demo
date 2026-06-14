# LEO GRANT EXPENSE DASHBOARD MATURITY PATCH PLAN v0.9.1

**Canonical Path:**
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\LEO_GRANT_EXPENSE_DASHBOARD_MATURITY_PATCH_PLAN_v0.9.1.md`

**Related Dashboard File:**
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html`

**Status:**
CONTROLLED PATCH PLAN

**Date:**
2026-05-19

---

# Purpose

This document defines the controlled maturity patch plan for the Grant Expense Review dashboard.

The purpose of this patch is not to simplify, reduce, remove, or roll back the dashboard.

The purpose is to mature the existing dashboard into a clearer local reviewer workstation by improving:

* version clarity,
* review action terminology consistency,
* reviewer navigation,
* page hierarchy,
* advisory handoff wording,
* expandable technical detail organization,
* and local human review usability.

The existing dashboard capabilities must be preserved.

---

# Current Active Dashboard

The active dashboard file for this patch is:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

This dashboard currently supports:

* loading the input quality report,
* loading the grant expense evidence report,
* local consistency validation,
* summary metrics,
* severity distribution,
* signal family distribution,
* zero-autonomy boundary display,
* interpretation boundary display,
* review summary layer,
* institutional handoff readiness layer,
* finding filtering,
* human review action recording,
* localStorage persistence,
* rule trace visualization,
* normative trace placeholder visualization,
* evidence attachment display,
* evidence attachment manifest display,
* attachment-level review actions,
* export package generation,
* and preservation of zero-autonomy operational boundaries.

---

# Non-Removal Rule

This patch must not remove the existing functional layers.

The following layers must remain present:

* Rule Traceability Layer,
* Normative Trace Placeholder Layer,
* Evidence Attachment Layer,
* Evidence Attachment Manifest Layer,
* Human Review Action Layer,
* Attachment Review Action Layer,
* Review Summary Layer,
* Advisory Handoff Readiness Layer,
* Export Package Layer,
* Zero-Autonomy Boundary Layer.

The dashboard may reorganize, rename, clarify, group, or collapse sections by default.

The dashboard must not silently delete any capability.

---

# Scope of Patch v0.9.1

Patch v0.9.1 is a dashboard maturity and usability pass only.

It may modify:

* HTML structure,
* CSS layout,
* local dashboard labels,
* local dashboard section order,
* JavaScript UI rendering logic,
* review-state naming consistency,
* localStorage key naming,
* dashboard-visible version labels,
* local export metadata labels,
* and advisory wording.

It must not modify:

* grant expense input CSV files,
* `grant_expense_input_quality_report.py`,
* `grant_expense_review_pipeline.py`,
* `grant_expense_evidence_report_validator.py`,
* `grant_expense_demo_package_validator.py`,
* generated evidence report structure,
* generated input quality report structure,
* protocol files,
* rule trace source mappings,
* normative trace generation logic,
* canonical registry files,
* runtime core files,
* production data,
* keys,
* signatures,
* or external integrations.

---

# Patch Area 1 — Version and Schema Clarity

## Current Issue

The dashboard currently mixes several visible and internal version markers:

```text
Dashboard title: v0.9
Review storage key: v0_3
Export package version: v0.4
```

This can confuse future maintenance and human reviewers.

## Required Correction

The dashboard must clearly distinguish:

```text
Dashboard UI Version
Review Storage Schema Version
Export Package Schema Version
```

## Recommended Version Declaration

Use:

```text
Dashboard UI Version: v0.9.1
Review Storage Schema Version: v0.9.1
Export Package Schema Version: v0.4
```

The export package schema version should remain `v0.4` unless the validator and exported package contract are intentionally changed.

## Required Visible Wording

The dashboard header should state:

```text
LEO Grant Expense Review Dashboard v0.9.1
```

A small technical note should clarify:

```text
Dashboard UI v0.9.1. Export package schema v0.4. Local review storage schema v0.9.1.
```

---

# Patch Area 2 — Review Action Terminology Stabilization

## Current Issue

The surrounding development discussion used several similar review action names:

```text
ACCEPT_AS_JUSTIFIED
ACCEPTED_AS_JUSTIFIED
FALSE_POSITIVE
MARK_FALSE_POSITIVE
```

The dashboard must use one stable vocabulary.

## Required Canonical Dashboard Review States

The Grant Expense Review dashboard should use the following local review action states:

```text
UNREVIEWED
ACCEPTED_AS_JUSTIFIED
ESCALATE_FOR_REVIEW
MARK_FALSE_POSITIVE
NEEDS_MORE_EVIDENCE
```

## Required Meaning

### UNREVIEWED

No local human review action has been saved for the finding.

### ACCEPTED_AS_JUSTIFIED

The reviewer records that the signal appears justified based on available context.

This is not a legal conclusion and not a donor compliance verdict.

### ESCALATE_FOR_REVIEW

The reviewer records that the finding should be escalated to an institutional review layer.

This does not execute escalation externally.

### MARK_FALSE_POSITIVE

The reviewer records that the signal appears not relevant or not supported after review.

The finding remains preserved as review history.

### NEEDS_MORE_EVIDENCE

The reviewer records that additional documentation or clarification is needed.

This does not automatically request documents externally.

---

# Patch Area 3 — Reviewer Navigation Layer

## Current Issue

The dashboard has filters and findings, but it does not yet provide a strong reviewer navigation workstation.

A reviewer can still feel that the page is a long list rather than a controlled review session.

## Required Addition

Add a reviewer navigation section near the top of the dashboard after validation status.

## Required Navigation Metrics

The navigation layer should show:

```text
All findings
Reviewed findings
Unreviewed findings
Unreviewed HIGH / CRITICAL findings
Escalated findings
Needs more evidence findings
Attachment blockers
```

## Required Navigation List

The navigation layer should provide compact finding rows:

```text
FINDING_ID | SEVERITY | SIGNAL_FAMILY | REVIEW_STATE
```

Each row should allow quick movement to the relevant finding card.

## Required Behavior

* Clicking a navigation item should scroll to the corresponding finding card.
* The target finding should be visually identifiable.
* Navigation should respect current filters where practical.
* It must not mutate evidence or review state.

---

# Patch Area 4 — Page Hierarchy Reordering

## Current Issue

The dashboard includes many useful sections, but the order can feel heavy for a human reviewer.

## Recommended Reviewer-Oriented Order

The dashboard should present sections in this order:

```text
1. Load local grant review outputs
2. Dashboard consistency validation
3. Reviewer navigation and progress
4. Priority review summary queues
5. Finding filters
6. Findings requiring human review
7. Rule trace, normative trace, and attachment details inside finding cards
8. Advisory institutional handoff readiness
9. Export human review package
10. Zero-autonomy and interpretation boundaries
```

## Important Constraint

This reordering must not remove existing content.

Technical depth may be moved into expandable sections where appropriate.

---

# Patch Area 5 — Advisory Handoff Wording

## Current Issue

The current institutional handoff readiness layer is useful, but its language must remain clearly advisory.

It must not appear to approve, reject, authorize, or submit anything.

## Required Naming

Use:

```text
Advisory Institutional Handoff Readiness
```

instead of wording that could be interpreted as an approval gate.

## Required Boundary Statement

The panel must state:

```text
This panel provides local advisory readiness guidance only. It does not approve, reject, submit, pay, sanction, mutate, sign, access keys, or execute external actions.
```

## Required State Names

The state names may remain deterministic, but must avoid implying formal authority.

Recommended states:

```text
ADVISORY_NOT_READY_FOR_HANDOFF
ADVISORY_PARTIAL_HANDOFF_REVIEW_REQUIRED
ADVISORY_READY_FOR_INTERNAL_REVIEW_PACKAGE
```

These states describe local package readiness only.

They do not represent legal, donor, accounting, management, or institutional approval.

---

# Patch Area 6 — Expandable Technical Depth

## Current Issue

The dashboard exposes many technical layers directly in each finding card.

This is valuable, but it can overload a first-time reviewer.

## Required Approach

Do not remove technical layers.

Instead, group them into expandable sections where appropriate.

## Recommended Expandable Groups

Inside each finding card:

```text
Core Review Summary
Rule Trace
Potential Normative References
Evidence Attachments
Evidence Attachment Manifest
Human Review Action
```

The core review summary should stay visible.

The deeper trace and manifest sections may be collapsible by default.

---

# Patch Area 7 — Export Package Clarity

## Current Issue

The dashboard exports a valid local human review package, but the visible export wording should make clear what is included and what is not included.

## Required Export Clarification

Before export, show a short summary:

```text
This export includes local reviewer actions, reviewed finding snapshots, rule traces, normative trace placeholders, attachment metadata, and zero-autonomy boundary metadata.
```

Also show:

```text
This export does not embed document files, parse documents, perform OCR, submit reports, sign records, mutate production systems, or modify the canonical registry.
```

## Export Version Rule

Do not change export package schema from `v0.4` unless the validator is updated intentionally.

---

# Patch Area 8 — LocalStorage Safety and Continuity

## Current Issue

Local review state is stored in browser localStorage, but storage naming should align with dashboard maturity.

## Required Correction

Use a storage key that clearly belongs to this dashboard and schema version:

```text
leo_grant_expense_review_actions_v0_9_1
leo_grant_expense_attachment_review_actions_v0_9_1
```

## Migration Rule

If previous keys exist, the dashboard may read them as fallback.

It must not silently delete old browser review state unless the reviewer explicitly clicks clear.

---

# Patch Area 9 — Boundary Preservation

Every patch must preserve the following prohibitions:

```text
no donor compliance verdict
no fraud verdict
no legal conclusion
no payment blocking
no supplier punishment
no production mutation
no canonical registry mutation
no autonomous enforcement
no signing or key access
no external execution
```

These prohibitions must remain visible in dashboard text and export metadata.

---

# Implementation Order

Patch implementation should proceed in this order:

## Step 1

Update visible version labels and add clear version schema note.

## Step 2

Stabilize review action vocabulary without changing the meaning of existing local review actions.

## Step 3

Add reviewer navigation and progress layer.

## Step 4

Adjust page order and section headings for reviewer workflow clarity.

## Step 5

Rename handoff layer to advisory handoff readiness and adjust state labels.

## Step 6

Group technical finding details into clearer expandable blocks.

## Step 7

Improve export package explanation text while preserving export schema compatibility.

## Step 8

Update localStorage keys with backward-compatible fallback.

## Step 9

Run manual browser verification using:

```text
output\grant_expense_input_quality_report.json
output\grant_expense_evidence_report.json
```

## Step 10

Export a human review package and validate that no production, canonical registry, signing, key, or external execution action is performed.

---

# Validation Checklist

The matured dashboard must satisfy:

* dashboard opens locally,
* input quality report loads,
* evidence report loads,
* local consistency check passes,
* findings count remains 25,
* HIGH / CRITICAL findings count remains 12,
* autonomous actions remain 0,
* rule_trace remains visible,
* normative_trace remains visible,
* attachment metadata remains visible,
* attachment review remains available,
* finding review actions persist in localStorage,
* attachment review actions persist in localStorage,
* reviewer navigation works,
* filters work,
* advisory handoff readiness renders,
* export package downloads,
* export package keeps zero-autonomy boundary,
* no source evidence JSON is mutated,
* no runtime Python file is modified,
* no canonical registry file is opened or mutated,
* no external system is contacted.

---

# Expected Result

After patch v0.9.1, the Grant Expense Review dashboard should be easier to understand as a local reviewer workstation.

It should no longer feel like a dense JSON viewer or overloaded technical page.

It should present the workflow as:

```text
LOAD REPORTS
VALIDATE LOCAL DATA
NAVIGATE REVIEW QUEUE
INSPECT FINDINGS
CHECK RULE TRACE
CHECK ATTACHMENT METADATA
RECORD HUMAN REVIEW
ASSESS ADVISORY HANDOFF READINESS
EXPORT LOCAL REVIEW PACKAGE
```

The system remains:

```text
LOCAL-FIRST
HUMAN-CONTROLLED
EVIDENCE-ORIENTED
NON-AUTONOMOUS
NON-PRODUCTION
READ-ONLY
```

---

# Final Boundary Confirmation

This patch plan does not authorize implementation outside the dashboard file.

This patch plan does not authorize production deployment.

This patch plan does not authorize donor compliance automation.

This patch plan does not authorize legal interpretation.

This patch plan does not authorize canonical registry mutation.

This patch plan does not authorize autonomous enforcement.

This patch plan does not authorize external execution.

The next correct step after this plan is a controlled dashboard HTML patch of:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```
