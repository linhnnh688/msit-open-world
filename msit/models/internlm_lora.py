"""InternLM-XComposer2 LoRA-fine-tuned backend (paper: MSIT(InternLM))."""

from typing import Any, List, Optional

from .lora_trainer import LoRATrainer, build_prompt
from ..config import MSITConfig


class InternLMLoRABackend:
    model_name_or_path: str = "internlm/internlm-xcomposer2-7b"

    def __init__(
        self,
        cfg: Optional[MSITConfig] = None,
        lora_weights: Optional[str] = None,
        target_modules: Optional[List[str]] = None,
    ):
        self.cfg = cfg or MSITConfig()
        self.trainer = LoRATrainer(
            self.model_name_or_path,
            self.cfg,
            use_causal_lm=True,
            target_modules=target_modules,
        )
        self.lora_weights = lora_weights
        self._model = None
        self._tokenizer = None

    def load(self) -> None:  # pragma: no cover - requires GPU
        if self.lora_weights:
            from peft import PeftModel

            base = self.trainer.load_model(apply_lora=False)
            self._model = PeftModel.from_pretrained(base, self.lora_weights)
        else:
            self._model = self.trainer.load_model()
        self._tokenizer = self.trainer.load_processor()

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


__all__ = ["InternLMLoRABackend", "build_prompt"]
