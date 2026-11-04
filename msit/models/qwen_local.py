"""Qwen2.5-VL 4-bit local generator for AGTD / CTTD labels.

Runs label construction on a single GPU without an API key: loads
Qwen2.5-VL-7B-Instruct in 4-bit (NF4) and provides the same two builders the
data pipeline needs:
  - `generate_agtd_sample`: text attributes + image attributes, then merge
    (mirrors the two-call modality separation of paper Section 3.1).
  - `generate_cttd_sample`: 5-step CoT judgement for one (product, attribute)
    pair (paper Appendix A.3).

Requires: torch, transformers with Qwen2.5-VL support, qwen-vl-utils.
Imports are deferred so the rest of `msit` works on CPU-only environments.
"""

from typing import Any, Dict, Optional
import os

from ..utils.json_parser import parse_attributes

DEFAULT_MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"

AGTD_TEXT_PROMPT = (
    "You are an expert in e-commerce. Extract product attributes and their values from the following text.\n"
    "Title: {title}\nBullet points: {bullet_point}\n\n"
    "Output strictly in JSON format where keys are attribute names and values are attribute values. "
    "Ensure all JSON keys are in lowercase snake_case format (e.g., compatible_phone_model)."
)

AGTD_IMAGE_PROMPT = (
    "Extract visible product attributes (e.g., color, shape, packaging type) directly from this image.\n"
    "Output strictly in JSON format where keys are attribute names and values are attribute values. "
    "Ensure all JSON keys are in lowercase snake_case format."
)

AGTD_MERGE_PROMPT = (
    "Merge the following two JSON objects containing product attributes. "
    "Remove duplicates and keep the most descriptive values.\n"
    "Text attributes: {text_attributes}\nImage attributes: {image_attributes}\n\n"
    "Output the merged result strictly in JSON format. Do not include any other text."
)

CTTD_PROMPT = (
    "Evaluate if the product has the attribute: '{target_attribute}'.\n"
    "Title: {title}\nBullet points: {bullet_point}\n\n"
    "Provide your reasoning strictly in the following 5 steps:\n"
    "Step 1: Determine the type of product based on pictures and text information.\n"
    "Step 2: Analyze the meaning of the attribute and judge whether it matches the product type based on common sense.\n"
    "Step 3: Check if the product exhibits this attribute from the image.\n"
    "Step 4: Check if the product exhibits this attribute from the text description and verify exact value if present.\n"
    "Step 5: Summarize the conclusions and draw the final decision (yes or no).\n"
)


class QwenLocalDataGenerator:
    """Label generator backed by a locally hosted Qwen2.5-VL model."""

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        load_in_4bit: bool = True,
        device: str = "cuda",
        max_new_tokens: int = 512,
        temperature: float = 0.2,
    ):
        import torch
        from transformers import AutoProcessor, BitsAndBytesConfig, Qwen2_5_VLForConditionalGeneration

        print(f"Đang tải mô hình {model_id}... Vui lòng đợi.")
        self._torch = torch
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

        load_kwargs: Dict[str, Any] = {"torch_dtype": torch.float16, "device_map": "auto"}
        if load_in_4bit:
            load_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
            )

        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(model_id, **load_kwargs)
        self.processor = AutoProcessor.from_pretrained(model_id)
        print("Tải mô hình hoàn tất! Sẵn sàng sinh dữ liệu.")

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _clean_json_output(text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    @staticmethod
    def _build_messages(prompt: str, image: Optional[Any] = None) -> list:
        content = []
        if isinstance(image, str):
            if os.path.exists(image):
                content.append({"type": "image", "image": image})
        elif image is not None:
            content.append({"type": "image", "image": image})
        content.append({"type": "text", "text": prompt})
        return [{"role": "user", "content": content}]

    # ------------------------------------------------------------- generation
    def generate(self, prompt: str, image: Optional[Any] = None, is_json: bool = False) -> str:
        """Run one multimodal chat completion (image may be a path or PIL image)."""
        from qwen_vl_utils import process_vision_info

        messages = self._build_messages(prompt, image)
        text_prompt = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=[text_prompt],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to(self.device)

        with self._torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
            )

        trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, generated_ids)]
        output_text = self.processor.batch_decode(
            trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        return self._clean_json_output(output_text) if is_json else output_text.strip()

    # ------------------------------------------------------------- builders
    def generate_agtd_sample(self, title: str, bullet_point: str, image_path: str) -> Dict[str, Any]:
        """Extract text and image attributes separately, then merge them."""
        text_prompt = AGTD_TEXT_PROMPT.format(title=title, bullet_point=bullet_point)
        text_attributes = self.generate(prompt=text_prompt, is_json=True)

        image_attributes = "{}"
        if image_path and os.path.exists(image_path):
            image_attributes = self.generate(
                prompt=AGTD_IMAGE_PROMPT, image=image_path, is_json=True
            )

        merge_prompt = AGTD_MERGE_PROMPT.format(
            text_attributes=text_attributes, image_attributes=image_attributes
        )
        merged_attributes = self.generate(prompt=merge_prompt, is_json=True)

        return {
            "title": title,
            "bullet_point": bullet_point,
            "image_path": image_path,
            "attributes": parse_attributes(merged_attributes),
        }

    def generate_cttd_sample(
        self, title: str, bullet_point: str, image_path: str, target_attribute: str
    ) -> Dict[str, Any]:
        """Produce the 5-step CoT trace and its yes/no decision."""
        prompt = CTTD_PROMPT.format(
            title=title, bullet_point=bullet_point, target_attribute=target_attribute
        )
        cot_response = self.generate(prompt=prompt, image=image_path or None)

        decision = "no"
        if cot_response:
            decision = "yes" if "yes" in cot_response.lower().split("\n")[-1] else "no"

        return {
            "title": title,
            "bullet_point": bullet_point,
            "image_path": image_path,
            "target_attribute": target_attribute,
            "cot_response": cot_response,
            "decision": decision,
        }


__all__ = [
    "QwenLocalDataGenerator",
    "DEFAULT_MODEL_ID",
    "AGTD_TEXT_PROMPT",
    "AGTD_IMAGE_PROMPT",
    "AGTD_MERGE_PROMPT",
    "CTTD_PROMPT",
]
