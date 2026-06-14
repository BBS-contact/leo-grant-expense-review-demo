r"""
Tests for LEO Grant Expense Review Demo Package Validator v0.2

Canonical Path:
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\tests\test_grant_expense_demo_package_validator.py

Purpose:
Validate the demo package validator without performing production actions,
external execution, PDF parsing, OCR, signing, key access, payment action,
supplier action, canonical registry mutation, or autonomous enforcement.

v0.2 alignment:
- findings count is read from summary.findings_count when present,
- high/critical count is read from summary.high_or_critical_findings_count when present,
- attachment review state is read from export package field action,
- readiness blocker is inferred from exported attachment review state,
- export package structure reflects real dashboard export format.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from grant_expense_demo_package_validator import (
    DemoPackageValidator,
    EXPECTED_ATTACHMENT_ID,
    EXPECTED_ATTACHMENT_REVIEW_STATE,
    EXPECTED_FINDINGS_COUNT,
    EXPECTED_HIGH_FINDINGS,
    EXPECTED_READINESS_BLOCKER,
    ValidationResult,
)


@pytest.fixture()
def valid_evidence_report() -> dict:
    """Return a minimal valid evidence report fixture aligned with v0.2."""

    return {
        "report_id": "LOCAL_GRANT_EXPENSE_REVIEW_REPORT",
        "summary": {
            "findings_count": EXPECTED_FINDINGS_COUNT,
            "high_or_critical_findings_count": EXPECTED_HIGH_FINDINGS,
            "autonomous_actions": 0,
        },
        "findings": [
            {
                "id": "GEV-001",
                "severity": "HIGH",
                "title": "Large expense review",
            }
        ],
        "zero_autonomy_boundary": {
            "autonomous_enforcement_actions": 0,
            "canonical_registry_mutated": False,
            "production_records_mutated": False,
            "payment_block_performed": False,
            "supplier_punishment_performed": False,
            "fraud_verdict_issued": False,
            "legal_conclusion_issued": False,
            "external_execution_performed": False,
        },
    }


@pytest.fixture()
def valid_evidence_report_without_summary_counts() -> dict:
    """Return evidence report where validator must compute counts."""

    findings = []
    for index in range(EXPECTED_FINDINGS_COUNT):
        findings.append(
            {
                "id": f"GEV-{index + 1:03d}",
                "severity": "HIGH" if index < EXPECTED_HIGH_FINDINGS else "MEDIUM",
                "title": "Synthetic test finding",
            }
        )

    return {
        "report_id": "LOCAL_GRANT_EXPENSE_REVIEW_REPORT",
        "summary": {},
        "findings": findings,
        "zero_autonomy_boundary": {
            "autonomous_enforcement_actions": 0,
            "canonical_registry_mutated": False,
            "production_records_mutated": False,
            "payment_block_performed": False,
            "supplier_punishment_performed": False,
            "fraud_verdict_issued": False,
            "legal_conclusion_issued": False,
            "external_execution_performed": False,
        },
    }


@pytest.fixture()
def valid_export_package() -> dict:
    """Return a minimal valid export package fixture aligned with dashboard v0.9."""

    return {
        "package_type": "LEO_LOCAL_GRANT_EXPENSE_HUMAN_REVIEW_PACKAGE",
        "package_version": "v0.4",
        "review_actions": [
            {
                "finding_id": "GEV-001",
                "action": "ESCALATE_FOR_REVIEW",
                "note": "Large expense requires institutional review.",
            }
        ],
        "attachment_reviews_count": 2,
        "attachment_reviews": [
            {
                "attachment_id": EXPECTED_ATTACHMENT_ID,
                "action": EXPECTED_ATTACHMENT_REVIEW_STATE,
                "note": "Invoice reference requires replacement.",
                "reviewer_mode": "LOCAL_BROWSER_DOCUMENT_REVIEW",
            },
            {
                "attachment_id": "ATT-002",
                "action": "REVIEWED",
                "note": "Contract reference reviewed locally.",
                "reviewer_mode": "LOCAL_BROWSER_DOCUMENT_REVIEW",
            },
        ],
        "reviewed_findings_snapshot": [
            {
                "finding_id": "GEV-001",
                "title": "Large expense review",
                "evidence_attachments": [
                    {
                        "attachment_id": EXPECTED_ATTACHMENT_ID,
                        "local_document_review": {
                            "attachment_id": EXPECTED_ATTACHMENT_ID,
                            "action": EXPECTED_ATTACHMENT_REVIEW_STATE,
                        },
                    }
                ],
            }
        ],
        "zero_autonomy_boundary": {
            "no_donor_compliance_verdict": True,
            "no_fraud_verdict": True,
            "no_legal_conclusion": True,
            "no_payment_blocking": True,
            "no_supplier_punishment": True,
            "no_production_mutation": True,
            "no_canonical_registry_mutation": True,
            "no_autonomous_enforcement": True,
            "no_signing_or_key_access": True,
            "no_external_execution": True,
        },
        "evidence_attachment_export_boundary": {
            "attachment_metadata_included": True,
            "document_files_embedded": False,
            "document_files_opened": False,
            "document_files_parsed": False,
            "ocr_performed": False,
            "ai_document_reading_performed": False,
            "document_signing_performed": False,
            "external_transmission_performed": False,
        },
    }


def write_json(path: Path, payload: dict) -> None:
    """Write JSON test fixture."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_validate_evidence_report_integrity_accepts_summary_counts(
    valid_evidence_report: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_evidence_report_integrity(valid_evidence_report)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 3


