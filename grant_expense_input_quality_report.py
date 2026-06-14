r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_input_quality_report.py

Status:
Input quality report generator v0.1 for the LEO grant expense review demo.

Purpose:
Assess whether local grant expense review CSV input files are structurally and
semantically ready for LEO grant expense evidence generation.

This module checks input data quality before grant expense review analysis.
It does not generate risk findings, fraud verdicts, legal conclusions, donor
compliance conclusions, or enforcement actions.

Checked input files:
- input/grant_expenses.csv
- input/grant_budget_lines.csv
- input/grant_reporting_rules.csv
- input/grant_supplier_profiles.csv

The report checks:
- required file presence;
- required columns;
- empty critical fields;
- duplicate primary IDs;
- decimal parseability;
- non-negative numeric values;
- boolean field validity;
- unsupported currencies;
- unknown budget line references;
- unknown supplier references;
- unknown reporting rule grant/project references;
- expense reporting period consistency;
- expense currency consistency against budget line;
- budget line grant/project consistency;
- zero-autonomy boundary.

Boundary:
- Read-only input quality assessment.
- No grant compliance verdicts.
- No fraud or legal conclusions.
- No production mutation.
- No canonical registry access.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.

Run from the grant demo folder:
python grant_expense_input_quality_report.py

Output:
output/grant_expense_input_quality_report.json
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "grant_expense_input_quality_report.json"

SUPPORTED_CURRENCIES = {"PLN", "EUR", "USD"}
BOOLEAN_VALUES = {"true", "false"}

REQUIRED_COLUMNS = {
    "grant_expenses": {
        "expense_id",
        "date",
        "project_id",
        "grant_id",
        "budget_line_id",
        "supplier_id",
        "supplier_name",
        "expense_category",
        "description",
        "amount",
        "currency",
        "payment_method",
        "invoice_id",
        "contract_id",
        "activity_reference",
        "reporting_period",
        "requested_by",
        "approved_by",
        "document_status",
    },
    "grant_budget_lines": {
        "budget_line_id",
        "grant_id",
        "project_id",
        "budget_line_name",
        "allowed_expense_categories",
        "approved_amount",
        "currency",
        "reporting_period",
        "requires_contract",
        "requires_invoice",
        "requires_activity_reference",
        "allow_cash_reimbursement",
        "deadline_sensitive",
        "notes",
    },
    "grant_reporting_rules": {
        "rule_id",
        "grant_id",
        "project_id",
        "reporting_period",
        "rule_type",
        "rule_name",
        "parameter",
        "value",
        "severity_if_triggered",
        "review_question",
        "notes",
    },
    "grant_supplier_profiles": {
        "supplier_id",
        "supplier_name",
        "declared_activity",
        "supplier_role",
        "capacity_score",
        "registration_status",
        "country",
        "risk_note",
    },
}

CRITICAL_FIELDS = {
    "grant_expenses": [
        "expense_id",
        "date",
        "project_id",
        "grant_id",
        "budget_line_id",
        "supplier_id",
        "supplier_name",
        "expense_category",
        "description",
        "amount",
        "currency",
        "payment_method",
        "reporting_period",
        "requested_by",
        "approved_by",
        "document_status",
    ],
    "grant_budget_lines": [
        "budget_line_id",
        "grant_id",
        "project_id",
        "budget_line_name",
        "allowed_expense_categories",
        "approved_amount",
        "currency",
        "reporting_period",
        "requires_contract",
        "requires_invoice",
        "requires_activity_reference",
        "allow_cash_reimbursement",
        "deadline_sensitive",
    ],
    "grant_reporting_rules": [
        "rule_id",
        "grant_id",
        "project_id",
        "reporting_period",
        "rule_type",
        "rule_name",
        "parameter",
        "value",
        "severity_if_triggered",
        "review_question",
    ],
    "grant_supplier_profiles": [
        "supplier_id",
        "supplier_name",
        "declared_activity",
        "supplier_role",
        "capacity_score",
        "registration_status",
        "country",
    ],
}

NUMERIC_FIELDS = {
    "grant_expenses": ["amount"],
    "grant_budget_lines": ["approved_amount"],
    "grant_reporting_rules": [],
    "grant_supplier_profiles": ["capacity_score"],
}

