"""Raw dataset readers for the two benchmark corpora used by MSIT.

  - WOAM: single JSONL file with one product per line; the category field is
    `pt` and the dev/test membership is encoded by `is_dev` / `is_test`.
  - OAMine: one `<category>.jsonl` annotation file per category plus a
    parallel `raw/` directory.

Both readers normalize a product into the record dict consumed by
`msit.data.preparator.MSITDataPreparator`:

    {"asin", "category", "title", "bullet_point", "raw"}
"""

from typing import Any, Dict, List, Optional
import json
import os


class WOAMRawReader:
    """Reader for the WOAM benchmark JSONL dump."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file WOAM: {file_path}")

    def load_records(
        self,
        category: Optional[str] = None,
        split: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Load products, optionally filtered by category and train/dev/test split."""
        records: List[Dict[str, Any]] = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)

                if category and item.get("pt", "").upper() != category.upper():
                    continue

                is_dev, is_test = item.get("is_dev", False), item.get("is_test", False)
                if split == "dev" and not is_dev:
                    continue
                elif split == "test" and not is_test:
                    continue
                elif split == "train" and (is_dev or is_test):
                    continue

                bullet_points = item.get("bullet_point", [])
                if isinstance(bullet_points, list):
                    bullet_text = " ".join(str(bp).strip() for bp in bullet_points if bp)
                else:
                    bullet_text = str(bullet_points).strip()

                records.append(
                    {
                        "asin": item.get("asin", ""),
                        "category": item.get("pt", ""),
                        "title": item.get("title", "").strip(),
                        "bullet_point": bullet_text,
                        "raw": item,
                    }
                )
                if limit and len(records) >= limit:
                    break
        return records


class OAMineRawReader:
    """Reader for the OAMine per-category annotation files."""

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.annotations_dir = os.path.join(base_dir, "annotations")
        self.raw_dir = os.path.join(base_dir, "raw")

    def list_categories(self, use_annotations: bool = True) -> List[str]:
        target_dir = self.annotations_dir if use_annotations else self.raw_dir
        if not os.path.exists(target_dir):
            return []
        return [f.replace(".jsonl", "") for f in os.listdir(target_dir) if f.endswith(".jsonl")]

    def load_annotated_records(
        self, category: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Load annotated products; `category=None` walks every annotation file."""
        if not os.path.exists(self.annotations_dir):
            raise FileNotFoundError(f"Không tìm thấy thư mục annotations: {self.annotations_dir}")

        records: List[Dict[str, Any]] = []
        files = [f"{category}.jsonl"] if category else os.listdir(self.annotations_dir)

        for filename in files:
            if not filename.endswith(".jsonl"):
                continue
            cat_name = filename.replace(".jsonl", "")
            filepath = os.path.join(self.annotations_dir, filename)
            if not os.path.exists(filepath):
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    records.append(
                        {
                            "asin": item.get("asin", ""),
                            "category": cat_name,
                            "title": item.get("title", "").strip(),
                            "bullet_point": item.get("bullet_points", item.get("description", "")),
                            "raw": item,
                        }
                    )
                    if limit and len(records) >= limit:
                        return records
        return records


__all__ = ["WOAMRawReader", "OAMineRawReader"]
