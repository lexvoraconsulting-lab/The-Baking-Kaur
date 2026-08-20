"""
Vision extraction - raw response to the two-channel contract (Build-008).

WHAT THIS CLOSES
  ai.vision.pipeline returns provider TEXT. ECP-200 recorded that "no code
  path converts this into an EAL record today". This module is that path.

WHY A PARSE FAILURE PRODUCES A RECORD, NOT AN EXCEPTION
  docs/AI/VisionExtractionContract.md section 5: "A parse failure is data. It
  produces a record with value_state 'unknown' and the raw response
  preserved... It never produces an absence." A pipeline that throws on bad
  model output silently loses the evidence that the prompt needs fixing.

WHY RawObservation IS NOT ai.eal.EALAttributeRecord
  An EALAttributeRecord requires a canonical_path, a namespace and a resolved
  group - i.e. it can only be built AFTER taxonomy matching. RawObservation is
  what exists BEFORE matching: the model's own words, unresolved. Building an
  EAL record here would mean inventing a canonical_path for something that may
  turn out to be unmatched, which is exactly the "force it into an approximate
  field" failure the contract forbids. ai.structure_discovery.matcher does the
  resolution; ai.eal records are built from the matched half only.
"""
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any

EXTRACTION_VERSION = "1.0"

_VALUE_STATES = ("present", "null", "unknown")


@dataclass(frozen=True)
class RawObservation:
    """One fact the model named, before taxonomy resolution."""
    group: str
    attribute: str
    value: Any
    value_state: str
    confidence: float | None = None
    evidence: str | None = None
    data_type: str | None = None
    vocabulary: str | None = None
    region: dict | None = None
    entity_type: str = "image"


@dataclass(frozen=True)
class UnmatchedObservation:
    """One fact the model saw but could not place. The channel that does not
    exist in either the n8n 6-key workflow or the current Python pipeline."""
    observed: str
    why_unmatched: str
    closest_group: str | None = None
    closest_attribute: str | None = None
    closest_term: str | None = None
    suggested_kind: str | None = None
    suggested_label: str | None = None
    confidence: float | None = None
    region: dict | None = None


@dataclass(frozen=True)
class RawRelationship:
    type: str
    source: str
    target: str
    confidence: float | None = None
    evidence: str | None = None


@dataclass(frozen=True)
class ExtractionResult:
    image_id: str
    taxonomy_version: str
    schema_version: str
    prompt_version: str | None
    provider: str | None
    model: str | None
    extracted_at: str | None
    observations: tuple[RawObservation, ...] = ()
    unmatched: tuple[UnmatchedObservation, ...] = ()
    relationships: tuple[RawRelationship, ...] = ()
    unparsed: tuple[str, ...] = ()
    leaked: tuple[LeakageRecord, ...] = ()
    parse_ok: bool = True
    raw_response: str = ""
    extraction_version: str = EXTRACTION_VERSION
    model_version: str | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        for key in ("observations", "unmatched", "relationships", "unparsed", "leaked"):
            d[key] = list(d[key])
        return d


@dataclass(frozen=True)
class LeakageRecord:
    """One model output that reproduced prompt/example text instead of
    describing the image.

    WHY THIS IS AN EXTRACTION-LAYER RECORD, NOT A NEW DIAGNOSTICS SYSTEM
      Leakage is a property of the relationship between the prompt SENT and the
      response RECEIVED - only this layer holds both. It carries the same
      observation text and the same reason vocabulary the rest of the pipeline
      uses, and flows into the genome's existing diagnostics field rather than
      into a parallel store.
    """
    observation: str
    channel: str                      # "observations" | "unmatched" | "relationships"
    matched_fragment: str             # the prompt text it reproduced
    classification: str = "prompt_leakage"
    source: str = "model_output"
    excluded_from_genome: bool = True
    excluded_from_discovery: bool = True
    reason: str = "matches_prompt_example"


def _normalize_for_leak_check(text: str) -> str:
    """Casefold, strip punctuation, collapse whitespace.

    Punctuation is stripped because a model reproducing prompt text drops the
    surrounding markdown: the template says "**visibly supported**" and the
    copy comes back "visibly supported". Comparing raw strings would miss the
    reproduction it is supposed to catch. Safe against false positives because
    the corpus is the template only and matches must be LEAK_MIN_LENGTH+.
    """
    cleaned = re.sub(r"[^0-9a-z]+", " ", str(text or "").casefold())
    return " ".join(cleaned.split())


# Below this length a coincidental overlap is likely (vocabulary labels,
# short phrases like "no lettering"). Example sentences are far longer.
LEAK_MIN_LENGTH = 25