BOOLEAN_FIELDS = {
    "grant_expenses": [],
    "grant_budget_lines": [
        "requires_contract",
        "requires_invoice",
        "requires_activity_reference",
        "allow_cash_reimbursement",
        "deadline_sensitive",
    ],
    "grant_reporting_rules": [],
    "grant_supplier_profiles": [],
}

PRIMARY_KEYS = {
    "grant_expenses": (["expense_id"], "DUPLICATE_EXPENSE_ID"),
    "grant_budget_lines": (["budget_line_id"], "DUPLICATE_BUDGET_LINE_ID"),
    "grant_reporting_rules": (["rule_id"], "DUPLICATE_RULE_ID"),
    "grant_supplier_profiles": (["supplier_id"], "DUPLICATE_SUPPLIER_ID"),
}


@dataclass(frozen=True)
class InputQualityIssue:
    severity: str
    code: str
    message: str
    file: str
    row_number: Optional[int] = None
    field: Optional[str] = None
    value: Optional[str] = None


@dataclass
class InputQualityReport:
    report_id: str
    generated_at: str
    input_dir: str
    status: str
    summary: Dict[str, Any]
    files: Dict[str, Dict[str, Any]]
    issues: List[InputQualityIssue] = field(default_factory=list)
    zero_autonomy_boundary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "input_dir": self.input_dir,
            "status": self.status,
            "summary": self.summary,
            "files": self.files,
            "issues": [issue.__dict__ for issue in self.issues],
            "zero_autonomy_boundary": self.zero_autonomy_boundary,
        }


@dataclass(frozen=True)
class CsvData:
    logical_name: str
    path: Path
    exists: bool
    fieldnames: List[str]
    rows: List[Dict[str, str]]


def main() -> None:
    report = generate_input_quality_report(INPUT_DIR, OUTPUT_FILE)
    print(json.dumps({"status": report.status, "output": str(OUTPUT_FILE), "summary": report.summary}, indent=2))


def generate_input_quality_report(input_dir: Path = INPUT_DIR, output_file: Path = OUTPUT_FILE) -> InputQualityReport:
    csv_data = {
        "grant_expenses": read_csv_data("grant_expenses", input_dir / "grant_expenses.csv"),
        "grant_budget_lines": read_csv_data("grant_budget_lines", input_dir / "grant_budget_lines.csv"),
        "grant_reporting_rules": read_csv_data("grant_reporting_rules", input_dir / "grant_reporting_rules.csv"),
        "grant_supplier_profiles": read_csv_data("grant_supplier_profiles", input_dir / "grant_supplier_profiles.csv"),
    }

    issues: List[InputQualityIssue] = []
    files_summary: Dict[str, Dict[str, Any]] = {}

    for logical_name, data in csv_data.items():
        files_summary[logical_name] = build_file_summary(data)
        issues.extend(validate_file_presence_and_columns(data))
        if data.exists:
            issues.extend(validate_empty_critical_fields(data))
            issues.extend(validate_numeric_fields(data))
            issues.extend(validate_boolean_fields(data))
            issues.extend(validate_supported_currencies(data))
            key_fields, duplicate_code = PRIMARY_KEYS[logical_name]
            issues.extend(validate_duplicate_keys(data, key_fields, duplicate_code))

    issues.extend(validate_expense_budget_line_coverage(csv_data["grant_expenses"], csv_data["grant_budget_lines"]))
    issues.extend(validate_expense_supplier_coverage(csv_data["grant_expenses"], csv_data["grant_supplier_profiles"]))
    issues.extend(validate_expense_budget_line_currency(csv_data["grant_expenses"], csv_data["grant_budget_lines"]))
    issues.extend(validate_expense_reporting_period(csv_data["grant_expenses"], csv_data["grant_budget_lines"]))
    issues.extend(validate_reporting_rule_scope(csv_data["grant_reporting_rules"], csv_data["grant_budget_lines"], csv_data["grant_expenses"]))

    status = calculate_status(issues)
    summary = build_report_summary(csv_data, issues)

    report = InputQualityReport(
        report_id="LOCAL_GRANT_EXPENSE_INPUT_QUALITY_REPORT",
        generated_at=datetime.now(timezone.utc).isoformat(),
        input_dir=str(input_dir),
        status=status,
        summary=summary,
        files=files_summary,
        issues=issues,
        zero_autonomy_boundary={
            "autonomous_enforcement_actions": 0,
            "canonical_registry_opened": False,
            "canonical_registry_mutated": False,
            "production_records_mutated": False,
            "signing_or_key_access_performed": False,
            "external_execution_performed": False,
            "pipeline_mode": "LOCAL_READ_ONLY_GRANT_EXPENSE_INPUT_QUALITY_ASSESSMENT",
        },
    )

    write_report(report, output_file)
    return report


