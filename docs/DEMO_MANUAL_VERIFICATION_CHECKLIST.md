# LEO GRANT EXPENSE REVIEW DEMO MANUAL VERIFICATION CHECKLIST v0.1

## Canonical Path

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\DEMO_MANUAL_VERIFICATION_CHECKLIST.md
```

---

# Status

```text
ACTIVE_MANUAL_VERIFICATION_CHECKLIST
```

---

# Purpose

This document defines the manual verification checklist for the LEO Grant Expense Review local prototype.

The purpose of this checklist is to confirm that the stabilized demo baseline behaves consistently before:

* demonstrations,
* external walkthroughs,
* screenshots,
* recordings,
* public presentations,
* governance discussions,
* or prototype reviews.

This checklist focuses on:

* dashboard rendering,
* evidence rendering,
* review continuity,
* attachment review propagation,
* export-package integrity,
* and zero-autonomy boundary preservation.

This checklist does NOT validate:

* production deployment,
* institutional approval,
* legal compliance,
* donor compliance,
* operational authorization,
* payment workflows,
* or autonomous execution.

---

# Verification Scope

The checklist applies to:

```text
LEO Grant Expense Review Dashboard v0.9
STABILIZED LOCAL REVIEW BASELINE
```

Canonical dashboard path:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

---

# Required Files

The following files must exist before verification begins.

## Dashboard

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

## Input Quality Report

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_input_quality_report.json
```

## Evidence Report

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_evidence_report.json
```

Optional exported package generated during testing:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\leo_grant_expense_human_review_package_v0.4.json
```

---

# Environment Verification

## EV-001 — Local Dashboard Opens

### Verification

Open:

```text
leo_grant_expense_review_dashboard.html
```

in a local browser.

### Expected Result

Dashboard loads successfully.

Visible title:

```text
LEO Grant Expense Review Dashboard v0.9
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-002 — No Immediate Render Failure

### Verification

Observe the dashboard after initial load.

### Expected Result

No blank screen.

No broken render state.

No visible JavaScript crash.

No infinite loading behavior.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# JSON Loading Verification

## EV-003 — Input Quality Report Loads

### Verification

Load:

```text
grant_expense_input_quality_report.json
```

### Expected Result

Dashboard confirms:

```text
Input quality loaded: yes
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-004 — Evidence Report Loads

### Verification

Load:

```text
grant_expense_evidence_report.json
```

### Expected Result

Dashboard confirms:

```text
Evidence report loaded: yes
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-005 — Dashboard Consistency Validation Passes

### Verification

Observe dashboard validation area after both reports are loaded.

### Expected Result

Dashboard displays:

```text
Dashboard consistency check passed
Loaded reports passed local dashboard consistency checks.
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Summary Metrics Verification

## EV-006 — Findings Count Renders Correctly

### Verification

Observe summary metrics.

### Expected Result

Dashboard displays:

```text
Findings: 25
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-007 — HIGH / CRITICAL Count Renders Correctly

### Verification

Observe summary metrics.

### Expected Result

Dashboard displays:

```text
High / Critical: 12
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-008 — Autonomous Actions Remain Zero

### Verification

Observe:

```text
Autonomous actions
```

### Expected Result

Dashboard displays:

```text
0
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Zero-Autonomy Boundary Verification

## EV-009 — Zero-Autonomy Boundary Visible

### Verification

Observe:

```text
Zero-autonomy boundary
```

### Expected Result

Visible fields include:

```text
autonomous_enforcement_actions: 0
canonical_registry_mutated: false
production_records_mutated: false
payment_block_performed: false
supplier_punishment_performed: false
fraud_verdict_issued: false
legal_conclusion_issued: false
external_execution_performed: false
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-010 — Interpretation Boundary Visible

### Verification

Observe:

```text
Interpretation boundary
```

### Expected Result

Dashboard explicitly states:

```text
This report contains evidence-backed review signals only.
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Review Summary Verification

## EV-011 — Review Summary Layer Renders

### Verification

Observe:

```text
2. Review summary layer
```

### Expected Result

Summary metrics render correctly.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-012 — Escalation Queue Renders

### Verification

Observe:

```text
Escalation queue
```

### Expected Result

Dashboard displays:

```text
GEV-001
ESCALATE_FOR_REVIEW
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-013 — Missing Evidence Queue Renders

### Verification

Observe:

```text
Missing evidence queue
```

### Expected Result

Dashboard displays:

```text
GEV-006
NEEDS_MORE_EVIDENCE
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Institutional Readiness Verification

## EV-014 — Institutional Readiness Panel Renders

### Verification

Observe:

```text
3. Institutional handoff readiness
```

### Expected Result

Dashboard renders correctly.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-015 — Readiness Status Renders Correctly

### Verification

Observe readiness status.

### Expected Result

Dashboard displays:

```text
NOT_READY_FOR_HANDOFF
REQUEST_EVIDENCE
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-016 — Readiness Blockers Render Correctly