def test_validate_evidence_report_integrity_computes_missing_summary_counts(
    valid_evidence_report_without_summary_counts: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_evidence_report_integrity(valid_evidence_report_without_summary_counts)

    assert validator.checks_failed == 0
    assert validator.checks_passed == 3
    assert any("findings_count not found" in warning for warning in validator.warnings)
    assert any("high findings count not found" in warning for warning in validator.warnings)


def test_validate_evidence_report_integrity_rejects_missing_findings() -> None:
    validator = DemoPackageValidator()

    validator._validate_evidence_report_integrity(
        {
            "summary": {
                "findings_count": EXPECTED_FINDINGS_COUNT,
                "high_or_critical_findings_count": EXPECTED_HIGH_FINDINGS,
            },
            "findings": [],
        }
    )

    assert validator.checks_failed == 1
    assert "findings list missing or empty" in validator.errors[0]


def test_validate_evidence_report_integrity_rejects_wrong_summary_counts(
    valid_evidence_report: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_report = json.loads(json.dumps(valid_evidence_report))
    invalid_report["summary"]["findings_count"] = 24
    invalid_report["summary"]["high_or_critical_findings_count"] = 11

    validator._validate_evidence_report_integrity(invalid_report)

    assert validator.checks_failed == 2
    assert any("Unexpected findings_count" in error for error in validator.errors)
    assert any("Unexpected high findings count" in error for error in validator.errors)


def test_validate_zero_autonomy_boundary_from_evidence_report_accepts_valid_boundary(
    valid_evidence_report: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_zero_autonomy_boundary_from_evidence_report(valid_evidence_report)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 8


def test_validate_zero_autonomy_boundary_from_evidence_report_rejects_missing_boundary() -> None:
    validator = DemoPackageValidator()

    validator._validate_zero_autonomy_boundary_from_evidence_report({})

    assert validator.checks_failed == 1
    assert validator.errors == ["zero_autonomy_boundary section missing from evidence report."]


def test_validate_zero_autonomy_boundary_from_evidence_report_rejects_violation(
    valid_evidence_report: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_report = json.loads(json.dumps(valid_evidence_report))
    invalid_report["zero_autonomy_boundary"]["production_records_mutated"] = True
    invalid_report["zero_autonomy_boundary"]["autonomous_enforcement_actions"] = 1

    validator._validate_zero_autonomy_boundary_from_evidence_report(invalid_report)

    assert validator.checks_failed == 2
    assert any("production_records_mutated=True" in error for error in validator.errors)
    assert any("autonomous_enforcement_actions" in error for error in validator.errors)


def test_validate_attachment_review_integrity_accepts_action_field(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_attachment_review_integrity(valid_export_package)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 2


def test_validate_attachment_review_integrity_accepts_legacy_local_document_review_field(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    package = json.loads(json.dumps(valid_export_package))
    package["attachment_reviews"] = [
        {
            "attachment_id": EXPECTED_ATTACHMENT_ID,
            "local_document_review": EXPECTED_ATTACHMENT_REVIEW_STATE,
        }
    ]

    validator._validate_attachment_review_integrity(package)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 2


def test_validate_attachment_review_integrity_rejects_missing_reviews() -> None:
    validator = DemoPackageValidator()

    validator._validate_attachment_review_integrity({"attachment_reviews": []})

    assert validator.checks_failed == 1
    assert validator.errors == ["attachment_reviews missing from export package."]


def test_validate_attachment_review_integrity_rejects_wrong_state(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_package = json.loads(json.dumps(valid_export_package))
    invalid_package["attachment_reviews"] = [
        {
            "attachment_id": EXPECTED_ATTACHMENT_ID,
            "action": "REVIEWED",
        }
    ]

    validator._validate_attachment_review_integrity(invalid_package)

    assert validator.checks_failed == 1
    assert "Expected attachment review state not found" in validator.errors[0]


def test_validate_inferred_readiness_blocker_accepts_expected_blocker(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_inferred_readiness_blocker(valid_export_package)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 1


def test_validate_inferred_readiness_blocker_rejects_missing_replacement(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_package = json.loads(json.dumps(valid_export_package))
    invalid_package["attachment_reviews"] = [
        {
            "attachment_id": EXPECTED_ATTACHMENT_ID,
            "action": "REVIEWED",
        }
    ]

    validator._validate_inferred_readiness_blocker(invalid_package)

    assert validator.checks_failed == 1
    assert "Expected inferred readiness blocker mismatch" in validator.errors[0]


def test_validate_export_package_integrity_accepts_required_fields(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_export_package_integrity(valid_export_package)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 6


def test_validate_export_package_integrity_rejects_missing_fields(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_package = json.loads(json.dumps(valid_export_package))
    invalid_package.pop("zero_autonomy_boundary")
    invalid_package.pop("evidence_attachment_export_boundary")

    validator._validate_export_package_integrity(invalid_package)

    assert validator.checks_failed == 2
    assert any("zero_autonomy_boundary" in error for error in validator.errors)
    assert any("evidence_attachment_export_boundary" in error for error in validator.errors)


def test_validate_export_package_integrity_rejects_attachment_count_mismatch(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_package = json.loads(json.dumps(valid_export_package))
    invalid_package["attachment_reviews_count"] = 99

    validator._validate_export_package_integrity(invalid_package)

    assert validator.checks_failed == 1
    assert "attachment_reviews_count mismatch" in validator.errors[0]


def test_validate_zero_autonomy_boundary_from_export_package_accepts_valid_boundary(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()

    validator._validate_zero_autonomy_boundary_from_export_package(valid_export_package)

    assert validator.checks_failed == 0
    assert validator.errors == []
    assert validator.checks_passed == 10


def test_validate_zero_autonomy_boundary_from_export_package_rejects_missing_boundary() -> None:
    validator = DemoPackageValidator()

    validator._validate_zero_autonomy_boundary_from_export_package({})

    assert validator.checks_failed == 1
    assert validator.errors == ["zero_autonomy_boundary section missing from export package."]


def test_validate_zero_autonomy_boundary_from_export_package_rejects_violation(
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    invalid_package = json.loads(json.dumps(valid_export_package))
    invalid_package["zero_autonomy_boundary"]["no_external_execution"] = False

    validator._validate_zero_autonomy_boundary_from_export_package(invalid_package)

    assert validator.checks_failed == 1
    assert "no_external_execution=False" in validator.errors[0]


def test_safe_load_json_accepts_valid_json(tmp_path: Path) -> None:
    validator = DemoPackageValidator()
    path = tmp_path / "valid.json"
    write_json(path, {"status": "ok"})

    result = validator._safe_load_json(path)

    assert result == {"status": "ok"}
    assert validator.checks_failed == 0
    assert validator.checks_passed == 1


def test_safe_load_json_rejects_invalid_json(tmp_path: Path) -> None:
    validator = DemoPackageValidator()
    path = tmp_path / "invalid.json"
    path.write_text("{invalid-json", encoding="utf-8")

    result = validator._safe_load_json(path)

    assert result is None
    assert validator.checks_failed == 1
    assert "Invalid JSON format" in validator.errors[0]


def test_safe_load_json_rejects_non_object_json(tmp_path: Path) -> None:
    validator = DemoPackageValidator()
    path = tmp_path / "list.json"
    path.write_text("[]", encoding="utf-8")

    result = validator._safe_load_json(path)

    assert result is None
    assert validator.checks_failed == 1
    assert "JSON root must be an object" in validator.errors[0]


def test_validation_result_to_dict() -> None:
    result = ValidationResult(
        status="DEMO_PACKAGE_READY",
        checks_passed=35,
        checks_failed=0,
        errors=[],
        warnings=[],
        export_package_path="demo.json",
    )

    payload = result.to_dict()

    assert payload == {
        "status": "DEMO_PACKAGE_READY",
        "checks_passed": 35,
        "checks_failed": 0,
        "errors": [],
        "warnings": [],
        "export_package_path": "demo.json",
    }


def test_validator_does_not_mutate_input_payloads(
    valid_evidence_report: dict,
    valid_export_package: dict,
) -> None:
    validator = DemoPackageValidator()
    evidence_before = json.dumps(valid_evidence_report, sort_keys=True)
    export_before = json.dumps(valid_export_package, sort_keys=True)

    validator._validate_evidence_report_integrity(valid_evidence_report)
    validator._validate_zero_autonomy_boundary_from_evidence_report(valid_evidence_report)
    validator._validate_attachment_review_integrity(valid_export_package)
    validator._validate_inferred_readiness_blocker(valid_export_package)
    validator._validate_export_package_integrity(valid_export_package)
    validator._validate_zero_autonomy_boundary_from_export_package(valid_export_package)

    assert json.dumps(valid_evidence_report, sort_keys=True) == evidence_before
    assert json.dumps(valid_export_package, sort_keys=True) == export_before