def read_csv_data(logical_name: str, path: Path) -> CsvData:
    if not path.exists():
        return CsvData(logical_name=logical_name, path=path, exists=False, fieldnames=[], rows=[])

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [field.strip() for field in (reader.fieldnames or [])]
        rows = [{key.strip(): (value or "").strip() for key, value in row.items()} for row in reader]

    return CsvData(logical_name=logical_name, path=path, exists=True, fieldnames=fieldnames, rows=rows)


def build_file_summary(data: CsvData) -> Dict[str, Any]:
    required = REQUIRED_COLUMNS[data.logical_name]
    actual = set(data.fieldnames)
    return {
        "path": str(data.path),
        "exists": data.exists,
        "row_count": len(data.rows),
        "column_count": len(data.fieldnames),
        "required_columns_present": data.exists and required.issubset(actual),
        "missing_columns": sorted(required - actual) if data.exists else sorted(required),
        "extra_columns": sorted(actual - required) if data.exists else [],
    }


def validate_file_presence_and_columns(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    if not data.exists:
        issues.append(
            InputQualityIssue(
                severity="ERROR",
                code="INPUT_FILE_MISSING",
                message=f"Required input file is missing: {data.path}",
                file=str(data.path),
            )
        )
        return issues

    actual = set(data.fieldnames)
    missing = REQUIRED_COLUMNS[data.logical_name] - actual
    for column in sorted(missing):
        issues.append(
            InputQualityIssue(
                severity="ERROR",
                code="REQUIRED_COLUMN_MISSING",
                message=f"Required column is missing: {column}",
                file=str(data.path),
                field=column,
            )
        )

    if len(data.rows) == 0:
        issues.append(
            InputQualityIssue(
                severity="WARNING",
                code="INPUT_FILE_EMPTY",
                message="Input file has a header but no data rows.",
                file=str(data.path),
            )
        )

    return issues


def validate_empty_critical_fields(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    available_fields = set(data.fieldnames)
    for row_index, row in enumerate(data.rows, start=2):
        for field_name in CRITICAL_FIELDS[data.logical_name]:
            if field_name not in available_fields:
                continue
            if row.get(field_name, "").strip() == "":
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="CRITICAL_FIELD_EMPTY",
                        message=f"Critical field is empty: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                    )
                )
    return issues


def validate_numeric_fields(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    available_fields = set(data.fieldnames)
    for row_index, row in enumerate(data.rows, start=2):
        for field_name in NUMERIC_FIELDS[data.logical_name]:
            if field_name not in available_fields:
                continue
            raw_value = row.get(field_name, "").strip()
            if raw_value == "":
                continue
            parsed = parse_decimal_or_none(raw_value)
            if parsed is None:
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="NUMERIC_FIELD_INVALID",
                        message=f"Numeric field is not parseable: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                        value=raw_value,
                    )
                )
                continue
            if parsed < 0:
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="NUMERIC_FIELD_NEGATIVE",
                        message=f"Numeric field must not be negative: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                        value=raw_value,
                    )
                )
    return issues


def validate_boolean_fields(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    available_fields = set(data.fieldnames)
    for row_index, row in enumerate(data.rows, start=2):
        for field_name in BOOLEAN_FIELDS[data.logical_name]:
            if field_name not in available_fields:
                continue
            raw_value = row.get(field_name, "").strip().lower()
            if raw_value == "":
                continue
            if raw_value not in BOOLEAN_VALUES:
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="BOOLEAN_FIELD_INVALID",
                        message=f"Boolean field must be true or false: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                        value=row.get(field_name, ""),
                    )
                )
    return issues


def validate_supported_currencies(data: CsvData) -> List[InputQualityIssue]:
    if "currency" not in data.fieldnames:
        return []

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(data.rows, start=2):
        currency = row.get("currency", "").strip().upper()
        if currency == "":
            continue
        if currency not in SUPPORTED_CURRENCIES:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="UNSUPPORTED_CURRENCY",
                    message=f"Currency is not in the supported demo currency set: {currency}",
                    file=str(data.path),
                    row_number=row_index,
                    field="currency",
                    value=currency,
                )
            )
    return issues


