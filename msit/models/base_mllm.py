"""MLLM backend interface.

Every component of MSIT (AGTD/CTTD construction and the 3 inference stages)
talks to a backend through this minimal protocol, so backends are swappable:
  - GPT4Backend: OpenAI GPT-4V (used in the paper to build AGTD/CTTD).
  - LLaVA/Qwen/InternLM LoRA backends: the fine-tuned models used at
    inference time (paper Section 3.3).
  - MockMLLMBackend: deterministic stand-in for tests and demos without a
    GPU or API key.
"""

from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class MLLMBackend(Protocol):
    def generate(
        self,
        prompt: str,
        image: Optional[Any] = None,
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_new_tokens: int = 512,
    ) -> str:
        """Generate text from (prompt, optional image).

        Decoding defaults follow the paper (Section 4.1):
        temperature=0.2, top_p=0.7.
        """
        ...
