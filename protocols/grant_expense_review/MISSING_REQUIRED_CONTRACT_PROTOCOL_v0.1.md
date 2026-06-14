# Missing Required Contract Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-007

Protocol name: Missing Required Contract Review Rule

Signal family: `missing_required_contract`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant expense where the transaction appears to require a contract, agreement, purchase order, engagement document, or other formal commitment record, but the required contract reference is missing or unavailable.

The purpose of this protocol is to make missing-contract findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, procurement review, reimbursement packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when a grant expense appears to require a formal contract or agreement reference and that reference is missing, empty, unclear, unavailable, or not linked to the expense record.

Such a case may include:

1. a supplier expense above a local documentation threshold;
2. a service purchase that normally requires an agreement;
3. a consulting, expert, venue, logistics, IT, training, or implementation service without a visible contract reference;
4. repeated supplier expenses where a framework agreement may be expected;
5. a large expense without a supporting contract or purchase order reference;
6. an expense description indicating contracted work but no contract reference;
7. a record that may require procurement or budget-owner confirmation.

This trigger identifies a review requirement only.

It does not determine whether the expense is eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

A grant expense requires human review when the transaction appears to require a contract or formal agreement but the required contract reference is missing or unavailable.

The reviewer must check whether:

1. a contract, agreement, purchase order, or equivalent commitment document exists;
2. the expense should have been linked to that document;
3. the missing reference is a data-entry problem;
4. the transaction falls below a threshold where a contract is not required;
5. the supplier or service type requires procurement documentation;
6. the expense is sufficiently documented for reporting and audit-readiness;
7. the budget owner, project manager, accountant, or procurement reviewer can provide clarification.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Does this expense require a contract, agreement, purchase order, or equivalent commitment document, and if so, where is the supporting reference or explanation?

The answer should be based on available accounting, procurement, budget, supplier, project, contract, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense record;
2. contract, agreement, purchase order, engagement letter, or equivalent document;
3. procurement request, procurement note, or supplier selection record;
4. invoice or receipt;
5. payment documentation;
6. supplier profile or supplier verification context;
7. budget line reference;
8. project activity record;
9. donor reporting rules, if applicable;
10. internal procurement or documentation threshold rules;
11. explanation from the project manager, accountant, procurement reviewer, or budget owner.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-007",
  "source_rule_name": "Missing Required Contract Review Rule",
  "source_rule_file": "MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant expense requires human review when the transaction appears to require a contract or formal agreement but the required contract reference is missing or unavailable.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the missing contract reference materially affects procurement traceability, supplier accountability, budget justification, reporting clarity, or audit-readiness.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* contract or procurement evidence should be checked before reporting or audit packaging;
* the absence of a reference should be explained or corrected if necessary;
* budget-owner, accountant, project-manager, or procurement-reviewer confirmation may be required.

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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, procurement rules, contract records, budget structure, donor rules, accounting records, project implementation records, supporting documentation, and legal context.

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
5. documented as contract reference corrected;
6. documented as contract not required under threshold;
7. documented as procurement clarification requested;
8. documented as supporting agreement attached.

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

This protocol is the seventh file in the Grant Expense Rule Traceability Layer.

The next protocol file in sequence is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md`
