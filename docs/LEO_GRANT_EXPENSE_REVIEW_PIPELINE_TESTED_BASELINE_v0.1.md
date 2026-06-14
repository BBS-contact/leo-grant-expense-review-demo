# LEO Grant Expense Review Pipeline Tested Baseline v0.1

Canonical path:
`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\LEO_GRANT_EXPENSE_REVIEW_PIPELINE_TESTED_BASELINE_v0.1.md`

Status: TESTED BASELINE FIXED

Date: 2026-05-11

---

## 1. Baseline purpose

This document fixes the tested baseline for the second implemented layer of the LEO Grant Expense Review slice.

The first implemented layer was:

`CSV INPUT → INPUT QUALITY REPORT`

This baseline confirms the second layer:

`INPUT QUALITY REPORT → GRANT EXPENSE REVIEW PIPELINE → GRANT EXPENSE EVIDENCE REPORT`

The pipeline generates evidence-backed human review signals from controlled local grant expense CSV input.

It does not generate donor compliance conclusions.

It does not generate legal conclusions.

It does not generate fraud verdicts.

It does not block payments.

It does not punish suppliers.

It does not mutate production records.

It does not open or mutate the canonical registry.

It does not perform autonomous enforcement.

---

## 2. Slice location

Grant Expense Review demo root:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Input folder:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\input\`

Output folder:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\`

Runtime tests folder:

`D:\BBS-09-01-2026\leo\runtime\tests\`

---

## 3. Implemented pipeline file

Implemented file:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_review_pipeline.py`

Status:

`Grant expense review evidence pipeline v0.1`

Purpose:

Generate evidence-backed human review signals from local grant expense CSV input.

---

## 4. Pipeline inputs

The pipeline reads:

1. `input\grant_expenses.csv`
2. `input\grant_budget_lines.csv`
3. `input\grant_reporting_rules.csv`
4. `input\grant_supplier_profiles.csv`
5. `output\grant_expense_input_quality_report.json`

The input quality report must permit analysis.

Allowed input quality statuses:

* `READY_FOR_ANALYSIS`
* `READY_WITH_WARNINGS`

The pipeline refuses to run when input quality is blocked.

---

## 5. Pipeline output

