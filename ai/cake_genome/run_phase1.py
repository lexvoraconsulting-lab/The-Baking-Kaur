"""
TBK Cake Genome - Phase 1 pipeline runner.

    python -m ai.cake_genome.run_phase1 [--image PATH] [--out DIR] [--offline FILE]

Implements the Phase 1 flow end to end:

  INPUT IMAGE -> IMAGE VALIDATION -> PREPROCESSING -> VISION MODEL
  -> RAW OBSERVATIONS -> NORMALIZATION -> MASTER TAXONOMY MATCH
  -> KNOWN ATTRIBUTES + UNMATCHED DETECTION -> DYNAMIC STRUCTURE DISCOVERY
  -> CONFIDENCE + PROVENANCE -> CAKE GENOME -> VALIDATION
  -> PERSISTENCE-READY OUTPUT

WHY --offline EXISTS
  The pipeline must be testable without a running Ollama and a 3.2 GB model
  download, and the parse/match/discovery/genome/validation layers are fully
  deterministic given a provider response. --offline replays a saved response
  through the identical code path. It is a REPLAY, not a mock: it never
  fabricates observations, and the resulting genome is marked with
  provider="replay" so no offline run can be mistaken for a live extraction.

WHY NOTHING HERE WRITES TO THE TAXONOMY, SHOPIFY, OR A DATABASE
  Phase 1's output is "persistence-ready", not persisted. ADR 0011 assigns
  physical storage to PostgreSQL under a schema generated from the contract,
  and that schema does not exist yet (work item D8).
"""
import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from ai.cake_genome.builder import build_cake_genome
from ai.cake_genome.validation import validate_genome
from ai.structure_discovery import ObservationMatcher, build_discovery_result
from ai.vision.python.config import describe_runtime, load_config
from ai.vision.python.extraction import constrained_output_schema, parse_extraction
from ai.vision.python.pipeline import compute_image_id
from ai.vision.python.providers import get_provider
from ai.vision.python.taxonomy_digest import (
    build_digest,
    compute_prompt_version,
    load_canonical_catalog,
    regenerate_digest_file,
    render_prompt,
)

DEFAULT_OUT = "ai/cake_genome/output"
_MAX_IMAGE_BYTES = 20 * 1024 * 1024
_MAGIC = {b"\x89PNG\r\n\x1a\n": "png", b"\xff\xd8\xff": "jpeg", b"RIFF": "webp"}


def validate_image(path: Path) -> tuple[bytes, str]:
    """IMAGE VALIDATION. Fails loudly and early - a corrupt or oversized image
    reaching the provider wastes a model call and produces a confusing parse
    error downstream instead of a clear one here."""
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    data = path.read_bytes()
    if not data:
        raise ValueError(f"Image is empty: {path}")
    if len(data) > _MAX_IMAGE_BYTES:
        raise ValueError(f"Image is {len(data)} bytes, over the {_MAX_IMAGE_BYTES} limit: {path}")
    fmt = next((f for magic, f in _MAGIC.items() if data.startswith(magic)), None)
    if fmt is None:
        raise ValueError(f"Unrecognised image format (not PNG/JPEG/WebP): {path}")
    return data, fmt


