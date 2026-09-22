"""LLaVA-7B LoRA-fine-tuned backend (paper: MSIT(LLaVA-7B)).

Loading is import-guarded so the module can be imported on CPU-only machines
for tests; `generate()` raises a clear error unless the model is loaded.
"""

from typing import Any, Optional

from .lora_trainer import LoRATrainer
from ..config import MSITConfig


class LLaVALoRABackend:
    model_name_or_path: str = "liuhaotian/llava-v1.5-7b"

    def __init__(self, cfg: Optional[MSITConfig] = None, lora_weights: Optional[str] = None):
        self.cfg = cfg or MSITConfig()
        self.trainer = LoRATrainer(self.model_name_or_path, self.cfg)
        self.lora_weights = lora_weights
        self._model = None
        self._processor = None

    def load(self) -> None:
        """Load base model + LoRA adapter (requires GPU + transformers/peft)."""
        self._model = self.trainer.load_model()
        try:
            from transformers import AutoProcessor

            self._processor = AutoProcessor.from_pretrained(self.model_name_or_path)
        except ImportError as e:  # pragma: no cover
            raise ImportError("transformers is required to load LLaVA.") from e

    def generate(
        self,
        prompt: str,
        image: Optional[Any] = None,
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_new_tokens: int = 512,
    ) -> str:
        if self._model is None:
            raise RuntimeError(
                "LLaVALoRABackend.generate() called before load(). "
                "On CPU-only machines use MockMLLMBackend instead."
            )
        import torch  # pragma: no cover

        inputs = self._processor(text=prompt, images=image, return_tensors="pt").to(
            self._model.device
        )
        with torch.no_grad():
            out = self._model.generate(
                **inputs,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
                do_sample=True,
            )
        return self._processor.decode(out[0], skip_special_tokens=True)
