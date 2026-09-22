"""End-to-end MSIT 3-stage inference pipeline (paper Section 3.4).

  Stage 1: Batch Attribute Generation   -> attribute-value pairs
  Stage 2: Filtering Repeated Attributes -> rule-based dedup (word2vec)
  Stage 3: Sequential Attribute Inference with 5-step CoT -> validated set
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..config import MSITConfig
from .stage1_batch_gen import Stage1BatchGenerator
from .stage2_dedup import Stage2RepeatedAttributeFilter, SimilarityFn
from .stage3_cot_infer import Stage3CoTValidator


@dataclass
class MSITInferencePipeline:
    """Orchestrates the three inference stages over a single fine-tuned backend."""

    backend: Any  # MLLMBackend protocol (the LoRA-fine-tuned MLLM)
    cfg: MSITConfig = field(default_factory=MSITConfig)
    sim_fn: Optional[SimilarityFn] = None

    def __post_init__(self):
        self.stage1 = Stage1BatchGenerator(self.backend, self.cfg)
        self.stage2 = Stage2RepeatedAttributeFilter(self.cfg, sim_fn=self.sim_fn)
        self.stage3 = Stage3CoTValidator(self.backend, self.cfg)

    def run(
        self,
        title: str,
        bullet_point: str,
        image: Optional[Any] = None,
        rng: Any = None,
    ) -> Dict[str, Any]:
        """Run all three stages for one product and return the mined attributes."""
        batch = self.stage1.run(title, bullet_point, image=image, rng=rng)
        filtered = self.stage2.filter(batch)
        validated, traces = self.stage3.run(
            title, bullet_point, filtered, image=image, rng=rng
        )
        return {
            "attributes": validated,
            "stage1_raw": batch,
            "stage2_filtered": filtered,
            "stage3_traces": traces,
        }
