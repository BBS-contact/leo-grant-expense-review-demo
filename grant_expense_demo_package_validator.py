r"""
LEO Grant Expense Review Demo Package Validator v0.2

Canonical Path:
D:\BBS-09-01-2026\leo\runtime\demos\grant_expense_review\grant_expense_demo_package_validator.py

Purpose:
Validate the integrity of the local Grant Expense Review demo package.

This validator verifies:
- required demo files exist,
- evidence report integrity,
- attachment review integrity,
- inferred readiness blocker integrity,
- export package integrity,
- and zero-autonomy boundary preservation.

Important correction in v0.2:
The dashboard computes some readiness data in the browser from localStorage and exported review state.
Therefore this validator must not expect dashboard-computed readiness blockers to already exist inside
output/grant_expense_evidence_report.json.

This validator does NOT:
- mutate files,
- execute institutional actions,
- parse PDFs,
- perform OCR,
- issue legal conclusions,
- issue donor compliance conclusions,
- block payments,
- punish suppliers,
- access keys,
- sign documents,
- or perform external execution.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


DASHBOARD_FILE = BASE_DIR / "leo_grant_expense_review_dashboard.html"
INPUT_QUALITY_REPORT_FILE = OUTPUT_DIR / "grant_expense_input_quality_report.json"
EVIDENCE_REPORT_FILE = OUTPUT_DIR / "grant_expense_evidence_report.json"
PREFERRED_EXPORT_PACKAGE_FILE = OUTPUT_DIR / "leo_grant_expense_human_review_package_v0.4.json"


EXPECTED_FINDINGS_COUNT = 25
EXPECTED_HIGH_FINDINGS = 12
EXPECTED_ATTACHMENT_ID = "ATT-001"
EXPECTED_ATTACHMENT_REVIEW_STATE = "NEEDS_REPLACEMENT"
EXPECTED_READINESS_BLOCKER = "1 attachment review item(s) need replacement."


@dataclass
class ValidationResult:
    """Container for demo package validation results."""

    status: str
    checks_passed: int
    checks_failed: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    export_package_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "errors": self.errors,
            "warnings": self.warnings,
            "export_package_path": self.export_package_path,
        }


class DemoPackageValidator:
    """Validator for the LEO Grant Expense Review local demo package."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks_passed = 0
        self.checks_failed = 0
        self.export_package_path: Path | None = None

    def validate(self) -> ValidationResult:
        """Run the complete validation sequence."""

        self._validate_required_static_files()

        evidence_report = self._safe_load_json(EVIDENCE_REPORT_FILE)
        export_package = self._load_export_package()

        if evidence_report is not None:
            self._validate_evidence_report_integrity(evidence_report)
            self._validate_zero_autonomy_boundary_from_evidence_report(evidence_report)

        if export_package is not None:
            self._validate_attachment_review_integrity(export_package)
            self._validate_inferred_readiness_blocker(export_package)
            self._validate_export_package_integrity(export_package)
            self._validate_zero_autonomy_boundary_from_export_package(export_package)

        final_status = (
            "DEMO_PACKAGE_READY"
            if self.checks_failed == 0
            else "DEMO_PACKAGE_VALIDATION_FAILED"
        )

        return ValidationResult(
            status=final_status,
            checks_passed=self.checks_passed,
            checks_failed=self.checks_failed,
            errors=self.errors,
            warnings=self.warnings,
            export_package_path=str(self.export_package_path) if self.export_package_path else None,
        )

    def _pass(self) -> None:
        self.checks_passed += 1

    def _fail(self, message: str) -> None:
        self.checks_failed += 1
        self.errors.append(message)

    def _warn(self, message: str) -> None:
        self.warnings.append(message)

    def _validate_required_static_files(self) -> None:
        """Validate required static demo files exist."""

        required_static_files = {
            "dashboard": DASHBOARD_FILE,
            "input_quality_report": INPUT_QUALITY_REPORT_FILE,
            "evidence_report": EVIDENCE_REPORT_FILE,
        }

        for label, path in required_static_files.items():
            if path.exists():
                self._pass()
            else:
                self._fail(f"Required file missing: {label} -> {path}")

    def _discover_export_package_path(self) -> Path | None:
        """Find the export package file used by the demo validator."""

        if PREFERRED_EXPORT_PACKAGE_FILE.exists():
            return PREFERRED_EXPORT_PACKAGE_FILE

        candidate_patterns = [
            "leo_grant_expense_human_review_package*.json",
            "leo_grant_expense_human_review_package*",
        ]

        candidates: list[Path] = []
        for directory in [OUTPUT_DIR, BASE_DIR]:
            if not directory.exists():
                continue
            for pattern in candidate_patterns:
                candidates.extend(path for path in directory.glob(pattern) if path.is_file())

        if not candidates:
            return None

        candidates = sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)
        selected = candidates[0]
        self._warn(
            "Preferred export package file was not found. "
            f"Using discovered export package: {selected}"
        )
        return selected

    def _load_export_package(self) -> dict[str, Any] | None:
        """Load the latest available export package."""

        export_path = self._discover_export_package_path()
        if export_path is None:
            self._fail(
                "Export package missing. Expected preferred path: "
                f"{PREFERRED_EXPORT_PACKAGE_FILE}"
            )
            return None

        self.export_package_path = export_path
        return self._safe_load_json(export_path)

    def _safe_load_json(self, path: Path) -> dict[str, Any] | None:
        """Safely load JSON content."""

        if not path.exists():
            return None

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                self._fail(f"JSON root must be an object in {path.name}.")
                return None

            self._pass()
            return data

        except json.JSONDecodeError as exc:
            self._fail(f"Invalid JSON format in {path.name}: {exc}")
            return None

        except OSError as exc:
            self._fail(f"Unable to read JSON file {path.name}: {exc}")
            return None

    def _validate_evidence_report_integrity(self, evidence_report: dict[str, Any]) -> None:
        """Validate evidence report structure and counts."""

        findings = evidence_report.get("findings", [])
        if isinstance(findings, list) and findings:
            self._pass()
        else:
            self._fail("Evidence report findings list missing or empty.")
            return

        summary = evidence_report.get("summary", {})
        if not isinstance(summary, dict):
            summary = {}

        findings_count = (
            summary.get("findings_count")
            if summary.get("findings_count") is not None
            else evidence_report.get("findings_count")
        )

        if findings_count is None:
            findings_count = len(findings)
            self._warn("findings_count not found in report summary; using computed findings length.")

        if findings_count == EXPECTED_FINDINGS_COUNT:
            self._pass()
        else:
            self._fail(
                "Unexpected findings_count: "
                f"expected {EXPECTED_FINDINGS_COUNT}, received {findings_count}"
            )

        high_findings = (
            summary.get("high_or_critical_findings_count")
            if summary.get("high_or_critical_findings_count") is not None
            else evidence_report.get("high_findings")
        )

        if high_findings is None:
            high_findings = sum(
                1
                for finding in findings
                if finding.get("severity") in {"HIGH", "CRITICAL"}
            )
            self._warn("high findings count not found in report summary; using computed severity count.")

        if high_findings == EXPECTED_HIGH_FINDINGS:
            self._pass()
        else:
            self._fail(
                "Unexpected high findings count: "
                f"expected {EXPECTED_HIGH_FINDINGS}, received {high_findings}"
            )

    def _validate_zero_autonomy_boundary_from_evidence_report(
        self,
        evidence_report: dict[str, Any],
    ) -> None:
        """Validate zero-autonomy boundary fields from evidence report."""

        boundary = evidence_report.get("zero_autonomy_boundary")
        if not isinstance(boundary, dict):
            self._fail("zero_autonomy_boundary section missing from evidence report.")
            return

        expected_false_fields = [
            "canonical_registry_mutated",
            "production_records_mutated",
            "payment_block_performed",
            "supplier_punishment_performed",
            "fraud_verdict_issued",
            "legal_conclusion_issued",
            "external_execution_performed",
        ]

        for field_name in expected_false_fields:
            value = boundary.get(field_name)
            if value is False:
                self._pass()
            else:
                self._fail(f"Zero-autonomy boundary violated in evidence report: {field_name}={value}")

        autonomous_actions = boundary.get("autonomous_enforcement_actions")
        if autonomous_actions == 0:
            self._pass()
        else:
            self._fail("autonomous_enforcement_actions must remain 0 in evidence report.")

    def _validate_attachment_review_integrity(self, export_package: dict[str, Any]) -> None:
        """Validate attachment review integrity from export package."""

        attachment_reviews = export_package.get("attachment_reviews", [])
        if not isinstance(attachment_reviews, list) or not attachment_reviews:
            self._fail("attachment_reviews missing from export package.")
            return

        self._pass()

        attachment_match_found = False
        for review in attachment_reviews:
            if not isinstance(review, dict):
                continue

            attachment_id = review.get("attachment_id")
            review_state = review.get("action") or review.get("local_document_review")

            if (
                attachment_id == EXPECTED_ATTACHMENT_ID
                and review_state == EXPECTED_ATTACHMENT_REVIEW_STATE
            ):
                attachment_match_found = True
                break

        if attachment_match_found:
            self._pass()
        else:
            self._fail(
                "Expected attachment review state not found in export package: "
                f"{EXPECTED_ATTACHMENT_ID} -> {EXPECTED_ATTACHMENT_REVIEW_STATE}"
            )

    def _validate_inferred_readiness_blocker(self, export_package: dict[str, Any]) -> None:
        """Validate readiness blocker by inferring it from exported attachment reviews."""

        attachment_reviews = export_package.get("attachment_reviews", [])
        if not isinstance(attachment_reviews, list):
            self._fail("Cannot infer readiness blocker because attachment_reviews is not a list.")
            return

        needs_replacement_count = sum(
            1
            for review in attachment_reviews
            if isinstance(review, dict)
            and (review.get("action") or review.get("local_document_review")) == "NEEDS_REPLACEMENT"
        )

        inferred_blocker = f"{needs_replacement_count} attachment review item(s) need replacement."

        if inferred_blocker == EXPECTED_READINESS_BLOCKER:
            self._pass()
        else:
            self._fail(
                "Expected inferred readiness blocker mismatch: "
                f"expected '{EXPECTED_READINESS_BLOCKER}', received '{inferred_blocker}'"
            )

    def _validate_export_package_integrity(self, export_package: dict[str, Any]) -> None:
        """Validate export package structure."""

        required_export_fields = [
            "review_actions",
            "attachment_reviews",
            "zero_autonomy_boundary",
            "evidence_attachment_export_boundary",
            "reviewed_findings_snapshot",
        ]

        for field_name in required_export_fields:
            if field_name in export_package:
                self._pass()
            else:
                self._fail(f"Export package field missing: {field_name}")

        attachment_reviews_count = export_package.get("attachment_reviews_count")
        attachment_reviews = export_package.get("attachment_reviews", [])

        if isinstance(attachment_reviews, list) and attachment_reviews_count == len(attachment_reviews):
            self._pass()
        else:
            self._fail(
                "attachment_reviews_count mismatch: "
                f"count={attachment_reviews_count}, actual={len(attachment_reviews) if isinstance(attachment_reviews, list) else 'not-list'}"
            )

    def _validate_zero_autonomy_boundary_from_export_package(
        self,
        export_package: dict[str, Any],
    ) -> None:
        """Validate zero-autonomy boundary fields from export package."""

        boundary = export_package.get("zero_autonomy_boundary")
        if not isinstance(boundary, dict):
            self._fail("zero_autonomy_boundary section missing from export package.")
            return

        expected_true_fields = [
            "no_donor_compliance_verdict",
            "no_fraud_verdict",
            "no_legal_conclusion",
            "no_payment_blocking",
            "no_supplier_punishment",
            "no_production_mutation",
            "no_canonical_registry_mutation",
            "no_autonomous_enforcement",
            "no_signing_or_key_access",
            "no_external_execution",
        ]

        for field_name in expected_true_fields:
            value = boundary.get(field_name)
            if value is True:
                self._pass()
            else:
                self._fail(f"Zero-autonomy export boundary violated: {field_name}={value}")


def main() -> None:
    """Run the demo package validator."""

    validator = DemoPackageValidator()
    result = validator.validate()

    print("=" * 70)
    print("LEO GRANT EXPENSE REVIEW DEMO PACKAGE VALIDATOR v0.2")
    print("=" * 70)
    print(f"STATUS: {result.status}")
    print(f"CHECKS PASSED: {result.checks_passed}")
    print(f"CHECKS FAILED: {result.checks_failed}")

    if result.export_package_path:
        print(f"EXPORT PACKAGE: {result.export_package_path}")

    if result.errors:
        print("\nERRORS:")
        for error in result.errors:
            print(f"- {error}")

    if result.warnings:
        print("\nWARNINGS:")
        for warning in result.warnings:
            print(f"- {warning}")

    print("=" * 70)


if __name__ == "__main__":
    main()
