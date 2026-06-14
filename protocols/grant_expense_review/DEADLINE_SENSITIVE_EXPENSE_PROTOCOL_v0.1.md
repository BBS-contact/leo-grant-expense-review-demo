# Deadline-Sensitive Expense Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-004

Protocol name: Deadline-Sensitive Expense Review Rule

Signal family: `deadline_sensitive_expense`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant expense whose timing is close to a reporting, eligibility, implementation, project-period, or documentation boundary.

The purpose of this protocol is to make time-sensitive expense findings explainable, traceable, and reviewable by a human reviewer before grant reporting, audit packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when a grant expense occurs near a relevant time boundary that may require additional human explanation or supporting evidence.

Such a time boundary may include:

1. reporting period end date;
2. project implementation end date;
3. grant eligibility period boundary;
4. invoice or payment deadline;
5. reimbursement deadline;
6. internal accounting cut-off date;
7. donor reporting submission deadline;
8. audit preparation or evidence packaging deadline.

This trigger identifies a review requirement only.

It does not determine whether the expense is eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

A grant expense requires human review when its timing is close to a reporting, eligibility, or project-period boundary that may require additional explanation.

The reviewer must check whether the expense timing is:

1. inside the relevant grant or project period;
2. linked to a valid project activity;
3. supported by documentation dated within the appropriate period;
4. explainable if invoice, payment, service delivery, or reimbursement dates differ;
5. properly classified for the relevant reporting period;
6. sufficiently documented for audit-readiness.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Is the timing of this expense properly supported, explainable, and aligned with the relevant project period, reporting period, or eligibility boundary?

The answer should be based on available project, accounting, invoice, payment, activity, reporting, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense record;
2. invoice date;
3. payment date;
4. service delivery date;
5. reimbursement request date;
6. project implementation period;
7. grant eligibility period;
8. donor reporting period;
9. activity or event record;
10. accounting cut-off documentation;
11. donor reporting rules, if applicable;
12. internal explanation from the project manager, accountant, or budget owner.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-004",
  "source_rule_name": "Deadline-Sensitive Expense Review Rule",
  "source_rule_file": "DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant expense requires human review when its timing is close to a reporting, eligibility, or project-period boundary that may require additional explanation.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the expense timing is materially close to a reporting deadline, eligibility boundary, project-period boundary, or audit packaging deadline.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* timing evidence should be checked before reporting or audit packaging;
* date differences should be explained where necessary;
* the finding may require budget-owner, accountant, or project-manager confirmation.

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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, project period, reporting period, donor rules, accounting records, project implementation records, and legal context.

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
5. documented as timing explanation required;
6. documented as timing evidence confirmed.

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

This protocol is the fourth file in the Grant Expense Rule Traceability Layer.

The next protocol file in sequence is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md`
