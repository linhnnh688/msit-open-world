"""Seed dataset for in-context attribute generation (paper Section 3.1).

"The seed set includes several applicable attribute types. We manually
construct and annotate the seed dataset to ensure consistency with product
characteristics." (WOAM: ~16.5 attribute types and 22 values per type on
average; OAMine: ~11.5 attributes per type, 48.1 unique values.)
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import json
import os


@dataclass
class SeedDataset:
    """category -> {attribute_name: value} seed attribute entries."""

    entries: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str) -> "SeedDataset":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Seed dataset must be a JSON object: {category: {attr: value}}")
        for cat, attrs in data.items():
            if not isinstance(attrs, dict):
                raise ValueError(f"Seed attributes for category '{cat}' must be a JSON object")
        return cls(entries=data)

    @classmethod
    def default(cls) -> "SeedDataset":
        """Small built-in seed set covering the four WOAM categories."""
        return cls(
            entries={
                "Tea": {
                    "brand": "Traditional Medicinals",
                    "Tea_Type": "Green",
                    "flavor": "eucalyptus and mint",
                    "caffeine_content": "caffeine-free",
                    "quantity": "16 tea bags",
                    "Packaging_Type": "Tea bags",
                    "Aroma": "Rich",
                    "Product_Shape": "Powder",
                },
                "Vitamin": {
                    "brand": "Rugby",
                    "product_name": "Tab-A-Vite Multivitamin Tablets",
                    "serving_size": "2 tablets",
                    "number_of_servings": 30,
                    "Dosage_Form": "Tablet",
                    "Target_Audience": "Adults",
                    "key_nutrients": ["Vitamin B6 (Pyridoxine HCI)", "Calcium"],
                },
                "Sofa": {
                    "material_frame": "Gold legs",
                    "style": "Modern, minimalist",
                    "size": "Three-Seater Sofa",
                    "color": "White",
                    "Padding": "High-Density Foam",
                    "Special_Features": "Electric Reclining",
                },
                "PhoneCase": {
                    "Material": "Silicone",
                    "Design": "Transparent",
                    "Function": "Shockproof",
                    "Compatibility": "iPhone 13",
                    "Color": "Black",
                    "Thickness": "Ultra-thin",
                },
            }
        )

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def categories(self) -> List[str]:
        return list(self.entries.keys())

    def attributes_for(self, category: str) -> Dict[str, Any]:
        return self.entries.get(category, {})
