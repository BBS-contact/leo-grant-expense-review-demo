# Repeated Round-Value Expense Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-008

Protocol name: Repeated Round-Value Expense Review Rule

Signal family: `repeated_round_value_expense`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for repeated grant expenses with round-value amounts that create a pattern requiring explanation, supporting documentation, budget-owner confirmation, or audit-readiness review.

The purpose of this protocol is to make repeated round-value expense findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, reimbursement packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when multiple grant expenses show repeated round-value amounts or amount patterns that require human review.

Such a pattern may include:

1. repeated identical round-value amounts;
2. multiple expenses with rounded amounts under the same supplier;
3. multiple rounded reimbursements under the same activity or budget line;
4. repeated values close to local review thresholds;
5. clustered round-value expenses near reporting deadlines;
6. repeated values that may require explanation before audit packaging;
7. amount patterns that require budget-owner, accountant, or project-manager confirmation.

This trigger identifies a review requirement only.

It does not determine whether the expenses are eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

Grant expenses require human review when repeated round-value amounts create a pattern that may need explanation, supporting documentation, or budget-owner confirmation.

The reviewer must check whether the repeated round-value pattern is:

1. expected because of fixed fees, standard rates, flat-rate reimbursements, or planned activity costs;
2. supported by invoices, receipts, contracts, reimbursement forms, or other evidence;
3. linked to legitimate activities or implementation records;
4. explainable by project design, supplier pricing, participant reimbursement rules, or procurement structure;
5. concentrated under one supplier, activity, or budget line in a way that requires additional explanation;
6. sufficiently documented for reporting and audit-readiness.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Are the repeated round-value expenses expected, documented, and explainable by project activities, supplier pricing, reimbursement rules, or approved budget structure?

The answer should be based on available accounting, budget, supplier, activity, reimbursement, procurement, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense records forming the repeated round-value pattern;
2. invoices, receipts, reimbursement forms, or payment documentation;
3. contracts, purchase orders, framework agreements, or rate sheets, if applicable;
4. budget line records;
5. activity records or implementation evidence;
6. supplier profile or supplier verification context;
7. reimbursement policy or participant payment rules, if applicable;
8. donor reporting rules, if applicable;
9. explanation from the project manager, accountant, procurement reviewer, or budget owner;
10. prior review notes or approval records.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-008",
  "source_rule_name": "Repeated Round-Value Expense Review Rule",
  "source_rule_file": "REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md",
  "human_readable_rule": "Grant expenses require human review when repeated round-value amounts create a pattern that may need explanation, supporting documentation, or budget-owner confirmation.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when repeated round-value amounts materially affect reporting clarity, budget interpretation, supplier concentration, reimbursement explanation, threshold sensitivity, or audit-readiness.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* repeated amount patterns should be explained before reporting or audit packaging;
* supporting evidence should be checked;
* budget-owner, accountant, project-manager, or procurement-reviewer confirmation may be required.

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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, budget structure, donor rules, accounting records, activity records, supplier records, procurement records, reimbursement records, supporting documentation, and legal context.

---

## 9. Zero-Autonomy Boundary

LEO may identify this signal, attach this protocol reference, generate evidence context, and ask a reviewer question.

LEO must not:

1. decide that the expenses are compliant or non-compliant;
2. decide that the expenses are eligible or ineligible;
3. decide that the expenses are fraudulent;
4. decide that the expenses are unlawful;
5. block or approve payment;
6. punish or clear a supplier or participant;
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
5. documented as fixed-rate pattern confirmed;
6. documented as reimbursement pattern explained;
7. documented as supplier pricing explanation required;
8. documented as budget-owner confirmation required.

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

## 12. Continuation Note

This protocol is the eighth file in the Grant Expense Rule Traceability Layer.

The next protocol file in sequence is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md`
