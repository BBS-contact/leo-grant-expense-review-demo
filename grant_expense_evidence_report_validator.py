r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_evidence_report_validator.py

Status:
Grant expense evidence report validator v0.1 for the LEO grant expense review demo.

Purpose:
Validate the local grant expense evidence report before any dashboard, external
explanation, or human review package layer consumes it.

Validated report:
- output/grant_expense_evidence_report.json

Rule Traceability Layer:
- Validates rule_trace for HIGH and CRITICAL findings.
- Requires protocol-level traceability for high-risk human review signals.
- Preserves zero-autonomy and non-verdict boundaries.

Boundary:
- Local read-only validation.
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

Run from the grant demo folder:
python grant_expense_evidence_report_validator.py output\grant_expense_evidence_report.json
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_FILE = BASE_DIR / "output" / "grant_expense_evidence_report.json"

EXPECTED_REPORT_ID = "LOCAL_GRANT_EXPENSE_REVIEW_REPORT"
EXPECTED_REPORT_TYPE = "LEO_GRANT_EXPENSE_REVIEW_EVIDENCE_REPORT"
EXPECTED_REPORT_VERSION = "v0.1"
EXPECTED_DASHBOARD_MODE = "LOCAL_GRANT_EXPENSE_REVIEW"
ALLOWED_INPUT_QUALITY_STATUSES = {"READY_FOR_ANALYSIS", "READY_WITH_WARNINGS"}
ALLOWED_SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
TRACE_REQUIRED_SEVERITIES = {"HIGH", "CRITICAL"}
REQUIRED_RULE_TRACE_PROTOCOL_PREFIX = "protocols/grant_expense_review/"
REQUIRED_RULE_TRACE_ID_PREFIX = "GER-RULE-"

REQUIRED_TOP_LEVEL_FIELDS = {
    "report_id",
    "report_type",
    "report_version",
    "source_name",
    "generated_at",
    "dashboard_mode",
    "input_quality_summary",
    "summary",
    "findings",
    "evidence_objects",
    "signal_families",
    "supplier_summary",
    "zero_autonomy_boundary",
    "interpretation_boundary",
}

REQUIRED_SUMMARY_FIELDS = {
    "findings_count",
    "evidence_count",
    "grant_expense_count",
    "supplier_count",
    "known_supplier_profile_count",
    "high_or_critical_findings_count",
    "reviewed_findings_count",
    "input_quality_status",
    "input_quality_warning_count",
    "input_quality_error_count",
    "signal_families",
    "severity_distribution",
    "autonomous_actions",
}

REQUIRED_FINDING_FIELDS = {
    "id",
    "title",
    "severity",
    "signal_family",
    "expense_id",
    "supplier_id",
    "supplier_name",
    "subject",
    "budget_line_id",
    "amount",
    "currency",
    "detected_signal",
    "why_it_matters",
    "reviewer_question",
    "next_action",
    "evidence",
    "metadata",
}

REQUIRED_RULE_TRACE_FIELDS = {
    "source_rule_id",
    "source_rule_name",
    "source_rule_file",
    "protocol_reference",
    "human_readable_rule",
    "verdict_boundary",
}

REQUIRED_NORMATIVE_TRACE_FIELDS = {
    "normative_trace_id",
    "trace_status",
    "jurisdiction",
    "reference_domain",
    "references",
    "reference_confidence",
    "legal_interpretation_status",
    "institutional_review_required",
    "responsible_review_layer",
    "verdict_boundary",
}

REQUIRED_EVIDENCE_FIELDS = {
    "evidence_id",
    "finding_id",
    "title",
    "severity",
    "signal_family",
    "expense_id",
    "supplier_id",
    "supplier_name",
    "budget_line_id",
    "reason",
    "reviewer_question",
}

FORBIDDEN_FREE_TEXT_PHRASES = {
    "fraud occurred",
    "corruption occurred",
    "illegal expense",
    "supplier is guilty",
    "payment must be blocked",
    "supplier must be punished",
    "donor compliance approved",
    "legally compliant",
    "legally non-compliant",
}

