# LEO GRANT EXPENSE REVIEW DEMO SCREENSHOT AND PRESENTATION NOTES v0.1

## Canonical Path

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\DEMO_SCREENSHOT_AND_PRESENTATION_NOTES.md
```

---

# Status

```text
ACTIVE_PRESENTATION_NOTES
```

---

# Purpose

This document defines the recommended screenshot and presentation sequence for the LEO Grant Expense Review local demo.

The purpose is to make LEO understandable to a non-technical or semi-technical observer without overexplaining internal architecture.

This document supports:

* external walkthroughs,
* LinkedIn visual posts,
* website preparation,
* grant/pilot conversations,
* governance discussions,
* audit/readiness conversations,
* and short demo presentations.

This document does not add new functionality.

It documents how to present the already validated demo baseline.

---

# Current Validated Demo Baseline

```text
LEO_GRANT_EXPENSE_REVIEW_DEMO_PACKAGE
VALIDATED_READY_BASELINE
```

Confirmed validator result:

```text
DEMO_PACKAGE_READY
CHECKS PASSED: 35
CHECKS FAILED: 0
```

Confirmed isolated test result:

```text
24 passed in 0.28s
```

Confirmed full runtime result:

```text
2369 passed in 56.24s
```

---

# Main Dashboard File

Open:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

Load:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_input_quality_report.json
```

and:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_evidence_report.json
```

---

# Presentation Principle

Do not try to show everything.

The purpose of the first presentation is to make the viewer understand this chain:

```text
records
→ evidence-backed findings
→ human review
→ attachment review
→ readiness blocker
→ exportable review package
```

The viewer does not need to understand every internal module.

The viewer should understand:

* what LEO sees,
* what LEO asks humans to review,
* what LEO preserves,
* what LEO refuses to automate,
* and why the workflow is useful.

---

# Recommended Screenshot Sequence

## Screenshot 1 — Dashboard Header And Purpose

### Capture Area

Top of dashboard:

```text
LEO Grant Expense Review Dashboard v0.9
```

and the short description below it.

### Caption

```text
LEO Grant Expense Review Dashboard is a local human-review interface for evidence-backed grant expense review signals.
```

### Explanation

Use this screenshot to establish that the dashboard is local, review-oriented, and non-autonomous.

Do not begin with technical details.

---

## Screenshot 2 — Loaded Reports And Consistency Check

### Capture Area

Section:

```text
1. Load local grant review outputs
```

including:

```text
Input quality loaded: yes. Evidence report loaded: yes.
Dashboard consistency check passed.
```

### Caption

```text
The dashboard loads local JSON outputs and verifies consistency before rendering the review workflow.
```

### Explanation

This shows the viewer that the demo is not a static mockup. It reads real generated local outputs.

---

## Screenshot 3 — Summary Metrics

### Capture Area

Top metrics:

```text
Findings: 25
High / Critical: 12
Input quality: READY_WITH_WARNINGS
Autonomous actions: 0
```

### Caption

```text
LEO generated 25 evidence-backed review findings, including 12 high-priority items, while preserving zero autonomous actions.
```

### Explanation

This screenshot explains the practical result of the analysis.

Important wording:

```text
Finding means review signal, not verdict.
```

---

## Screenshot 4 — Zero-Autonomy Boundary

### Capture Area

Sections:

```text
Zero-autonomy boundary
Interpretation boundary
```

### Caption

```text
LEO explicitly preserves the boundary between review support and institutional decision-making.
```

### Explanation

This is one of the most important screenshots.

Show that LEO does not:

* issue fraud verdicts,
* issue legal conclusions,
* block payments,
* punish suppliers,
* mutate production records,
* or execute autonomous enforcement.

---

## Screenshot 5 — Review Summary Layer

### Capture Area

Section:

```text
2. Review summary layer
```

including:

```text
Unresolved findings
Unresolved HIGH / CRITICAL
Escalated locally
Needs more evidence
```

### Caption

```text
LEO organizes the reviewer workload without replacing the reviewer.
```

### Explanation

This screenshot shows that LEO helps reduce review chaos by organizing what still needs attention.

---

## Screenshot 6 — Institutional Handoff Readiness

### Capture Area

Section:

```text
3. Institutional handoff readiness
```

including:

```text
NOT_READY_FOR_HANDOFF
REQUEST_EVIDENCE
```

and blockers:

```text
11 unresolved HIGH / CRITICAL finding(s) remain.
1 evidence request(s) remain active.
1 escalation review item(s) remain active.
1 attachment review item(s) need replacement.
```

### Caption

```text
Readiness guidance is derived from local human review states and remains advisory only.
```

### Explanation

This screenshot shows the key practical value:

LEO can explain why a case is not ready for institutional handoff.

Boundary:

```text
This is not approval, rejection, legal interpretation, or donor submission.
```

---

## Screenshot 7 — Findings List

### Capture Area

Section:

```text
5. Findings requiring human review
```

Show several findings:

```text
GEV-001 — Large expense review — HIGH
GEV-006 — Missing activity reference — MEDIUM
GEV-013 — Deadline-sensitive expense — HIGH
```

### Caption

```text
Each finding is a traceable human-review signal, not an automated conclusion.
```

### Explanation

This screenshot shows that LEO gives the reviewer a structured queue of review items.

---

## Screenshot 8 — Expanded Finding GEV-001

### Capture Area

Open:

```text
GEV-001
```

Show:

* detected signal,
* reviewer question,
* next action,
* rule trace,
* human review state.

### Caption

```text
A high-priority finding connects the signal, review question, rule trace, and human review action.
```

### Explanation

This screenshot should make the viewer understand the evidence chain.

Important wording:

```text
LEO explains why review is needed. It does not decide the final outcome.
```

---

## Screenshot 9 — Rule Traceability

### Capture Area

Inside GEV-001, show:

```text
Rule trace
GER-RULE-005
Large Expense Human Review Rule
```

### Caption

```text
Rule traceability explains why a finding exists and keeps the review path auditable.
```

### Explanation

This screenshot is useful for governance, audit, GRC, and institutional audiences.

---

## Screenshot 10 — Evidence Attachments

### Capture Area

Inside GEV-001, show:

```text
Evidence attachments
ATT-001 — invoice_GE_002.pdf
ATT-002 — contract_GE_002.pdf
```

### Caption

```text
LEO links findings to expected supporting documents without opening, parsing, OCRing, or interpreting those documents.
```

### Explanation

This screenshot shows attachment-level accountability.

Important boundary:

```text
The dashboard displays local references only. Human review remains required.
```

---

## Screenshot 11 — Attachment Review State

### Capture Area

Inside GEV-001, show ATT-001 local document review state:

```text
NEEDS_REPLACEMENT
```

and reviewer note.

### Caption

```text
Document-level review state can affect institutional readiness without becoming an autonomous decision.
```

### Explanation

This is the key screenshot for showing the attachment review chain.

---

## Screenshot 12 — Attachment Blocker In Readiness Panel

### Capture Area

Return to institutional readiness panel and show:

```text
1 attachment review item(s) need replacement.
```

### Caption

```text
Attachment review state propagates into readiness blockers and preserves review accountability.
```

### Explanation

This screenshot demonstrates the core end-to-end flow:

```text
attachment review
→ readiness blocker
→ institutional handoff guidance
```

---

## Screenshot 13 — Export Human Review Package

### Capture Area

Show button:

```text
Export human review package
```

and optionally show exported JSON file name:

```text
leo_grant_expense_human_review_package_v0.4.json
```

### Caption

```text
Human review state can be exported as a structured local review package for audit preparation or institutional handoff.
```

### Explanation

This screenshot shows that review state is not trapped in the browser UI.

---

## Screenshot 14 — Export Package JSON

### Capture Area

Open exported package and show key fields:

```text
attachment_reviews_count
attachment_reviews
review_actions
zero_autonomy_boundary
evidence_attachment_export_boundary
```

### Caption

```text
The export package preserves reviewer actions, attachment review states, evidence boundaries, and zero-autonomy constraints.
```

### Explanation

This screenshot is for more technical or governance-oriented viewers.

---

## Screenshot 15 — Validator DEMO_PACKAGE_READY

### Capture Area

PowerShell output:

```text
STATUS: DEMO_PACKAGE_READY
CHECKS PASSED: 35
CHECKS FAILED: 0
```

### Caption

```text
The local demo package is validated before demonstration.
```

### Explanation

This screenshot is useful if presenting to technical, audit, governance, or AI trust audiences.

---

# Minimum Screenshot Set

If only a short presentation is needed, capture these five screenshots:

```text
1. Summary metrics
2. Zero-autonomy boundary
3. Institutional handoff readiness
4. GEV-001 with ATT-001 NEEDS_REPLACEMENT
5. DEMO_PACKAGE_READY validator output
```

This minimal set is enough to explain:

```text
LEO finds review signals
LEO preserves boundaries
LEO supports human review
LEO tracks document-level readiness
LEO validates demo package integrity
```

---

# Suggested Short Presentation Flow

Use this sequence for a short 3–5 minute explanation:

## 1. Opening

```text
LEO is a human-controlled institutional review system. This demo shows grant expense review, not autonomous compliance or enforcement.
```

## 2. Evidence Signals

```text
The dashboard loads local reports and renders 25 evidence-backed findings, including 12 high-priority review items.
```

## 3. Human Review

```text
Each finding asks a reviewer question and preserves human review action.
```

## 4. Attachment Review

```text
A document reference can be marked as needing replacement, which creates a readiness blocker.
```

## 5. Handoff Readiness

```text
LEO explains why a case is not ready for handoff, but does not approve, reject, pay, sanction, or enforce.
```

## 6. Export

```text
The review state can be exported into a local human review package.
```

## 7. Closing

```text
The purpose is to reduce institutional review chaos and preserve accountable evidence continuity before problems escalate.
```

---

# Recommended Public Caption

For a public-facing post or presentation image, use this wording:

```text
LEO does not replace institutional judgment.

It helps structure evidence-backed review signals, reviewer questions, attachment review states, readiness blockers, and exportable human review packages while preserving strict zero-autonomy boundaries.
```

---

# Language To Avoid

Avoid describing LEO as:

```text
fraud detector
AI judge
autonomous compliance engine
automated payment blocker
autonomous governance system
AI enforcement system
```

These terms misrepresent the current prototype and can create unnecessary institutional resistance.

---

# Preferred Language

Use:

```text
human-controlled institutional review system
evidence-backed review workflow
accountable review infrastructure
zero-autonomy boundary
local-first review prototype
audit-ready review continuity
institutional handoff readiness
```

---

# Current Presentation Boundary

This presentation material may describe LEO as:

```text
a validated local prototype
```

It must NOT describe LEO as:

```text
a production system
an autonomous compliance system
a certified audit system
a legal decision engine
a donor submission engine
```

---

# Final Status

```text
DEMO_SCREENSHOT_AND_PRESENTATION_NOTES_ACTIVE
PRESENTATION_SEQUENCE_DEFINED
MINIMUM_SCREENSHOT_SET_DEFINED
PUBLIC_CAPTION_LANGUAGE_DEFINED
ZERO_AUTONOMY_PRESENTATION_BOUNDARY_PRESERVED
```
