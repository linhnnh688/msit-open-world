"""Deterministic mock MLLM backend for tests and CPU-only demos.

Not part of the paper - it exists so the full MSIT pipeline (Stage 1 -> 2 -> 3,
metrics, tests) can run end-to-end without a GPU or an OpenAI API key. It
imitates a fine-tuned model by:
  - extracting attributes from a keyword table seeded from the product text,
  - answering Stage-3 CoT prompts with a canned 5-step reasoning trace whose
    conclusion follows simple substring matching against the product text.
"""

from typing import Any, Dict, Optional
import json
import re

from ..prompts.cttd_prompts import FIVE_STEP_COT


class MockMLLMBackend:
    def __init__(self, attributes_db: Optional[Dict[str, Dict[str, Any]]] = None):
        """Args:
        attributes_db: optional ground-truth-like table {title: {attr: value}}
            used to answer extraction prompts deterministically.
        """
        self.attributes_db = attributes_db or {}
        self.calls = []  # log of (prompt_kind, attribute) for tests

    # ------------------------------------------------------------------ util
    def _lookup_product(self, prompt: str) -> Dict[str, Any]:
        for title, attrs in self.attributes_db.items():
            if title in prompt:
                return attrs
        return {}

    # -------------------------------------------------------------- generate
    def generate(
        self,
        prompt: str,
        image: Optional[Any] = None,
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_new_tokens: int = 512,
    ) -> str:
        lower = prompt.lower()
        if "merge them into one" in lower:
            return self._answer_merge(prompt)
        if "the attribute i want to judge is" in lower:
            return self._answer_cot(prompt)
        if "json format" in lower or "attribute" in lower:
            return self._answer_extract(prompt)
        return json.dumps({"Attributes": self._lookup_product(prompt)})

    # --------------------------------------------------------- answer types
    def _answer_extract(self, prompt: str) -> str:
        attrs = self._lookup_product(prompt)
        if "image information" in prompt.lower() and not attrs:
            # Image modality: mock sees fewer attributes (modality separation).
            attrs = {}
        return json.dumps({"Attributes": attrs}, ensure_ascii=False)

    def _answer_merge(self, prompt: str) -> str:
        # Parse the two JSON dicts embedded in the merge prompt.
        objs = re.findall(r"\{[^{}]*\}", prompt)
        merged: Dict[str, Any] = {}
        for o in objs:
            try:
                merged.update(json.loads(o))
            except json.JSONDecodeError:
                continue
        return json.dumps({"Attributes": merged}, ensure_ascii=False)

    def _answer_cot(self, prompt: str) -> str:
        m = re.search(r"the attribute i want to judge is (.+)$", prompt, flags=re.IGNORECASE | re.MULTILINE)
        attribute = m.group(1).strip() if m else ""
        title_match = re.search(r"Title: (.+)", prompt)
        bullet_match = re.search(r"Bullet [Pp]oint: (.+)", prompt)
        product_text = " ".join(x for x in [title_match.group(1) if title_match else "",
                                            bullet_match.group(1) if bullet_match else ""] if x)

        attrs = self._lookup_product(prompt)
        if attribute in attrs:
            value = attrs[attribute]
            in_text = str(value).lower() in product_text.lower()
            conclusion = "yes"
            step3 = f"From the image, I can infer that the product appears to have attribute '{attribute}'."
            step4 = (
                f"The text confirms the attribute value: {value}."
                if in_text
                else "The text provided does not explicitly mention this attribute."
            )
        else:
            value = None
            conclusion = "no"
            step3 = "From the image, there is no explicit indication of this attribute."
            step4 = "The text provided does not mention this attribute."

        product_type = "product"
        for cat in ("Tea", "Vitamin", "Sofa", "Phone", "Bread", "Mix"):
            if cat.lower() in product_text.lower():
                product_type = cat
                break

        return (
            f"Step 1 Product Type Narrowing: Based on the image and text, the product is identified as \"{product_type}\".\n"
            f"Step 2 Reasoning with Internal Common-sense Knowledge: The attribute '{attribute}' refers to a characteristic of such products. {'It commonly applies to this product type.' if conclusion == 'yes' else 'It does not typically apply to this product type.'}\n"
            f"Step 3 Image-Based Attribute Validation: {step3}\n"
            f"Step 4 Text-Based Attribute Verification: {step4}\n"
            f"Step 5 Final Evaluation and Decision-Making: Combining the reasoning above, the product {'has' if conclusion == 'yes' else 'does not have'} this attribute.\n"
            f"Conclusion: {conclusion}"
        )
