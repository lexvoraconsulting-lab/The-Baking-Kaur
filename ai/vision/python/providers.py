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
    def analyze(self, image_bytes: bytes, prompt: str, *, timeout: int) -> ProviderResponse:
        """Send image + prompt to the model, return its text response plus
        the token usage the provider itself reported for the call."""


class OllamaProvider(VisionProvider):
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    def analyze(self, image_bytes: bytes, prompt: str, *, timeout: int) -> ProviderResponse:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
        }
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
        return OllamaProvider(url=cfg["provider"]["url"], model=cfg["provider"]["model"])
    raise ValueError(f"Unknown vision provider: {name}")
