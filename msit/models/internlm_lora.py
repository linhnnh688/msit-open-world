"""InternLM-XComposer2 LoRA-fine-tuned backend (paper: MSIT(InternLM))."""

from typing import Any, Optional

from .lora_trainer import LoRATrainer
from ..config import MSITConfig


class InternLMLoRABackend:
    model_name_or_path: str = "internlm/internlm-xcomposer2-7b"

    def __init__(self, cfg: Optional[MSITConfig] = None, lora_weights: Optional[str] = None):
        self.cfg = cfg or MSITConfig()
        self.trainer = LoRATrainer(self.model_name_or_path, self.cfg)
        self.lora_weights = lora_weights
        self._model = None
        self._tokenizer = None

    def load(self) -> None:  # pragma: no cover - requires GPU
        self._model = self.trainer.load_model()
        try:
            from transformers import AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name_or_path, trust_remote_code=True
            )
        except ImportError as e:
            raise ImportError("transformers is required to load InternLM.") from e

    def generate(
        self,
        prompt: str,
        image: Optional[Any] = None,
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_new_tokens: int = 512,
    ) -> str:
        if self._model is None:
            raise RuntimeError("InternLMLoRABackend.generate() called before load().")
        import torch  # pragma: no cover

        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        with torch.no_grad():
            out = self._model.generate(
                **inputs,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
                do_sample=True,
            )
        return self._tokenizer.decode(out[0], skip_special_tokens=True)
