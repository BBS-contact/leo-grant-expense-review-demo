# LEO Grant Expense Input Quality Report Tested Baseline v0.1

Canonical path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\LEO_GRANT_EXPENSE_INPUT_QUALITY_REPORT_TESTED_BASELINE_v0.1.md`

Status: TESTED BASELINE FIXED

Date: 2026-05-10

---

## 1. Baseline purpose

This document fixes the tested baseline for the first implemented layer of the LEO Grant Expense Review slice.

The current slice is a second practical LEO domain after the procurement/accounting anomaly review prototype.

The purpose of this layer is to check whether local grant expense CSV input files are structurally and semantically ready for analysis before any grant review signals are generated.

This is a data-readiness layer.

It does not generate grant risk findings.

It does not generate donor compliance conclusions.

It does not generate fraud verdicts.

It does not generate legal conclusions.

It does not perform enforcement.

---

## 2. Slice location

Grant Expense Review demo root:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Input folder:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\input\`

Output folder:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\`

---

## 3. Implemented input files

The current grant expense review input set contains four CSV files:

1. `input\grant_expenses.csv`
2. `input\grant_budget_lines.csv`
3. `input\grant_reporting_rules.csv`
4. `input\grant_supplier_profiles.csv`

These files create the controlled local demo input for the Grant Expense Review slice.

---

## 4. Input file roles

### 4.1 `grant_expenses.csv`

Purpose:

Stores local grant expense records.

Current baseline:

* 15 grant expense records;
* normal expenses;
* category mismatch scenarios;
* missing activity reference scenarios;
* partial documentation scenarios;
* repeated round-value expense scenarios;
* unknown supplier references;
* deadline concentration scenarios;
* budget line mapping scenario.

### 4.2 `grant_budget_lines.csv`

Purpose:

Defines grant budget lines, allowed expense categories, approved amounts, documentation requirements, cash reimbursement policy, and deadline sensitivity.

Current baseline:

* 8 budget lines;
* including `BL-008` for communication and public visibility;
* allowed category mappings;
* reporting period definitions;
* contract/invoice/activity requirements.

### 4.3 `grant_reporting_rules.csv`

Purpose:

Defines grant reporting rules used later by the review pipeline.

Current baseline:

* 12 reporting rules;
* reporting period close date;
* deadline-sensitive window;
* invoice requirement;
* activity reference requirement;
* contract-required categories;
* cash reimbursement documentation rule;
* category/budget line matching rule;
* known supplier profile requirement;
* repeated round-value threshold;
* large expense threshold;
* budget usage warning ratio;
* forbidden verdict language boundary.

### 4.4 `grant_supplier_profiles.csv`

Purpose:

Defines known supplier profiles for the grant expense review dataset.

Current baseline:

* 7 known supplier profiles;
* `SUP-001` through `SUP-007` are present;
* `SUP-008`, `SUP-009`, `SUP-010`, and `SUP-011` are intentionally absent.

Reason:

The missing suppliers produce controlled `UNKNOWN_SUPPLIER_REFERENCE` warnings.

This is intentional.

It allows the input quality layer to show that data can be ready for analysis while still containing review-worthy supplier reference warnings.

---

## 5. Implemented module

Implemented module:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_input_quality_report.py`

Status:

`Grant expense input quality report generator v0.1`

