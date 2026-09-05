"""
TBK Cake Genome - Phase 1 validation report.

WHAT THIS IS NOT
  This is NOT Build-006, the Enterprise Validation Engine. Build-006 owns
  runtime enforcement of Validation.md's four dimensions (structural,
  confidence thresholding, consistency, completeness) across the whole
  platform, has no package, and is sequenced as work item D7.

  This module runs the *structural* and *completeness* checks only, over one
  genome, plus the safety invariants Phase 1 must not violate. It reports; it
  never rejects, never patches, and never fabricates a value to pass -
  Validation.md: "an incomplete or conflicting record is left incomplete/
  conflicting and flagged, not patched."

  Confidence thresholding is deliberately absent: Validation.md requires
  PER-ATTRIBUTE-GROUP thresholds, which live in EAD's confidence_expectations
  and belong to Build-006. A single global bar invented here would be a second,
  competing rule.
"""
from dataclasses import asdict, dataclass

SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"
SEVERITY_INFO = "info"


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str


@dataclass(frozen=True)
class ValidationReport:
    passed: bool
    dimensions_run: tuple
    dimensions_deferred: tuple
    findings: tuple

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "dimensions_run": list(self.dimensions_run),
            "dimensions_deferred": list(self.dimensions_deferred),
            "findings": [asdict(f) for f in self.findings],
            "error_count": sum(1 for f in self.findings if f.severity == SEVERITY_ERROR),
            "warning_count": sum(1 for f in self.findings if f.severity == SEVERITY_WARNING),
        }


def _structural(genome, findings: list) -> None:
    """Does every record conform to the contract's own field rules?"""
    for section in genome.sections.values():
        for attr in section["attributes"]:
            state, value, conf = attr["value_state"], attr["value"], attr["confidence"]
            if state in ("null", "unknown") and value not in (None, ""):
                findings.append(Finding(
                    "STRUCT_VALUE_WITH_NONPRESENT_STATE", SEVERITY_ERROR,
                    f"{attr['attribute']}: value_state={state} but value={value!r}. "
                    "EALAttributeRecordModel._value_state_consistency would reject this.",
                ))
            if state != "present" and conf is not None:
                findings.append(Finding(
                    "STRUCT_CONFIDENCE_WITHOUT_VALUE", SEVERITY_ERROR,
                    f"{attr['attribute']}: confidence={conf} with value_state={state}. "
                    "Confidence_Standard.md: nothing to be confident about.",
                ))
            if conf is not None and not 0.0 <= conf <= 1.0:
                findings.append(Finding(
                    "STRUCT_CONFIDENCE_RANGE", SEVERITY_ERROR,
                    f"{attr['attribute']}: confidence {conf} outside [0.0, 1.0].",
                ))
            if attr["data_type"] == "enum" and state == "present" and not attr["term_id"]:
                findings.append(Finding(
                    "STRUCT_ENUM_UNRESOLVED", SEVERITY_WARNING,
                    f"{attr['attribute']}: enum attribute with no resolved Term.",
                ))


def _completeness(genome, findings: list) -> None:
    """A data-quality signal, never a blocker - Validation.md is explicit."""
    for entry in genome.unrepresented_sections:
        findings.append(Finding(
            "COMPLETENESS_SECTION_EMPTY", SEVERITY_INFO,
            f"section {entry['section']!r}: {entry['reason']}",
        ))
    if not genome.sections:
        findings.append(Finding(
            "COMPLETENESS_NO_SECTIONS", SEVERITY_ERROR,
            "no section resolved - the genome describes nothing.",
        ))


def _provenance(genome, findings: list) -> None:
    """ADR 0011: a record that cannot populate schema_version and
    taxonomy_version must not be written at all."""
    required = ("provider", "model", "schema_version", "taxonomy_version", "extracted_at")
    for key in required:
        if not genome.provenance.get(key):
            findings.append(Finding(
                "PROV_MISSING_FIELD", SEVERITY_ERROR,
                f"provenance.{key} is empty - record is not re-derivable and must not persist.",
            ))
    if not genome.provenance.get("prompt_version"):
        findings.append(Finding(
            "PROV_NO_PROMPT_VERSION", SEVERITY_WARNING,
            "provenance.prompt_version is empty - extraction is not exactly reproducible.",
        ))


def _safety(genome, findings: list) -> None:
    """The invariants Phase 1 exists to guarantee. A failure here is a design
    breach, not a data-quality issue."""
    if genome.verification_status != "unverified":
        findings.append(Finding(
            "SAFETY_SELF_VERIFIED", SEVERITY_ERROR,
            f"verification_status is {genome.verification_status!r}. No automated path may "
            "assert verification - EPR section 04, VIG-007.",
        ))
    for proposal in genome.candidate_discoveries:
        if proposal.get("status") not in ("observed", "candidate"):
            findings.append(Finding(
                "SAFETY_PROPOSAL_ADVANCED", SEVERITY_ERROR,
                f"proposal {proposal.get('canonical_name')!r} has status "
                f"{proposal.get('status')!r}; extraction may only produce 'observed'.",
            ))
        if proposal.get("promoted_to"):
            findings.append(Finding(
                "SAFETY_PROPOSAL_PROMOTED", SEVERITY_ERROR,
                f"proposal {proposal.get('canonical_name')!r} carries promoted_to - "
                "no proposal may be auto-promoted at any confidence.",
            ))


def _leakage(genome, findings: list) -> None:
    """Defect D-3. Leaked output must be visible in diagnostics and absent
    everywhere else. This checks the SEPARATION, not merely that leakage
    occurred - detecting leakage is success; letting it through is the fault."""
    records = genome.diagnostics.get("prompt_leakage") or []
    if not records:
        return
    findings.append(Finding(
        "LEAK_DETECTED_AND_EXCLUDED", SEVERITY_WARNING,
        f"{len(records)} model output(s) reproduced prompt/example text and were excluded "
        "from the genome, the lock and discovery. Retained in diagnostics.",
    ))
    leaked_text = {str(r.get("observation", "")).casefold() for r in records}
    for proposal in genome.candidate_discoveries:
        if str(proposal.get("label", "")).casefold() in leaked_text:
            findings.append(Finding(
                "LEAK_REACHED_DISCOVERY", SEVERITY_ERROR,
                f"leaked text became candidate discovery {proposal.get('canonical_name')!r}.",
            ))
    lock = genome.design_identity_lock
    if lock:
        for value in lock.locked_attributes.values():
            if str(value).casefold() in leaked_text:
                findings.append(Finding(
                    "LEAK_REACHED_LOCK", SEVERITY_ERROR,
                    f"leaked text {value!r} entered the Design Identity Lock.",
                ))


def validate_genome(genome) -> ValidationReport:
    findings: list = []
    _leakage(genome, findings)
    _structural(genome, findings)
    _completeness(genome, findings)
    _provenance(genome, findings)
    _safety(genome, findings)
    return ValidationReport(
        passed=not any(f.severity == SEVERITY_ERROR for f in findings),
        dimensions_run=("structural", "completeness", "provenance", "safety_invariants",
                        "prompt_leakage_separation"),
        dimensions_deferred=(
            "confidence_thresholding (per-group, Build-006 + EAD confidence_expectations)",
            "consistency (needs prior verified Genome Attributes to contradict; none persist yet)",
        ),
        findings=tuple(findings),
    )
