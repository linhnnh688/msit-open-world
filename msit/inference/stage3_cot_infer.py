"""Stage 3: Sequential Attribute Inference with 5-step CoT (paper Section 3.4).

"The final stage sequentially inputs each filtered attribute into the MLLM
for inference using the 5-step CoT process. Whether an attribute is reserved
is determined by the yes or no output in the last step of CoT."
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..prompts.inference_prompts import build_stage3_prompt
from ..config import MSITConfig


def parse_conclusion(output: str) -> Optional[bool]:
    """Parse the final yes/no of the 5-step CoT trace (Appendix A.3 Step 5:
    'Please mark the last paragraph with yes or no.')."""
    tail = output.strip().lower()
    last_par = tail.split("\n")[-1]
    if "conclusion" in last_par:
        last_par = last_par.split("conclusion", 1)[-1]
    last_par = last_par.strip().strip(".!")
    if last_par == "yes":
        return True
    if last_par == "no":
        return False
    # Fallback: search the final paragraph for yes/no keywords.
    if " yes" in f" {last_par}" and "no" not in last_par:
        return True
    if last_par.startswith("no"):
        return False
    return None


@dataclass
class Stage3CoTValidator:
    backend: Any  # MLLMBackend protocol (fine-tuned MLLM)
    cfg: MSITConfig = field(default_factory=MSITConfig)

    def validate_attribute(
        self,
        title: str,
        bullet_point: str,
        attribute: str,
        image: Optional[Any] = None,
        rng: Any = None,
    ) -> Tuple[bool, str]:
        """Run the 5-step CoT for one attribute.

        Returns (kept, raw_reasoning). `kept` is True iff the final CoT step
        concludes "yes". A None conclusion (unparseable) conservatively
        drops the attribute (precision-oriented, matching the paper's goal
        of self-correcting false positives).
        """
        prompt = build_stage3_prompt(title, bullet_point, attribute, rng=rng)
        raw = self.backend.generate(
            prompt,
            image=image,
            temperature=self.cfg.temperature,
            top_p=self.cfg.top_p,
            max_new_tokens=self.cfg.max_new_tokens,
        )
        conclusion = parse_conclusion(raw)
        return (conclusion is True, raw)

    def run(
        self,
        title: str,
        bullet_point: str,
        attributes: Dict[str, Any],
        image: Optional[Any] = None,
        rng: Any = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Sequentially validate every attribute from Stages 1+2.

        Returns (validated_attributes, traces) where traces keeps the raw
        5-step reasoning per attribute (for analysis, cf. paper Figure 7).
        """
        kept: Dict[str, Any] = {}
        traces: List[Dict[str, Any]] = []
        for attr, value in attributes.items():
            kept_flag, raw = self.validate_attribute(
                title, bullet_point, attr, image=image, rng=rng
            )
            traces.append({"attribute": attr, "kept": kept_flag, "reasoning": raw})
            if kept_flag:
                kept[attr] = value
        return kept, traces