def detect_prompt_leakage(
    text: str, prompt_template: str, *, min_length: int = LEAK_MIN_LENGTH,
) -> str | None:
    """Return the reproduced fragment if `text` appears verbatim in the prompt.

    WHY THE TEMPLATE, NOT THE RENDERED PROMPT
      The rendered prompt contains the taxonomy digest - every legitimate Term
      label and synonym. Screening against it would flag "White", "Round" and
      every other correct enum value as leakage, suppressing exactly the
      observations the pipeline exists to capture. The TEMPLATE is the static
      instruction/example text with {{TAXONOMY_DIGEST}} unsubstituted, so
      taxonomy content is structurally excluded from the leak corpus.

    WHY EXACT CONTAINMENT, NOT FUZZY MATCHING
      The requirement is "exactly reproduces prompt/example content". A
      similarity threshold would eventually suppress a genuine observation that
      happens to share wording with an example - a false positive here silently
      deletes real visual data, which is worse than the leak it prevents.
    """
    needle = _normalize_for_leak_check(text)
    if len(needle) < min_length:
        return None
    return needle if needle in _normalize_for_leak_check(prompt_template) else None


def constrained_output_schema() -> dict:
    """The schema handed to a provider for CONSTRAINED DECODING.

    WHY THIS IS NOT tbk_image_schema_v1.json ITSELF
      That file is the full contract, including $schema/$id/const and
      documentation-bearing keywords. Constrained decoding (llama.cpp GBNF
      behind Ollama's `format`) supports a narrower JSON Schema subset. This
      is the same envelope, trimmed to what constrains reliably - it is
      deliberately PERMISSIVE, because the parser above already enforces the
      strict rules (confidence range, value_state consistency). Constraining
      the shape is the provider's job; validating the content is ours.

    ponytail: hand-maintained subset, not a schema-downgrade transform. Two
    consumers, one shape. Write the transform if a third format appears.
    """
    return {
        "type": "object",
        "required": ["observations", "unmatched"],
        "properties": {
            "observations": {"type": "array", "items": {
                "type": "object",
                # `value` is REQUIRED here even though the full contract lets
                # it be absent: without it a constrained model happily emits
                # value_state "present" with no value (observed live on
                # qwen2.5vl:3b), which the parser then has to degrade to
                # "unknown" - losing a real observation to a schema gap rather
                # than to genuine uncertainty. Requiring the key costs nothing;
                # null is still a legal value for it.
                "required": ["group", "attribute", "value", "value_state"],
                "properties": {
                    "group": {"type": "string"},
                    "attribute": {"type": "string"},
                    "value": {"type": ["string", "number", "boolean", "null"]},
                    "value_state": {"type": "string", "enum": list(_VALUE_STATES)},
                    "confidence": {"type": ["number", "null"]},
                    "evidence": {"type": ["string", "null"]},
                }}},
            "unmatched": {"type": "array", "items": {
                "type": "object",
                "required": ["observed", "why_unmatched"],
                "properties": {
                    "observed": {"type": "string"},
                    "why_unmatched": {"type": "string"},
                    "closest_group": {"type": ["string", "null"]},
                    "closest_attribute": {"type": ["string", "null"]},
                    "suggested_kind": {"type": ["string", "null"]},
                    "suggested_label": {"type": ["string", "null"]},
                    "confidence": {"type": ["number", "null"]},
                }}},
            "relationships": {"type": "array", "items": {
                "type": "object",
                "required": ["type", "source", "target"],
                "properties": {
                    "type": {"type": "string"},
                    "source": {"type": "string"},
                    "target": {"type": "string"},
                    "confidence": {"type": ["number", "null"]},
                    "evidence": {"type": ["string", "null"]},
                }}},
            "unparsed": {"type": "array", "items": {"type": "string"}},
        },
    }


def _coerce_confidence(raw: Any) -> float | None:
    """Out-of-range or non-numeric confidence becomes None rather than
    raising or clamping. Clamping would silently manufacture a score the model
    did not give; None is honest and the record survives."""
    if raw is None or isinstance(raw, bool):
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if 0.0 <= value <= 1.0 else None


def _coerce_value_state(raw: Any, value: Any) -> str:
    """Trust the model's value_state only when it is one of the three legal
    values AND consistent with `value`. Anything else degrades to 'unknown' -
    never to 'present', which would assert a fact the pipeline cannot back."""
    state = raw if raw in _VALUE_STATES else None
    if state is None:
        return "present" if value not in (None, "") else "unknown"
    if state == "present" and value in (None, ""):
        return "unknown"
    return state


