r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_review_pipeline.py

Status:
Grant expense review evidence pipeline v0.1 for the LEO grant expense review demo.

Purpose:
Generate evidence-backed human review signals from local grant expense CSV input.

This pipeline reads:
- input/grant_expenses.csv
- input/grant_budget_lines.csv
- input/grant_reporting_rules.csv
- input/grant_supplier_profiles.csv
- output/grant_expense_input_quality_report.json

It writes:
- output/grant_expense_evidence_report.json

Rule Traceability Layer:
- Adds protocol-level rule_trace to generated findings.
- rule_trace is derived from signal_family.
- HIGH findings must have traceable review rules before validator hardening.
- All currently supported signal families receive rule_trace.

Normative Traceability Placeholder Layer:
- Adds placeholder-based normative_trace to generated findings.
- normative_trace is derived from signal_family.
- normative_trace shows reference domains and responsible review layers only.
- normative_trace references remain empty until manually verified sources are approved.
- normative_trace does not interpret law and does not issue legal, donor compliance,
  fraud, corruption, guilt, payment, sanction, or enforcement conclusions.

Boundary:
- Local read-only demo pipeline.
- Generates review signals only.
- No donor compliance verdicts.
- No fraud verdicts.
- No legal conclusions.
- No payment blocking.
- No supplier punishment.
- No production mutation.
- No canonical registry access or mutation.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.
- No unverified legal citations.

Run from the grant demo folder:
python grant_expense_review_pipeline.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
INPUT_QUALITY_REPORT_FILE = OUTPUT_DIR / "grant_expense_input_quality_report.json"
OUTPUT_FILE = OUTPUT_DIR / "grant_expense_evidence_report.json"

EXPENSES_FILE = INPUT_DIR / "grant_expenses.csv"
BUDGET_LINES_FILE = INPUT_DIR / "grant_budget_lines.csv"
REPORTING_RULES_FILE = INPUT_DIR / "grant_reporting_rules.csv"
SUPPLIER_PROFILES_FILE = INPUT_DIR / "grant_supplier_profiles.csv"

REVIEWABLE_INPUT_STATUSES = {"READY_FOR_ANALYSIS", "READY_WITH_WARNINGS"}
ROUND_VALUE_UNIT = Decimal("1000.00")
DEFAULT_DEADLINE_WINDOW_DAYS = 7
DEFAULT_LARGE_EXPENSE_THRESHOLD = Decimal("10000.00")
DEFAULT_ROUND_VALUE_REPEAT_THRESHOLD = 2

SEVERITY_RANK = {
    "INFO": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}