Output:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_input_quality_report.json`

Purpose:

Assess whether local grant expense review CSV input files are structurally and semantically ready for LEO grant expense evidence generation.

---

## 6. Implemented checks

The module checks:

* required file presence;
* required columns;
* empty critical fields;
* duplicate expense IDs;
* duplicate budget line IDs;
* duplicate reporting rule IDs;
* duplicate supplier IDs;
* decimal parseability;
* non-negative numeric values;
* boolean field validity;
* unsupported currencies;
* unknown budget line references;
* unknown supplier references;
* reporting rule grant/project/period scope consistency;
* expense reporting period consistency against budget line;
* expense currency consistency against budget line;
* budget line grant/project consistency;
* zero-autonomy boundary.

---

## 7. Initial blocking defect found and corrected

Initial run result:

`BLOCKED_BY_INPUT_ERRORS`

Cause:

`grant_expenses.csv` referenced `BL-008`, but `grant_budget_lines.csv` did not yet define `BL-008`.

Detected issue:

```text
ERROR: UNKNOWN_BUDGET_LINE_REFERENCE
Expense references budget_line_id without budget line definition: BL-008
```

Corrective action:

A new budget line was added to `grant_budget_lines.csv`:

```csv
BL-008,GRANT-BBS-2026-001,PRJ-LEO-001,Communication and public visibility,communications;public_materials;media_content,9000.00,PLN,2026-Q1,true,true,true,false,true,Communication and public visibility expenses require clear activity reference and donor reporting justification.
```

Reason:

The validator was correct.

A referenced budget line must exist.

The correct fix was to add the missing budget line, not to weaken the input quality logic.

---

## 8. Confirmed input quality run after correction

Command executed from:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Command:

```powershell
python grant_expense_input_quality_report.py
```

Confirmed result:

```json
{
  "status": "READY_WITH_WARNINGS",
  "output": "D:\\BBS-09-01-2026\\leo\\runtime\\demos\\grant_expense_review\\output\\grant_expense_input_quality_report.json",
  "summary": {
    "file_count": 4,
    "existing_file_count": 4,
    "grant_expense_count": 15,
    "budget_line_count": 8,
    "reporting_rule_count": 12,
    "supplier_profile_count": 7,
    "issue_count": 5,
    "error_count": 0,
    "warning_count": 5,
    "info_count": 0,
    "ready_for_analysis": true
  }
}
```

Meaning:

The input is ready for analysis, but with controlled warnings.

This is the intended baseline state.

---

## 9. Confirmed warnings

The remaining 5 warnings are all `UNKNOWN_SUPPLIER_REFERENCE` warnings.

Confirmed missing supplier references:

* `SUP-008`
* `SUP-009`
* `SUP-009`
* `SUP-010`
* `SUP-011`

The duplicate `SUP-009` warning is expected because two expenses reference `SUP-009`.

These warnings are intentional and should not be removed at this stage.

They support the future grant expense review pipeline by preserving controlled supplier-reference quality signals.

---

## 10. Interpretation of `READY_WITH_WARNINGS`

`READY_WITH_WARNINGS` means:

* the input files exist;
* required structure is present;
* there are no blocking input errors;
* analysis may continue;
* the system detected non-blocking data quality warnings that should be visible to a reviewer.

It does not mean:

* the expenses are approved;
* the expenses are donor-compliant;
* the expenses are legally compliant;
* the suppliers are acceptable;
* the project is audit-ready;
* there is no risk;
* there is fraud or corruption.

---

## 11. Zero-autonomy boundary

The generated input quality report preserves the following boundary:

* `autonomous_enforcement_actions`: `0`
* `canonical_registry_opened`: `false`
* `canonical_registry_mutated`: `false`
* `production_records_mutated`: `false`
* `signing_or_key_access_performed`: `false`
* `external_execution_performed`: `false`
* `pipeline_mode`: `LOCAL_READ_ONLY_GRANT_EXPENSE_INPUT_QUALITY_ASSESSMENT`

This layer is read-only.

It does not mutate input files.

It does not write to production systems.

It does not open or mutate the canonical registry.

It does not perform autonomous enforcement.

---

## 12. Implemented test file

Test file:

`D:\BBS-09-01-2026\leo\runtime\tests\test_grant_expense_input_quality_report.py`

Purpose:

Verify that `grant_expense_input_quality_report.py` accepts the controlled grant demo input with warnings and blocks malformed, incomplete, or cross-file-inconsistent grant expense input before grant review analysis.

---

## 13. Test coverage

The test file verifies:

* current grant demo input gives `READY_WITH_WARNINGS`;
* `error_count = 0`;
* `warning_count = 5`;
* `ready_for_analysis = true`;
* `grant_expense_count = 15`;
* `budget_line_count = 8`;
* `reporting_rule_count = 12`;
* `supplier_profile_count = 7`;
* expected unknown supplier warnings exist;
* `SUP-009` warning appears twice;
* zero-autonomy boundary is clean;
* clean minimal fixture gives `READY_FOR_ANALYSIS`;
* missing file blocks analysis;
* missing required column blocks analysis;
* empty critical field blocks analysis;
* invalid decimal blocks analysis;
* negative numeric value blocks analysis;
* invalid boolean blocks analysis;
* duplicate expense ID blocks analysis;
* duplicate budget line ID blocks analysis;
* duplicate rule ID blocks analysis;
* duplicate supplier ID blocks analysis;
* unknown budget line blocks analysis;
* unknown supplier gives warning but remains ready;
* currency mismatch gives warning;
* reporting period mismatch gives warning;
* unsupported currency gives warning;
* reporting rule scope not referenced gives warning;
* extra columns are reported in file summary.

---

## 14. Isolated test result

Command executed from:

`D:\BBS-09-01-2026\leo\runtime\`

Command:

```powershell
python -m pytest tests\test_grant_expense_input_quality_report.py
```

Confirmed result:

```text
21 passed in 1.26s
```

Meaning:

The grant expense input quality report has isolated pytest coverage.

---

## 15. Full runtime test result

Command executed from:

`D:\BBS-09-01-2026\leo\runtime\`

Command:

```powershell
python -m pytest tests
```

Confirmed result:

```text
2301 passed in 53.74s
```

Meaning:

The new Grant Expense Review input quality layer did not break the existing LEO runtime baseline.

The full runtime test count increased from `2280` to `2301`, reflecting the 21 new grant expense input quality tests.

Current full runtime state:

`CLEAN PASS`

---

## 16. Current Grant Expense Review slice status

Current slice root:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Current implemented artifacts:

1. `input\grant_expenses.csv`
2. `input\grant_budget_lines.csv`
3. `input\grant_reporting_rules.csv`
4. `input\grant_supplier_profiles.csv`
5. `grant_expense_input_quality_report.py`
6. `output\grant_expense_input_quality_report.json`
7. `tests\test_grant_expense_input_quality_report.py`

Current status:

`Grant Expense Review input quality layer v0.1 — tested baseline`

---

## 17. Relationship to procurement/accounting slice

The procurement/accounting slice remains the first completed local prototype flow.

The Grant Expense Review slice is now the second practical domain slice.

At this stage, Grant Expense Review has only its input quality layer implemented and tested.

This is intentional.

The slice should develop in the same disciplined sequence:

`CSV INPUT → INPUT QUALITY REPORT → REVIEW PIPELINE → EVIDENCE REPORT → EVIDENCE VALIDATOR → DASHBOARD/REPORT → HUMAN REVIEW PACKAGE → PACKAGE VALIDATOR`

Do not skip directly to dashboard or public claims.

---

## 18. Recommended next step

Recommended next step:

Create the first grant expense review pipeline:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_review_pipeline.py`