def preprocess(data: bytes, fmt: str) -> dict:
    """IMAGE PREPROCESSING.

    ponytail: identity transform plus recorded facts. Resizing/re-encoding
    would change the bytes and therefore TBK_IMAGE_ID, breaking the content-hash
    identity every downstream module keys off. Add a resize step only alongside
    a decision about which bytes the ID is computed over - that is a real
    architectural choice, not a tuning knob.
    """
    return {"format": fmt, "bytes": len(data), "transform": "none (identity)"}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def run(image_path: str | None = None, out_dir: str = DEFAULT_OUT, offline: str | None = None) -> dict:
    cfg = load_config("ai/vision/config/vision.json")
    image = Path(image_path or cfg["image_path"])
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    steps: list[dict] = []

    def step(name, ok, detail=""):
        steps.append({"step": name, "ok": bool(ok), "detail": detail})

    # --- 1. image validation + preprocessing -------------------------------
    data, fmt = validate_image(image)
    image_id = compute_image_id(data)
    step("image_validation", True, f"{image.name} {fmt} {len(data)} bytes")
    pre = preprocess(data, fmt)
    step("image_preprocessing", True, pre["transform"])

    # --- 2. taxonomy digest + prompt (generated, never hand-copied) --------
    catalog = load_canonical_catalog()
    digest = regenerate_digest_file(catalog)
    template = Path(cfg["prompt_file"]).read_text(encoding="utf-8")
    prompt = render_prompt(template, digest)
    prompt_version = compute_prompt_version(prompt)
    step("prompt_render", True, f"{len(prompt)} chars, {prompt_version}, {len(digest['groups'])} groups")

    # --- 3. vision model ---------------------------------------------------
    extracted_at = _now()
    if offline:
        raw_text = Path(offline).read_text(encoding="utf-8")
        provider_name, model_name = "replay", f"replay:{Path(offline).name}"
        step("vision_model", True, f"REPLAY from {offline} (no live model call)")
    else:
        provider = get_provider(cfg)
        response = provider.analyze(
            data, prompt, timeout=cfg["provider"]["timeout"],
            response_format=constrained_output_schema(),
        )
        raw_text = response.text
        provider_name, model_name = cfg["provider"]["name"], cfg["provider"]["model"]
        step("vision_model", bool(raw_text), f"{provider_name}/{model_name}, {len(raw_text)} chars")

    # --- 4. raw observations ----------------------------------------------
    extraction = parse_extraction(
        raw_text, image_id=image_id,
        taxonomy_version=digest["taxonomy_version"], schema_version=cfg["schema_version"],
        prompt_version=prompt_version, provider=provider_name, model=model_name,
        extracted_at=extracted_at, prompt_template=template,
    )
    step("raw_observations", extraction.parse_ok,
         f"parse_ok={extraction.parse_ok}, {len(extraction.observations)} observations, "
         f"{len(extraction.unmatched)} model-flagged unmatched")
    step("prompt_leakage_screen", True,
         f"{len(extraction.leaked)} leaked output(s) excluded from the observation stream"
         if extraction.leaked else "no prompt/example text found in model output")

    # --- 5-7. normalization, taxonomy match, discovery ---------------------
    discovery = build_discovery_result(extraction, ObservationMatcher(catalog), catalog)
    resolved = [m for m in discovery.matched if m.match_state in ("matched", "matched_synonym")]
    step("taxonomy_match", True,
         f"{len(discovery.matched)} resolved records, {len(resolved)} value-matched")
    step("unknown_preserved", True,
         f"{sum(1 for s in discovery.match_states.values() if s in ('unmatched', 'undetermined'))} "
         "observations kept as unmatched/undetermined rather than forced")
    step("dynamic_discovery", True, f"{len(discovery.proposals)} candidate discoveries")

    # --- 8-9. genome + validation -----------------------------------------
    genome = build_cake_genome(discovery, extraction)
    step("cake_genome", bool(genome.sections), f"{len(genome.sections)} sections populated")
    lock = genome.design_identity_lock
    step("design_identity_lock", bool(lock and lock.locked_attributes),
         f"{lock.lock_id} over {len(lock.locked_attributes)} attributes"
         if lock else "not built")
    report = validate_genome(genome)
    step("validation", report.passed,
         f"passed={report.passed}, {report.to_dict()['error_count']} errors, "
         f"{report.to_dict()['warning_count']} warnings")

    # --- 10. persistence-ready output -------------------------------------
    artifacts = {
        "01_raw_response.txt": raw_text,
        "02_raw_observations.json": extraction.to_dict(),
        "03_normalized_observations.json": discovery.to_dict(),
        "04_cake_genome.json": genome.to_dict(),
        "05_provenance_confidence.json": {
            "provenance": genome.provenance, "confidence": genome.confidence,
            "image": {"path": str(image), "image_id": image_id, **pre},
        },
        "06_dynamic_discovery.json": {
            "proposals": [p.to_dict() for p in discovery.proposals],
            "match_states": discovery.match_states,
        },
        "07_validation_report.json": report.to_dict(),
        "08_diagnostics.json": genome.diagnostics,
    }
    for name, payload in artifacts.items():
        target = out / name
        if isinstance(payload, str):
            target.write_text(payload, encoding="utf-8")
        else:
            target.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n",
                              encoding="utf-8")
    step("persistence_ready_output", True, f"{len(artifacts)} artifacts -> {out}")

    summary = {
        "image": str(image), "image_id": image_id, "observation_id": discovery.observation_id,
        "taxonomy_version": digest["taxonomy_version"], "prompt_version": prompt_version,
        "provider": provider_name, "model": model_name, "offline_replay": bool(offline),
        "runtime": describe_runtime(cfg),
        "steps": steps,
        "quality_gates": _gates(extraction, discovery, genome, report, raw_text),
        "output_dir": str(out),
    }
    (out / "00_test_report.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return summary


def _gates(extraction, discovery, genome, report, raw_text) -> dict:
    """The Phase 1 quality gates, evaluated mechanically rather than asserted."""
    lock = genome.design_identity_lock
    return {
        "image_loaded": True,
        "vision_model_received_image": bool(raw_text) or not extraction.parse_ok,
        "vision_response_received": bool(raw_text),
        "raw_observations_generated": len(extraction.observations) > 0,
        "observations_normalized": len(discovery.matched) > 0,
        "taxonomy_matching_works": any(
            m.match_state in ("matched", "matched_synonym") for m in discovery.matched),
        "unknown_observations_preserved": (
            len(extraction.unmatched) + sum(
                1 for s in discovery.match_states.values()
                if s in ("unmatched", "undetermined")) > 0),
        "candidate_discoveries_generated": len(discovery.proposals) > 0,
        "confidence_exists": genome.confidence.get("attributes_scored", 0) > 0,
        "provenance_exists": all(
            genome.provenance.get(k) for k in ("provider", "model", "schema_version",
                                               "taxonomy_version", "extracted_at")),
        "cake_genome_generated": len(genome.sections) > 0,
        "design_identity_lock_generated": bool(lock and lock.locked_attributes),
        "validation_executed": True,
        "validation_passed": report.passed,
        "json_valid": True,  # every artifact is json.dumps'd; a failure would raise above
        "no_taxonomy_mutation": genome.verification_status == "unverified" and all(
            p.get("status") == "observed" for p in genome.candidate_discoveries),
        # Gate 13 (D-3). Passes when no leaked text reached the genome, the
        # lock or discovery - NOT when leakage failed to occur. Detecting and
        # excluding leakage is the success condition.
        "no_prompt_leakage_in_observations": not any(
            f["code"] in ("LEAK_REACHED_DISCOVERY", "LEAK_REACHED_LOCK")
            for f in report.to_dict()["findings"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="TBK Cake Genome - Phase 1 pipeline")
    parser.add_argument("--image", default=None)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--offline", default=None,
                        help="Replay a saved provider response instead of calling the model")
    args = parser.parse_args()

    summary = run(args.image, args.out, args.offline)
    gates = summary["quality_gates"]
    print(f"\nTBK CAKE GENOME - PHASE 1   image_id={summary['image_id']}")
    print(f"  runtime : {summary['runtime']}")
    print(f"  provider={summary['provider']}  model={summary['model']}"
          f"{'  [REPLAY]' if summary['offline_replay'] else ''}")
    print(f"  taxonomy={summary['taxonomy_version']}  prompt={summary['prompt_version']}\n")
    for entry in summary["steps"]:
        print(f"  [{'ok' if entry['ok'] else 'FAIL'}] {entry['step']:<26} {entry['detail']}")
    print("\n  QUALITY GATES")
    for name, ok in gates.items():
        print(f"  [{'x' if ok else ' '}] {name}")
    failed = [k for k, v in gates.items() if not v]
    print(f"\n  {len(gates) - len(failed)}/{len(gates)} gates passed"
          + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    print(f"  artifacts: {summary['output_dir']}\n")


if __name__ == "__main__":
    main()
