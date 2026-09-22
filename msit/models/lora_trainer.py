"""LoRA fine-tuning of MLLMs (paper Section 3.3).

"The core idea of this method is to freeze the language model and tune only
the rank-decomposition module of the Transformer layer."

Training objective (paper Eq. 1): standard autoregressive LM loss over the
instruction-tuning data D = AGTD ∪ CTTD:
    θ̂ = argmin E_{(I,T,s)∈D} [ -Σ_j log P(s_j | s_<j, I, T; M\θ, θ) ]

Implementation details (Section 4.1): PyTorch, Adam, lr=3e-4, 10 epochs,
one Tesla A100. This module is import-guarded: it only requires
transformers/peft when actually training.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..config import MSITConfig


def build_lora_config(cfg: MSITConfig) -> Any:
    """Build the peft LoRA config (only imported when training)."""
    try:
        from peft import LoraConfig, TaskType
    except ImportError as e:  # pragma: no cover
        raise ImportError(
            "peft is required for LoRA fine-tuning: pip install peft transformers"
        ) from e
    return LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        lora_dropout=cfg.lora_dropout,
        target_modules=cfg.lora_target_modules,
        bias="none",
    )


@dataclass
class LoRATrainer:
    """Generic LoRA trainer for LLaVA / Qwen-VL / InternLM."""

    model_name_or_path: str
    cfg: MSITConfig

    def load_model(self, load_in_4bit: bool = True) -> Any:
        try:
            import torch
            from transformers import AutoModelForVision2Seq, AutoProcessor
            from peft import get_peft_model
        except ImportError as e:  # pragma: no cover
            raise ImportError(
                "Training requires: pip install transformers peft accelerate bitsandbytes"
            ) from e

        model = AutoModelForVision2Seq.from_pretrained(
            self.model_name_or_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            load_in_4bit=load_in_4bit,
        )
        model = get_peft_model(model, build_lora_config(self.cfg))
        model.print_trainable_parameters()
        return model

    def train(self, train_dataset: List[Dict[str, Any]], output_dir: str) -> None:
        """Fine-tune with the paper's hyperparameters.

        train_dataset items follow the AGTD/CTTD sample format produced by
        the builders: {instruction, input, image, output}.
        """
        try:
            import torch
            from transformers import (
                AutoProcessor,
                Trainer,
                TrainingArguments,
            )
        except ImportError as e:  # pragma: no cover
            raise ImportError("Training requires transformers/accelerate.") from e

        model = self.load_model()
        processor = AutoProcessor.from_pretrained(self.model_name_or_path)

        args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.cfg.epochs,
            learning_rate=self.cfg.learning_rate,
            optim=self.cfg.optimizer,
            per_device_train_batch_size=self.cfg.per_device_batch_size,
            gradient_accumulation_steps=self.cfg.gradient_accumulation_steps,
            logging_steps=10,
            save_strategy="epoch",
            bf16=True,
            report_to=[],
            seed=self.cfg.random_seed,
        )

        # Collator: render instruction+input as prompt and output as the
        # completion, masking the prompt tokens in the loss (standard
        # instruction-tuning objective, paper Eq. 1).
        def collate(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
            prompts, completions = [], []
            for item in batch:
                prompts.append(f"{item['instruction']}\n\n{item['input']}")
                completions.append(item["output"])
            enc = processor(
                text=prompts,
                images=[b.get("image") for b in batch],
                padding=True,
                return_tensors="pt",
            )
            comp = processor.tokenizer(
                completions, padding=True, return_tensors="pt"
            )
            labels = comp["input_ids"].clone()
            labels[labels == processor.tokenizer.pad_token_id] = -100
            enc["labels"] = labels
            return enc

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_dataset,
            data_collator=collate,
        )
        trainer.train()
        model.save_pretrained(output_dir)
        processor.save_pretrained(output_dir)
