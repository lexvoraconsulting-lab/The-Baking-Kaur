"""
Vision provider abstraction.

WHY
  test_vision.py originally called Ollama directly. This layer separates
  "call a vision model" from "which vision model" so a second backend
  (Google, OpenAI, Claude) can be added later as one new class + one new
  branch in get_provider() - no changes to pipeline.py or test_vision.py.
"""
import base64
from abc import ABC, abstractmethod

import requests


class VisionProvider(ABC):
    @abstractmethod
    def analyze(self, image_bytes: bytes, prompt: str, *, timeout: int) -> str:
        """Send image + prompt to the model, return its raw text response."""


class OllamaProvider(VisionProvider):
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    def analyze(self, image_bytes: bytes, prompt: str, *, timeout: int) -> str:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
        }
        response = requests.post(self.url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()["response"]


def get_provider(cfg: dict) -> VisionProvider:
    name = cfg["provider"]["name"]
    if name == "ollama":
        return OllamaProvider(url=cfg["provider"]["url"], model=cfg["provider"]["model"])
    raise ValueError(f"Unknown vision provider: {name}")