The pipeline writes:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\output\grant_expense_evidence_report.json`

Report identity:

* `report_id`: `LOCAL_GRANT_EXPENSE_REVIEW_REPORT`
* `report_type`: `LEO_GRANT_EXPENSE_REVIEW_EVIDENCE_REPORT`
* `report_version`: `v0.1`
* `source_name`: `grant_expense_review_pipeline.py`
* `dashboard_mode`: `LOCAL_GRANT_EXPENSE_REVIEW`

---

## 6. Confirmed manual execution

Commands executed from:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Commands:

```powershell
python grant_expense_input_quality_report.py
python grant_expense_review_pipeline.py
```

Confirmed pipeline output:

```json
{
  "status": "OK",
  "output": "D:\\BBS-09-01-2026\\leo\\runtime\\demos\\grant_expense_review\\output\\grant_expense_evidence_report.json",
  "summary": {
    "findings_count": 25,
    "evidence_count": 25,
    "grant_expense_count": 15,
    "supplier_count": 11,
    "known_supplier_profile_count": 7,
    "high_or_critical_findings_count": 12,
    "reviewed_findings_count": 0,
    "input_quality_status": "READY_WITH_WARNINGS",
    "input_quality_warning_count": 5,
    "input_quality_error_count": 0,
    "signal_families": {
      "budget_line_category_mismatch": 1,
      "budget_line_usage_review": 3,
      "cash_reimbursement_documentation_review": 1,
      "deadline_sensitive_expense": 5,
      "large_expense_review": 5,
      "missing_activity_reference": 1,
      "missing_required_contract": 2,
      "repeated_round_value_expense": 2,
      "unknown_supplier_reference": 5
    },
    "severity_distribution": {
      "HIGH": 12,
      "MEDIUM": 13
    },
    "autonomous_actions": 0
  }
}
```

---

## 7. Confirmed generated report summary

The generated `output\grant_expense_evidence_report.json` summary was inspected directly and confirmed:

```json
{
  "findings_count": 25,
  "evidence_count": 25,
  "grant_expense_count": 15,
  "supplier_count": 11,
  "known_supplier_profile_count": 7,
  "high_or_critical_findings_count": 12,
  "reviewed_findings_count": 0,
  "input_quality_status": "READY_WITH_WARNINGS",
  "input_quality_warning_count": 5,
  "input_quality_error_count": 0,
  "signal_families": {
    "budget_line_category_mismatch": 1,
    "budget_line_usage_review": 3,
    "cash_reimbursement_documentation_review": 1,
    "deadline_sensitive_expense": 5,
    "large_expense_review": 5,
    "missing_activity_reference": 1,
    "missing_required_contract": 2,
    "repeated_round_value_expense": 2,
    "unknown_supplier_reference": 5
  },
  "severity_distribution": {
    "HIGH": 12,
    "MEDIUM": 13
  },
  "autonomous_actions": 0
}
```

---

## 8. Implemented signal families

The pipeline currently generates the following signal families:

1. `unknown_supplier_reference`
2. `budget_line_category_mismatch`
3. `missing_required_invoice`
4. `missing_required_contract`
5. `missing_activity_reference`
6. `cash_reimbursement_documentation_review`
7. `deadline_sensitive_expense`
8. `large_expense_review`
9. `repeated_round_value_expense`
10. `budget_line_usage_review`

Not every family appears in the current baseline count.

The current baseline data produces 9 active signal families, with `missing_required_invoice` available in the pipeline and covered by tests.

---

## 9. Current baseline signal distribution

Confirmed current distribution:

```text
budget_line_category_mismatch: 1
budget_line_usage_review: 3
cash_reimbursement_documentation_review: 1
deadline_sensitive_expense: 5
large_expense_review: 5
missing_activity_reference: 1
missing_required_contract: 2
repeated_round_value_expense: 2
unknown_supplier_reference: 5
```

Total findings:

`25`

Total evidence objects:

`25`

---

## 10. Current severity distribution

Confirmed current severity distribution:

```text
HIGH: 12
MEDIUM: 13
```

High or critical findings:

`12`

Critical findings:

`0`

This is intentional for the current demo.

The pipeline creates review signals, not legal or enforcement conclusions.

---

## 11. Evidence model

Each finding includes:

* evidence ID;
* title;
* severity;
* signal family;
* expense ID;
* supplier ID;
* supplier name;
* budget line ID;
* amount;
* currency;
* detected signal;
* why it matters;
* reviewer question;
* next action;
* evidence references;
* metadata.

Each evidence object maps back to a finding.

Confirmed rule:

`one finding → one evidence object`

Current baseline:

`25 findings → 25 evidence objects`

---

## 12. Input quality relationship

The pipeline consumes the input quality report and propagates its state into the evidence report summary:

```text
input_quality_status: READY_WITH_WARNINGS
input_quality_warning_count: 5
input_quality_error_count: 0
```

Meaning:

The pipeline acknowledges that input data is analyzable but contains 5 non-blocking data quality warnings.

Those warnings are expected and are caused by controlled unknown supplier references.

The pipeline does not hide those warnings.

---

## 13. Zero-autonomy boundary

The pipeline output preserves the following boundary:

* `autonomous_enforcement_actions`: `0`
* `canonical_registry_opened`: `false`
* `canonical_registry_mutated`: `false`
* `production_records_mutated`: `false`
* `payment_block_performed`: `false`
* `supplier_punishment_performed`: `false`
* `donor_compliance_conclusion_issued`: `false`
* `fraud_verdict_issued`: `false`
* `legal_conclusion_issued`: `false`
* `signing_or_key_access_performed`: `false`
* `external_execution_performed`: `false`
* `pipeline_mode`: `LOCAL_READ_ONLY_GRANT_EXPENSE_REVIEW_SIGNAL_GENERATION`

The report is a local review artifact.

It does not authorize action.

---

## 14. Interpretation boundary

The generated report explicitly states that it contains evidence-backed review signals only.

It does not issue:

* fraud verdicts;
* legal conclusions;
* donor compliance conclusions;
* payment blocks;
* supplier punishments;
* production mutations;
* autonomous enforcement actions.

Human review remains required.

---

## 15. Initial test defect and correction

During isolated test execution, one test failed:

`test_budget_usage_signal_is_generated`

Cause:

The minimal fixture used:

```text
amount = 12000.00
approved_amount = 15000.00
```

This produced usage:

```text
12000 / 15000 = 0.80
```

The pipeline threshold for `budget_line_usage_review` is:

```text
0.85
```

Therefore the pipeline was correct not to generate the signal.

The test was corrected by changing the temporary fixture amount to:

```text
13000.00
```

This produces:

```text
13000 / 15000 = 0.8666...
```

which is above the threshold and correctly triggers `budget_line_usage_review`.

This was a test fixture correction, not a pipeline defect.

---

## 16. Implemented test file

Test file:

`D:\BBS-09-01-2026\leo\runtime\tests\test_grant_expense_review_pipeline.py`

Purpose:

Verify that `grant_expense_review_pipeline.py` generates a stable local evidence report from controlled grant expense CSV input and preserves the zero-autonomy boundary.

---

## 17. Test coverage

The test file verifies:

* current pipeline baseline: 25 findings / 25 evidence objects;
* report identity fields;
* signal family distribution;
* severity distribution;
* unknown supplier findings;
* evidence object consistency;
* zero-autonomy boundary;
* interpretation boundary;
* written JSON parseability;
* pipeline refuses missing input quality report;
* pipeline refuses `BLOCKED_BY_INPUT_ERRORS`;
* pipeline refuses `ready_for_analysis = false`;
* minimal fixture generates expected signals;
* category mismatch signal;
* missing invoice signal;
* cash reimbursement signal;
* unknown supplier signal;
* repeated round-value signal;
* budget usage signal;
* no forbidden verdict phrases.

---

## 18. Isolated pipeline test result

Command executed from:

`D:\BBS-09-01-2026\leo\runtime\`

Command:

```powershell
python -m pytest tests\test_grant_expense_review_pipeline.py
```

Confirmed result after test correction:

```text
19 passed in 0.83s
```

Meaning:

The grant expense review pipeline has isolated pytest coverage.

---

## 19. Full runtime test result

Command executed from:

`D:\BBS-09-01-2026\leo\runtime\`

Command:

```powershell
python -m pytest tests
```

Confirmed result:

```text
2320 passed in 54.73s
```

Meaning:

The new Grant Expense Review pipeline layer did not break the existing LEO runtime baseline.

The full runtime test count increased from `2301` to `2320`, reflecting the 19 new grant expense review pipeline tests.

Current full runtime state:

`CLEAN PASS`

---

## 20. Current Grant Expense Review slice status

Current slice root:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\`

Current implemented artifacts:

1. `input\grant_expenses.csv`
2. `input\grant_budget_lines.csv`
3. `input\grant_reporting_rules.csv`
4. `input\grant_supplier_profiles.csv`
5. `grant_expense_input_quality_report.py`
6. `output\grant_expense_input_quality_report.json`
7. `grant_expense_review_pipeline.py`
8. `output\grant_expense_evidence_report.json`
9. `tests\test_grant_expense_input_quality_report.py`
10. `tests\test_grant_expense_review_pipeline.py`

Current status:

`Grant Expense Review pipeline v0.1 — tested baseline`

---

## 21. Relationship to procurement/accounting slice

The procurement/accounting slice remains the first completed local prototype flow.

The Grant Expense Review slice is the second practical domain slice.

At this stage, Grant Expense Review now has:

1. tested input quality layer;
2. tested evidence generation pipeline.

It does not yet have:

* evidence report validator;
* dashboard;
* human review package export;
* human review package validator.

Those should be added in order, not skipped.

---

## 22. Recommended next step

Recommended next step:

Create an evidence report validator for the Grant Expense Review slice:

`D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_evidence_report_validator.py`

Purpose:

Validate `output\grant_expense_evidence_report.json` before any dashboard or external explanation layer consumes it.

The validator should check:

* file exists;
* JSON parseability;
* report identity fields;
* required summary fields;
* findings count equals evidence object count;
* signal family counts match findings;
* severity distribution matches findings;
* each finding has evidence ID;
* each evidence object maps to a finding;
* zero-autonomy boundary is clean;
* interpretation boundary is clean;
* input quality status is present;
* forbidden verdict phrases are absent.

This mirrors the architecture used in the procurement/accounting slice.

---

## 23. Baseline conclusion

The LEO Grant Expense Review pipeline v0.1 is now a tested baseline.

It confirms that the second practical LEO domain slice can now move from data readiness into evidence-backed grant expense review signal generation.

The pipeline produced:

* 25 findings;
* 25 evidence objects;
* 12 high-severity findings;
* 13 medium-severity findings;
* 0 autonomous actions;
* 0 donor compliance conclusions;
* 0 legal conclusions;
* 0 fraud verdicts;
* 0 production mutations.

Current full runtime baseline:

`2320 passed in 54.73s`

Status:

`GRANT EXPENSE REVIEW PIPELINE TESTED BASELINE FIXED`
