# Unknown Supplier Reference Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-009

Protocol name: Unknown Supplier Reference Review Rule

Signal family: `unknown_supplier_reference`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant expense whose referenced supplier is not present in the known supplier profile register or cannot be matched to an existing supplier profile used by the local prototype.

The purpose of this protocol is to make unknown-supplier findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, procurement review, reimbursement packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when a grant expense references a supplier, vendor, contractor, consultant, service provider, participant, or reimbursement counterparty that is not found in the known supplier profile register.

Such a case may include:

1. supplier identifier not present in the supplier profile file;
2. supplier name present in the expense record but missing from known profiles;
3. incomplete supplier reference;
4. supplier profile not yet created;
5. inconsistent supplier naming;
6. reimbursement counterparty requiring clarification;
7. supplier context needed before audit packaging or procurement review.

This trigger identifies a review requirement only.

It does not determine whether the supplier is legitimate, illegitimate, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, sanctionable, approved, or prohibited.

---

## 3. Human-Readable Rule

A grant expense requires human review when the referenced supplier is not present in the known supplier profile register and must be checked before audit packaging.

The reviewer must check whether:

1. the supplier exists and is correctly identified;
2. the supplier profile is missing because of data-entry or onboarding delay;
3. the supplier name or identifier is inconsistent across records;
4. the counterparty is a reimbursement participant rather than a supplier;
5. the expense requires procurement or supplier documentation;
6. the supplier context is sufficient for reporting and audit-readiness;
7. a supplier profile should be created or linked by a human reviewer.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Who is the referenced supplier or counterparty, why is the supplier profile missing, and what documentation confirms the supplier context for this expense?

The answer should be based on available accounting, supplier, procurement, reimbursement, project, budget, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense record;
2. supplier profile register;
3. supplier onboarding record, if available;
4. invoice or receipt;
5. contract, agreement, purchase order, or procurement record, if applicable;
6. reimbursement request or participant record, if applicable;
7. payment documentation;
8. budget line reference;
9. activity or implementation record;
10. donor reporting rules, if applicable;
11. explanation from the project manager, accountant, procurement reviewer, or budget owner.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-009",
  "source_rule_name": "Unknown Supplier Reference Review Rule",
  "source_rule_file": "UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant expense requires human review when the referenced supplier is not present in the known supplier profile register and must be checked before audit packaging.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the missing supplier profile materially affects supplier traceability, procurement review, reimbursement explanation, reporting clarity, budget justification, or audit-readiness.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* supplier or counterparty identity should be clarified before reporting or audit packaging;
* supplier documentation should be checked or linked if available;
* project-manager, accountant, procurement-reviewer, or budget-owner confirmation may be required.

A HIGH finding does not mean:

* donor non-compliance has been established;
* fraud has been detected;
* a legal violation has been found;
* payment must be blocked;
* a supplier or participant must be punished;
* an autonomous action is authorized.

---

## 8. Verdict Boundary

This protocol creates a human review requirement only.

It does not create or imply:

1. donor compliance verdict;
2. fraud verdict;
3. legal conclusion;
4. payment blocking decision;
5. supplier punishment;
6. production mutation;
7. canonical registry mutation;
8. autonomous enforcement;
9. signing or key access;
10. external execution.

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, supplier records, procurement records, budget structure, donor rules, accounting records, project implementation records, reimbursement records, supporting documentation, and legal context.

---

## 9. Zero-Autonomy Boundary

LEO may identify this signal, attach this protocol reference, generate evidence context, and ask a reviewer question.

LEO must not:

1. decide that the supplier is legitimate or illegitimate;
2. decide that the supplier is compliant or non-compliant;
3. decide that the expense is eligible or ineligible;
4. decide that the supplier or expense is fraudulent;
5. decide that the supplier or expense is unlawful;
6. block or approve payment;
7. punish or clear a supplier or participant;
8. mutate production records;
9. mutate canonical registry records;
10. execute enforcement actions;
11. access signing keys;
12. perform external execution.

---

## 10. Review Outcome Categories

A human reviewer may later classify the finding using review actions such as:

1. accepted as justified;
2. escalated for review;
3. marked as false positive;
4. marked as needing more evidence;
5. documented as supplier profile created;
6. documented as supplier profile linked;
7. documented as supplier naming corrected;
8. documented as reimbursement participant clarified;
9. documented as procurement clarification requested.

These review outcomes are human review classifications only.

They are not autonomous legal, donor compliance, fraud, payment, supplier approval, supplier rejection, or supplier punishment decisions.

---

## 11. Local Prototype Status

This protocol belongs to the local Grant Expense Review prototype slice.

It is intended to support explainability, evidence traceability, and reviewer accountability in a controlled local demo environment.

It is not a production donor compliance mechanism.

It is not a legal decision mechanism.

It is not an autonomous enforcement mechanism.

---

## 12. Protocol Pack Completion Note

This protocol is the ninth file in the Grant Expense Rule Traceability Layer protocol pack.

The initial protocol pack now contains protocol coverage for the following signal families:

1. `budget_line_category_mismatch` — `GER-RULE-001`
2. `budget_line_usage_review` — `GER-RULE-002`
3. `cash_reimbursement_documentation_review` — `GER-RULE-003`
4. `deadline_sensitive_expense` — `GER-RULE-004`
5. `large_expense_review` — `GER-RULE-005`
6. `missing_activity_reference` — `GER-RULE-006`
7. `missing_required_contract` — `GER-RULE-007`
8. `repeated_round_value_expense` — `GER-RULE-008`
9. `unknown_supplier_reference` — `GER-RULE-009`

The next implementation step is to update:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_review_pipeline.py`

so that generated findings include `rule_trace` derived from `signal_family`.

After that, update:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_evidence_report_validator.py`

to require valid `rule_trace` for HIGH findings.
