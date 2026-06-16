# LEO Grant Expense Review Demo

Public evaluation package for the LEO grant expense review runtime demonstration.

## Purpose

This repository demonstrates a review-oriented grant expense analysis workflow.

The demonstration is designed to support human review of grant expenses, supplier references, reporting rules, budget line usage, documentation completeness, and generated evidence objects.

LEO does not approve expenses, reject expenses, issue fraud determinations, perform enforcement actions, block payments, or modify production records.

## Runtime Boundary

This demonstration operates under the following constraints:

* Human review required
* No autonomous approval
* No autonomous rejection
* No autonomous enforcement
* No payment blocking
* No production mutation
* No legal verdicts
* No fraud verdicts
* Evidence preservation required
* Provenance preservation required

## What This Demo Shows

The demonstration verifies that LEO can:

* load grant expense review inputs;
* perform input quality validation;
* generate evidence-linked review findings;
* preserve evidence records;
* validate generated evidence reports;
* generate human review packages;
* provide reviewer guidance protocols;
* expose a local reviewer dashboard;
* validate demonstration package readiness.

## Repository Structure

```text
input/
  grant_expenses.csv
  grant_budget_lines.csv
  grant_reporting_rules.csv
  grant_supplier_profiles.csv

output/
  grant_expense_input_quality_report.json
  grant_expense_evidence_report.json
  leo_grant_expense_human_review_package_v0.4.json

tests/
  test_grant_expense_demo_package_validator.py

protocols/
  grant_expense_review/

docs/
  reviewer documentation
  tested baselines
  validation checkpoints

grant_expense_input_quality_report.py
grant_expense_review_pipeline.py
grant_expense_evidence_report_validator.py
grant_expense_demo_package_validator.py
leo_grant_expense_review_dashboard.html
```

## Verified Runtime Status

Latest staging verification:

```text
Tests:
24 passed

Input Quality Status:
READY_WITH_WARNINGS

Input Files:
4 / 4 loaded

Input Quality Errors:
0

Input Quality Warnings:
5

Ready For Analysis:
true

Pipeline Status:
OK

Findings:
25

Evidence Objects:
25

High Findings:
12

Autonomous Actions:
0

Evidence Report Validation:
PASSED

Validator Errors:
0

Validator Warnings:
0

Demo Package Status:
DEMO_PACKAGE_READY

Demo Package Checks Passed:
35

Demo Package Checks Failed:
0
```

## Run Tests

~~~bash
pytest
~~~

Expected result:

~~~text
24 passed
~~~

## Run the Demo Pipeline

~~~bash
python grant_expense_input_quality_report.py
python grant_expense_review_pipeline.py
python grant_expense_evidence_report_validator.py
python grant_expense_demo_package_validator.py
~~~

## Review Generated Outputs

Generated artifacts:

~~~text
output/grant_expense_input_quality_report.json
output/grant_expense_evidence_report.json
output/leo_grant_expense_human_review_package_v0.4.json
~~~

Reviewers should inspect generated outputs together with source inputs, protocols, tests, and dashboard artifacts.

## Human Review Workflow

The demonstration follows a review-first workflow:

```text
Input Validation
        ->
Evidence Generation
        ->
Evidence Validation
        ->
Human Review Package
        ->
Reviewer Dashboard
        ->
Human Decision Making
```

LEO provides review support and evidence organization.

Human reviewers remain responsible for all decisions.

## Reviewer Protocol Library

The repository includes reviewer protocols covering:

* budget line category mismatch;
* budget line usage review;
* cash reimbursement review;
* deadline-sensitive expenses;
* large expense review;
* missing activity references;
* missing required contracts;
* missing required invoices;
* repeated round-value expenses;
* unknown supplier references.

These protocols are intended to support consistent human review.

## Public Evaluation Goals

This repository is published to support:

* transparency;
* reproducibility;
* traceability;
* evidence-oriented review;
* independent evaluation;
* external critique.

Reviewers are encouraged to inspect:

* source code;
* tests;
* outputs;
* protocols;
* dashboards;
* validation artifacts.

## Verification Checkpoint

```text
Repository Status:
PUBLIC EVALUATION CANDIDATE

Staging Verification:
PASSED

Human Review Boundary:
MAINTAINED

Autonomous Approval:
NO

Autonomous Rejection:
NO

Autonomous Enforcement:
NO

Fraud Verdict Generation:
NO

Payment Blocking:
NO

Production Mutation:
NO
```

## License

Published for public evaluation, inspection, testing, and review of demonstrated capabilities and operational boundaries.
