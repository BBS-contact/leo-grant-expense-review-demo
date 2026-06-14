# LEO GRANT EXPENSE REVIEW DEMO WALKTHROUGH SCRIPT v0.1

## Canonical Path

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\DEMO_WALKTHROUGH_SCRIPT.md
```

---

# Status

```text
ACTIVE_DEMO_SCRIPT
```

---

# Purpose

This document provides a practical walkthrough script for demonstrating the LEO Grant Expense Review local prototype to a first-time observer.

The purpose is to show LEO in action without overwhelming the viewer with internal architecture.

This script explains:

* what to open,
* what files to load,
* what dashboard areas to show,
* what evidence signals mean,
* how human review works,
* how attachment review affects readiness,
* how export packages preserve review state,
* and what LEO explicitly does not do.

This script is intended for:

* external specialists,
* institutional reviewers,
* audit/governance observers,
* grant management professionals,
* AI governance professionals,
* and people who want to understand what LEO does in practice.

---

# Demo Boundary

This walkthrough demonstrates a local prototype only.

The demo does NOT show:

* production integration,
* live donor submission,
* payment authorization,
* supplier action,
* legal interpretation,
* autonomous enforcement,
* document OCR,
* AI document reading,
* signing,
* key access,
* or canonical registry mutation.

The correct explanation is:

```text
LEO supports structured human review.
LEO does not replace human judgment.
```

---

# Required Files

The following files should be available in the local demo folder:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_input_quality_report.json
```

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_evidence_report.json
```

Optional exported file generated during the demo:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\leo_grant_expense_human_review_package_v0.4.json
```

If the browser downloads the export to the default Downloads folder, move or copy it into the demo folder manually if it needs to be archived with the demo package.

---

# Recommended Opening Explanation

Use this short explanation at the beginning of the demo:

```text
This is a local LEO prototype for grant expense review.

It reads structured local JSON outputs, identifies evidence-backed review signals, shows rule traceability, supports human review, tracks attachment-level document review states, and generates an exportable human review package.

It does not issue legal conclusions, donor compliance decisions, fraud verdicts, payment blocks, supplier sanctions, production mutations, or autonomous enforcement actions.
```

---

# Step 1 — Open The Dashboard

Open the local dashboard file:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

Expected visible title:

```text
LEO Grant Expense Review Dashboard v0.9
```

Explain:

```text
This dashboard is a local human-review interface. It does not connect to production systems and does not execute institutional actions.
```

---

# Step 2 — Load The Input Quality Report

In the dashboard section:

```text
1. Load local grant review outputs
```

Load:

```text
output\grant_expense_input_quality_report.json
```

Expected status should indicate that the input quality report has loaded.

Explain:

```text
The input quality report checks whether the source data is usable for review. It does not issue risk conclusions.
```

---

# Step 3 — Load The Evidence Report

Load:

```text
output\grant_expense_evidence_report.json
```

Expected dashboard status:

```text
Input quality loaded: yes. Evidence report loaded: yes.
```

Expected consistency check:

```text
Dashboard consistency check passed
Loaded reports passed local dashboard consistency checks.
```

Explain:

```text
The dashboard validates that the loaded evidence report is internally consistent before rendering the review workflow.
```

---

# Step 4 — Show Summary Metrics

Show the top dashboard metrics.

Expected values:

```text
Findings: 25
High / Critical: 12
Input quality: READY_WITH_WARNINGS
Autonomous actions: 0
```

Explain:

```text
LEO generated 25 evidence-backed review findings from the local grant expense dataset. Twelve are high-priority or critical review signals. Autonomous actions remain zero.
```

Important boundary:

```text
A finding is not a verdict. It is a structured human-review signal.
```

---

# Step 5 — Show Severity And Signal Families

Show:

```text
Severity distribution
Signal families
```

Expected severity distribution:

```text
HIGH: 12
MEDIUM: 13
```

Expected signal families include:

```text
large_expense_review
missing_required_contract
budget_line_category_mismatch
deadline_sensitive_expense
unknown_supplier_reference
missing_activity_reference
cash_reimbursement_documentation_review
repeated_round_value_expense
budget_line_usage_review
```

Explain:

```text
These signal families help a reviewer understand why a record needs attention. They do not create legal, compliance, or enforcement conclusions.
```

---

# Step 6 — Show Zero-Autonomy Boundary

Show:

```text
Zero-autonomy boundary
Interpretation boundary
```

Expected values include:

```text
autonomous_enforcement_actions: 0
canonical_registry_opened: false
canonical_registry_mutated: false
production_records_mutated: false
payment_block_performed: false
supplier_punishment_performed: false
donor_compliance_conclusion_issued: false
fraud_verdict_issued: false
legal_conclusion_issued: false
signing_or_key_access_performed: false
external_execution_performed: false
```

Explain:

```text
This is one of the most important design boundaries. LEO does not act as an autonomous authority. It supports review, evidence visibility, and accountability.
```

---

# Step 7 — Show Review Summary Layer

Show:

```text
2. Review summary layer
```

Expected values in the current verified scenario:

```text
Unresolved findings: 22
Unresolved HIGH / CRITICAL: 11
Escalated locally: 1
Needs more evidence: 1
```

Explain:

```text
This section gives the reviewer a local navigation summary. It helps identify what still needs attention before institutional handoff.
```

Do not describe this as an automated decision.

Correct framing:

```text
This is review navigation, not institutional execution.
```

---

# Step 8 — Show Escalation And Missing Evidence Queues

Show:

```text
Escalation queue
Missing evidence queue
```

Expected current examples:

```text
GEV-001 — ESCALATE_FOR_REVIEW
GEV-006 — NEEDS_MORE_EVIDENCE
```

Explain:

```text
The reviewer can mark a finding for escalation or request more evidence. These local review states help preserve accountability and review continuity.
```

---

# Step 9 — Show Institutional Handoff Readiness

Show:

```text
3. Institutional handoff readiness
```

Expected current readiness state:

```text
NOT_READY_FOR_HANDOFF
REQUEST_EVIDENCE
```

Expected blockers include:

```text
11 unresolved HIGH / CRITICAL finding(s) remain.
1 evidence request(s) remain active.
1 escalation review item(s) remain active.
1 attachment review item(s) need replacement.
```

Explain:

```text
This panel converts local reviewer states into readiness guidance. It does not approve or reject anything. It only explains why the handoff is not ready yet.
```

Important boundary:

```text
REQUEST_EVIDENCE is not a legal decision. It is an advisory review status based on local review state.
```

---

# Step 10 — Show Findings List

Scroll to:

```text
5. Findings requiring human review
```

Show the findings list.

Expected examples:

```text
GEV-001 — Large expense review — HIGH
GEV-003 — Cash reimbursement documentation review — MEDIUM
GEV-006 — Missing activity reference — MEDIUM
```

Explain:

```text
Each finding can be expanded. LEO shows the signal, why it matters, the reviewer question, the next action, rule traceability, normative placeholders, evidence attachments, and human review controls.
```

---

# Step 11 — Open GEV-001

Open:

```text
GEV-001
```

Show:

* detected signal,
* why it matters,
* reviewer question,
* next action,
* rule trace,
* evidence attachments,
* attachment manifest,
* human review action.

Expected finding state:

```text
ESCALATE_FOR_REVIEW
```

Explain:

```text
This finding is marked for institutional escalation because it is a large expense requiring human review of supporting documents, budget justification, invoice, contract, and activity evidence.
```

Boundary:

```text
LEO does not say the expense is wrong. LEO says it requires structured human review.
```

---

# Step 12 — Show Rule Traceability

Inside GEV-001, show:

```text
Rule trace
```

Expected example:

```text
GER-RULE-005
Large Expense Human Review Rule
LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md
```

Explain:

```text
Rule traceability shows why the finding exists. The rule creates a human review requirement, not a compliance verdict or enforcement action.
```

---

# Step 13 — Show Normative Placeholder Boundary