RULE_TRACE_BOUNDARY_REQUIRED_PHRASES = {
    "human review requirement only",
    "does not create",
    "donor compliance verdict",
    "fraud finding",
    "legal conclusion",
    "payment block",
    "supplier sanction",
    "autonomous enforcement action",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    location: str
    severity: str = "ERROR"

    def to_dict(self) -> Dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "location": self.location,
        }


def main() -> None:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REPORT_FILE
    result = validate_grant_expense_evidence_report(report_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["is_valid"]:
        raise SystemExit(1)


def validate_grant_expense_evidence_report(report_path: Path | str = DEFAULT_REPORT_FILE) -> Dict[str, Any]:
    path = Path(report_path)
    issues: List[ValidationIssue] = []
    warnings: List[ValidationIssue] = []

    if not path.exists():
        issues.append(
            ValidationIssue(
                code="REPORT_FILE_MISSING",
                message=f"Report file does not exist: {path}",
                location="report_path",
            )
        )
        return build_result(False, path, {}, issues, warnings)

    try:
        with path.open("r", encoding="utf-8") as handle:
            report = json.load(handle)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                code="REPORT_JSON_INVALID",
                message=f"Report JSON is not parseable: {exc}",
                location="report_json",
            )
        )
        return build_result(False, path, {}, issues, warnings)

    if not isinstance(report, dict):
        issues.append(
            ValidationIssue(
                code="REPORT_ROOT_NOT_OBJECT",
                message="Report root must be a JSON object.",
                location="report",
            )
        )
        return build_result(False, path, {}, issues, warnings)

    issues.extend(validate_required_top_level_fields(report))
    issues.extend(validate_report_identity(report))
    issues.extend(validate_summary(report))
    issues.extend(validate_findings(report))
    issues.extend(validate_rule_trace(report))
    issues.extend(validate_evidence_objects(report))
    issues.extend(validate_count_consistency(report))
    issues.extend(validate_signal_family_consistency(report))
    issues.extend(validate_severity_distribution_consistency(report))
    issues.extend(validate_evidence_mapping(report))
    issues.extend(validate_supplier_summary(report))
    issues.extend(validate_zero_autonomy_boundary(report))
    issues.extend(validate_interpretation_boundary(report))
    issues.extend(validate_forbidden_free_text(report))
    issues.extend(validate_normative_trace(report))

    summary = build_summary(report) if not issues else build_partial_summary(report)
    return build_result(len(issues) == 0, path, summary, issues, warnings)


