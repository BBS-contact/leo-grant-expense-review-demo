# LEO GRANT EXPENSE REVIEW DEMO PACKAGE INDEX v0.1

## Canonical Path

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\DEMO_PACKAGE_INDEX.md
```

---

# Status

```text
ACTIVE_DEMO_PACKAGE_INDEX
```

---

# Purpose

This document provides a concise index of the LEO Grant Expense Review demo package.

Its purpose is to help a reviewer, observer, or demonstrator quickly understand:

* what files exist,
* what each file is for,
* which file to open first,
* which files are inputs,
* which files are generated outputs,
* which files explain the workflow,
* which files validate the package,
* and which boundaries must remain preserved.

This document is an orientation file only.

It does not introduce new architecture, new features, new runtime behavior, or new institutional authority.

---

# Demo Package Root

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\
```

---

# Recommended First File To Open

For a live local demo, open:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\leo_grant_expense_review_dashboard.html
```

This is the main local dashboard for Grant Expense Review.

---

# Main Dashboard

## File

```text
leo_grant_expense_review_dashboard.html
```

## Purpose

Local browser dashboard for reviewing grant expense evidence signals.

It supports:

* local JSON loading,
* input quality status rendering,
* evidence-backed findings,
* rule traceability display,
* normative placeholder display,
* evidence attachment display,
* evidence attachment manifest display,
* finding-level human review,
* attachment-level document review,
* institutional handoff readiness,
* readiness blockers,
* and human review package export.

## Boundary

The dashboard does not:

* perform legal interpretation,
* issue donor compliance decisions,
* issue fraud verdicts,
* block payments,
* punish suppliers,
* mutate production data,
* mutate canonical registries,
* access keys,
* sign documents,
* parse PDFs,
* perform OCR,
* read documents with AI,
* or execute external actions.

---

# Required Input / Output JSON Files

## Input Quality Report

```text
output\grant_expense_input_quality_report.json
```

Purpose:

* records the quality and readiness status of local grant expense input data,
* shows warnings and errors,
* confirms whether analysis can proceed.

Expected current status:

```text
READY_WITH_WARNINGS
```

---

## Evidence Report

```text
output\grant_expense_evidence_report.json
```

Purpose:

* contains evidence-backed grant expense review findings,
* contains signal families,
* contains rule traces,
* contains zero-autonomy boundary fields,
* contains review-ready data consumed by the dashboard.

Expected current baseline:

```text
25 findings
12 HIGH findings
0 autonomous actions
```

---

## Exported Human Review Package

```text
output\leo_grant_expense_human_review_package_v0.4.json
```

Purpose:

* preserves local finding-level review actions,
* preserves attachment-level review actions,
* includes reviewer notes,
* includes reviewed findings snapshot,
* includes evidence attachment export boundary,
* includes zero-autonomy boundary.

Expected current verified attachment state:

```text
ATT-001 -> NEEDS_REPLACEMENT
```

Expected current readiness blocker:

```text
1 attachment review item(s) need replacement.
```

---

# Demo Explanation Documents

## README Demo Review Flow

```text
README_DEMO_REVIEW_FLOW.md
```

Purpose:

* explains the Grant Expense Review demo workflow,
* explains what the prototype does,
* explains what the prototype does not do,
* explains required files,
* explains human review workflow,
* explains institutional handoff readiness,
* explains export package meaning.

Use this file when someone needs a practical explanation of the demo flow.

---

## One-Page LEO Explanation

```text
LEO_ONE_PAGE_EXPLANATION.md
```

Purpose:

* explains LEO at a higher level,
* gives non-technical positioning,
* clarifies that LEO is a human-controlled institutional review and evidence accountability system,
* explains why LEO exists,
* explains the current prototype state,
* and preserves zero-autonomy positioning.

Use this file when someone asks:

```text
What is LEO?
```

---

## Demo Walkthrough Script

```text
DEMO_WALKTHROUGH_SCRIPT.md
```

Purpose:

* provides a step-by-step script for demonstrating the dashboard,
* explains what to show first,
* explains how to show GEV-001,
* explains how to show ATT-001,
* explains how to show readiness blockers,
* explains how to export the human review package,
* and provides recommended demo language.

Use this file when preparing for a live walkthrough.

---

## Manual Verification Checklist

```text
DEMO_MANUAL_VERIFICATION_CHECKLIST.md
```

Purpose:

* provides a checklist for manually verifying that the demo works before showing it,
* confirms dashboard loading,
* confirms JSON loading,
* confirms findings rendering,
* confirms attachment review rendering,
* confirms readiness blocker rendering,
* confirms export package generation,
* confirms zero-autonomy boundary visibility.

Use this file before demos, screenshots, recordings, or external reviews.

---

# Runtime Validation Utility

## Demo Package Validator

```text
grant_expense_demo_package_validator.py
```

Purpose:

* validates required demo files,
* validates evidence report integrity,
* validates expected finding counts,
* validates zero-autonomy boundary fields,
* validates attachment review integrity,
* validates expected ATT-001 NEEDS_REPLACEMENT state,
* validates readiness blocker presence,
* validates export package structure.

Run from:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review
```

