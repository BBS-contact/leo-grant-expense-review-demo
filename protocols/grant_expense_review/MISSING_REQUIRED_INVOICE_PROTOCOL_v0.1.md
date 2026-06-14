# Missing Required Invoice Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\MISSING_REQUIRED_INVOICE_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-010

Protocol name: Missing Required Invoice Review Rule

Signal family: `missing_required_invoice`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant expense where the referenced budget line requires an invoice or equivalent accounting document, but the expense record does not contain an invoice reference.

The purpose of this protocol is to make missing-invoice findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, reimbursement packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when all of the following conditions are present:

1. a grant expense references a budget line;
2. the referenced budget line exists in the budget line register;
3. the budget line requires an invoice or equivalent accounting document;
4. the expense record has no invoice reference or the invoice reference is empty;
5. the missing invoice reference may affect accounting traceability, reporting clarity, or audit-readiness.

This trigger identifies a review requirement only.

It does not determine whether the expense is eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

A grant expense requires human review when its budget line requires an invoice or equivalent accounting document, but the expense record has no invoice reference.

The reviewer must check whether:

1. a valid invoice exists but was not referenced in the expense record;
2. an equivalent accounting document may be acceptable for the expense type;
3. the missing invoice reference is a data-entry problem;
4. the expense is a reimbursement or transaction type that uses another supporting document;
5. the budget line requirement was applied correctly;
6. the expense can be made audit-ready through documentation correction or explanation.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Is there a valid invoice or equivalent accounting document for this expense, and if so, why is it not referenced in the expense record?

The answer should be based on available accounting, invoice, reimbursement, budget, supplier, project, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense record;
2. invoice or equivalent accounting document;
3. receipt or proof of payment;
4. reimbursement request, if applicable;
5. budget line record and invoice requirement;
6. supplier profile or supplier verification context;
7. contract, purchase order, or agreement, if applicable;
8. activity or implementation record;
9. donor reporting rules, if applicable;
10. explanation from the accountant, project manager, budget owner, or procurement reviewer.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-010",
  "source_rule_name": "Missing Required Invoice Review Rule",
  "source_rule_file": "MISSING_REQUIRED_INVOICE_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/MISSING_REQUIRED_INVOICE_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant expense requires human review when its budget line requires an invoice or equivalent accounting document, but the expense record has no invoice reference.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the missing invoice reference materially affects accounting traceability, donor reporting clarity, supporting evidence completeness, or audit-readiness.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* invoice or equivalent accounting evidence should be checked before reporting or audit packaging;
* the missing reference should be corrected or explained if documentation exists elsewhere;
* accountant, project-manager, budget-owner, or procurement-reviewer confirmation may be required.

A HIGH finding does not mean:

* donor non-compliance has been established;
* fraud has been detected;
* a legal violation has been found;
* payment must be blocked;
* a supplier must be punished;
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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, budget structure, donor rules, accounting records, invoice records, reimbursement records, supplier records, project implementation records, supporting documentation, and legal context.

---

## 9. Zero-Autonomy Boundary

LEO may identify this signal, attach this protocol reference, generate evidence context, and ask a reviewer question.

LEO must not:

1. decide that the expense is compliant or non-compliant;
2. decide that the expense is eligible or ineligible;
3. decide that the expense is fraudulent;
4. decide that the expense is unlawful;
5. block or approve payment;
6. punish or clear a supplier;
7. mutate production records;
8. mutate canonical registry records;
9. execute enforcement actions;
10. access signing keys;
11. perform external execution.

---

## 10. Review Outcome Categories

A human reviewer may later classify the finding using review actions such as:

1. accepted as justified;
2. escalated for review;
3. marked as false positive;
4. marked as needing more evidence;
5. documented as invoice reference corrected;
6. documented as equivalent accounting evidence attached;
7. documented as reimbursement documentation accepted for review;
8. documented as accountant clarification requested.

These review outcomes are human review classifications only.

They are not autonomous legal, donor compliance, fraud, payment, or supplier punishment decisions.

---

## 11. Local Prototype Status

This protocol belongs to the local Grant Expense Review prototype slice.

It is intended to support explainability, evidence traceability, and reviewer accountability in a controlled local demo environment.

It is not a production donor compliance mechanism.

It is not a legal decision mechanism.

It is not an autonomous enforcement mechanism.

---

## 12. Protocol Pack Correction Note

This protocol is an additional correction file in the Grant Expense Rule Traceability Layer.

It was added because `missing_required_invoice` is an existing HIGH signal family generated by `grant_expense_review_pipeline.py`, but it was not included in the first nine-file protocol pack.

The protocol pack now covers all known signal families generated by the current Grant Expense Review pipeline:

1. `budget_line_category_mismatch` — `GER-RULE-001`
2. `budget_line_usage_review` — `GER-RULE-002`
3. `cash_reimbursement_documentation_review` — `GER-RULE-003`
4. `deadline_sensitive_expense` — `GER-RULE-004`
5. `large_expense_review` — `GER-RULE-005`
6. `missing_activity_reference` — `GER-RULE-006`
7. `missing_required_contract` — `GER-RULE-007`
8. `repeated_round_value_expense` — `GER-RULE-008`
9. `unknown_supplier_reference` — `GER-RULE-009`
10. `missing_required_invoice` — `GER-RULE-010`

The next implementation step is to update:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_review_pipeline.py`

so that `missing_required_invoice` also receives `rule_trace` through `RULE_TRACE_BY_SIGNAL_FAMILY`.