RULE_TRACE_BY_SIGNAL_FAMILY: Dict[str, Dict[str, str]] = {
    "budget_line_category_mismatch": {
        "source_rule_id": "GER-RULE-001",
        "source_rule_name": "Budget Line Category Mismatch Review Rule",
        "source_rule_file": "BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/BUDGET_LINE_CATEGORY_MISMATCH_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when its recorded expense category does not align with the referenced budget line category.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "budget_line_usage_review": {
        "source_rule_id": "GER-RULE-002",
        "source_rule_name": "Budget Line Usage Review Rule",
        "source_rule_file": "BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/BUDGET_LINE_USAGE_REVIEW_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant budget line requires human review when accumulated expense usage indicates material consumption of the allocated budget or a pattern requiring budget-owner confirmation.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "cash_reimbursement_documentation_review": {
        "source_rule_id": "GER-RULE-003",
        "source_rule_name": "Cash Reimbursement Documentation Review Rule",
        "source_rule_file": "CASH_REIMBURSEMENT_DOCUMENTATION_REVIEW_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/CASH_REIMBURSEMENT_DOCUMENTATION_REVIEW_PROTOCOL_v0.1.md",
        "human_readable_rule": "A cash reimbursement requires human review when supporting documentation, activity linkage, or reimbursement justification must be checked before audit packaging.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "deadline_sensitive_expense": {
        "source_rule_id": "GER-RULE-004",
        "source_rule_name": "Deadline-Sensitive Expense Review Rule",
        "source_rule_file": "DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/DEADLINE_SENSITIVE_EXPENSE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when its timing is close to a reporting, eligibility, or project-period boundary that may require additional explanation.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "large_expense_review": {
        "source_rule_id": "GER-RULE-005",
        "source_rule_name": "Large Expense Human Review Rule",
        "source_rule_file": "LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/LARGE_EXPENSE_REVIEW_PROTOCOL_v0.1.md",
        "human_readable_rule": "A large grant expense requires human review when the amount is material enough to warrant additional budget, activity, supplier, and documentation checks.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "missing_activity_reference": {
        "source_rule_id": "GER-RULE-006",
        "source_rule_name": "Missing Activity Reference Review Rule",
        "source_rule_file": "MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/MISSING_ACTIVITY_REFERENCE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when it lacks an activity reference needed to connect the cost to a project activity, output, or implementation record.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "missing_required_contract": {
        "source_rule_id": "GER-RULE-007",
        "source_rule_name": "Missing Required Contract Review Rule",
        "source_rule_file": "MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/MISSING_REQUIRED_CONTRACT_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when the transaction appears to require a contract or formal agreement but the required contract reference is missing or unavailable.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "repeated_round_value_expense": {
        "source_rule_id": "GER-RULE-008",
        "source_rule_name": "Repeated Round-Value Expense Review Rule",
        "source_rule_file": "REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/REPEATED_ROUND_VALUE_EXPENSE_PROTOCOL_v0.1.md",
        "human_readable_rule": "Grant expenses require human review when repeated round-value amounts create a pattern that may need explanation, supporting documentation, or budget-owner confirmation.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "unknown_supplier_reference": {
        "source_rule_id": "GER-RULE-009",
        "source_rule_name": "Unknown Supplier Reference Review Rule",
        "source_rule_file": "UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/UNKNOWN_SUPPLIER_REFERENCE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when the referenced supplier is not present in the known supplier profile register and must be checked before audit packaging.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
    "missing_required_invoice": {
        "source_rule_id": "GER-RULE-010",
        "source_rule_name": "Missing Required Invoice Review Rule",
        "source_rule_file": "MISSING_REQUIRED_INVOICE_PROTOCOL_v0.1.md",
        "protocol_reference": "protocols/grant_expense_review/MISSING_REQUIRED_INVOICE_PROTOCOL_v0.1.md",
        "human_readable_rule": "A grant expense requires human review when its budget line requires an invoice or equivalent accounting document, but the expense record has no invoice reference.",
        "verdict_boundary": "This rule creates a human review requirement only and does not create a donor compliance verdict, fraud finding, legal conclusion, payment block, supplier sanction, or autonomous enforcement action.",
    },
}

NORMATIVE_VERDICT_BOUNDARY = (
    "LEO identifies potentially relevant normative references and review requirements only. "
    "LEO does not issue legal conclusions, donor compliance conclusions, payment decisions, "
    "supplier sanctions, or enforcement conclusions."
)

NORMATIVE_TRACE_BY_SIGNAL_FAMILY: Dict[str, Dict[str, Any]] = {
    "budget_line_category_mismatch": {
        "normative_trace_id": "NT-GER-001",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR"],
        "reference_domain": ["GRANT_AGREEMENT", "INTERNAL_POLICY", "ACCOUNTING_RULE"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "project_manager", "management_board"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "budget_line_usage_review": {
        "normative_trace_id": "NT-GER-002",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR"],
        "reference_domain": ["GRANT_AGREEMENT", "DONOR_RULE", "ACCOUNTING_RULE", "INTERNAL_POLICY"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "project_manager", "management_board"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "cash_reimbursement_documentation_review": {
        "normative_trace_id": "NT-GER-003",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR", "PL"],
        "reference_domain": ["ACCOUNTING_RULE", "INTERNAL_POLICY", "DONOR_RULE"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "internal_audit", "management_board"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "deadline_sensitive_expense": {
        "normative_trace_id": "NT-GER-004",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR"],
        "reference_domain": ["GRANT_AGREEMENT", "DONOR_RULE", "INTERNAL_POLICY"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["project_manager", "accounting", "donor_contact"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "large_expense_review": {
        "normative_trace_id": "NT-GER-005",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR", "PL"],
        "reference_domain": ["INTERNAL_POLICY", "DONOR_RULE", "PROCUREMENT_RULE", "ACCOUNTING_RULE"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "management_board", "internal_audit"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "missing_activity_reference": {
        "normative_trace_id": "NT-GER-006",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR"],
        "reference_domain": ["GRANT_AGREEMENT", "DONOR_RULE", "INTERNAL_POLICY"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["project_manager", "accounting"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "missing_required_contract": {
        "normative_trace_id": "NT-GER-007",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR", "PL", "CONTRACTUAL"],
        "reference_domain": ["CONTRACT", "INTERNAL_POLICY", "PROCUREMENT_RULE", "DONOR_RULE", "ACCOUNTING_RULE"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "management_board", "legal_counsel"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "repeated_round_value_expense": {
        "normative_trace_id": "NT-GER-008",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR"],
        "reference_domain": ["INTERNAL_POLICY", "DONOR_RULE", "ACCOUNTING_RULE", "PROCUREMENT_RULE"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "internal_audit", "management_board"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "unknown_supplier_reference": {
        "normative_trace_id": "NT-GER-009",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR", "CONTRACTUAL"],
        "reference_domain": ["INTERNAL_POLICY", "DONOR_RULE", "CONTRACT", "PROCUREMENT_RULE"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["project_manager", "accounting", "management_board"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
    "missing_required_invoice": {
        "normative_trace_id": "NT-GER-010",
        "trace_status": "REFERENCE_MAPPING_PENDING",
        "jurisdiction": ["INTERNAL", "DONOR", "PL"],
        "reference_domain": ["ACCOUNTING_RULE", "DONOR_RULE", "INTERNAL_POLICY"],
        "references": [],
        "reference_confidence": "REFERENCE_NEEDS_VERIFICATION",
        "legal_interpretation_status": "HUMAN_INTERPRETATION_REQUIRED",
        "institutional_review_required": True,
        "responsible_review_layer": ["accounting", "internal_audit", "management_board"],
        "verdict_boundary": NORMATIVE_VERDICT_BOUNDARY,
    },
}


@dataclass(frozen=True)
class EvidenceFinding:
    id: str
    title: str
    severity: str
    signal_family: str
    expense_id: str
    supplier_id: str
    supplier_name: str
    budget_line_id: str
    amount: str
    currency: str
    detected_signal: str
    why_it_matters: str
    reviewer_question: str
    next_action: str
    evidence: List[str]
    rule_trace: Optional[Dict[str, str]] = None
    normative_trace: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "title": self.title,
            "severity": self.severity,
            "signal_family": self.signal_family,
            "expense_id": self.expense_id,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
            "subject": self.supplier_name or self.supplier_id or self.expense_id,
            "budget_line_id": self.budget_line_id,
            "amount": self.amount,
            "currency": self.currency,
            "detected_signal": self.detected_signal,
            "why_it_matters": self.why_it_matters,
            "reviewer_question": self.reviewer_question,
            "next_action": self.next_action,
            "evidence": list(self.evidence),
            "metadata": dict(self.metadata),
        }
        if self.rule_trace is not None:
            payload["rule_trace"] = dict(self.rule_trace)
        if self.normative_trace is not None:
            payload["normative_trace"] = deep_copy_json_object(self.normative_trace)
        return payload


@dataclass(frozen=True)
class CsvData:
    path: Path
    rows: List[Dict[str, str]]


@dataclass(frozen=True)
class RuleConfig:
    period_end_date: Optional[date]
    deadline_window_days: int
    large_expense_threshold: Decimal
    round_value_repeat_threshold: int
    contract_required_categories: Set[str]
    forbidden_verdict_language: Set[str]


def main() -> None:
    report = generate_grant_expense_evidence_report()
    print(json.dumps({"status": "OK", "output": str(OUTPUT_FILE), "summary": report["summary"]}, indent=2))


def generate_grant_expense_evidence_report(
    input_dir: Path = INPUT_DIR,
    output_file: Path = OUTPUT_FILE,
    input_quality_report_file: Path = INPUT_QUALITY_REPORT_FILE,
) -> Dict[str, Any]:
    input_quality = read_input_quality_report(input_quality_report_file)
    validate_input_quality_allows_pipeline(input_quality)

    expenses = read_csv(input_dir / "grant_expenses.csv").rows
    budget_lines = read_csv(input_dir / "grant_budget_lines.csv").rows
    rules = read_csv(input_dir / "grant_reporting_rules.csv").rows
    suppliers = read_csv(input_dir / "grant_supplier_profiles.csv").rows

    budget_by_id = {row["budget_line_id"]: row for row in budget_lines}
    supplier_by_id = {row["supplier_id"]: row for row in suppliers}
    rule_config = build_rule_config(rules)

    findings: List[EvidenceFinding] = []
    evidence_counter = 1

    def add_finding(finding: EvidenceFinding) -> None:
        findings.append(finding)

    def next_evidence_id() -> str:
        nonlocal evidence_counter
        evidence_id = f"GEV-{evidence_counter:03d}"
        evidence_counter += 1
        return evidence_id

    round_value_groups = build_round_value_groups(expenses)
    budget_usage = build_budget_usage(expenses)

    for expense in expenses:
        budget_line = budget_by_id.get(expense.get("budget_line_id", ""))
        supplier = supplier_by_id.get(expense.get("supplier_id", ""))

        unknown_supplier = build_unknown_supplier_finding(next_evidence_id, expense, supplier)
        if unknown_supplier:
            add_finding(unknown_supplier)

        category_mismatch = build_category_mismatch_finding(next_evidence_id, expense, budget_line)
        if category_mismatch:
            add_finding(category_mismatch)

        missing_invoice = build_missing_invoice_finding(next_evidence_id, expense, budget_line)
        if missing_invoice:
            add_finding(missing_invoice)

        missing_contract = build_missing_contract_finding(next_evidence_id, expense, budget_line, rule_config)
        if missing_contract:
            add_finding(missing_contract)

        missing_activity = build_missing_activity_reference_finding(next_evidence_id, expense, budget_line)
        if missing_activity:
            add_finding(missing_activity)

        cash_review = build_cash_reimbursement_finding(next_evidence_id, expense, budget_line)
        if cash_review:
            add_finding(cash_review)

        deadline_review = build_deadline_sensitive_finding(next_evidence_id, expense, budget_line, rule_config)
        if deadline_review:
            add_finding(deadline_review)

        large_expense = build_large_expense_finding(next_evidence_id, expense, rule_config)
        if large_expense:
            add_finding(large_expense)

    for group_key, group_rows in sorted(round_value_groups.items()):
        if len(group_rows) >= rule_config.round_value_repeat_threshold:
            add_finding(build_repeated_round_value_finding(next_evidence_id(), group_key, group_rows))

    for budget_line_id, usage in sorted(budget_usage.items()):
        budget_line = budget_by_id.get(budget_line_id)
        if not budget_line:
            continue
        finding = build_budget_usage_finding(next_evidence_id, budget_line, usage)
        if finding:
            add_finding(finding)

    finding_dicts = [finding.to_dict() for finding in findings]
    evidence_objects = build_evidence_objects(finding_dicts)
    summary = build_summary(finding_dicts, evidence_objects, expenses, suppliers, input_quality)

    report = {
        "report_id": "LOCAL_GRANT_EXPENSE_REVIEW_REPORT",
        "report_type": "LEO_GRANT_EXPENSE_REVIEW_EVIDENCE_REPORT",
        "report_version": "v0.1",
        "source_name": "grant_expense_review_pipeline.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dashboard_mode": "LOCAL_GRANT_EXPENSE_REVIEW",
        "input_quality_summary": input_quality.get("summary", {}),
        "summary": summary,
        "findings": finding_dicts,
        "evidence_objects": evidence_objects,
        "signal_families": count_by_field(finding_dicts, "signal_family"),
        "supplier_summary": build_supplier_summary(finding_dicts),
        "zero_autonomy_boundary": build_zero_autonomy_boundary(),
        "interpretation_boundary": {
            "fraud_verdict_issued": False,
            "legal_conclusion_issued": False,
            "donor_compliance_conclusion_issued": False,
            "payment_block_performed": False,
            "supplier_punishment_performed": False,
            "human_review_required": True,
            "statement": "This report contains evidence-backed review signals only. It does not issue fraud, legal, donor compliance, payment, or enforcement conclusions.",
        },
    }

    assert_no_forbidden_verdict_language(report, rule_config.forbidden_verdict_language)
    write_json(report, output_file)
    return report


def read_csv(path: Path) -> CsvData:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [{key.strip(): (value or "").strip() for key, value in row.items()} for row in reader]
    return CsvData(path=path, rows=rows)


def read_input_quality_report(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Input quality report does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_input_quality_allows_pipeline(input_quality: Mapping[str, Any]) -> None:
    status = str(input_quality.get("status", ""))
    summary = input_quality.get("summary", {}) if isinstance(input_quality.get("summary", {}), dict) else {}
    if status not in REVIEWABLE_INPUT_STATUSES:
        raise ValueError(f"Input quality status does not allow review pipeline: {status}")
    if summary.get("ready_for_analysis") is not True:
        raise ValueError("Input quality report does not mark input as ready_for_analysis.")
    if int(summary.get("error_count", 0)) != 0:
        raise ValueError("Input quality report contains blocking errors.")


def build_rule_config(rules: Sequence[Mapping[str, str]]) -> RuleConfig:
    period_end_date: Optional[date] = None
    deadline_window_days = DEFAULT_DEADLINE_WINDOW_DAYS
    large_expense_threshold = DEFAULT_LARGE_EXPENSE_THRESHOLD
    round_value_repeat_threshold = DEFAULT_ROUND_VALUE_REPEAT_THRESHOLD
    contract_required_categories: Set[str] = set()
    forbidden_verdict_language: Set[str] = {"fraud", "corruption", "illegal", "guilty", "punished", "blocked"}

    for rule in rules:
        parameter = normalize_token(rule.get("parameter", ""))
        value = rule.get("value", "").strip()
        if parameter == "period_end_date":
            period_end_date = parse_date_or_none(value)
        elif parameter == "days_before_period_end":
            parsed_days = parse_int_or_none(value)
            if parsed_days is not None:
                deadline_window_days = parsed_days
        elif parameter == "large_expense_amount_threshold":
            parsed_amount = parse_decimal_or_none(value)
            if parsed_amount is not None:
                large_expense_threshold = parsed_amount
        elif parameter == "round_value_repeat_threshold":
            parsed_threshold = parse_int_or_none(value)
            if parsed_threshold is not None:
                round_value_repeat_threshold = parsed_threshold
        elif parameter == "contract_required_categories":
            contract_required_categories = split_semicolon_tokens(value)
        elif parameter == "forbidden_verdict_language":
            forbidden_verdict_language = split_semicolon_tokens(value)

    return RuleConfig(
        period_end_date=period_end_date,
        deadline_window_days=deadline_window_days,
        large_expense_threshold=large_expense_threshold,
        round_value_repeat_threshold=round_value_repeat_threshold,
        contract_required_categories=contract_required_categories,
        forbidden_verdict_language=forbidden_verdict_language,
    )


def build_rule_trace(signal_family: str) -> Optional[Dict[str, str]]:
    rule_trace = RULE_TRACE_BY_SIGNAL_FAMILY.get(signal_family)
    if rule_trace is None:
        return None
    return dict(rule_trace)


def build_normative_trace(signal_family: str) -> Optional[Dict[str, Any]]:
    normative_trace = NORMATIVE_TRACE_BY_SIGNAL_FAMILY.get(signal_family)
    if normative_trace is None:
        return None
    return deep_copy_json_object(normative_trace)


def build_unknown_supplier_finding(next_id, expense: Mapping[str, str], supplier: Optional[Mapping[str, str]]) -> Optional[EvidenceFinding]:
    if supplier is not None:
        return None
    supplier_id = expense.get("supplier_id", "")
    return make_finding(
        evidence_id=next_id(),
        title="Unknown supplier reference",
        severity="MEDIUM",
        signal_family="unknown_supplier_reference",
        expense=expense,
        detected_signal=f"Expense {expense.get('expense_id')} references supplier_id {supplier_id}, but no supplier profile exists in the grant review dataset.",
        why_it_matters="The expense supplier is not present in the supplier reference file. The reviewer should verify identity, role, and suitability before accepting the expense trail.",
        reviewer_question="Does this supplier have verified identity, role, and documentation for the grant-funded activity?",
        next_action="Request supplier profile or supporting identity documentation before accepting this expense.",
        metadata={"missing_supplier_id": supplier_id},
    )


def build_category_mismatch_finding(next_id, expense: Mapping[str, str], budget_line: Optional[Mapping[str, str]]) -> Optional[EvidenceFinding]:
    if budget_line is None:
        return None
    expense_category = normalize_token(expense.get("expense_category", ""))
    allowed_categories = split_semicolon_tokens(budget_line.get("allowed_expense_categories", ""))
    if expense_category in allowed_categories:
        return None
    return make_finding(
        evidence_id=next_id(),
        title="Budget line category mismatch",
        severity="HIGH",
        signal_family="budget_line_category_mismatch",
        expense=expense,
        detected_signal=(
            f"Expense category '{expense.get('expense_category')}' is not listed as allowed under budget line "
            f"{budget_line.get('budget_line_id')} ({budget_line.get('budget_line_name')})."
        ),
        why_it_matters="The expense category does not match the allowed categories for the selected budget line. This may be explainable, but it requires budget and donor reporting review.",
        reviewer_question="Is this expense category allowed under the selected budget line, or should the expense be reclassified or justified?",
        next_action="Escalate for human review of budget line mapping before accepting the expense.",
        metadata={
            "allowed_expense_categories": sorted(allowed_categories),
            "expense_category": expense.get("expense_category", ""),
        },
    )


def build_missing_invoice_finding(next_id, expense: Mapping[str, str], budget_line: Optional[Mapping[str, str]]) -> Optional[EvidenceFinding]:
    if budget_line is None:
        return None
    if not parse_bool(budget_line.get("requires_invoice", "false")):
        return None
    if expense.get("invoice_id", "").strip():
        return None
    return make_finding(
        evidence_id=next_id(),
        title="Missing required invoice",
        severity="HIGH",
        signal_family="missing_required_invoice",
        expense=expense,
        detected_signal=f"Expense {expense.get('expense_id')} has no invoice_id, but its budget line requires an invoice.",
        why_it_matters="A missing invoice weakens accounting traceability and donor reporting evidence.",
        reviewer_question="Is a valid invoice or equivalent accounting document attached elsewhere?",
        next_action="Request invoice or equivalent accounting evidence before accepting the expense.",
        metadata={"requires_invoice": True},
    )


def build_missing_contract_finding(next_id, expense: Mapping[str, str], budget_line: Optional[Mapping[str, str]], rule_config: RuleConfig) -> Optional[EvidenceFinding]:
    category = normalize_token(expense.get("expense_category", ""))
    budget_requires_contract = budget_line is not None and parse_bool(budget_line.get("requires_contract", "false"))
    rule_requires_contract = category in rule_config.contract_required_categories
    if not budget_requires_contract and not rule_requires_contract:
        return None
    if expense.get("contract_id", "").strip():
        return None
    return make_finding(
        evidence_id=next_id(),
        title="Missing required contract",
        severity="HIGH",
        signal_family="missing_required_contract",
        expense=expense,
        detected_signal=f"Expense {expense.get('expense_id')} has no contract_id, but contract evidence is expected for category '{expense.get('expense_category')}'.",
        why_it_matters="Contracted services or travel-related expenses require authorization evidence to support grant reporting traceability.",
        reviewer_question="Is there a contract or equivalent authorization for this expense?",
        next_action="Request contract or equivalent authorization evidence before accepting the expense.",
        metadata={
            "budget_line_requires_contract": budget_requires_contract,
            "rule_requires_contract": rule_requires_contract,
            "expense_category": expense.get("expense_category", ""),
        },
    )


def build_missing_activity_reference_finding(next_id, expense: Mapping[str, str], budget_line: Optional[Mapping[str, str]]) -> Optional[EvidenceFinding]:
    budget_requires_activity = budget_line is not None and parse_bool(budget_line.get("requires_activity_reference", "false"))
    if not budget_requires_activity:
        return None
    if expense.get("activity_reference", "").strip():
        return None
    return make_finding(
        evidence_id=next_id(),
        title="Missing activity reference",
        severity="MEDIUM",
        signal_family="missing_activity_reference",
        expense=expense,
        detected_signal=f"Expense {expense.get('expense_id')} has no activity_reference, but its budget line requires a link to an activity or output.",
        why_it_matters="A missing activity reference weakens the connection between the expense and the reported grant activity.",
        reviewer_question="Which project activity, output, or deliverable does this expense support?",
        next_action="Request activity or output reference before accepting the expense for reporting.",
        metadata={"requires_activity_reference": True},
    )


def build_cash_reimbursement_finding(next_id, expense: Mapping[str, str], budget_line: Optional[Mapping[str, str]]) -> Optional[EvidenceFinding]:
    if normalize_token(expense.get("payment_method", "")) != "cash_reimbursement":
        return None
    budget_allows_cash = budget_line is not None and parse_bool(budget_line.get("allow_cash_reimbursement", "false"))
    document_status = normalize_token(expense.get("document_status", ""))
    if budget_allows_cash and document_status == "complete":
        return None
    severity = "HIGH" if not budget_allows_cash else "MEDIUM"
    return make_finding(
        evidence_id=next_id(),
        title="Cash reimbursement documentation review",
        severity=severity,
        signal_family="cash_reimbursement_documentation_review",
        expense=expense,
        detected_signal=(
            f"Expense {expense.get('expense_id')} uses cash reimbursement with document_status "
            f"'{expense.get('document_status')}'. Budget line cash permission: {budget_allows_cash}."
        ),
        why_it_matters="Cash reimbursement requires stronger documentation discipline because it is harder to trace than direct bank transfer.",
        reviewer_question="Is the reimbursement supported by complete participant, recipient, or payment documentation?",
        next_action="Review reimbursement documentation before accepting the expense.",
        metadata={"budget_allows_cash_reimbursement": budget_allows_cash, "document_status": expense.get("document_status", "")},
    )


def build_deadline_sensitive_finding(next_id, expense: Mapping[str, str], budget_line: Optional[Mapping[str, str]], rule_config: RuleConfig) -> Optional[EvidenceFinding]:
    if rule_config.period_end_date is None:
        return None
    expense_date = parse_date_or_none(expense.get("date", ""))
    if expense_date is None:
        return None
    days_before_close = (rule_config.period_end_date - expense_date).days
    if days_before_close < 0 or days_before_close > rule_config.deadline_window_days:
        return None
    budget_deadline_sensitive = budget_line is not None and parse_bool(budget_line.get("deadline_sensitive", "false"))
    severity = "HIGH" if budget_deadline_sensitive else "MEDIUM"
    return make_finding(
        evidence_id=next_id(),
        title="Deadline-sensitive expense",
        severity=severity,
        signal_family="deadline_sensitive_expense",
        expense=expense,
        detected_signal=(
            f"Expense {expense.get('expense_id')} was recorded {days_before_close} day(s) before reporting period close "
            f"({rule_config.period_end_date.isoformat()})."
        ),
        why_it_matters="Expenses recorded close to the reporting deadline may be legitimate, but they require complete documentation and timing justification.",
        reviewer_question="Was this expense submitted near the reporting deadline for a documented operational reason?",
        next_action="Review timing, documentation completeness, and reporting justification.",
        metadata={
            "period_end_date": rule_config.period_end_date.isoformat(),
            "days_before_close": days_before_close,
            "deadline_window_days": rule_config.deadline_window_days,
            "budget_line_deadline_sensitive": budget_deadline_sensitive,
        },
    )


def build_large_expense_finding(next_id, expense: Mapping[str, str], rule_config: RuleConfig) -> Optional[EvidenceFinding]:
    amount = parse_decimal_or_none(expense.get("amount", ""))
    if amount is None or amount < rule_config.large_expense_threshold:
        return None
    return make_finding(
        evidence_id=next_id(),
        title="Large expense review",
        severity="HIGH",
        signal_family="large_expense_review",
        expense=expense,
        detected_signal=(
            f"Expense {expense.get('expense_id')} amount {format_decimal(amount)} {expense.get('currency')} meets or exceeds "
            f"the large expense threshold {format_decimal(rule_config.large_expense_threshold)}."
        ),
        why_it_matters="Large expenses require stronger documentation, budget justification, and reviewer traceability.",
        reviewer_question="Is this large expense supported by contract, invoice, activity evidence, and budget justification?",
        next_action="Review supporting documents before accepting the expense.",
        metadata={"large_expense_threshold": format_decimal(rule_config.large_expense_threshold)},
    )


def build_round_value_groups(expenses: Sequence[Mapping[str, str]]) -> Dict[Tuple[str, str, str], List[Mapping[str, str]]]:
    groups: Dict[Tuple[str, str, str], List[Mapping[str, str]]] = defaultdict(list)
    for expense in expenses:
        amount = parse_decimal_or_none(expense.get("amount", ""))
        if amount is None or amount <= 0:
            continue
        if amount % ROUND_VALUE_UNIT != 0:
            continue
        key = (
            expense.get("supplier_id", ""),
            expense.get("expense_category", ""),
            expense.get("reporting_period", ""),
        )
        groups[key].append(expense)
    return groups


def build_repeated_round_value_finding(evidence_id: str, group_key: Tuple[str, str, str], group_rows: Sequence[Mapping[str, str]]) -> EvidenceFinding:
    supplier_id, expense_category, reporting_period = group_key
    total_amount = sum((parse_decimal_or_none(row.get("amount", "")) or Decimal("0")) for row in group_rows)
    evidence_expense_ids = [row.get("expense_id", "") for row in group_rows]
    first_row = group_rows[0]
    return make_finding(
        evidence_id=evidence_id,
        title="Repeated round-value expenses",
        severity="MEDIUM",
        signal_family="repeated_round_value_expense",
        expense=first_row,
        detected_signal=(
            f"{len(group_rows)} round-value expenses were detected for supplier {supplier_id}, category "
            f"'{expense_category}', period {reporting_period}. Total amount: {format_decimal(total_amount)} {first_row.get('currency')}"
        ),
        why_it_matters="Repeated round-value expenses may be legitimate, but they can also indicate weak cost breakdown or repeated advances requiring documentation review.",
        reviewer_question="Are repeated round-value expenses supported by real cost breakdowns and activity evidence?",
        next_action="Review the grouped expenses together instead of treating them as isolated rows.",
        metadata={
            "group_supplier_id": supplier_id,
            "group_expense_category": expense_category,
            "group_reporting_period": reporting_period,
            "group_expense_ids": evidence_expense_ids,
            "group_total_amount": format_decimal(total_amount),
        },
    )


def build_budget_usage(expenses: Sequence[Mapping[str, str]]) -> Dict[str, Decimal]:
    usage: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for expense in expenses:
        budget_line_id = expense.get("budget_line_id", "")
        amount = parse_decimal_or_none(expense.get("amount", ""))
        if budget_line_id and amount is not None:
            usage[budget_line_id] += amount
    return usage


def build_budget_usage_finding(next_id, budget_line: Mapping[str, str], used_amount: Decimal) -> Optional[EvidenceFinding]:
    approved_amount = parse_decimal_or_none(budget_line.get("approved_amount", ""))
    if approved_amount is None or approved_amount <= 0:
        return None
    ratio = used_amount / approved_amount
    if ratio < Decimal("0.85"):
        return None
    severity = "HIGH" if ratio > Decimal("1.00") else "MEDIUM"
    synthetic_expense = {
        "expense_id": f"BUDGET-USAGE-{budget_line.get('budget_line_id')}",
        "supplier_id": "MULTIPLE_OR_NOT_APPLICABLE",
        "supplier_name": "Budget line aggregate",
        "budget_line_id": budget_line.get("budget_line_id", ""),
        "amount": format_decimal(used_amount),
        "currency": budget_line.get("currency", ""),
    }
    return make_finding(
        evidence_id=next_id(),
        title="Budget line usage review",
        severity=severity,
        signal_family="budget_line_usage_review",
        expense=synthetic_expense,
        detected_signal=(
            f"Budget line {budget_line.get('budget_line_id')} has used {format_decimal(used_amount)} "
            f"of approved {format_decimal(approved_amount)} {budget_line.get('currency')} ({format_decimal(ratio * Decimal('100'))}%)."
        ),
        why_it_matters="A budget line near or above its approved amount requires spending justification and reporting review.",
        reviewer_question="Is the budget line approaching or exceeding its approved amount for documented reasons?",
        next_action="Review aggregate budget usage before accepting additional expenses under this budget line.",
        metadata={
            "budget_line_id": budget_line.get("budget_line_id", ""),
            "approved_amount": format_decimal(approved_amount),
            "used_amount": format_decimal(used_amount),
            "usage_ratio": str(ratio),
        },
    )


def make_finding(
    evidence_id: str,
    title: str,
    severity: str,
    signal_family: str,
    expense: Mapping[str, str],
    detected_signal: str,
    why_it_matters: str,
    reviewer_question: str,
    next_action: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> EvidenceFinding:
    return EvidenceFinding(
        id=evidence_id,
        title=title,
        severity=severity,
        signal_family=signal_family,
        expense_id=expense.get("expense_id", ""),
        supplier_id=expense.get("supplier_id", ""),
        supplier_name=expense.get("supplier_name", ""),
        budget_line_id=expense.get("budget_line_id", ""),
        amount=expense.get("amount", ""),
        currency=expense.get("currency", ""),
        detected_signal=detected_signal,
        why_it_matters=why_it_matters,
        reviewer_question=reviewer_question,
        next_action=next_action,
        evidence=[evidence_id],
        rule_trace=build_rule_trace(signal_family),
        normative_trace=build_normative_trace(signal_family),
        metadata=metadata or {},
    )


def build_evidence_objects(findings: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "evidence_id": finding["id"],
            "finding_id": finding["id"],
            "title": finding["title"],
            "severity": finding["severity"],
            "signal_family": finding["signal_family"],
            "expense_id": finding["expense_id"],
            "supplier_id": finding["supplier_id"],
            "supplier_name": finding["supplier_name"],
            "budget_line_id": finding["budget_line_id"],
            "reason": finding["detected_signal"],
            "reviewer_question": finding["reviewer_question"],
        }
        for finding in findings
    ]


def build_summary(findings: Sequence[Mapping[str, Any]], evidence_objects: Sequence[Mapping[str, Any]], expenses: Sequence[Mapping[str, str]], suppliers: Sequence[Mapping[str, str]], input_quality: Mapping[str, Any]) -> Dict[str, Any]:
    high_or_critical_count = sum(1 for finding in findings if finding.get("severity") in {"HIGH", "CRITICAL"})
    supplier_ids = {expense.get("supplier_id", "") for expense in expenses if expense.get("supplier_id", "")}
    return {
        "findings_count": len(findings),
        "evidence_count": len(evidence_objects),
        "grant_expense_count": len(expenses),
        "supplier_count": len(supplier_ids),
        "known_supplier_profile_count": len(suppliers),
        "high_or_critical_findings_count": high_or_critical_count,
        "reviewed_findings_count": 0,
        "input_quality_status": input_quality.get("status"),
        "input_quality_warning_count": input_quality.get("summary", {}).get("warning_count", 0),
        "input_quality_error_count": input_quality.get("summary", {}).get("error_count", 0),
        "signal_families": count_by_field(findings, "signal_family"),
        "severity_distribution": count_by_field(findings, "severity"),
        "autonomous_actions": 0,
    }


def build_supplier_summary(findings: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for finding in findings:
        grouped[finding.get("supplier_id", "UNKNOWN")].append(finding)

    summary = []
    for supplier_id, supplier_findings in grouped.items():
        supplier_name = supplier_findings[0].get("supplier_name", "")
        max_severity = max((finding.get("severity", "INFO") for finding in supplier_findings), key=lambda value: SEVERITY_RANK.get(value, 0))
        summary.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "finding_count": len(supplier_findings),
                "max_severity": max_severity,
                "evidence_references": [finding.get("id") for finding in supplier_findings],
            }
        )

    return sorted(summary, key=lambda item: (-SEVERITY_RANK.get(item["max_severity"], 0), -item["finding_count"], item["supplier_id"]))


def build_zero_autonomy_boundary() -> Dict[str, Any]:
    return {
        "autonomous_enforcement_actions": 0,
        "canonical_registry_opened": False,
        "canonical_registry_mutated": False,
        "production_records_mutated": False,
        "payment_block_performed": False,
        "supplier_punishment_performed": False,
        "donor_compliance_conclusion_issued": False,
        "fraud_verdict_issued": False,
        "legal_conclusion_issued": False,
        "signing_or_key_access_performed": False,
        "external_execution_performed": False,
        "pipeline_mode": "LOCAL_READ_ONLY_GRANT_EXPENSE_REVIEW_SIGNAL_GENERATION",
    }


def count_by_field(items: Sequence[Mapping[str, Any]], field_name: str) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for item in items:
        counts[str(item.get(field_name, "UNKNOWN"))] += 1
    return dict(sorted(counts.items()))


def assert_no_forbidden_verdict_language(report: Mapping[str, Any], forbidden_terms: Set[str]) -> None:
    serialized = json.dumps(report, ensure_ascii=False).lower()
    allowed_context_phrases = {
        "fraud_verdict_issued",
        "legal_conclusion_issued",
        "donor_compliance_conclusion_issued",
        "payment_block_performed",
        "supplier_punishment_performed",
        "forbidden_verdict_language",
        "does not issue fraud",
        "no fraud verdicts",
        "no fraud verdict",
        "no legal conclusions",
        "legal, donor compliance",
        "fraud, legal",
        "fraud finding",
        "fraud, payment",
        "not create a donor compliance verdict, fraud finding",
        "does not create a donor compliance verdict, fraud finding",
        "does not issue legal, donor compliance",
        "does not issue legal, donor compliance, fraud",
        "fraud, corruption, guilt",
    }
    sanitized = serialized
    for phrase in allowed_context_phrases:
        sanitized = sanitized.replace(phrase, "")
    for term in forbidden_terms:
        normalized = term.strip().lower()
        if normalized and normalized in sanitized:
            raise ValueError(f"Forbidden verdict language detected in generated report: {term}")


def write_json(payload: Mapping[str, Any], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def split_semicolon_tokens(value: str) -> Set[str]:
    return {normalize_token(part) for part in str(value or "").split(";") if normalize_token(part)}


def normalize_token(value: str) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def parse_bool(value: str) -> bool:
    return normalize_token(value) == "true"


def parse_decimal_or_none(value: str) -> Optional[Decimal]:
    try:
        return Decimal(str(value).strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        return None


def parse_int_or_none(value: str) -> Optional[int]:
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def parse_date_or_none(value: str) -> Optional[date]:
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        return None


def format_decimal(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


def deep_copy_json_object(payload: Dict[str, Any]) -> Dict[str, Any]:
    return json.loads(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