Show:

```text
Potential normative references
```

Explain:

```text
The dashboard can show placeholders for potentially relevant rules, policies, or review domains, but it does not create legal citations or interpret the law.
```

Boundary:

```text
Legal interpretation remains a human responsibility.
```

---

# Step 14 — Show Evidence Attachments

Inside GEV-001, show:

```text
Evidence attachments
```

Expected attachments:

```text
ATT-001 — invoice_GE_002.pdf
ATT-002 — contract_GE_002.pdf
```

Explain:

```text
The dashboard displays local document references only. It does not open, parse, OCR, summarize, validate, sign, transmit, or interpret the documents.
```

---

# Step 15 — Show Attachment Review State

Show:

```text
ATT-001
```

Expected local document review state:

```text
NEEDS_REPLACEMENT
```

Expected note:

```text
Invoice reference requires replacement or updated supporting evidence before institutional handoff. No PDF parsing, OCR, legal interpretation, or compliance conclusion performed.
```

Explain:

```text
Attachment review is local and human-controlled. A reviewer can mark a document reference as reviewed, missing, needing replacement, or requiring escalation.
```

---

# Step 16 — Show Blocker Propagation

Return to:

```text
Institutional handoff readiness
```

Confirm the blocker:

```text
1 attachment review item(s) need replacement.
```

Explain:

```text
This shows that document-level review state affects institutional readiness. The dashboard does not approve or reject the case; it explains why the handoff remains blocked.
```

---

# Step 17 — Export Human Review Package

Click:

```text
Export human review package
```

Expected export file name may be:

```text
leo_grant_expense_human_review_package_v0.4.json
```

Explain:

```text
The export package preserves local human review actions and attachment review states so that the review workflow can be archived or handed off without losing context.
```

---

# Step 18 — Verify Export Package Content

Open the exported JSON.

Expected fields include:

```text
package_type
package_version
review_actions
attachment_reviews_count
attachment_reviews
reviewed_findings_snapshot
evidence_attachment_export_boundary
zero_autonomy_boundary
```

Expected attachment review example:

```text
ATT-001
NEEDS_REPLACEMENT
```

Explain:

```text
This confirms that attachment review state is not only displayed in the browser UI. It is preserved in the export package.
```

---

# Recommended Closing Explanation

Use this closing explanation:

```text
This prototype demonstrates LEO as a human-controlled institutional review system.

It turns grant expense records into evidence-backed findings, reviewer questions, attachment review states, readiness blockers, and exportable review packages.

It does not make legal, donor compliance, fraud, payment, supplier, or enforcement decisions.

The purpose is to help institutions preserve evidence, structure review, reduce context loss, and keep human accountability clear.
```

---

# Questions To Invite From The Viewer

Useful questions to invite:

* Does this review flow match how institutional review happens in your environment?
* What evidence would your organization require before handoff?
* Which review states are missing or unclear?
* Would exportable review packages help audit preparation?
* Which parts should remain strictly human-controlled?
* Which parts should never be automated?

Avoid asking:

* Would you let LEO make the decision?
* Should LEO automatically block payments?
* Should LEO issue compliance verdicts?

Those questions violate the current prototype boundary.

---

# Demonstration Checklist Summary

Before ending the demo, confirm that the viewer has seen:

```text
Dashboard opened
Input quality report loaded
Evidence report loaded
25 findings rendered
12 HIGH findings rendered
0 autonomous actions visible
GEV-001 opened
ATT-001 shown
NEEDS_REPLACEMENT shown
Readiness blocker shown
Export package generated
Attachment review present in export
Zero-autonomy boundary visible
```

---

# Current Demo Status

```text
LEO_GRANT_EXPENSE_REVIEW_DASHBOARD_v0.9
STABILIZED_LOCAL_REVIEW_BASELINE
DEMO_WALKTHROUGH_SCRIPT_ACTIVE
```

---

# Final Boundary Statement

```text
LEO helps people review institutional evidence.
LEO does not replace institutional responsibility.
```
