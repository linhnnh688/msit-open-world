"""Prompts for AGTD construction (Attribute Generation Tuning Data).

Reproduced from Appendix A.1 (generation of text/image attributes) and
Appendix A.2 (merging text and image attributes) of the MSIT paper.

Key design choice from Section 3.1: text and image attributes are generated
SEPARATELY (two independent calls) because GPT-4 tends to only use text
information when both modalities are provided simultaneously (modality bias).
"""

from typing import Dict, Any, Optional

# --------------------------------------------------------------------------
# Appendix A.1 - Task description (text variant). For the image variant only
# the phrasing of the modality is changed, exactly as described in the paper:
# "To generate image attributes, we only need to extract image attributes in
# the task description and change the third part of the information to image
# information."
# --------------------------------------------------------------------------
TEXT_TASK_DESCRIPTION = """Task Description:
You are a world-class algorithm for extracting information in structured formats.
There are some product descriptions, and your task is to extract the attribute values from the text information of the product in a JSON format.
Please provide me with the corresponding attribute value of the attribute. If there is no corresponding attribute value in the information I provide you, please do not provide me with this attribute."""

IMAGE_TASK_DESCRIPTION = """Task Description:
You are a world-class algorithm for extracting information in structured formats.
There are some product descriptions, and your task is to extract the attribute values from the image information of the product in a JSON format.
Please provide me with the corresponding attribute value of the attribute. If there is no corresponding attribute value in the information I provide you, please do not provide me with this attribute."""

# --------------------------------------------------------------------------
# Appendix A.1 - In-context learning examples (verbatim from the paper).
# --------------------------------------------------------------------------
ICL_EXAMPLES = [
    {
        "type": "Sofa",
        "material_frame": "Gold legs",
        "style": "Modern, minimalist",
        "size": "Three-Seater Sofa",
        "color": "White",
        "Padding": "High-Density Foam",
        "Accessories": "Throw Pillows",
        "Special Features": "Electric Reclining",
        "Maintenance Requirements": "Dry Clean Only",
    },
    {
        "brand": "Traditional Medicinals",
        "type": "herbal tea",
        "flavor": "eucalyptus and mint",
        "caffeine_content": "caffeine-free",
        "quantity": "16 tea bags",
        "Packaging Type": "Tea bags",
        "Storage conditions": "Dry and Well-Ventilated Area",
        "Processing Level": "Fermented",
        "Aroma": "Rich",
        "Tea Benefits": ["Refreshment", "Digestive Aid"],
    },
    {
        "brand": "Rugby",
        "product_name": "Tab-A-Vite Multivitamin Tablets",
        "serving_size": "2 tablets",
        "number_of_servings": 30,
        "Dosage Form": "Tablet",
        "Target Audience": "Adults",
        "Indications": "Vitamin Supplementation",
        "key_nutrients": [
            "Thiamin (as Thiamine HCI)",
            "Vitamin B6 (Pyridoxine HCI)",
            "Calcium (as Dicalcium Phosphate)",
            "Magnesium (as Magnesium Oxide)",
        ],
    },
    {
        "Type": "Phone case",
        "Material": "Silicone",
        "Design": "Transparent",
        "Function": "Shockproof",
        "Compatibility": "Compatible Models",
        "Color": "Black",
        "Thickness": "Ultra-thin",
        "Weight": "Lightweight",
        "Texture": "Smooth",
    },
]


def _format_icl_examples() -> str:
    import json

    parts = ["In-context learning:"]
    for ex in ICL_EXAMPLES:
        parts.append(json.dumps(ex, ensure_ascii=False, indent=2))
    return "\n".join(parts)


def build_extraction_prompt(
    modality: str, title: str, bullet_point: str, image_caption: Optional[str] = None
) -> str:
    """Build the Appendix A.1 prompt.

    Args:
        modality: "text" or "image".
        title: product title.
        bullet_point: product bullet point description.
        image_caption: only used in the mock backend path where a real image
            cannot be shown; the real GPT-4 backend attaches the image itself.

    The paper inputs image and text SEPARATELY to avoid modality bias
    (Section 3.1), so `modality` selects which task description and which
    product information section are used.
    """
    if modality not in ("text", "image"):
        raise ValueError("modality must be 'text' or 'image'")
    task = TEXT_TASK_DESCRIPTION if modality == "text" else IMAGE_TASK_DESCRIPTION

    if modality == "text":
        info = (
            "Text information of the product:\n"
            "Below is the text information of the product whose attributes I want you to extract\n"
            f"Title: {title}\n"
            f"Bullet point: {bullet_point}"
        )
    else:
        info = (
            "Image information of the product:\n"
            "Below is the image information of the product whose attributes I want you to extract\n"
            f"Product image: {image_caption or '<image attached>'}"
        )

    return f"{task}\n\n{_format_icl_examples()}\n\n{info}"


# --------------------------------------------------------------------------
# Appendix A.2 - Merging prompt.
# --------------------------------------------------------------------------
MERGE_TASK_DESCRIPTION = """Task Description
The following is the information of the attribute value pairs extracted from the image and text of the same product respectively. Please help me merge them into one. The same attributes will be regarded as one after being merged. If I only provide text or image information, then there is no need to merge and directly output the text or image information I provide. If you encounter a attribute like Features, which is a bit general, try to give more detailed attribute. Please let the output follow the json format strictly and do not send me any other text."""

import json


def build_merge_prompt(
    image_attributes: Optional[Dict[str, Any]] = None,
    text_attributes: Optional[Dict[str, Any]] = None,
) -> str:
    """Build the Appendix A.2 merge prompt.

    Follows the paper: if only one modality is provided, the model directly
    outputs that modality's attributes without merging.
    """
    img = json.dumps(image_attributes or {}, ensure_ascii=False)
    txt = json.dumps(text_attributes or {}, ensure_ascii=False)
    return (
        f"{MERGE_TASK_DESCRIPTION}\n\n"
        f"Image and text attributes\n"
        f"Image attributes: {img}\n"
        f"Text attributes: {txt}"
    )
