# LEO GRANT EXPENSE DASHBOARD REVIEWER EXPERIENCE PASS v1.0

**Canonical Path:**
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\LEO_GRANT_EXPENSE_DASHBOARD_REVIEWER_EXPERIENCE_PASS_v1.0.md`

**Related Active Dashboard File:**
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html`

**Status:**
REVIEWER EXPERIENCE MATURITY PASS

**Date:**
2026-05-19

---

# Purpose

This document defines the Reviewer Experience Pass for the Grant Expense Review dashboard after stabilization of:

* Rule Traceability Layer,
* Normative Trace Placeholder Layer,
* Evidence Attachment Layer,
* Human Review Workflow Layer,
* Advisory Institutional Handoff Readiness Layer,
* and Dashboard Maturity Patch v0.9.1.

The goal of this pass is not to simplify the system or remove capabilities.

The goal is to improve reviewer ergonomics, navigation clarity, visual prioritization, and controlled inspection flow while preserving all existing evidence-review layers.

---

# Current Stable Baseline

The dashboard currently supports:

* local report loading,
* consistency validation,
* findings navigation,
* severity filtering,
* signal-family filtering,
* review-state filtering,
* local reviewer actions,
* attachment reviewer actions,
* rule trace visualization,
* normative trace visualization,
* evidence attachment manifest visualization,
* advisory handoff readiness,
* export package generation,
* localStorage persistence,
* and zero-autonomy operational boundaries.

The dashboard has transitioned from a raw JSON review surface into a local institutional review workstation.

The next maturity step is reviewer usability and inspection-flow optimization.

---

# Reviewer Workflow Model

The dashboard should support the following reviewer workflow:

```text
LOAD REPORTS
VALIDATE LOCAL DATA
VIEW REVIEW QUEUE
SELECT FINDING
OPEN ONLY REQUIRED DETAILS
RECORD HUMAN REVIEW
MOVE TO NEXT FINDING
ASSESS HANDOFF READINESS
EXPORT LOCAL REVIEW PACKAGE
```

The reviewer should not be visually overloaded by all technical layers simultaneously.

The reviewer should control depth expansion intentionally.

---

# Non-Removal Rule

This Reviewer Experience Pass must not remove:

* Rule Traceability Layer,
* Normative Trace Placeholder Layer,
* Evidence Attachment Layer,
* Evidence Attachment Manifest Layer,
* Human Review Action Layer,
* Advisory Handoff Readiness Layer,
* Export Package Layer,
* or Zero-Autonomy Boundary Layer.

Technical layers may be collapsed, grouped, reordered, visually compressed, or reorganized.

Capabilities must remain available.

---

# Reviewer Experience Goal

The dashboard should evolve from:

```text
technical evidence wall
```

into:

```text
focused institutional review session
```

The reviewer must feel guided through a queue-oriented review process.

---

# Experience Pass Scope

This pass may modify:

* HTML structure,
* CSS layout,
* visual grouping,
* finding-card presentation,
* details expansion behavior,
* reviewer navigation layout,
* priority highlighting,
* toolbar positioning,
* spacing,
* review-flow organization,
* and collapsible section behavior.

This pass must not modify:

* Python pipeline logic,
* validators,
* JSON report structures,
* rule generation,
* normative trace generation,
* export schema contract,
* canonical registry logic,
* runtime core,
* or external integrations.

---

# Reviewer Experience Area 1 — Compact Finding Headers

## Current Issue

Finding cards still expose too much information immediately.

Even after Dashboard Maturity Patch v0.9.1, reviewers may experience cognitive overload when reviewing many findings sequentially.

---

## Required Compact Header Structure

Collapsed finding cards should display only:

```text
severity
finding_id
title
supplier
expense_id
signal_family
review_state
```

The header should allow:

* fast scanning,
* fast queue prioritization,
* and quick review-state recognition.

---

## Required Header Behavior

The compact header should:

* visually separate HIGH / CRITICAL findings,
* show review state clearly,
* preserve finding identity,
* preserve supplier context,
* preserve signal-family context,
* and remain readable on narrow screens.

---

# Reviewer Experience Area 2 — Default Collapsed Findings

## Current Issue

Even with structured cards, reviewers may still see too much content simultaneously.

---

## Required Behavior

All finding cards should be collapsed by default.

The reviewer intentionally expands only the findings currently under review.

---

## Required Expansion Logic

The dashboard should support:

```text
collapsed by default
expand on click
preserve expanded state during session
allow multiple expanded findings
```

Expansion behavior must remain local-only.

No server communication or persistence outside browser localStorage is allowed.

---

# Reviewer Experience Area 3 — Expandable Technical Sections

## Current Issue

Technical trace layers remain visually heavy when findings are expanded.

The reviewer should be able to open technical depth progressively.

---

## Required Internal Finding Structure

Expanded findings should follow this order:

```text
Core Review Summary
Human Review Action
Rule Trace
Potential Normative References
Evidence Attachments
Evidence Attachment Manifest
Boundary Notes
```

---

## Required Expansion Policy

The following sections may be collapsed by default:

```text
Rule Trace
Potential Normative References
Evidence Attachment Manifest
Boundary Notes
```

The following sections should remain visible immediately:

```text
Core Review Summary
Human Review Action
```

---

## Required Reviewer Philosophy

The dashboard should expose:

```text
summary first
trace second
technical depth on demand
```

not:

```text
all technical layers immediately
```

---

# Reviewer Experience Area 4 — Visual Priority Flow

