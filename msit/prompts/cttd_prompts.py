"""Prompts for CTTD construction (Chain-of-Thought Tuning Data).

Reproduced from Appendix A.3 of the MSIT paper: the structured 5-step
reasoning process that guides the MLLM to self-correct generated attributes.

The 5 steps (Section 3.2):
  1. Product Type Range Narrowing
  2. Reasoning with Internal Common-sense Knowledge
  3. Image-Based Attribute Validation
  4. Text-Based Attribute Verification
  5. Final Evaluation and Decision-Making
"""

from typing import Optional

CTTD_TASK_DESCRIPTION = """Task Description
I will provide you with product images as well as text information and attributes. Please judge whether the product has this attribute. Please follow the steps below to reason step by step and give your reasoning process."""

FIVE_STEP_COT = """Five-step Chain of thought
Step 1: In this step, you need to determine the type of product based on pictures and text information, such as whether the product is a mobile phone case, tea, or other types of products.
Step 2: This step requires analyzing the meaning of the attributes. If the attribute's meaning is unclear, we will make a preliminary determination that it cannot be considered a product attribute. If the intent of the attribute is clear, use common sense to initially judge whether the attribute matches the product type, and initially explain the meaning of the attribute and why it may match the product.
Step 3: If you preliminarily judge in the second step that this type of product may have this attribute, then please use the picture I provided to guess its attribute value to confirm that the product indeed has this attribute. Since images do not provide explicit attribute value information, there is no need to derive exact attribute values. You only need to determine a rough attribute value to confirm.
Step 4: If you preliminarily judge that this type of product may have this attribute in the second step, then in this step, please use the text I provided to guess its attribute value to confirm that the product indeed has this attribute. If you inferred an attribute value from the text, give the exact attribute value.
Step 5, please combine the reasoning from the above steps to draw a conclusion whether the product has this attribute. Please mark the last paragraph with yes or no. No other text is needed in this paragraph."""


def build_cttd_prompt(
    title: str,
    bullet_point: str,
    attribute: str,
    image_caption: Optional[str] = None,
) -> str:
    """Build the Appendix A.3 prompt for constructing CTTD samples.

    Contrastive sampling (positive/negative) is handled by the CTTDBuilder;
    this function only renders the prompt for one (product, attribute) pair.
    """
    info = (
        "The product's text and image information and the attributes that need to be judged\n"
        f"Image: {image_caption or '<product image>'}\n"
        f"Title: {title}\n"
        f"Bullet Point: {bullet_point}\n"
        f"The attribute i want to judge is {attribute}"
    )
    return f"{CTTD_TASK_DESCRIPTION}\n\n{FIVE_STEP_COT}\n\n{info}"