def validate_required_top_level_fields(report: Mapping[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    missing = REQUIRED_TOP_LEVEL_FIELDS - set(report.keys())
    for field_name in sorted(missing):
        issues.append(
            ValidationIssue(
                code="TOP_LEVEL_FIELD_MISSING",
                message=f"Required top-level field is missing: {field_name}",
                location=f"report.{field_name}",
            )
        )
    return issues


def validate_report_identity(report: Mapping[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    expected_values = {
        "report_id": EXPECTED_REPORT_ID,
        "report_type": EXPECTED_REPORT_TYPE,
        "report_version": EXPECTED_REPORT_VERSION,
        "dashboard_mode": EXPECTED_DASHBOARD_MODE,
    }
    for field_name, expected_value in expected_values.items():
        actual_value = report.get(field_name)
        if actual_value != expected_value:
            issues.append(
                ValidationIssue(
                    code="REPORT_IDENTITY_MISMATCH",
                    message=f"{field_name} must be {expected_value!r}, got {actual_value!r}.",
                    location=f"report.{field_name}",
                )
            )
    if not report.get("source_name"):
        issues.append(
            ValidationIssue(
                code="SOURCE_NAME_MISSING",
                message="source_name must be present.",
                location="report.source_name",
            )
        )
    if not report.get("generated_at"):
        issues.append(
            ValidationIssue(
                code="GENERATED_AT_MISSING",
                message="generated_at must be present.",
                location="report.generated_at",
            )
        )
    return issues


def validate_summary(report: Mapping[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    summary = report.get("summary")
    if not isinstance(summary, dict):
        return [ValidationIssue(code="SUMMARY_NOT_OBJECT", message="summary must be an object.", location="report.summary")]

    missing = REQUIRED_SUMMARY_FIELDS - set(summary.keys())
    for field_name in sorted(missing):
        issues.append(
            ValidationIssue(
                code="SUMMARY_FIELD_MISSING",
                message=f"Required summary field is missing: {field_name}",
                location=f"report.summary.{field_name}",
            )
        )

    input_quality_status = summary.get("input_quality_status")
    if input_quality_status not in ALLOWED_INPUT_QUALITY_STATUSES:
        issues.append(
            ValidationIssue(
                code="INPUT_QUALITY_STATUS_INVALID",
                message=f"input_quality_status must be one of {sorted(ALLOWED_INPUT_QUALITY_STATUSES)}, got {input_quality_status!r}.",
                location="report.summary.input_quality_status",
            )
        )

    if summary.get("input_quality_error_count") != 0:
        issues.append(
            ValidationIssue(
                code="INPUT_QUALITY_ERRORS_PRESENT",
                message="input_quality_error_count must be 0 for a valid evidence report.",
                location="report.summary.input_quality_error_count",
            )
        )

    if summary.get("autonomous_actions") != 0:
        issues.append(
            ValidationIssue(
                code="AUTONOMOUS_ACTIONS_NOT_ZERO",
                message="autonomous_actions must remain 0.",
                location="report.summary.autonomous_actions",
            )
        )

    return issues


def validate_findings(report: Mapping[str, Any]) -> List[ValidationIssue]:
    findings = report.get("findings")
    if not isinstance(findings, list):
        return [ValidationIssue(code="FINDINGS_NOT_LIST", message="findings must be a list.", location="report.findings")]

    issues: List[ValidationIssue] = []
    seen_ids: Set[str] = set()
    for index, finding in enumerate(findings):
        location = f"report.findings[{index}]"
        if not isinstance(finding, dict):
            issues.append(ValidationIssue(code="FINDING_NOT_OBJECT", message="Finding must be an object.", location=location))
            continue

        missing = REQUIRED_FINDING_FIELDS - set(finding.keys())
        for field_name in sorted(missing):
            issues.append(
                ValidationIssue(
                    code="FINDING_FIELD_MISSING",
                    message=f"Required finding field is missing: {field_name}",
                    location=f"{location}.{field_name}",
                )
            )

        finding_id = finding.get("id")
        if not finding_id:
            issues.append(ValidationIssue(code="FINDING_ID_EMPTY", message="Finding id must not be empty.", location=f"{location}.id"))
        elif finding_id in seen_ids:
            issues.append(ValidationIssue(code="FINDING_ID_DUPLICATE", message=f"Duplicate finding id: {finding_id}", location=f"{location}.id"))
        else:
            seen_ids.add(str(finding_id))

        severity = finding.get("severity")
        if severity not in ALLOWED_SEVERITIES:
            issues.append(
                ValidationIssue(
                    code="FINDING_SEVERITY_INVALID",
                    message=f"Finding severity is invalid: {severity!r}",
                    location=f"{location}.severity",
                )
            )

        evidence = finding.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            issues.append(
                ValidationIssue(
                    code="FINDING_EVIDENCE_INVALID",
                    message="Finding evidence must be a non-empty list.",
                    location=f"{location}.evidence",
                )
            )

        for required_text_field in ("title", "signal_family", "detected_signal", "why_it_matters", "reviewer_question", "next_action"):
            value = finding.get(required_text_field)
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    ValidationIssue(
                        code="FINDING_TEXT_FIELD_EMPTY",
                        message=f"Finding text field must not be empty: {required_text_field}",
                        location=f"{location}.{required_text_field}",
                    )
                )

    return issues


def validate_rule_trace(report: Mapping[str, Any]) -> List[ValidationIssue]:
    findings = report.get("findings")
    if not isinstance(findings, list):
        return []

    issues: List[ValidationIssue] = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            continue

        severity = finding.get("severity")
        location = f"report.findings[{index}].rule_trace"
        if severity not in TRACE_REQUIRED_SEVERITIES:
            continue

        rule_trace = finding.get("rule_trace")
        if rule_trace is None:
            issues.append(
                ValidationIssue(
                    code="HIGH_FINDING_RULE_TRACE_MISSING",
                    message="HIGH and CRITICAL findings must include rule_trace.",
                    location=location,
                )
            )
            continue

        if not isinstance(rule_trace, dict):
            issues.append(
                ValidationIssue(
                    code="RULE_TRACE_NOT_OBJECT",
                    message="rule_trace must be an object.",
                    location=location,
                )
            )
            continue

        missing = REQUIRED_RULE_TRACE_FIELDS - set(rule_trace.keys())
        for field_name in sorted(missing):
            issues.append(
                ValidationIssue(
                    code="RULE_TRACE_FIELD_MISSING",
                    message=f"Required rule_trace field is missing: {field_name}",
                    location=f"{location}.{field_name}",
                )
            )

        for field_name in sorted(REQUIRED_RULE_TRACE_FIELDS & set(rule_trace.keys())):
            value = rule_trace.get(field_name)
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    ValidationIssue(
                        code="RULE_TRACE_FIELD_EMPTY",
                        message=f"rule_trace field must be a non-empty string: {field_name}",
                        location=f"{location}.{field_name}",
                    )
                )

        source_rule_id = rule_trace.get("source_rule_id")
        if isinstance(source_rule_id, str) and not source_rule_id.startswith(REQUIRED_RULE_TRACE_ID_PREFIX):
            issues.append(
                ValidationIssue(
                    code="RULE_TRACE_SOURCE_RULE_ID_INVALID",
                    message=f"source_rule_id must start with {REQUIRED_RULE_TRACE_ID_PREFIX}.",
                    location=f"{location}.source_rule_id",
                )
            )

        source_rule_file = rule_trace.get("source_rule_file")
        if isinstance(source_rule_file, str) and not source_rule_file.endswith(".md"):
            issues.append(
                ValidationIssue(
                    code="RULE_TRACE_SOURCE_RULE_FILE_NOT_MARKDOWN",
                    message="source_rule_file must reference a Markdown .md protocol file.",
                    location=f"{location}.source_rule_file",
                )
            )

        protocol_reference = rule_trace.get("protocol_reference")
        if isinstance(protocol_reference, str):
            if not protocol_reference.startswith(REQUIRED_RULE_TRACE_PROTOCOL_PREFIX):
                issues.append(
                    ValidationIssue(
                        code="RULE_TRACE_PROTOCOL_REFERENCE_INVALID_PREFIX",
                        message=f"protocol_reference must start with {REQUIRED_RULE_TRACE_PROTOCOL_PREFIX}.",
                        location=f"{location}.protocol_reference",
                    )
                )
            if not protocol_reference.endswith(".md"):
                issues.append(
                    ValidationIssue(
                        code="RULE_TRACE_PROTOCOL_REFERENCE_NOT_MARKDOWN",
                        message="protocol_reference must reference a Markdown .md protocol file.",
                        location=f"{location}.protocol_reference",
                    )
                )

        verdict_boundary = rule_trace.get("verdict_boundary")
        if isinstance(verdict_boundary, str):
            boundary_text = verdict_boundary.lower()
            for phrase in sorted(RULE_TRACE_BOUNDARY_REQUIRED_PHRASES):
                if phrase not in boundary_text:
                    issues.append(
                        ValidationIssue(
                            code="RULE_TRACE_VERDICT_BOUNDARY_INCOMPLETE",
                            message=f"verdict_boundary must preserve zero-autonomy boundary phrase: {phrase}",
                            location=f"{location}.verdict_boundary",
                        )
                    )

    return issues

def validate_normative_trace(report: Mapping[str, Any]) -> List[ValidationIssue]:
    findings = report.get("findings")
    if not isinstance(findings, list):
        return []

    issues: List[ValidationIssue] = []

    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            continue

        location = f"report.findings[{index}].normative_trace"
        normative_trace = finding.get("normative_trace")

        if normative_trace is None:
            issues.append(
                ValidationIssue(
                    code="NORMATIVE_TRACE_MISSING",
                    message="All generated Grant Expense findings must include normative_trace.",
                    location=location,
                )
            )
            continue

        if not isinstance(normative_trace, dict):
            issues.append(
                ValidationIssue(
                    code="NORMATIVE_TRACE_NOT_OBJECT",
                    message="normative_trace must be an object.",
                    location=location,
                )
            )
            continue

        missing = REQUIRED_NORMATIVE_TRACE_FIELDS - set(normative_trace.keys())
        for field_name in sorted(missing):
            issues.append(
                ValidationIssue(
                    code="NORMATIVE_TRACE_FIELD_MISSING",
                    message=f"Required normative_trace field is missing: {field_name}",
                    location=f"{location}.{field_name}",
                )
            )

        for field_name in ("normative_trace_id", "trace_status", "reference_confidence", "legal_interpretation_status", "verdict_boundary"):
            value = normative_trace.get(field_name)
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    ValidationIssue(
                        code="NORMATIVE_TRACE_FIELD_EMPTY",
                        message=f"normative_trace field must be a non-empty string: {field_name}",
                        location=f"{location}.{field_name}",
                    )
                )

        if not str(normative_trace.get("normative_trace_id", "")).startswith("NT-GER-"):
            issues.append(
                ValidationIssue(
                    code="NORMATIVE_TRACE_ID_INVALID",
                    message="normative_trace_id must start with NT-GER-.",
                    location=f"{location}.normative_trace_id",
                )
            )

        for list_field in ("jurisdiction", "reference_domain", "references", "responsible_review_layer"):
            value = normative_trace.get(list_field)
            if not isinstance(value, list):
                issues.append(
                    ValidationIssue(
                        code="NORMATIVE_TRACE_LIST_FIELD_INVALID",
                        message=f"{list_field} must be a list.",
                        location=f"{location}.{list_field}",
                    )
                )
            elif list_field != "references" and not value:
                issues.append(
                    ValidationIssue(
                        code="NORMATIVE_TRACE_LIST_FIELD_EMPTY",
                        message=f"{list_field} must be a non-empty list.",
                        location=f"{location}.{list_field}",
                    )
                )

        if normative_trace.get("institutional_review_required") is not True:
            issues.append(
                ValidationIssue(
                    code="NORMATIVE_TRACE_REVIEW_REQUIRED_NOT_TRUE",
                    message="institutional_review_required must be true.",
                    location=f"{location}.institutional_review_required",
                )
            )

        if normative_trace.get("references") != []:
            issues.append(
                ValidationIssue(
                    code="NORMATIVE_TRACE_REFERENCES_NOT_PLACEHOLDER_EMPTY",
                    message="references must remain an empty list during placeholder stage.",
                    location=f"{location}.references",
                )
            )

        verdict_boundary = normative_trace.get("verdict_boundary")
        if isinstance(verdict_boundary, str):
            boundary_text = verdict_boundary.lower()
            required_phrases = [
               "does not issue legal conclusions",
               "donor compliance conclusions",
               "payment decisions",
               "supplier sanctions",
               "enforcement conclusions",
            ]
            for phrase in required_phrases:
                if phrase not in boundary_text:
                    issues.append(
                        ValidationIssue(
                            code="NORMATIVE_TRACE_BOUNDARY_INCOMPLETE",
                            message=f"verdict_boundary missing phrase: {phrase}",
                            location=f"{location}.verdict_boundary",
                        )
                    )

    return issues

def validate_evidence_objects(report: Mapping[str, Any]) -> List[ValidationIssue]:
    evidence_objects = report.get("evidence_objects")
    if not isinstance(evidence_objects, list):
        return [ValidationIssue(code="EVIDENCE_OBJECTS_NOT_LIST", message="evidence_objects must be a list.", location="report.evidence_objects")]

    issues: List[ValidationIssue] = []
    seen_ids: Set[str] = set()
    for index, evidence in enumerate(evidence_objects):
        location = f"report.evidence_objects[{index}]"
        if not isinstance(evidence, dict):
            issues.append(ValidationIssue(code="EVIDENCE_OBJECT_NOT_OBJECT", message="Evidence object must be an object.", location=location))
            continue

        missing = REQUIRED_EVIDENCE_FIELDS - set(evidence.keys())
        for field_name in sorted(missing):
            issues.append(
                ValidationIssue(
                    code="EVIDENCE_FIELD_MISSING",
                    message=f"Required evidence field is missing: {field_name}",
                    location=f"{location}.{field_name}",
                )
            )

        evidence_id = evidence.get("evidence_id")
        if not evidence_id:
            issues.append(ValidationIssue(code="EVIDENCE_ID_EMPTY", message="Evidence ID must not be empty.", location=f"{location}.evidence_id"))
        elif evidence_id in seen_ids:
            issues.append(ValidationIssue(code="EVIDENCE_ID_DUPLICATE", message=f"Duplicate evidence ID: {evidence_id}", location=f"{location}.evidence_id"))
        else:
            seen_ids.add(str(evidence_id))

    return issues


def validate_count_consistency(report: Mapping[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    findings = report.get("findings", []) if isinstance(report.get("findings"), list) else []
    evidence_objects = report.get("evidence_objects", []) if isinstance(report.get("evidence_objects"), list) else []

    expected_pairs = {
        "findings_count": len(findings),
        "evidence_count": len(evidence_objects),
        "high_or_critical_findings_count": sum(1 for item in findings if isinstance(item, dict) and item.get("severity") in {"HIGH", "CRITICAL"}),
    }

    for field_name, expected_value in expected_pairs.items():
        actual_value = summary.get(field_name)
        if actual_value != expected_value:
            issues.append(
                ValidationIssue(
                    code="SUMMARY_COUNT_MISMATCH",
                    message=f"{field_name} must be {expected_value}, got {actual_value}.",
                    location=f"report.summary.{field_name}",
                )
            )

    return issues


def validate_signal_family_consistency(report: Mapping[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    findings = report.get("findings", []) if isinstance(report.get("findings"), list) else []
    report_signal_families = report.get("signal_families")
    summary_signal_families = report.get("summary", {}).get("signal_families") if isinstance(report.get("summary"), dict) else None
    computed = count_by_field(findings, "signal_family")

    if report_signal_families != computed:
        issues.append(
            ValidationIssue(
                code="REPORT_SIGNAL_FAMILIES_MISMATCH",
                message=f"Top-level signal_families does not match findings. Expected {computed}, got {report_signal_families}.",
                location="report.signal_families",
            )
        )

    if summary_signal_families != computed:
        issues.append(
            ValidationIssue(
                code="SUMMARY_SIGNAL_FAMILIES_MISMATCH",
                message=f"Summary signal_families does not match findings. Expected {computed}, got {summary_signal_families}.",
                location="report.summary.signal_families",
            )
        )

    return issues


def validate_severity_distribution_consistency(report: Mapping[str, Any]) -> List[ValidationIssue]:
    findings = report.get("findings", []) if isinstance(report.get("findings"), list) else []
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    computed = count_by_field(findings, "severity")
    actual = summary.get("severity_distribution")
    if actual != computed:
        return [
            ValidationIssue(
                code="SEVERITY_DISTRIBUTION_MISMATCH",
                message=f"severity_distribution does not match findings. Expected {computed}, got {actual}.",
                location="report.summary.severity_distribution",
            )
        ]
    return []


def validate_evidence_mapping(report: Mapping[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    findings = report.get("findings", []) if isinstance(report.get("findings"), list) else []
    evidence_objects = report.get("evidence_objects", []) if isinstance(report.get("evidence_objects"), list) else []

    finding_ids = {str(item.get("id")) for item in findings if isinstance(item, dict) and item.get("id")}
    evidence_by_id = {str(item.get("evidence_id")): item for item in evidence_objects if isinstance(item, dict) and item.get("evidence_id")}

    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            continue
        finding_id = str(finding.get("id", ""))
        evidence_list = finding.get("evidence")
        if evidence_list != [finding_id]:
            issues.append(
                ValidationIssue(
                    code="FINDING_EVIDENCE_REFERENCE_MISMATCH",
                    message=f"Finding evidence must reference its own ID exactly once: {finding_id}",
                    location=f"report.findings[{index}].evidence",
                )
            )
        if finding_id not in evidence_by_id:
            issues.append(
                ValidationIssue(
                    code="EVIDENCE_OBJECT_MISSING_FOR_FINDING",
                    message=f"No evidence object exists for finding ID: {finding_id}",
                    location=f"report.findings[{index}].id",
                )
            )

    for index, evidence in enumerate(evidence_objects):
        if not isinstance(evidence, dict):
            continue
        finding_id = str(evidence.get("finding_id", ""))
        evidence_id = str(evidence.get("evidence_id", ""))
        if evidence_id != finding_id:
            issues.append(
                ValidationIssue(
                    code="EVIDENCE_ID_FINDING_ID_MISMATCH",
                    message=f"Evidence ID and finding ID must match. evidence_id={evidence_id}, finding_id={finding_id}",
                    location=f"report.evidence_objects[{index}]",
                )
            )
        if finding_id not in finding_ids:
            issues.append(
                ValidationIssue(
                    code="EVIDENCE_REFERENCES_UNKNOWN_FINDING",
                    message=f"Evidence object references unknown finding ID: {finding_id}",
                    location=f"report.evidence_objects[{index}].finding_id",
                )
            )

    return issues


def validate_supplier_summary(report: Mapping[str, Any]) -> List[ValidationIssue]:
    supplier_summary = report.get("supplier_summary")
    if not isinstance(supplier_summary, list):
        return [ValidationIssue(code="SUPPLIER_SUMMARY_NOT_LIST", message="supplier_summary must be a list.", location="report.supplier_summary")]

    issues: List[ValidationIssue] = []
    for index, item in enumerate(supplier_summary):
        location = f"report.supplier_summary[{index}]"
        if not isinstance(item, dict):
            issues.append(ValidationIssue(code="SUPPLIER_SUMMARY_ITEM_NOT_OBJECT", message="Supplier summary item must be an object.", location=location))
            continue
        for field_name in ("supplier_id", "supplier_name", "finding_count", "max_severity", "evidence_references"):
            if field_name not in item:
                issues.append(
                    ValidationIssue(
                        code="SUPPLIER_SUMMARY_FIELD_MISSING",
                        message=f"Supplier summary field is missing: {field_name}",
                        location=f"{location}.{field_name}",
                    )
                )
    return issues


def validate_zero_autonomy_boundary(report: Mapping[str, Any]) -> List[ValidationIssue]:
    boundary = report.get("zero_autonomy_boundary")
    if not isinstance(boundary, dict):
        return [ValidationIssue(code="ZERO_AUTONOMY_BOUNDARY_NOT_OBJECT", message="zero_autonomy_boundary must be an object.", location="report.zero_autonomy_boundary")]

    expected_false_fields = [
        "canonical_registry_opened",
        "canonical_registry_mutated",
        "production_records_mutated",
        "payment_block_performed",
        "supplier_punishment_performed",
        "donor_compliance_conclusion_issued",
        "fraud_verdict_issued",
        "legal_conclusion_issued",
        "signing_or_key_access_performed",
        "external_execution_performed",
    ]

    issues: List[ValidationIssue] = []
    if boundary.get("autonomous_enforcement_actions") != 0:
        issues.append(
            ValidationIssue(
                code="BOUNDARY_AUTONOMOUS_ACTIONS_NOT_ZERO",
                message="autonomous_enforcement_actions must be 0.",
                location="report.zero_autonomy_boundary.autonomous_enforcement_actions",
            )
        )

    for field_name in expected_false_fields:
        if boundary.get(field_name) is not False:
            issues.append(
                ValidationIssue(
                    code="BOUNDARY_FIELD_NOT_FALSE",
                    message=f"Boundary field must be false: {field_name}",
                    location=f"report.zero_autonomy_boundary.{field_name}",
                )
            )

    if boundary.get("pipeline_mode") != "LOCAL_READ_ONLY_GRANT_EXPENSE_REVIEW_SIGNAL_GENERATION":
        issues.append(
            ValidationIssue(
                code="BOUNDARY_PIPELINE_MODE_INVALID",
                message="pipeline_mode is not the expected local read-only signal generation mode.",
                location="report.zero_autonomy_boundary.pipeline_mode",
            )
        )

    return issues


def validate_interpretation_boundary(report: Mapping[str, Any]) -> List[ValidationIssue]:
    boundary = report.get("interpretation_boundary")
    if not isinstance(boundary, dict):
        return [ValidationIssue(code="INTERPRETATION_BOUNDARY_NOT_OBJECT", message="interpretation_boundary must be an object.", location="report.interpretation_boundary")]

    expected_false_fields = [
        "fraud_verdict_issued",
        "legal_conclusion_issued",
        "donor_compliance_conclusion_issued",
        "payment_block_performed",
        "supplier_punishment_performed",
    ]

    issues: List[ValidationIssue] = []
    for field_name in expected_false_fields:
        if boundary.get(field_name) is not False:
            issues.append(
                ValidationIssue(
                    code="INTERPRETATION_BOUNDARY_FIELD_NOT_FALSE",
                    message=f"Interpretation boundary field must be false: {field_name}",
                    location=f"report.interpretation_boundary.{field_name}",
                )
            )

    if boundary.get("human_review_required") is not True:
        issues.append(
            ValidationIssue(
                code="HUMAN_REVIEW_REQUIRED_NOT_TRUE",
                message="human_review_required must be true.",
                location="report.interpretation_boundary.human_review_required",
            )
        )

    return issues


def validate_forbidden_free_text(report: Mapping[str, Any]) -> List[ValidationIssue]:
    serialized = json.dumps(report, ensure_ascii=False).lower()
    issues: List[ValidationIssue] = []
    for phrase in sorted(FORBIDDEN_FREE_TEXT_PHRASES):
        if phrase in serialized:
            issues.append(
                ValidationIssue(
                    code="FORBIDDEN_FREE_TEXT_PHRASE_FOUND",
                    message=f"Forbidden phrase found in report text: {phrase}",
                    location="report",
                )
            )
    return issues


def build_result(is_valid: bool, path: Path, summary: Mapping[str, Any], errors: Sequence[ValidationIssue], warnings: Sequence[ValidationIssue]) -> Dict[str, Any]:
    return {
        "is_valid": is_valid,
        "report_path": str(path),
        "summary": dict(summary),
        "errors": [issue.to_dict() for issue in errors],
        "warnings": [issue.to_dict() for issue in warnings],
    }


def build_summary(report: Mapping[str, Any]) -> Dict[str, Any]:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    return {
        "report_id": report.get("report_id"),
        "report_type": report.get("report_type"),
        "report_version": report.get("report_version"),
        "generated_at": report.get("generated_at"),
        "source_name": report.get("source_name"),
        "findings_count": summary.get("findings_count"),
        "evidence_count": summary.get("evidence_count"),
        "grant_expense_count": summary.get("grant_expense_count"),
        "supplier_count": summary.get("supplier_count"),
        "known_supplier_profile_count": summary.get("known_supplier_profile_count"),
        "high_or_critical_findings_count": summary.get("high_or_critical_findings_count"),
        "reviewed_findings_count": summary.get("reviewed_findings_count"),
        "input_quality_status": summary.get("input_quality_status"),
        "input_quality_warning_count": summary.get("input_quality_warning_count"),
        "input_quality_error_count": summary.get("input_quality_error_count"),
        "signal_families": summary.get("signal_families"),
        "severity_distribution": summary.get("severity_distribution"),
        "autonomous_actions": summary.get("autonomous_actions"),
    }


def build_partial_summary(report: Mapping[str, Any]) -> Dict[str, Any]:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    return {
        "report_id": report.get("report_id"),
        "report_type": report.get("report_type"),
        "findings_count": summary.get("findings_count"),
        "evidence_count": summary.get("evidence_count"),
        "input_quality_status": summary.get("input_quality_status"),
        "autonomous_actions": summary.get("autonomous_actions"),
    }


def count_by_field(items: Sequence[Any], field_name: str) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for item in items:
        if isinstance(item, dict):
            counts[str(item.get(field_name, "UNKNOWN"))] += 1
    return dict(sorted(counts.items()))


if __name__ == "__main__":
    main()
