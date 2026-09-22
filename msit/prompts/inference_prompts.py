"""Inference instructions (paper Appendix B).

- Table 4: instructions for Stage 1 (Batch Attribute Generation).
- Table 5: instructions for Stage 3 (Filtering Wrong Attributes / sequential
  attribute inference with 5-step CoT).

"The list of instructions ... They present the same meaning with natural
language variance." (paper Appendix B.1 / B.3). During inference one variant
is sampled per call.
"""

from typing import Optional
import random

# Appendix B.1 / Table 4 - Batch Attribute Generation instructions.
BATCH_GEN_INSTRUCTIONS = [
    "Extract the information from the title, bullet points, and product picture into JSON format.",
    "Convert the attribute values of the product from the provided information into JSON format.",
    "Generate the product attribute values in JSON format based on the provided title, bullet points, and picture.",
    "Compile the product's characteristic attributes into JSON format according to the provided information.",
    "Extract the product attribute information into JSON format from the provided title, bullet points, and picture.",
    "Parse the product's features and attributes into JSON format from the given information.",
    "Extract the product's characteristics into JSON format using the provided title, bullet points, and picture.",
    "Retrieve and organize the product's attribute values into JSON format from the provided information.",
    "Compile the product's attribute information into JSON format based on the title, bullet points, and picture content.",
    "Generate JSON-formatted product attribute data based on the provided information.",
]

# Appendix B.3 / Table 5 - Filtering Wrong Attributes instructions.
FILTER_INSTRUCTIONS = [
    "I provide you with text and image information of a product along with one attribute of this product. Please determine if this product possesses this attribute through the text and image. Let's think step by step, and please provide your reasoning process.",
    "Here's textual and visual data about a product, along with a specific attribute. Your job is to discern if this attribute applies to the product, using both the text and the visuals. Let's methodically analyze the information, detailing your reasoning process step by step.",
    "I present you with textual and visual data about a product, along with a single attribute associated with it. Your task is to determine whether this product exhibits this attribute, utilizing both the text and the image. Let's think step by step, and please provide your reasoning process.",
    "I provide you with the text and picture information of a product and an attribute of this product, please help me judge whether this product has this attribute through the text and picture, we will think step by step, please give me your reasoning process.",
    "I will give you the text and image information of a product, as well as one of its attributes. Please use the text and image to help me determine whether the product has this attribute. Let's think step by step, and please explain your reasoning process.",
]

from .cttd_prompts import FIVE_STEP_COT


def sample_batch_gen_instruction(rng: Optional[random.Random] = None) -> str:
    """Sample one Table-4 instruction (natural language variance)."""
    r = rng or random
    return r.choice(BATCH_GEN_INSTRUCTIONS)


def sample_filter_instruction(rng: Optional[random.Random] = None) -> str:
    """Sample one Table-5 instruction."""
    r = rng or random
    return r.choice(FILTER_INSTRUCTIONS)


def build_stage1_prompt(title: str, bullet_point: str, rng=None) -> str:
    """Stage 1 prompt: batch attribute generation (image + text together)."""
    instruction = sample_batch_gen_instruction(rng)
    return (
        f"{instruction}\n\n"
        f"Title: {title}\n"
        f"Bullet point: {bullet_point}"
    )


def build_stage3_prompt(
    title: str, bullet_point: str, attribute: str, rng=None
) -> str:
    """Stage 3 prompt: sequential attribute inference with 5-step CoT.

    Combines a sampled Table-5 filtering instruction with the structured
    5-step reasoning process (Appendix A.3), matching Figure 2 of the paper.
    """
    instruction = sample_filter_instruction(rng)
    return (
        f"{instruction}\n\n{FIVE_STEP_COT}\n\n"
        f"Title: {title}\n"
        f"Bullet point: {bullet_point}\n"
        f"The attribute i want to judge is {attribute}"
    )
