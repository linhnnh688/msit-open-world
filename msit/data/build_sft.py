"""End-to-end SFT data build driver (Kaggle-friendly).

Pipeline:
  OAMine annotations + product images
    -> `MSITDataPreparator` (noise filter, category balance, dynamic split)
    -> `splits_checkpoint.json` (cached so a restarted session skips step 1)
    -> `QwenLocalDataGenerator` labels
    -> test_set.jsonl + agtd_train.jsonl + cttd_train.jsonl

Usage:
    python -m msit.data.build_sft [--input-dir DIR] [--working-dir DIR]
                                  [--model-id ID] [--seed N] [--rebuild]
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple
import argparse
import json
import os

from .preparator import MSITDataPreparator
from .readers import OAMineRawReader
from .sft_labels import generate_and_save_sft_labels, save_test_set

DEFAULT_INPUT_DIR = "/kaggle/input/datasets/kunzero106/msit-open-world-dataset"
DEFAULT_WORKING_DIR = "/kaggle/working"


@dataclass
class SFTBuildConfig:
    """Input/output layout; defaults follow the Kaggle dataset mount."""

    oamine_dir: str
    image_dir: str
    checkpoint_file: str
    test_set_file: str
    agtd_out_file: str
    cttd_out_file: str
    seed: int = 42

    @classmethod
    def from_dirs(
        cls,
        input_dir: str = DEFAULT_INPUT_DIR,
        working_dir: str = DEFAULT_WORKING_DIR,
        seed: int = 42,
    ) -> "SFTBuildConfig":
        return cls(
            oamine_dir=os.path.join(input_dir, "datasets", "oamine"),
            image_dir=os.path.join(input_dir, "datasets", "images", "oamine"),
            checkpoint_file=os.path.join(working_dir, "splits_checkpoint.json"),
            test_set_file=os.path.join(working_dir, "test_set.jsonl"),
            agtd_out_file=os.path.join(working_dir, "agtd_train.jsonl"),
            cttd_out_file=os.path.join(working_dir, "cttd_train.jsonl"),
            seed=seed,
        )


def load_or_create_splits(
    cfg: SFTBuildConfig, rebuild: bool = False
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Return (test_pool, agtd_pool, cttd_pool), reusing the cached checkpoint."""
    if not rebuild and os.path.exists(cfg.checkpoint_file):
        print("Đang tải lại dữ liệu từ checkpoint...")
        with open(cfg.checkpoint_file, "r", encoding="utf-8") as f:
            splits = json.load(f)
        return splits.get("test", []), splits.get("agtd", []), splits.get("cttd", [])

    print("Tạo checkpoint và chia tập dữ liệu mới...")
    raw_records = OAMineRawReader(cfg.oamine_dir).load_annotated_records()
    test_pool, agtd_pool, cttd_pool = MSITDataPreparator(
        raw_records, cfg.image_dir, seed=cfg.seed
    ).prepare_splits()

    os.makedirs(os.path.dirname(cfg.checkpoint_file) or ".", exist_ok=True)
    with open(cfg.checkpoint_file, "w", encoding="utf-8") as f:
        json.dump(
            {"test": test_pool, "agtd": agtd_pool, "cttd": cttd_pool},
            f,
            ensure_ascii=False,
            indent=2,
        )
    return test_pool, agtd_pool, cttd_pool


def build_sft_dataset(
    cfg: SFTBuildConfig,
    generator: Optional[Any] = None,
    rebuild: bool = False,
    model_id: Optional[str] = None,
) -> Dict[str, int]:
    """Run the whole build; returns per-split sample counts."""
    test_pool, agtd_pool, cttd_pool = load_or_create_splits(cfg, rebuild=rebuild)

    if generator is None:
        from ..models.qwen_local import DEFAULT_MODEL_ID, QwenLocalDataGenerator

        generator = QwenLocalDataGenerator(model_id=model_id or DEFAULT_MODEL_ID)

    save_test_set(test_pool, cfg.test_set_file)
    n_agtd = generate_and_save_sft_labels(
        agtd_pool, cfg.agtd_out_file, mode="agtd", generator=generator
    )
    n_cttd = generate_and_save_sft_labels(
        cttd_pool, cfg.cttd_out_file, mode="cttd", generator=generator
    )

    print("\nHuấn luyện dữ liệu Local GPU hoàn tất. Hãy tải các file jsonl từ mục Output về máy.")
    return {
        "test": len(test_pool),
        "agtd": n_agtd,
        "cttd": n_cttd,
    }


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Kaggle dataset mount root")
    parser.add_argument("--working-dir", default=DEFAULT_WORKING_DIR, help="output directory")
    parser.add_argument("--model-id", default=None, help="override the Qwen2.5-VL checkpoint")
    parser.add_argument("--seed", type=int, default=42, help="split RNG seed")
    parser.add_argument(
        "--rebuild", action="store_true", help="ignore splits_checkpoint.json and re-split"
    )
    args = parser.parse_args(argv)

    cfg = SFTBuildConfig.from_dirs(args.input_dir, args.working_dir, seed=args.seed)
    counts = build_sft_dataset(cfg, rebuild=args.rebuild, model_id=args.model_id)
    print(f"Kết quả: {counts}")


if __name__ == "__main__":
    main()
