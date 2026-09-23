"""LoRA fine-tuning of MLLMs (paper Section 3.3).

"The core idea of this method is to freeze the language model and tune only
the rank-decomposition module of the Transformer layer."

Training objective (paper Eq. 1): standard autoregressive LM loss over the
instruction-tuning data D = AGTD ∪ CTTD:
    θ̂ = argmin E_{(I,T,s)∈D} [ -Σ_j log P(s_j | s_<j, I, T; M\θ, θ) ]

Implementation details (Section 4.1): PyTorch, Adam, lr=3e-4, 10 epochs.
This module is import-guarded: it only requires transformers/peft when
actually training.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..config import MSITConfig


def build_prompt(item: Dict[str, Any]) -> str:
    """Render an AGTD/CTTD sample as a training/inference prompt."""
    return f"{item['instruction']}\n\n{item['input']}"


def build_lora_config(
    cfg: MSITConfig, target_modules: Optional[List[str]] = None
) -> Any:
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
        target_modules=target_modules or cfg.lora_target_modules,
        bias="none",
    )


@dataclass
class LoRATrainer:
    """Generic LoRA trainer for LLaVA / Qwen-VL / InternLM."""

    model_name_or_path: str
    cfg: MSITConfig
    use_causal_lm: bool = False
    torch_dtype: str = "float16"
    hf_token: Optional[str] = None
    target_modules: Optional[List[str]] = None
    save_strategy: str = "epoch"

    def _dtype(self) -> Any:
        import torch

        return getattr(torch, self.torch_dtype)

    def load_model(self, load_in_4bit: bool = True, apply_lora: bool = True) -> Any:
        """Load base model (optionally QLoRA-wrapped) for training or inference."""
        try:
            from transformers import AutoModelForCausalLM, AutoModelForVision2Seq
        except ImportError as e:  # pragma: no cover
            raise ImportError(
                "Training requires: pip install transformers peft accelerate bitsandbytes"
            ) from e

        dtype = self._dtype()
        loader = AutoModelForCausalLM if self.use_causal_lm else AutoModelForVision2Seq
        kwargs: Dict[str, Any] = {
            "torch_dtype": dtype,
            "device_map": "auto",
            "trust_remote_code": self.use_causal_lm,
        }
        if self.hf_token:
            kwargs["token"] = self.hf_token
        if load_in_4bit:
            try:
                from transformers import BitsAndBytesConfig
            except ImportError as e:  # pragma: no cover
                raise ImportError("bitsandbytes/transformers required for 4-bit load") from e
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=dtype,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        model = loader.from_pretrained(self.model_name_or_path, **kwargs)

        if load_in_4bit:
            try:
                from peft import prepare_model_for_kbit_training
            except ImportError as e:  # pragma: no cover
                raise ImportError("peft is required for kbit training") from e
            model = prepare_model_for_kbit_training(model)

        model.config.use_cache = False
        model.gradient_checkpointing_enable()

        if apply_lora:
            try:
                from peft import get_peft_model
            except ImportError as e:  # pragma: no cover
                raise ImportError("peft is required for LoRA fine-tuning") from e
            model = get_peft_model(
                model, build_lora_config(self.cfg, self.target_modules)
            )
            model.print_trainable_parameters()
        return model

    def load_processor(self) -> Any:
        """Load AutoProcessor (vision2seq) or AutoTokenizer (causal LM)."""
        try:
            from transformers import AutoProcessor, AutoTokenizer
        except ImportError as e:  # pragma: no cover
            raise ImportError("transformers is required to load the processor.") from e

        kwargs: Dict[str, Any] = {"trust_remote_code": self.use_causal_lm}
        if self.hf_token:
            kwargs["token"] = self.hf_token
        if self.use_causal_lm:
            return AutoTokenizer.from_pretrained(self.model_name_or_path, **kwargs)
        return AutoProcessor.from_pretrained(self.model_name_or_path, **kwargs)

    def train(self, train_dataset: List[Dict[str, Any]], output_dir: str) -> None:
        """Fine-tune with the paper's hyperparameters.

        train_dataset items follow the AGTD/CTTD sample format produced by
        the builders: {instruction, input, image, output}.
        """
        try:
            import torch
            from transformers import Trainer, TrainingArguments
        except ImportError as e:  # pragma: no cover
            raise ImportError("Training requires transformers/accelerate.") from e

        model = self.load_model()
        processor = self.load_processor()
        tok = processor.tokenizer if hasattr(processor, "tokenizer") else processor
        use_fp16 = self.torch_dtype == "float16"
        use_bf16 = self.torch_dtype == "bfloat16"

        args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.cfg.epochs,
            learning_rate=self.cfg.learning_rate,
            optim=self.cfg.optimizer,
            per_device_train_batch_size=self.cfg.per_device_batch_size,
            gradient_accumulation_steps=self.cfg.gradient_accumulation_steps,
            logging_steps=10,
            save_strategy=self.save_strategy,
            fp16=use_fp16,
            bf16=use_bf16,
            report_to=[],
            seed=self.cfg.random_seed,
            gradient_checkpointing=True,
        )

        def collate(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
            """Full-sequence labels with prompt masked (-100), paper Eq. 1."""
            input_ids_list: List[List[int]] = []
            labels_list: List[List[int]] = []
            for item in batch:
                prompt = build_prompt(item)
                p_ids = tok(prompt, add_special_tokens=False)["input_ids"]
                eos = tok.eos_token or ""
                c_ids = tok(
                    item["output"] + eos, add_special_tokens=False
                )["input_ids"]
                input_ids_list.append(p_ids + c_ids)
                labels_list.append([-100] * len(p_ids) + c_ids)

            maxlen = max(len(x) for x in input_ids_list)
            pad_id = (
                tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
            )
            input_ids, labels, attn = [], [], []
            for ids, lab in zip(input_ids_list, labels_list):
                pad = maxlen - len(ids)
                input_ids.append(ids + [pad_id] * pad)
                labels.append(lab + [-100] * pad)
                attn.append([1] * len(ids) + [0] * pad)
            out: Dict[str, Any] = {
                "input_ids": torch.tensor(input_ids),
                "attention_mask": torch.tensor(attn),
                "labels": torch.tensor(labels),
            }
            if not self.use_causal_lm and any(
                item.get("image") is not None for item in batch
            ):
                try:
                    imgs = processor(
                        images=[item.get("image") for item in batch],
                        return_tensors="pt",
                    )
                    if "pixel_values" in imgs:
                        out["pixel_values"] = imgs["pixel_values"]
                except Exception:
                    pass
            return out

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_dataset,
            data_collator=collate,
        )
        trainer.train()
        model.save_pretrained(output_dir)
        processor.save_pretrained(output_dir)
        del trainer, model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("saved ->", output_dir)
