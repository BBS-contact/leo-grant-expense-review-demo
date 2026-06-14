# Budget Line Usage Review Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-002

Protocol name: Budget Line Usage Review Rule

Signal family: `budget_line_usage_review`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant budget line whose accumulated expense usage indicates material consumption of the allocated budget or a pattern requiring budget-owner confirmation.

The purpose of this protocol is to make budget-line usage findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when one or more expenses linked to a budget line create a usage pattern that requires human review.

Such a pattern may include:

1. material consumption of the allocated budget line;
2. repeated use of the same budget line across multiple expenses;
3. concentration of spending under one budget line;
4. usage that approaches a reporting or internal review threshold;
5. usage that requires confirmation by the budget owner or project manager;
6. usage that may require explanation before audit packaging.

This trigger identifies a review requirement only.

It does not determine whether the budget line usage is eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

A grant budget line requires human review when accumulated expense usage indicates material consumption of the allocated budget or a pattern requiring budget-owner confirmation.

The reviewer must check whether the usage pattern is:

1. expected under the approved project plan;
2. supported by implementation progress;
3. consistent with the approved budget structure;
4. explainable by project timing, procurement, delivery, staffing, or activity requirements;
5. supported by sufficient documentation;
6. requiring budget-owner confirmation or donor reporting explanation.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Is the current use of this budget line justified by project implementation, approved budget structure, supporting documentation, and budget-owner confirmation?

The answer should be based on available budget, project, accounting, activity, supplier, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense records linked to the budget line;
2. budget line register;
3. approved project budget or donor budget annex;
4. project implementation schedule;
5. activity records linked to the expenses;
6. invoices, receipts, contracts, reimbursement forms, or other supporting documents;
7. budget-owner or project-manager explanation;
8. donor reporting rules, if applicable;
9. prior internal review notes, if available.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-002",
  "source_rule_name": "Budget Line Usage Review Rule",
  "source_rule_file": "BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant budget line requires human review when accumulated expense usage indicates material consumption of the allocated budget or a pattern requiring budget-owner confirmation.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the budget line usage is materially significant, concentrated, close to an internal threshold, or likely to require explanation before reporting or audit packaging.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* budget-owner confirmation may be required;
* supporting evidence should be checked before reporting or audit packaging;
* the usage pattern should be explained in review notes if necessary.

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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, budget, donor rules, accounting records, project implementation records, and legal context.

---

## 9. Zero-Autonomy Boundary

LEO may identify this signal, attach this protocol reference, generate evidence context, and ask a reviewer question.

LEO must not:

1. decide that the budget line usage is compliant or non-compliant;
2. decide that the budget line usage is fraudulent;
3. decide that the budget line usage is unlawful;
4. block or approve payment;
5. punish or clear a supplier;
6. mutate production records;
7. mutate canonical registry records;
8. execute enforcement actions;
9. access signing keys;
10. perform external execution.

---

## 10. Review Outcome Categories

A human reviewer may later classify the finding using review actions such as:

1. accepted as justified;
2. escalated for review;
3. marked as false positive;
4. marked as needing more evidence;
5. documented as budget-owner confirmed;
6. documented as requiring reporting explanation.

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

This protocol is the second file in the Grant Expense Rule Traceability Layer.

The next protocol file in sequence is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\CASH_REIMBURSEMENT_DOCUMENTATION_REVIEW_PROTOCOL_v0.1.md`