### Verification

Observe readiness blockers.

### Expected Result

Dashboard displays:

```text
11 unresolved HIGH / CRITICAL finding(s) remain.
1 evidence request(s) remain active.
1 escalation review item(s) remain active.
1 attachment review item(s) need replacement.
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Findings Rendering Verification

## EV-017 — Findings List Renders

### Verification

Observe:

```text
5. Findings requiring human review
```

### Expected Result

Findings list renders successfully.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-018 — GEV-001 Opens Correctly

### Verification

Open:

```text
GEV-001
```

### Expected Result

Expanded finding displays:

* signal description,
* reviewer question,
* next action,
* rule trace,
* evidence attachments,
* attachment review controls.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-019 — Rule Traceability Renders

### Verification

Inside GEV-001 observe:

```text
Rule trace
```

### Expected Result

Dashboard displays:

```text
GER-RULE-005
Large Expense Human Review Rule
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-020 — Normative Placeholder Section Renders

### Verification

Inside GEV-001 observe:

```text
Potential normative references
```

### Expected Result

Normative placeholder section visible.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Attachment Review Verification

## EV-021 — Evidence Attachments Render

### Verification

Inside GEV-001 observe:

```text
Evidence attachments
```

### Expected Result

Dashboard displays:

```text
ATT-001
ATT-002
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-022 — Attachment Review State Renders

### Verification

Observe ATT-001.

### Expected Result

Dashboard displays:

```text
NEEDS_REPLACEMENT
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-023 — Attachment Review Note Renders

### Verification

Observe ATT-001 reviewer note.

### Expected Result

Dashboard displays note explaining replacement requirement.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-024 — Attachment Blocker Propagates To Readiness

### Verification

Return to institutional readiness panel.

### Expected Result

Dashboard displays:

```text
1 attachment review item(s) need replacement.
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Human Review Persistence Verification

## EV-025 — Human Review States Persist After Refresh

### Verification

Refresh browser.

### Expected Result

Existing review states remain visible.

Expected examples:

```text
ESCALATE_FOR_REVIEW
ACCEPTED_AS_JUSTIFIED
NEEDS_MORE_EVIDENCE
NEEDS_REPLACEMENT
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Export Package Verification

## EV-026 — Export Package Downloads Successfully

### Verification

Click:

```text
Export human review package
```

### Expected Result

JSON package downloads successfully.

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-027 — Export Package Contains Review Actions

### Verification

Open exported JSON.

### Expected Result

Export contains:

```text
review_actions
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-028 — Export Package Contains Attachment Reviews

### Verification

Open exported JSON.

### Expected Result

Export contains:

```text
attachment_reviews_count
attachment_reviews
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-029 — Export Package Preserves NEEDS_REPLACEMENT

### Verification

Open exported JSON.

### Expected Result

Export includes:

```text
ATT-001
NEEDS_REPLACEMENT
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

## EV-030 — Export Package Preserves Zero-Autonomy Boundary

### Verification

Open exported JSON.

### Expected Result

Export contains:

```text
zero_autonomy_boundary
```

### Status

```text
[ ] PASS
[ ] FAIL
```

---

# Final Verification Summary

## Minimum Required Pass Conditions

The demo baseline is considered verified only if:

* dashboard loads,
* JSON reports load,
* consistency validation passes,
* findings render,
* attachment review renders,
* readiness blockers render,
* export package downloads,
* attachment review persists into export,
* and zero-autonomy boundaries remain visible.

---

# Verification Outcome

## Final Status

```text
[ ] VERIFIED_STABLE_BASELINE
[ ] VERIFIED_WITH_WARNINGS
[ ] VERIFICATION_FAILED
```

---

# Reviewer Notes

```text
__________________________________________________________________
__________________________________________________________________
__________________________________________________________________
__________________________________________________________________
```

---

# Current Verification Scope Boundary

This checklist verifies:

* local prototype continuity,
* review visibility,
* evidence continuity,
* export persistence,
* and zero-autonomy boundary preservation.

This checklist does NOT verify:

* production safety,
* legal correctness,
* donor compliance,
* operational deployment,
* security certification,
* institutional authorization,
* or autonomous decision quality.

---

# Current Checklist Status

```text
LEO_GRANT_EXPENSE_REVIEW_DASHBOARD_v0.9
STABILIZED_LOCAL_REVIEW_BASELINE
MANUAL_VERIFICATION_CHECKLIST_ACTIVE
```
