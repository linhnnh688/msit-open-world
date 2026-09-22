"""Global configuration for the MSIT reproduction.

All values referenced to the original paper:
  - Liu et al., "Open-World Attribute Mining for E-Commerce Products with
    Multimodal Self-Correction Instruction Tuning", ACL 2025 (Long Papers).

Paper citations for each group of settings:
  - Training (Section 4.1 Implementation Details): Adam, lr=3e-4, 10 epochs,
    one Tesla A100, LoRA fine-tuning.
  - Inference decoding (Section 4.1): top_p sampling, temperature=0.2, top_p=0.7,
    5 independent trials with random seeds.
  - Data sizes (Section 4.1): 1,000 AGTD + 300 CTTD training samples, 1,000 test.
  - Dedup (Appendix B.2): word2vec-google-news-300 cosine similarity with a
    (higher) threshold for single-subword phrases.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class MSITConfig:
    # ---------------- Training (paper Section 4.1) ----------------
    learning_rate: float = 3e-4
    epochs: int = 10
    optimizer: str = "adam"
    per_device_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    # LoRA hyper-parameters (paper does not report them; sensible defaults)
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "v_proj", "k_proj", "o_proj"]
    )

    # ---------------- Inference decoding (paper Section 4.1) ----------------
    temperature: float = 0.2
    top_p: float = 0.7
    max_new_tokens: int = 512
    n_trials: int = 5  # paper reports mean +- std of 5 independent trials
    random_seed: int = 42

    # ---------------- Stage 2 dedup (paper Appendix B.2) ----------------
    # word2vec-google-news-300 cosine-similarity thresholds. The paper only says
    # "set the threshold" and "a higher threshold" for single-subword phrases;
    # these are the reproduction choices.
    similarity_threshold: float = 0.70
    single_subword_threshold: float = 0.85
    word2vec_model: str = "word2vec-google-news-300"

    # ---------------- Data construction (paper Section 4.1) ----------------
    n_agtd_samples: int = 1000
    n_cttd_samples: int = 300
    n_test_samples: int = 1000

    # ---------------- Evaluation ----------------
    # Matching mode: "similar" allows value synonyms; "exact" requires strict
    # consistency with the gold standard (paper Section 4.1).
    match_mode: str = "similar"