def validate_duplicate_keys(data: CsvData, key_fields: Sequence[str], code: str) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    if not set(key_fields).issubset(set(data.fieldnames)):
        return issues

    seen: Dict[Tuple[str, ...], int] = {}
    for row_index, row in enumerate(data.rows, start=2):
        key = tuple(normalize_key_value(row.get(field_name, "")) for field_name in key_fields)
        if any(value == "" for value in key):
            continue
        if key in seen:
            issues.append(
                InputQualityIssue(
                    severity="ERROR",
                    code=code,
                    message=f"Duplicate key detected for fields {list(key_fields)}: {key}",
                    file=str(data.path),
                    row_number=row_index,
                    field="|".join(key_fields),
                    value="|".join(key),
                )
            )
        else:
            seen[key] = row_index
    return issues


def validate_expense_budget_line_coverage(expenses: CsvData, budget_lines: CsvData) -> List[InputQualityIssue]:
    if not expenses.exists or not budget_lines.exists:
        return []
    if "budget_line_id" not in expenses.fieldnames or "budget_line_id" not in budget_lines.fieldnames:
        return []

    known_budget_lines = {normalize_key_value(row.get("budget_line_id", "")) for row in budget_lines.rows if row.get("budget_line_id", "")}
    issues: List[InputQualityIssue] = []

    for row_index, row in enumerate(expenses.rows, start=2):
        budget_line_id = normalize_key_value(row.get("budget_line_id", ""))
        if budget_line_id == "":
            continue
        if budget_line_id not in known_budget_lines:
            issues.append(
                InputQualityIssue(
                    severity="ERROR",
                    code="UNKNOWN_BUDGET_LINE_REFERENCE",
                    message=f"Expense references budget_line_id without budget line definition: {budget_line_id}",
                    file=str(expenses.path),
                    row_number=row_index,
                    field="budget_line_id",
                    value=budget_line_id,
                )
            )
    return issues


def validate_expense_supplier_coverage(expenses: CsvData, suppliers: CsvData) -> List[InputQualityIssue]:
    if not expenses.exists or not suppliers.exists:
        return []
    if "supplier_id" not in expenses.fieldnames or "supplier_id" not in suppliers.fieldnames:
        return []

    known_suppliers = {normalize_key_value(row.get("supplier_id", "")) for row in suppliers.rows if row.get("supplier_id", "")}
    issues: List[InputQualityIssue] = []

    for row_index, row in enumerate(expenses.rows, start=2):
        supplier_id = normalize_key_value(row.get("supplier_id", ""))
        if supplier_id == "":
            continue
        if supplier_id not in known_suppliers:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="UNKNOWN_SUPPLIER_REFERENCE",
                    message=f"Expense references supplier_id without supplier profile: {supplier_id}",
                    file=str(expenses.path),
                    row_number=row_index,
                    field="supplier_id",
                    value=supplier_id,
                )
            )
    return issues


def validate_expense_budget_line_currency(expenses: CsvData, budget_lines: CsvData) -> List[InputQualityIssue]:
    if not expenses.exists or not budget_lines.exists:
        return []
    required_expense_fields = {"budget_line_id", "currency"}
    required_budget_fields = {"budget_line_id", "currency"}
    if not required_expense_fields.issubset(set(expenses.fieldnames)):
        return []
    if not required_budget_fields.issubset(set(budget_lines.fieldnames)):
        return []

    budget_currency = {
        normalize_key_value(row.get("budget_line_id", "")): normalize_key_value(row.get("currency", "")).upper()
        for row in budget_lines.rows
        if row.get("budget_line_id", "")
    }

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(expenses.rows, start=2):
        budget_line_id = normalize_key_value(row.get("budget_line_id", ""))
        expense_currency = normalize_key_value(row.get("currency", "")).upper()
        expected_currency = budget_currency.get(budget_line_id)
        if not expected_currency or not expense_currency:
            continue
        if expense_currency != expected_currency:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="EXPENSE_BUDGET_LINE_CURRENCY_MISMATCH",
                    message=f"Expense currency {expense_currency} differs from budget line currency {expected_currency}.",
                    file=str(expenses.path),
                    row_number=row_index,
                    field="currency",
                    value=expense_currency,
                )
            )
    return issues


