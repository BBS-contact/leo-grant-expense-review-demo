# Missing Activity Reference Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-006

Protocol name: Missing Activity Reference Review Rule

Signal family: `missing_activity_reference`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant expense that lacks an activity reference needed to connect the cost to a project activity, output, event, implementation step, or documented project purpose.

The purpose of this protocol is to make missing-activity-reference findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, reimbursement packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when a grant expense does not contain a sufficient activity reference.

Such a missing or insufficient activity reference may include:

1. an empty activity reference field;
2. an unknown activity identifier;
3. a vague activity description;
4. a cost that cannot be linked to an implementation event;
5. a cost that cannot be linked to a project output;
6. a cost that requires project-manager explanation;
7. a cost that may be difficult to explain in reporting or audit packaging without additional context.

This trigger identifies a review requirement only.

It does not determine whether the expense is eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

A grant expense requires human review when it lacks an activity reference needed to connect the cost to a project activity, output, or implementation record.

The reviewer must check whether the expense can be connected to:

1. a valid project activity;
2. a documented implementation event;
3. a project output or deliverable;
4. an approved work plan item;
5. a beneficiary or participant activity;
6. a project-management explanation;
7. supporting documentation that makes the project purpose clear.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> What project activity, output, event, or implementation record justifies this expense, and is the connection documented clearly enough for reporting and audit-readiness?

The answer should be based on available project, activity, accounting, budget, supplier, reimbursement, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense record;
2. project activity register;
3. implementation schedule;
4. work plan or project plan;
5. event record, attendance list, training record, meeting note, delivery note, or field activity record;
6. project output or deliverable reference;
7. invoice, receipt, reimbursement request, contract, or other supporting document;
8. budget line reference;
9. donor reporting rules, if applicable;
10. explanation from the project manager, activity owner, accountant, or budget owner.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-006",
  "source_rule_name": "Missing Activity Reference Review Rule",
  "source_rule_file": "MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant expense requires human review when it lacks an activity reference needed to connect the cost to a project activity, output, or implementation record.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the missing activity reference materially affects project-purpose explanation, reporting clarity, budget justification, or audit-readiness.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* project-purpose evidence should be checked before reporting or audit packaging;
* activity linkage should be documented or clarified;
* project-manager or activity-owner explanation may be required.

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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, project activity records, work plan, budget structure, donor rules, accounting records, supporting documentation, and legal context.

---

## 9. Zero-Autonomy Boundary

LEO may identify this signal, attach this protocol reference, generate evidence context, and ask a reviewer question.

LEO must not:

1. decide that the expense is compliant or non-compliant;
2. decide that the expense is eligible or ineligible;
3. decide that the expense is fraudulent;
4. decide that the expense is unlawful;
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
5. documented as activity link corrected;
6. documented as project-manager explanation required;
7. documented as activity evidence attached.

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

This protocol is the sixth file in the Grant Expense Rule Traceability Layer.

The next protocol file in sequence is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md`
