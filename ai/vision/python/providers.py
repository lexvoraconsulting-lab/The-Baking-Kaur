"""
Vision provider abstraction.

WHY
  test_vision.py originally called Ollama directly. This layer separates
  "call a vision model" from "which vision model" so a second backend
  (Google, OpenAI, Claude) can be added later as one new class + one new
  branch in get_provider() - no changes to pipeline.py or test_vision.py.

WHY analyze() RETURNS ProviderResponse, NOT A BARE STRING
  ai.pricing (see docs/AI/PricingService.md) requires token usage to be
  captured "always... from the provider response" - a bare string return
  type has nowhere to carry that. ProviderResponse.input_tokens/output_tokens
  come straight from the provider's own response body (Ollama's
  prompt_eval_count/eval_count today), never estimated. This module has no
  dependency on ai.pricing itself - pipeline.py is what turns a
  ProviderResponse into an ai.pricing.TokenUsage, keeping "which provider was
  called" and "what did it cost" as separate concerns.
"""
import base64
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    input_tokens: int
    output_tokens: int


class VisionProvider(ABC):
    @abstractmethod
    def analyze(
        self, image_bytes: bytes, prompt: str, *, timeout: int,
        response_format: dict | None = None,
    ) -> ProviderResponse:
        """Send image + prompt to the model, return its text response plus
        the token usage the provider itself reported for the call.

        response_format is an optional JSON Schema for CONSTRAINED DECODING.
        docs/AI/VisionExtractionContract.md section 5 makes structured output
        mandatory: without it a small model reliably returns a single bare
        observation instead of the two-channel envelope (observed live on
        qwen2.5vl:3b, 2026-08-20). A provider that cannot constrain output
        ignores this argument rather than failing - the parser degrades to a
        parse_error record, which is data, not an exception."""


class OllamaProvider(VisionProvider):
    def __init__(self, url: str, model: str, options: dict | None = None,
                 keep_alive: str | None = None, think: bool | None = None):
        self.url = url
        self.model = model
        # num_predict / num_ctx etc. Ollama's default num_predict truncates a
        # structured response mid-JSON (observed live: 1053 chars, cut inside
        # the unmatched array). Externalised to config rather than hardcoded -
        # the right value depends on taxonomy size, which grows.
        self.options = options or {}
        self.keep_alive = keep_alive
        # Reasoning models (qwen3.5 family) route their output into the
        # response's `thinking` field. Combined with structured output
        # (`format`), `response` comes back EMPTY - measured live 2026-08-20 on
        # qwen3.5:4b: format on + think on => response 0 chars / thinking 2106;
        # format on + think off => response 2104 chars, valid envelope.
        # Sent only when explicitly configured, so non-reasoning models
        # (qwen2.5vl) are unaffected.
        self.think = think

    def analyze(
        self, image_bytes: bytes, prompt: str, *, timeout: int,
        response_format: dict | None = None,
    ) -> ProviderResponse:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
        }
        if response_format is not None:
            # Ollama accepts a JSON Schema here and constrains decoding to it.
            payload["format"] = response_format
        if self.options:
            payload["options"] = self.options
        if self.think is not None:
            payload["think"] = self.think
        if self.keep_alive:
            # Without this Ollama evicts the model after ~5 min idle, and the
            # next call pays a full cold load. Observed live: a 3.2 GB reload
            # blew a 300 s read timeout between two runs of the same test.
            payload["keep_alive"] = self.keep_alive
        response = requests.post(self.url, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        # prompt_eval_count/eval_count are Ollama's own reported token counts
        # for this exact call (/api/generate, non-streaming) - not always
        # present on every Ollama version, so default to 0 rather than raise.
        return ProviderResponse(
            text=data["response"],
            input_tokens=data.get("prompt_eval_count", 0),
            output_tokens=data.get("eval_count", 0),
        )


def get_provider(cfg: dict) -> VisionProvider:
    name = cfg["provider"]["name"]
    if name == "ollama":
        return OllamaProvider(
            url=cfg["provider"]["url"], model=cfg["provider"]["model"],
            options=cfg["provider"].get("options"),
            keep_alive=cfg["provider"].get("keep_alive"),
            think=cfg["provider"].get("think"),
        )
    raise ValueError(f"Unknown vision provider: {name}")
