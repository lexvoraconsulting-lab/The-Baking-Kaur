"""
Vision pipeline orchestration: load image + prompt, call the configured
provider, return a VisionResult carrying the response plus identity/version
metadata every downstream module (embeddings, OCR, vector DB, Shopify sync,
ERP, CRM, JARVIS) is expected to key off. See docs/AI/VisionPipeline.md.

WHY THIS MODULE, NOT providers.py, IMPORTS ai.pricing
  providers.py only knows how to call a specific vision backend; it has no
  business constructing a cross-cutting TokenUsage/CostResult. This module
  already orchestrates "provider response -> VisionResult" and is the
  natural place to also do "provider response -> recorded, priced usage" -
  see docs/AI/PricingService.md.
"""
import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ai.pricing import AuditEngine, CostResult, PricingService, TokenUsage
from ai.vision.python.providers import get_provider

_FALLBACK_PROMPT = """
You are an expert cake designer.

Analyse ONLY what is visible.

Do not guess.

Describe:

- Product Type
- Shape
- Colours
- Decorations
- Flowers
- Theme
- Style
- Packaging
- Visible Text
"""


@dataclass(frozen=True)
class VisionResult:
    image_id: str
    image_path: str
    schema_version: str
    taxonomy_version: str
    provider_name: str
    model: str
    response: str
    token_usage: TokenUsage
    cost: CostResult


def compute_image_id(image_bytes: bytes) -> str:
    """Permanent, deterministic per-image identifier (TBK_IMAGE_ID). Content
    hash, not a random UUID or counter - reprocessing the same image file
    always yields the same ID, with no registry/database required."""
    return "TBK-" + hashlib.sha256(image_bytes).hexdigest()[:16]


def _load_prompt(prompt_file: str) -> str:
    text = Path(prompt_file).read_text().strip()
    if text:
        return text
    # ponytail: extractor_v1.md is an intentionally-empty placeholder this
    # phase (content authoring is out of scope) - fall back to the known-good
    # inline prompt so the smoke test keeps working. Delete this fallback once
    # the prompt file is authored.
    return _FALLBACK_PROMPT


def run_vision_pipeline(cfg: dict) -> VisionResult:
    image_path = Path(cfg["image_path"])
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image_bytes = image_path.read_bytes()
    prompt = _load_prompt(cfg["prompt_file"])
    provider = get_provider(cfg)
    provider_response = provider.analyze(image_bytes, prompt, timeout=cfg["provider"]["timeout"])

    usage = TokenUsage(
        provider=cfg["provider"]["name"],
        model=cfg["provider"]["model"],
        input_tokens=provider_response.input_tokens,
        output_tokens=provider_response.output_tokens,
        recorded_at=datetime.now(UTC).isoformat(),
    )
    cost = PricingService().calculate_cost(usage)
    AuditEngine().record(usage, cost)  # always records usage, even if cost is Pending

    return VisionResult(
        image_id=compute_image_id(image_bytes),
        image_path=str(image_path),
        schema_version=cfg["schema_version"],
        taxonomy_version=cfg["taxonomy_version"],
        provider_name=cfg["provider"]["name"],
        model=cfg["provider"]["model"],
        response=provider_response.text,
        token_usage=usage,
        cost=cost,
    )
