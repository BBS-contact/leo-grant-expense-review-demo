# Budget Line Category Mismatch Protocol v0.1

Canonical save path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md`

Status: ACTIVE LOCAL PROTOTYPE PROTOCOL

Protocol ID: GER-RULE-001

Protocol name: Budget Line Category Mismatch Review Rule

Signal family: `budget_line_category_mismatch`

Layer: Grant Expense Rule Traceability Layer

Scope: Grant Expense Review local prototype slice

---

## 1. Purpose

This protocol defines the human review rule for a grant expense whose recorded expense category does not align with the category of the referenced budget line.

The purpose of this protocol is to make the finding explainable, traceable, and reviewable by a human reviewer before any grant reporting, audit packaging, or internal management response is prepared.

This protocol does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.

---

## 2. Review Trigger

A finding may be generated under this protocol when all of the following conditions are present:

1. a grant expense references a budget line;
2. the referenced budget line exists in the budget line register;
3. the expense category differs from the budget line category;
4. the mismatch may affect how the expense is interpreted, reported, explained, or reviewed.

This trigger identifies a review requirement only.

It does not determine whether the expense is eligible, ineligible, compliant, non-compliant, fraudulent, unlawful, payable, non-payable, or sanctionable.

---

## 3. Human-Readable Rule

A grant expense requires human review when its recorded expense category does not align with the referenced budget line category.

The reviewer must check whether the mismatch is caused by:

1. a data-entry issue;
2. a wrong budget line reference;
3. a legitimate cross-category allocation;
4. a reclassification that requires explanation;
5. a reporting rule that allows or restricts the allocation;
6. missing supporting context.

---

## 4. Reviewer Question

The reviewer should answer the following question:

> Why does this expense category differ from the referenced budget line category, and is there documented justification for treating the expense under this budget line?

The answer should be based on available project, budget, accounting, activity, and supporting documentation.

---

## 5. Expected Evidence

The reviewer may need to inspect one or more of the following evidence sources:

1. grant expense record;
2. referenced budget line record;
3. project budget or approved budget annex;
4. donor reporting rules, if applicable;
5. invoice, receipt, contract, reimbursement form, or other supporting document;
6. activity reference or implementation record;
7. internal explanation from the budget owner or project manager.

The absence of one evidence source does not automatically create a verdict.

It only identifies a need for further review or explanation.

---

## 6. Rule Trace Object

Findings using this protocol should include the following `rule_trace` object:

```json
{
  "source_rule_id": "GER-RULE-001",
  "source_rule_name": "Budget Line Category Mismatch Review Rule",
  "source_rule_file": "BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md",
  "protocol_reference": "protocols/grant_expense_review/BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md",
  "human_readable_rule": "A grant expense requires human review when its recorded expense category does not align with the referenced budget line category.",
  "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action."
}
```

---

## 7. Severity Handling

This protocol may support a HIGH severity finding when the category mismatch materially affects budget interpretation, reporting clarity, activity linkage, or audit-readiness.

Severity does not change the verdict boundary.

A HIGH finding means:

* human review is more urgent;
* the explanation should be documented;
* supporting evidence should be checked before reporting or audit packaging.

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

Any final interpretation must be made by an authorized human reviewer using the applicable grant agreement, budget, donor rules, accounting records, and legal context.

---

## 9. Zero-Autonomy Boundary

LEO may identify this signal, attach this protocol reference, generate evidence context, and ask a reviewer question.

LEO must not:

1. decide that the expense is compliant or non-compliant;
2. decide that the expense is fraudulent;
3. decide that the expense is unlawful;
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
5. documented as corrected data-entry issue.

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

This protocol is the first file in the Grant Expense Rule Traceability Layer.

The next protocol file in sequence is:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\protocols\grant_expense_review\BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md`