Command:

```powershell
python grant_expense_demo_package_validator.py
```

Expected successful status:

```text
DEMO_PACKAGE_READY
```

---

# Validator Tests

## Test File

```text
tests\test_grant_expense_demo_package_validator.py
```

Purpose:

* tests the demo package validator logic,
* verifies expected evidence report conditions,
* verifies zero-autonomy boundary checks,
* verifies attachment review checks,
* verifies readiness blocker checks,
* verifies export package structure checks.

Run from:

```text
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review
```

Command:

```powershell
python -m pytest tests\test_grant_expense_demo_package_validator.py
```

Confirmed result:

```text
18 passed in 0.30s
```

---

# Full Runtime Test Baseline

Run from:

```text
D:\BBS-09-01-2026\leo\runtime
```

Command:

```powershell
python -m pytest tests
```

Confirmed result:

```text
2369 passed in 60.21s
```

This confirms that the Grant Expense Review demo package validator did not break the wider LEO runtime baseline.

---

# Current Demo Package File Map

```text
grant_expense_review\
│
├── leo_grant_expense_review_dashboard.html
│
├── README_DEMO_REVIEW_FLOW.md
├── LEO_ONE_PAGE_EXPLANATION.md
├── DEMO_WALKTHROUGH_SCRIPT.md
├── DEMO_MANUAL_VERIFICATION_CHECKLIST.md
├── DEMO_PACKAGE_INDEX.md
├── LEO_GRANT_EXPENSE_DEMO_PACKAGE_VALIDATOR_TESTED_BASELINE_CHECKPOINT_v0.1.md
│
├── grant_expense_demo_package_validator.py
│
├── output\
│   ├── grant_expense_input_quality_report.json
│   ├── grant_expense_evidence_report.json
│   └── leo_grant_expense_human_review_package_v0.4.json
│
└── tests\
    └── test_grant_expense_demo_package_validator.py
```

---

# Recommended Demo Preparation Sequence

Before presenting LEO Grant Expense Review:

```text
1. Open DEMO_PACKAGE_INDEX.md
2. Open README_DEMO_REVIEW_FLOW.md
3. Open DEMO_WALKTHROUGH_SCRIPT.md
4. Run DEMO_MANUAL_VERIFICATION_CHECKLIST.md
5. Run grant_expense_demo_package_validator.py
6. Run isolated validator tests
7. Open leo_grant_expense_review_dashboard.html
8. Load the two JSON reports
9. Show GEV-001 and ATT-001
10. Export human review package
```

---

# Current Verified Demo Scenario

The currently verified demo scenario includes:

```text
GEV-001
Large expense review
QuickBuild Technical Services Sp. z o.o.
ATT-001
invoice_GE_002.pdf
NEEDS_REPLACEMENT
1 attachment review item(s) need replacement.
NOT_READY_FOR_HANDOFF
REQUEST_EVIDENCE
```

This scenario demonstrates:

```text
finding-level review
→ attachment-level review
→ readiness blocker propagation
→ institutional handoff guidance
→ export package preservation
```

---

# Non-Goals

This demo package is NOT:

* a production deployment package,
* a legal compliance package,
* a donor submission package,
* a payment authorization package,
* a supplier sanction package,
* an autonomous enforcement package,
* a PDF analysis package,
* an OCR package,
* or a signing/key-management package.

---

# Current Status

```text
LEO_GRANT_EXPENSE_REVIEW_DEMO_PACKAGE_INDEX_ACTIVE
DEMO_PACKAGE_STRUCTURE_DOCUMENTED
DEMO_READINESS_FILES_INDEXED
VALIDATOR_TESTED_BASELINE_REFERENCED
ZERO_AUTONOMY_BOUNDARY_PRESERVED
```