The pipeline should read:

* `input\grant_expenses.csv`
* `input\grant_budget_lines.csv`
* `input\grant_reporting_rules.csv`
* `input\grant_supplier_profiles.csv`
* optionally `output\grant_expense_input_quality_report.json`

The pipeline should generate:

`output\grant_expense_evidence_report.json`

Initial review signal families should include:

* `unknown_supplier_reference`
* `budget_line_category_mismatch`
* `missing_required_invoice`
* `missing_required_contract`
* `missing_activity_reference`
* `cash_reimbursement_documentation_review`
* `deadline_sensitive_expense`
* `repeated_round_value_expense`
* `large_expense_review`

The pipeline must preserve the same boundaries:

* no donor compliance conclusion;
* no legal conclusion;
* no fraud verdict;
* no payment blocking;
* no supplier punishment;
* no production mutation;
* no canonical registry mutation;
* no autonomous enforcement.

---

## 19. Baseline conclusion

The LEO Grant Expense Review input quality report v0.1 is now a tested baseline.

It confirms that the second practical LEO domain slice has begun correctly:

* controlled local input files exist;
* input quality is checked before analysis;
* blocking input errors are detected;
* controlled warnings remain visible;
* the zero-autonomy boundary is preserved;
* isolated tests pass;
* full runtime tests pass.

Current full runtime baseline:

`2301 passed in 53.74s`

Status:

`GRANT EXPENSE INPUT QUALITY TESTED BASELINE FIXED`
