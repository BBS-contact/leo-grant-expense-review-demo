# LEO Grant Expense Review — Rule Traceability Layer Implementation Handoff v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\LEO_GRANT_EXPENSE_RULE_TRACEABILITY_LAYER_IMPLEMENTATION_HANDOFF_v0.1.md`

Status: IMPLEMENTATION HANDOFF

Date: 2026-05-11

Scope: Grant Expense Review local prototype slice

Previous confirmed baseline: Grant Expense Evidence Report Validator tested baseline

Previous full runtime baseline: `2355 passed in 59.10s`

---

## 1. Purpose

This document defines the next implementation step for the Grant Expense Review slice: the Rule Traceability Layer.

The purpose of this layer is to make every high-severity grant expense finding traceable to a protocol-level review rule, without converting LEO into a donor compliance authority, legal decision-maker, fraud detector, payment blocker, or autonomous enforcement system.

This layer must add rule references that explain why a finding requires human review.

It must not create final donor compliance verdicts, fraud conclusions, legal conclusions, payment decisions, supplier sanctions, production mutations, canonical registry mutations, signing operations, key access, or external execution.

---

## 2. Current Baseline Confirmed Before This Layer

The current working directory is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Existing completed layers:

1. Grant Expense Input Quality layer
2. Grant Expense Review Pipeline layer
3. Grant Expense Evidence Report Validator layer

