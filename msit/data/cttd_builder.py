"""CTTD construction (paper Section 3.2 + Appendix A.3).

Builds the 5-step chain-of-thought tuning data with CONTRASTIVE samples:
  - Positive examples: attributes manually reviewed as belonging to the product.
  - Negative examples: attributes randomly chosen from OTHER products.
  - Positive/negative counts are balanced (Section 3.2).

Each sample pairs the Appendix A.3 prompt with the GPT-4-produced 5-step
reasoning trace ending in a final yes/no paragraph.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import random

from ..prompts.cttd_prompts import build_cttd_prompt


@dataclass
class CTTDBuilder:
    backend: Any  # MLLMBackend protocol
    generation_config: Dict[str, Any] = field(default_factory=dict)
    rng: random.Random = field(default_factory=lambda: random.Random(42))

    def build_reasoning(
        self,
        title: str,
        bullet_point: str,
        attribute: str,
        image: Any = None,
        image_caption: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate one 5-step CoT sample for (product, attribute)."""
        prompt = build_cttd_prompt(title, bullet_point, attribute, image_caption)
        output = self.backend.generate(prompt, image=image, **self.generation_config)
        # The final paragraph must be a bare yes / no (Appendix A.3, Step 5).
        label = "yes" if _concludes_yes(output) else "no"
        return {
            "instruction": prompt,
            "input": f"Title: {title}\nBullet point: {bullet_point}",
            "image": image,
            "output": output,
            "label": label,
        }

    def sample_contrastive_negatives(
        self,
        product: Dict[str, Any],
        other_products: List[Dict[str, Any]],
        n: int,
    ) -> List[str]:
        """Sample n negative attributes from OTHER products' attribute pools."""
        pool: List[str] = []
        for p in other_products:
            pool.extend(list(p.get("attributes", {}).keys()))
        pool = [a for a in pool if a not in product.get("attributes", {})]
        if not pool:
            return []
        return self.rng.sample(pool, k=min(n, len(pool)))

    def build_batch(
        self,
        products: List[Dict[str, Any]],
        attributes_per_product: int = 2,
    ) -> List[Dict[str, Any]]:
        """Build a balanced CTTD set.

        Args:
            products: list of {title, bullet_point, image?, image_caption?,
                attributes: {name: value}}. `attributes` are the manually
                reviewed positives from AGTD.
            attributes_per_product: number of positive attributes sampled per
                product (an equal number of negatives is added).
        """
        samples: List[Dict[str, Any]] = []
        for idx, product in enumerate(products):
            others = [p for j, p in enumerate(products) if j != idx]
            positives = list(product.get("attributes", {}).keys())
            self.rng.shuffle(positives)
            chosen_pos = positives[:attributes_per_product]

            for attr in chosen_pos:
                samples.append(
                    self.build_reasoning(
                        title=product["title"],
                        bullet_point=product.get("bullet_point", ""),
                        attribute=attr,
                        image=product.get("image"),
                        image_caption=product.get("image_caption"),
                    )
                )

            negatives = self.sample_contrastive_negatives(
                product, others, n=len(chosen_pos)
            )
            for attr in negatives:
                samples.append(
                    self.build_reasoning(
                        title=product["title"],
                        bullet_point=product.get("bullet_point", ""),
                        attribute=attr,
                        image=product.get("image"),
                        image_caption=product.get("image_caption"),
                    )
                )
        return samples


def _concludes_yes(output: str) -> bool:
    """Detect the final yes/no paragraph (Appendix A.3, Step 5)."""
    tail = output.strip().lower()
    # Look at the last line/paragraph only, as instructed ("No other text is
    # needed in this paragraph").
    last_par = tail.split("\n")[-1]
    if "conclusion" in last_par:
        last_par = last_par.split("conclusion")[-1]
    return "yes" in last_par and "no" not in last_par.replace("yes", "", 1)
