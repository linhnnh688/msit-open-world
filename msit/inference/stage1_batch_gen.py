"""Stage 1: Batch Attribute Generation (paper Section 3.4).

"The fine-tuned MLLM generates attributes for a given sample ... to produce a
batch of relevant attributes. We extract a set of normalized attributes and
values from the output texts."
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..prompts.inference_prompts import build_stage1_prompt
from ..utils.json_parser import parse_attributes
from ..config import MSITConfig


@dataclass
class Stage1BatchGenerator:
    backend: Any  # MLLMBackend protocol
    cfg: MSITConfig = field(default_factory=MSITConfig)

    def run(
        self,
        title: str,
        bullet_point: str,
        image: Optional[Any] = None,
        rng: Any = None,
    ) -> Dict[str, Any]:
        """Generate a batch of attribute-value pairs for one product."""
        prompt = build_stage1_prompt(title, bullet_point, rng=rng)
        raw = self.backend.generate(
            prompt,
            image=image,
            temperature=self.cfg.temperature,
            top_p=self.cfg.top_p,
            max_new_tokens=self.cfg.max_new_tokens,
        )
        return parse_attributes(raw)