Existing evidence report output:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_evidence_report.json`

Confirmed evidence report summary before Rule Traceability Layer:

* `findings_count`: 25
* `evidence_count`: 25
* `grant_expense_count`: 15
* `supplier_count`: 11
* `known_supplier_profile_count`: 7
* `high_or_critical_findings_count`: 12
* `reviewed_findings_count`: 0
* `input_quality_status`: `READY_WITH_WARNINGS`
* `input_quality_warning_count`: 5
* `input_quality_error_count`: 0
* `autonomous_actions`: 0

Severity distribution before this layer:

* `HIGH`: 12
* `MEDIUM`: 13

Signal families before this layer:

* `budget_line_category_mismatch`: 1
* `budget_line_usage_review`: 3
* `cash_reimbursement_documentation_review`: 1
* `deadline_sensitive_expense`: 5
* `large_expense_review`: 5
* `missing_activity_reference`: 1
* `missing_required_contract`: 2
* `repeated_round_value_expense`: 2
* `unknown_supplier_reference`: 5

---

## 3. Non-Negotiable Boundaries

The Rule Traceability Layer is documentation and evidence-traceability support only.

It must preserve all of the following boundaries:

* no donor compliance verdict;
* no fraud verdict;
* no legal conclusion;
* no payment blocking;
* no supplier punishment;
* no production mutation;
* no canonical registry mutation;
* no autonomous enforcement;
* no signing or key access;
* no external execution.

The layer must only answer:

> Which internal review protocol explains why this finding requires human review?

It must not answer:

> Is this expense compliant, unlawful, fraudulent, payable, non-payable, sanctioned, or punishable?

---

## 4. Required New Directory

Create the following directory:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\`

This directory must contain Markdown protocol files used by `rule_trace` references in findings.

---

## 5. Required Protocol Files

Create protocol files that map directly to the existing signal families.

Minimum required files:

1. `BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md`
2. `BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md`
3. `CASH_REIMBURSEMENT_DOCUMENTATION_REVIEW_PROTOCOL_v0.1.md`
4. `DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md`
5. `LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md`
6. `MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md`
7. `MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md`
8. `REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md`
9. `UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md`

Each file must be concise but complete enough to support traceability.

Each protocol file must include:

* protocol id;
* protocol name;
* signal family;
* purpose;
* human-readable review rule;
* reviewer question;
* evidence expected;
* verdict boundary;
* zero-autonomy boundary.

---

## 6. Required `rule_trace` Object

Each finding that requires protocol-level traceability must contain a `rule_trace` object.

Required fields:

```json
{
  "source_rule_id": "string",
  "source_rule_name": "string",
  "source_rule_file": "string",
  "protocol_reference": "string",
  "human_readable_rule": "string",
  "verdict_boundary": "string"
}
```

Field requirements:

### `source_rule_id`

A stable internal protocol identifier.

Recommended format:

`GER-RULE-XXX`

Example:

`GER-RULE-005`

### `source_rule_name`

A short stable name for the rule.

Example:

`Large Expense Human Review Rule`

### `source_rule_file`

The Markdown protocol filename.

Example:

`LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md`

### `protocol_reference`

The local relative path to the protocol file from the Grant Expense Review demo root.

Example:

`protocols/grant_expense_review/LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md`

### `human_readable_rule`

Plain English explanation of the review trigger.

Example:

`A large grant expense requires human review when the amount is material enough to warrant additional budget, activity, supplier, and documentation checks.`

### `verdict_boundary`

A strict statement that the rule creates a review requirement only.

Example:

`This rule does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.`

---

## 7. Recommended Rule ID Map

Use one rule per existing signal family.

```python
RULE_TRACE_BY_SIGNAL_FAMILY = {
    "budget_line_category_mismatch": {
        "source_rule_id": "GER-RULE-001",
        "source_rule_name": "Budget Line Category Mismatch Review Rule",
        "source_rule_file": "BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when its recorded expense category does not align with the referenced budget line category.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "budget_line_usage_review": {
        "source_rule_id": "GER-RULE-002",
        "source_rule_name": "Budget Line Usage Review Rule",
        "source_rule_file": "BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant budget line requires human review when accumulated expense usage indicates material consumption of the allocated budget or a pattern requiring budget-owner confirmation.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "cash_reimbursement_documentation_review": {
        "source_rule_id": "GER-RULE-003",
        "source_rule_name": "Cash Reimbursement Documentation Review Rule",
        "source_rule_file": "CASH_REIMBURSEMENT_DOCUMENTATION_REVIEW_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/CASH_REIMBURSEMENT_DOCUMENTATION_REVIEW_PROTOCOL_v0.1.md",
        "human_readable_rule": "A cash reimbursement requires human review when supporting documentation, activity linkage, or reimbursement justification must be checked before audit packaging.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "deadline_sensitive_expense": {
        "source_rule_id": "GER-RULE-004",
        "source_rule_name": "Deadline-Sensitive Expense Review Rule",
        "source_rule_file": "DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when its timing is close to a reporting, eligibility, or project-period boundary that may require additional explanation.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "large_expense_review": {
        "source_rule_id": "GER-RULE-005",
        "source_rule_name": "Large Expense Human Review Rule",
        "source_rule_file": "LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md",
        "human_readable_rule": "A large grant expense requires human review when the amount is material enough to warrant additional budget, activity, supplier, and documentation checks.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "missing_activity_reference": {
        "source_rule_id": "GER-RULE-006",
        "source_rule_name": "Missing Activity Reference Review Rule",
        "source_rule_file": "MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when it lacks an activity reference needed to connect the cost to a project activity, output, or implementation record.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "missing_required_contract": {
        "source_rule_id": "GER-RULE-007",
        "source_rule_name": "Missing Required Contract Review Rule",
        "source_rule_file": "MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when the transaction appears to require a contract or formal agreement but the required contract reference is missing or unavailable.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "repeated_round_value_expense": {
        "source_rule_id": "GER-RULE-008",
        "source_rule_name": "Repeated Round-Value Expense Review Rule",
        "source_rule_file": "REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md",
        "human_readable_rule": "Grant expenses require human review when repeated round-value amounts create a pattern that may need explanation, supporting documentation, or budget-owner confirmation.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "unknown_supplier_reference": {
        "source_rule_id": "GER-RULE-009",
        "source_rule_name": "Unknown Supplier Reference Review Rule",
        "source_rule_file": "UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when the referenced supplier is not present in the known supplier profile register and must be checked before audit packaging.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
}
```

---

## 8. Pipeline Update Requirement

Update:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_review_pipeline.py`

Required behavior:

1. Every generated finding must preserve all existing fields and behavior.
2. Every finding with severity `HIGH` must include `rule_trace`.
3. Recommended: every finding should include `rule_trace`, including `MEDIUM`, because each signal family already has a protocol.
4. `rule_trace` must be derived from `signal_family` using the stable rule map.
5. The pipeline must not change the count of findings or evidence objects solely because of traceability.
6. The pipeline must not change severity logic unless a test explicitly verifies that existing severity remains stable.
7. The output summary should remain compatible with the existing validator and tests.
8. No autonomous action may be introduced.

Expected post-update summary should still preserve the baseline counts unless existing tests intentionally prove otherwise:

* `findings_count`: 25
* `evidence_count`: 25
* `high_or_critical_findings_count`: 12
* `autonomous_actions`: 0

---

## 9. Validator Update Requirement

Update:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_evidence_report_validator.py`

New validation rule:

Every finding with severity `HIGH` must contain a valid `rule_trace` object.

Validator must require the following fields for HIGH findings:

* `source_rule_id`
* `source_rule_name`
* `source_rule_file`
* `protocol_reference`
* `human_readable_rule`
* `verdict_boundary`

Validator must reject HIGH findings when:

1. `rule_trace` is missing;
2. `rule_trace` is not an object;
3. any required field is missing;
4. any required field is empty or not a string;
5. `verdict_boundary` does not preserve the zero-autonomy boundary;
6. `protocol_reference` does not point to `protocols/grant_expense_review/`;
7. `source_rule_file` is not a Markdown protocol file ending in `.md`.

Recommended additional warning, not error:

* MEDIUM findings without `rule_trace` may be allowed initially, but should produce a validator warning only if the project intentionally wants progressive adoption.

Preferred stricter approach:

* Add `rule_trace` to all findings and keep validator warning-free.

---

## 10. Test Update Requirement

Update:

`D:\BBS-09-01-2026\leo\runtime\tests\test_grant_expense_review_pipeline.py`

Required new tests:

1. generated report includes `rule_trace` for every HIGH finding;
2. generated report includes valid protocol references for every HIGH finding;
3. all HIGH `rule_trace.verdict_boundary` values preserve zero-autonomy language;
4. findings count remains 25;
5. evidence count remains 25;
6. high findings count remains 12;
7. autonomous actions remain 0;
8. each existing signal family maps to a stable `GER-RULE-XXX` rule id.

Update:

`D:\BBS-09-01-2026\leo\runtime\tests\test_grant_expense_evidence_report_validator.py`

Required new tests:

1. validator accepts a report where all HIGH findings include valid `rule_trace`;
2. validator rejects a HIGH finding with missing `rule_trace`;
3. validator rejects a HIGH finding with incomplete `rule_trace`;
4. validator rejects a HIGH finding with empty required fields;
5. validator rejects a HIGH finding with invalid `protocol_reference`;
6. validator rejects a HIGH finding with non-Markdown `source_rule_file`;
7. validator rejects a HIGH finding whose `verdict_boundary` omits zero-autonomy boundaries;
8. validator remains compatible with existing valid report structure.

---

## 11. Required Isolated Test Commands

From:

`D:\BBS-09-01-2026\leo\runtime`

Run:

```powershell
python -m pytest tests\test_grant_expense_review_pipeline.py
python -m pytest tests\test_grant_expense_evidence_report_validator.py
```

Expected result:

* both isolated test files pass;
* previous tested behavior remains intact;
* no autonomous actions are introduced.

---

## 12. Required Full Runtime Test Command

From:

`D:\BBS-09-01-2026\leo\runtime`

Run:

```powershell
python -m pytest tests
```

Expected result:

* full runtime passes;
* final count should be greater than or equal to the previous baseline of `2355 passed`, depending on the number of added tests;
* no unrelated failures are introduced.

---

## 13. Required Checkpoint After Successful Implementation

After protocol files, pipeline update, validator update, tests, isolated test runs, and full runtime pass, create:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\LEO_GRANT_EXPENSE_RULE_TRACEABILITY_LAYER_TESTED_BASELINE_v0.1.md`

The checkpoint must include:

* layer name;
* status;
* files created;
* files updated;
* evidence output summary;
* rule_trace coverage summary;
* validator behavior summary;
* isolated test results;
* full runtime result;
* zero-autonomy boundary confirmation;
* next recommended step.

Recommended next step after successful Rule Traceability Layer:

Grant Expense local reviewer dashboard / human review package layer, only after traceability is confirmed.

---

## 14. Implementation Acceptance Criteria

The Rule Traceability Layer is complete only when all of the following are true:

1. protocol directory exists;
2. required Markdown protocol files exist;
3. all HIGH findings contain valid `rule_trace`;
4. preferred: all findings contain valid `rule_trace`;
5. validator rejects HIGH findings without valid `rule_trace`;
6. generated report remains structurally valid;
7. no evidence/finding count regression is introduced;
8. isolated pipeline tests pass;
9. isolated validator tests pass;
10. full runtime suite passes;
11. checkpoint file is created;
12. zero-autonomy boundaries remain explicit and unchanged.

---

## 15. Explicit Non-Authorization Statement

This handoff does not authorize production use.

This handoff does not authorize canonical registry mutation.

This handoff does not authorize donor compliance verdicts.

This handoff does not authorize legal conclusions.

This handoff does not authorize fraud conclusions.

This handoff does not authorize payment blocking.

This handoff does not authorize supplier punishment.

This handoff does not authorize autonomous enforcement.

This handoff does not authorize signing, key access, external execution, or production mutation.

---

## 16. Current Stopping Point After This Handoff

The next concrete implementation action is to create the protocol Markdown files and update the Grant Expense Review pipeline to emit `rule_trace` objects.

Do not start dashboard or human review maturity work before Rule Traceability Layer is implemented and tested.
