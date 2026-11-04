"""Split construction for MSIT SFT data (AGTD / CTTD / test).

Steps, in order:
  1. Drop products without an image on disk or with < 10 words of text.
  2. Balance categories with a round-robin pool so no category dominates.
  3. Allocate a dynamic split: CTTD ~13% of the pool (rounded up to an even
     number so positives/negatives split 50/50), the rest is halved into the
     test set and the AGTD training set.
  4. Assign CTTD labels: half "yes" (attribute present), half "no" (attribute
     sampled from another category), the contrastive setup of paper Section 3.2.

The prepared splits are cached as JSON by `msit.data.build_sft` so a Kaggle
session can resume without recomputing.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import os
import random

# Share of the balanced pool reserved for CTTD construction (paper Section 4.1
# uses 300 CTTD vs 1000 AGTD; 13% keeps that ratio on smaller pools).
CTTD_RATIO = 0.13

Record = Dict[str, Any]


@dataclass
class MSITDataPreparator:
    records: List[Record]
    image_dir: str
    seed: int = 42

    def _filter_noise(self) -> List[Record]:
        """Keep records that have an image and at least 10 words of text."""
        valid_records: List[Record] = []
        for r in self.records:
            img_path = os.path.join(self.image_dir, f"{r['asin']}.jpg")
            if not os.path.exists(img_path):
                continue

            text_length = len(r["title"].split()) + len(r["bullet_point"].split())
            if text_length < 10:
                continue

            r["image_path"] = img_path
            valid_records.append(r)
        return valid_records

    @staticmethod
    def split_sizes(total_valid: int) -> Tuple[int, int, int]:
        """Return (test_size, agtd_size, cttd_size) for a pool of `total_valid`."""
        cttd_size = max(2, int(total_valid * CTTD_RATIO))
        if cttd_size % 2 != 0:
            cttd_size += 1

        remaining = total_valid - cttd_size
        test_size = remaining // 2
        agtd_size = remaining - test_size
        return test_size, agtd_size, cttd_size

    @staticmethod
    def _round_robin(records: List[Record], rng: random.Random) -> List[Record]:
        """Interleave categories so the pool is balanced before slicing."""
        cat_dict: Dict[str, List[Record]] = {}
        for r in records:
            cat_dict.setdefault(r["category"], []).append(r)

        for cat in cat_dict:
            rng.shuffle(cat_dict[cat])

        pool: List[Record] = []
        while cat_dict:
            for cat in list(cat_dict.keys()):
                if cat_dict[cat]:
                    pool.append(cat_dict[cat].pop(0))
                else:
                    del cat_dict[cat]
        return pool

    @staticmethod
    def _assign_cttd_labels(cttd_pool: List[Record], all_categories: List[str], rng: random.Random) -> None:
        """Mark the first half "yes" and sample cross-category attributes for the rest."""
        for i, item in enumerate(cttd_pool):
            if i < len(cttd_pool) // 2:
                item["cttd_label"] = "yes"
                # TODO: Thay thế bằng code bốc 1 key thật từ dữ liệu gốc
                item["attribute_to_judge"] = "target_attribute_placeholder"
            else:
                item["cttd_label"] = "no"
                other_cats = [c for c in all_categories if c != item["category"]]
                random_fake_cat = rng.choice(other_cats) if other_cats else "Khác"
                item["attribute_to_judge"] = f"Fake attribute from {random_fake_cat}"

    def prepare_splits(self) -> Tuple[List[Record], List[Record], List[Record]]:
        """Return (test_pool, agtd_pool, cttd_pool)."""
        rng = random.Random(self.seed)
        cleaned_records = self._filter_noise()

        if not cleaned_records:
            raise ValueError(
                "Không còn mẫu nào hợp lệ sau khi lọc nhiễu. Hãy kiểm tra lại thư mục ảnh."
            )

        balanced_pool = self._round_robin(cleaned_records, rng)
        total_valid = len(balanced_pool)
        test_size, agtd_size, cttd_size = self.split_sizes(total_valid)

        print("\n[PHÂN BỔ DỮ LIỆU ĐỘNG]")
        print(f"Tổng số mẫu có ảnh hợp lệ : {total_valid}")
        print(f"  - Tập Test Set          : {test_size} mẫu")
        print(f"  - Tập Train SFT (AGTD)  : {agtd_size} mẫu")
        print(f"  - Tập Train SFT (CTTD)  : {cttd_size} mẫu")

        test_pool = balanced_pool[:test_size]
        agtd_pool = balanced_pool[test_size : test_size + agtd_size]
        cttd_pool = balanced_pool[test_size + agtd_size :]

        all_categories = sorted({r["category"] for r in cleaned_records})
        self._assign_cttd_labels(cttd_pool, all_categories, rng)

        return test_pool, agtd_pool, cttd_pool


__all__ = ["MSITDataPreparator", "CTTD_RATIO"]