## Current Issue

HIGH findings already exist but the visual review flow can become flat during long review sessions.

---

## Required Priority Ordering

Finding queue order should remain:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFO
```

---

## Required Visual Distinction

HIGH / CRITICAL findings should visually dominate the queue.

Possible techniques:

* stronger border contrast,
* stronger header accent,
* stronger severity pill,
* subtle shadow emphasis,
* priority grouping sections.

---

## Important Constraint

Visual emphasis must not imply:

* guilt,
* fraud,
* legal violation,
* donor violation,
* or enforcement conclusion.

The emphasis is reviewer prioritization only.

---

# Reviewer Experience Area 5 — Sticky Reviewer Toolbar

## Current Issue

During long scrolling sessions reviewers can lose access to:

* filters,
* review progress,
* export controls,
* and navigation state.

---

## Required Sticky Toolbar

The dashboard should maintain a sticky toolbar during scrolling.

Recommended visible toolbar elements:

```text
review progress
reviewed count
unreviewed HIGH count
search
filters
export button
```

---

## Required Toolbar Properties

The toolbar should:

* remain compact,
* avoid covering finding cards,
* remain readable on smaller screens,
* and preserve local-only operation.

---

# Reviewer Experience Area 6 — Queue-Oriented Review Mode

## Current Issue

The dashboard still behaves partially like a technical inspection page instead of a sequential review workstation.

---

## Required Queue-Oriented Philosophy

The dashboard should encourage:

```text
review next finding
complete review action
continue queue
```

instead of:

```text
read entire page vertically
```

---

## Recommended Improvements

Potential future improvements:

```text
next unresolved finding button
jump to next HIGH finding
jump to next NEEDS_MORE_EVIDENCE finding
jump to next ESCALATE_FOR_REVIEW finding
```

These features remain optional for this pass.

---

# Reviewer Experience Area 7 — Technical Compression Without Information Loss

## Current Issue

The dashboard contains many institutional layers simultaneously:

* rule trace,
* normative trace,
* attachment metadata,
* manifest metadata,
* export boundaries,
* review metadata,
* handoff readiness.

All are important.

However, simultaneous visibility creates visual fatigue.

---

## Required Compression Rule

Compression must mean:

```text
hide until needed
```

not:

```text
remove functionality
```

---

## Required Preservation

All technical content must remain:

* inspectable,
* exportable,
* readable,
* and structurally preserved.

---

# Reviewer Experience Area 8 — Review-State Visibility

## Current Issue

Review states exist but should become more visually actionable.

---

## Required Visibility

Review states should be visible in:

* queue navigation,
* finding headers,
* summary layers,
* and handoff readiness.

---

## Required Stable Vocabulary

The dashboard should preserve the stabilized review-state vocabulary:

```text
UNREVIEWED
ACCEPTED_AS_JUSTIFIED
ESCALATE_FOR_REVIEW
MARK_FALSE_POSITIVE
NEEDS_MORE_EVIDENCE
```

No synonym drift should reappear.

---

# Reviewer Experience Area 9 — Boundary Preservation

Every Reviewer Experience Pass implementation must preserve:

```text
no fraud verdict
no legal conclusion
no donor compliance conclusion
no payment blocking
no supplier punishment
no production mutation
no canonical registry mutation
no signing or key access
no external execution
```

Reviewer UX improvements must not blur institutional boundaries.

---

# Implementation Order

Reviewer Experience implementation should proceed in this order:

## Step 1

Compact finding-card headers.

## Step 2

Default collapsed findings.

## Step 3

Expandable technical sections inside findings.

## Step 4

Visual priority refinement for HIGH / CRITICAL findings.

## Step 5

Sticky reviewer toolbar.

## Step 6

Queue-oriented reviewer-flow refinement.

## Step 7

Manual browser validation.

## Step 8

Export package validation after UX modifications.

---

# Validation Checklist

After Reviewer Experience Pass implementation:

* findings remain readable,
* findings remain exportable,
* all findings remain accessible,
* technical trace remains inspectable,
* rule_trace remains visible,
* normative_trace remains visible,
* attachments remain visible,
* manifest remains visible,
* review actions still save locally,
* attachment review actions still save locally,
* navigation still works,
* filters still work,
* handoff readiness still works,
* export package still works,
* no JSON mutation occurs,
* no runtime mutation occurs,
* no canonical registry mutation occurs,
* no production action occurs,
* no external execution occurs.

---

# Expected Result

After Reviewer Experience Pass v1.0, the dashboard should behave as:

```text
institutional human review workstation
```

rather than:

```text
technical evidence dump
```

The reviewer should feel:

* guided,
* focused,
* able to review incrementally,
* able to inspect depth intentionally,
* and able to complete queue-oriented review sessions.

---

# Final Boundary Confirmation

This Reviewer Experience Pass does not authorize:

* AI legal interpretation,
* donor compliance automation,
* autonomous recommendation issuance,
* autonomous escalation,
* production mutation,
* canonical registry mutation,
* signing,
* key access,
* or external execution.

The dashboard remains:

```text
LOCAL-FIRST
HUMAN-CONTROLLED
READ-ONLY
NON-AUTONOMOUS
EVIDENCE-ORIENTED
REVIEW-CENTERED
```

---

# Next Correct Step

After this Reviewer Experience Pass plan, the next correct step is a controlled UX patch of:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

focused on:

* compact finding review flow,
* progressive technical expansion,
* queue-oriented reviewer ergonomics,
* and reduced reviewer cognitive overload.