def validate_expense_reporting_period(expenses: CsvData, budget_lines: CsvData) -> List[InputQualityIssue]:
    if not expenses.exists or not budget_lines.exists:
        return []
    required_expense_fields = {"budget_line_id", "reporting_period"}
    required_budget_fields = {"budget_line_id", "reporting_period"}
    if not required_expense_fields.issubset(set(expenses.fieldnames)):
        return []
    if not required_budget_fields.issubset(set(budget_lines.fieldnames)):
        return []

    budget_period = {
        normalize_key_value(row.get("budget_line_id", "")): normalize_key_value(row.get("reporting_period", ""))
        for row in budget_lines.rows
        if row.get("budget_line_id", "")
    }

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(expenses.rows, start=2):
        budget_line_id = normalize_key_value(row.get("budget_line_id", ""))
        expense_period = normalize_key_value(row.get("reporting_period", ""))
        expected_period = budget_period.get(budget_line_id)
        if not expected_period or not expense_period:
            continue
        if expense_period != expected_period:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="EXPENSE_REPORTING_PERIOD_MISMATCH",
                    message=f"Expense reporting period {expense_period} differs from budget line period {expected_period}.",
                    file=str(expenses.path),
                    row_number=row_index,
                    field="reporting_period",
                    value=expense_period,
                )
            )
    return issues


def validate_reporting_rule_scope(rules: CsvData, budget_lines: CsvData, expenses: CsvData) -> List[InputQualityIssue]:
    if not rules.exists:
        return []
    required_fields = {"grant_id", "project_id", "reporting_period"}
    if not required_fields.issubset(set(rules.fieldnames)):
        return []

    known_scopes = set()
    for data in (budget_lines, expenses):
        if not data.exists or not required_fields.issubset(set(data.fieldnames)):
            continue
        for row in data.rows:
            known_scopes.add(
                (
                    normalize_key_value(row.get("grant_id", "")),
                    normalize_key_value(row.get("project_id", "")),
                    normalize_key_value(row.get("reporting_period", "")),
                )
            )

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(rules.rows, start=2):
        scope = (
            normalize_key_value(row.get("grant_id", "")),
            normalize_key_value(row.get("project_id", "")),
            normalize_key_value(row.get("reporting_period", "")),
        )
        if any(value == "" for value in scope):
            continue
        if known_scopes and scope not in known_scopes:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="REPORTING_RULE_SCOPE_NOT_REFERENCED",
                    message=f"Reporting rule scope is not referenced by current expenses or budget lines: {scope}",
                    file=str(rules.path),
                    row_number=row_index,
                    field="grant_id|project_id|reporting_period",
                    value="|".join(scope),
                )
            )
    return issues


def build_report_summary(csv_data: Mapping[str, CsvData], issues: List[InputQualityIssue]) -> Dict[str, Any]:
    error_count = count_issues_by_severity(issues, "ERROR")
    warning_count = count_issues_by_severity(issues, "WARNING")
    info_count = count_issues_by_severity(issues, "INFO")

    return {
        "file_count": len(csv_data),
        "existing_file_count": sum(1 for data in csv_data.values() if data.exists),
        "grant_expense_count": len(csv_data["grant_expenses"].rows),
        "budget_line_count": len(csv_data["grant_budget_lines"].rows),
        "reporting_rule_count": len(csv_data["grant_reporting_rules"].rows),
        "supplier_profile_count": len(csv_data["grant_supplier_profiles"].rows),
        "issue_count": len(issues),
        "error_count": error_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "ready_for_analysis": error_count == 0,
    }


def calculate_status(issues: List[InputQualityIssue]) -> str:
    if any(issue.severity == "ERROR" for issue in issues):
        return "BLOCKED_BY_INPUT_ERRORS"
    if any(issue.severity == "WARNING" for issue in issues):
        return "READY_WITH_WARNINGS"
    return "READY_FOR_ANALYSIS"


def count_issues_by_severity(issues: Iterable[InputQualityIssue], severity: str) -> int:
    return sum(1 for issue in issues if issue.severity == severity)


def write_report(report: InputQualityReport, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(report.to_dict(), handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def parse_decimal_or_none(value: str) -> Optional[Decimal]:
    try:
        return Decimal(str(value).strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        return None


def normalize_key_value(value: str) -> str:
    return str(value or "").strip()


if __name__ == "__main__":
    main()
