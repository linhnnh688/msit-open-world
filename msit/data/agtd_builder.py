"""AGTD construction (paper Section 3.1 + Appendix A.1/A.2).

Pipeline per product:
  1. Generate attributes from TEXT only (in-context learning, GPT-4).
  2. Generate attributes from IMAGE only (separate call, avoids the modality
     bias described in Section 3.1).
  3. Manual review hook (paper: "The generated attributes are manually
     reviewed to filter out incorrect attributes") - pluggable `review_fn`.
  4. GPT-4 merges the two attribute sets (Appendix A.2).

Output sample format (Figures 2/7 of the paper):
  {"instruction": <natural language>, "input": title + bullet, "image": <img>,
   "output": {"Attributes": {...}}}
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from ..prompts.agtd_prompts import build_extraction_prompt, build_merge_prompt
from ..utils.json_parser import parse_attributes, format_attributes
from .seed_dataset import SeedDataset

# A manual review callback: receives the raw attribute dict, returns the
# corrected dict. The paper performs this step by hand; here it is a hook so
# the construction pipeline stays faithful and automatable.
ReviewFn = Callable[[Dict[str, Any]], Dict[str, Any]]


def identity_review(attrs: Dict[str, Any]) -> Dict[str, Any]:
    """Default review hook: accept everything (no manual curation)."""
    return attrs


@dataclass
class AGTDBuilder:
    backend: Any  # MLLMBackend protocol (models/base_mllm.py)
    seed: SeedDataset = field(default_factory=SeedDataset.default)
    review_fn: ReviewFn = identity_review
    generation_config: Dict[str, Any] = field(default_factory=dict)

    # -- Step 1 & 2: modality-separated generation -------------------------
    def generate_from_text(self, title: str, bullet_point: str) -> Dict[str, Any]:
        prompt = build_extraction_prompt("text", title, bullet_point)
        out = self.backend.generate(prompt, image=None, **self.generation_config)
        return parse_attributes(out)

    def generate_from_image(self, image: Any, image_caption: Optional[str] = None) -> Dict[str, Any]:
        prompt = build_extraction_prompt("image", title="", bullet_point="", image_caption=image_caption)
        out = self.backend.generate(prompt, image=image, **self.generation_config)
        return parse_attributes(out)

    # -- Step 3: manual review (hook) --------------------------------------
    def review(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        return self.review_fn(attrs)

    # -- Step 4: merge ------------------------------------------------------
    def merge_modalities(
        self,
        image_attributes: Optional[Dict[str, Any]],
        text_attributes: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """GPT-4 merges image/text attribute sets (Appendix A.2).

        Per the paper, if only one modality is provided it is returned
        directly without merging.
        """
        image_attributes = image_attributes or {}
        text_attributes = text_attributes or {}
        if not image_attributes:
            return text_attributes
        if not text_attributes:
            return image_attributes
        prompt = build_merge_prompt(image_attributes, text_attributes)
        out = self.backend.generate(prompt, image=None, **self.generation_config)
        merged = parse_attributes(out)
        return merged

    # -- Full per-product construction --------------------------------------
    def build_sample(
        self,
        title: str,
        bullet_point: str,
        image: Any = None,
        image_caption: Optional[str] = None,
        instruction: str = "Given this product, please generate its attribute-value pairs",
    ) -> Dict[str, Any]:
        """Construct one AGTD tuning sample for a product."""
        text_attrs = self.review(self.generate_from_text(title, bullet_point))
        image_attrs = (
            self.review(self.generate_from_image(image, image_caption)) if image is not None else {}
        )
        merged = self.merge_modalities(image_attrs, text_attrs)
        return {
            "instruction": instruction,
            "input": f"Title: {title}\nBullet point: {bullet_point}",
            "image": image,
            "output": format_attributes(merged),
        }

    def build_batch(
        self, products: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Construct AGTD for a list of products.

        Each product dict: {title, bullet_point, image (optional),
        image_caption (optional)}.
        """
        samples = []
        for p in products:
            samples.append(
                self.build_sample(
                    title=p["title"],
                    bullet_point=p.get("bullet_point", ""),
                    image=p.get("image"),
                    image_caption=p.get("image_caption"),
                )
            )
        return samples