def extract_json_object(text: str) -> dict | None:
    """Pull the first complete JSON object out of a provider response.

    ponytail: brace-balance scan, not a full parser. Vision models routinely
    wrap JSON in ```json fences or a sentence of preamble despite being told
    not to; this handles both without a dependency. Returns None rather than
    raising - the caller turns that into a parse_error record.
    """
    if not text:
        return None
    fenced = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text
    start = candidate.find("{")
    if start == -1:
        return None
    depth, in_string, escaped = 0, False, False
    for index in range(start, len(candidate)):
        char = candidate[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                try:
                    parsed = json.loads(candidate[start:index + 1])
                except json.JSONDecodeError:
                    return None
                return parsed if isinstance(parsed, dict) else None
    return None


def parse_extraction(
    raw_text: str,
    *,
    image_id: str,
    taxonomy_version: str,
    schema_version: str,
    prompt_version: str | None = None,
    provider: str | None = None,
    model: str | None = None,
    model_version: str | None = None,
    extracted_at: str | None = None,
    prompt_template: str | None = None,
) -> ExtractionResult:
    """Provider text -> ExtractionResult. Never raises on bad model output.

    prompt_template enables prompt-leakage screening (defect D-3): a model that
    reproduces example text instead of describing the image has its output
    routed to `leaked` rather than into the observation stream. Screening is
    skipped when no template is supplied, so a caller replaying a fixture
    without the prompt still parses normally.
    """
    meta = dict(
        image_id=image_id, taxonomy_version=taxonomy_version, schema_version=schema_version,
        prompt_version=prompt_version, provider=provider, model=model,
        model_version=model_version, extracted_at=extracted_at, raw_response=raw_text,
    )
    payload = extract_json_object(raw_text)
    if payload is None:
        # A parse failure is data. The raw response is preserved on the record
        # so the extraction is re-derivable once the prompt is corrected.
        return ExtractionResult(
            **meta, parse_ok=False,
            unparsed=(raw_text,) if raw_text else (),
        )

    leaked: list[LeakageRecord] = []
    observations = []
    for item in payload.get("observations") or []:
        if not isinstance(item, dict) or not item.get("group") or not item.get("attribute"):
            continue
        value = item.get("value")
        state = _coerce_value_state(item.get("value_state"), value)
        if prompt_template:
            # An observation whose EVIDENCE is copied prompt text is not an
            # observation of this image, whatever value it asserts.
            fragment = detect_prompt_leakage(item.get("evidence") or "", prompt_template)
            if fragment:
                leaked.append(LeakageRecord(
                    observation=f"{item['group']}.{item['attribute']} = {value!r}"
                                f" | evidence: {item.get('evidence')}",
                    channel="observations", matched_fragment=fragment,
                ))
                continue
        observations.append(RawObservation(
            group=str(item["group"]),
            attribute=str(item["attribute"]),
            value=value if state == "present" else None,
            value_state=state,
            # Confidence is meaningless unless a value is actually present -
            # Confidence_Standard.md. Enforced here, not left to the model.
            confidence=_coerce_confidence(item.get("confidence")) if state == "present" else None,
            evidence=item.get("evidence"),
            data_type=item.get("data_type"),
            vocabulary=item.get("vocabulary"),
            region=item.get("region") if isinstance(item.get("region"), dict) else None,
            entity_type=item.get("entity_type") or "image",
        ))

    unmatched = []
    for item in payload.get("unmatched") or []:
        if not isinstance(item, dict) or not item.get("observed"):
            continue
        if prompt_template:
            # The channel D-3 actually corrupted: all three canonical images
            # returned the prompt's own unmatched example, verbatim.
            fragment = next(
                (f for f in (
                    detect_prompt_leakage(item.get("observed") or "", prompt_template),
                    detect_prompt_leakage(item.get("why_unmatched") or "", prompt_template),
                ) if f), None,
            )
            if fragment:
                leaked.append(LeakageRecord(
                    observation=str(item["observed"]), channel="unmatched",
                    matched_fragment=fragment,
                ))
                continue
        unmatched.append(UnmatchedObservation(
            observed=str(item["observed"]),
            why_unmatched=str(item.get("why_unmatched") or "no reason supplied by the model"),
            closest_group=item.get("closest_group"),
            closest_attribute=item.get("closest_attribute"),
            closest_term=item.get("closest_term"),
            suggested_kind=item.get("suggested_kind"),
            suggested_label=item.get("suggested_label"),
            confidence=_coerce_confidence(item.get("confidence")),
            region=item.get("region") if isinstance(item.get("region"), dict) else None,
        ))

    relationships = []
    for item in payload.get("relationships") or []:
        if not (isinstance(item, dict) and item.get("type")
                and item.get("source") and item.get("target")):
            continue
        if prompt_template:
            fragment = detect_prompt_leakage(item.get("evidence") or "", prompt_template)
            if fragment:
                leaked.append(LeakageRecord(
                    observation=f"{item['source']} -{item['type']}-> {item['target']}",
                    channel="relationships", matched_fragment=fragment,
                ))
                continue
        relationships.append(RawRelationship(
            type=str(item["type"]), source=str(item["source"]), target=str(item["target"]),
            confidence=_coerce_confidence(item.get("confidence")), evidence=item.get("evidence"),
        ))

    unparsed = [str(u) for u in (payload.get("unparsed") or []) if u]

    return ExtractionResult(
        **meta,
        observations=tuple(observations),
        unmatched=tuple(unmatched),
        relationships=tuple(relationships),
        unparsed=tuple(unparsed),
        leaked=tuple(leaked),
        parse_ok=True,
    )
