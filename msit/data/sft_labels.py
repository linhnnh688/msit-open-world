"""Resumable JSONL writers for the AGTD / CTTD SFT label files.

Labeling hundreds of samples on a single GPU takes long enough that a Kaggle
session can die mid-run. Both writers therefore append one sample per line and
skip ASINs already present in the output file, so re-running resumes where the
previous session stopped.
"""

from typing import Any, Dict, List, Set
import json
import os


def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


def _free_cuda_cache() -> None:
    """Release cached VRAM periodically; no-op when torch/GPU is unavailable."""
    try:
        import torch
    except ImportError:
        return
    torch.cuda.empty_cache()


def save_test_set(test_pool: List[Dict[str, Any]], output_file: str) -> int:
    """Overwrite `output_file` with the test split; returns the number written."""
    _ensure_parent(output_file)
    with open(output_file, "w", encoding="utf-8") as f:
        for item in test_pool:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Đã lưu {len(test_pool)} mẫu Test Set.")
    return len(test_pool)


def load_processed_asins(output_file: str) -> Set[str]:
    """ASINs already written to `output_file` (empty set if it does not exist)."""
    processed: Set[str] = set()
    if not os.path.exists(output_file):
        return processed
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                processed.add(json.loads(line).get("asin", ""))
    return processed


def generate_and_save_sft_labels(
    pool: List[Dict[str, Any]],
    output_file: str,
    mode: str,
    generator: Any,
) -> int:
    """Label `pool` with `generator` and append the results to `output_file`.

    Args:
        mode: "agtd" (attribute extraction) or "cttd" (5-step CoT judgement).
        generator: object exposing `generate_agtd_sample` / `generate_cttd_sample`
            (e.g. `msit.models.qwen_local.QwenLocalDataGenerator`).

    Returns the number of samples written in this run.
    """
    if mode not in ("agtd", "cttd"):
        raise ValueError("mode must be 'agtd' or 'cttd'")

    _ensure_parent(output_file)
    processed_asins = load_processed_asins(output_file)
    print(
        f"\nBắt đầu sinh nhãn {mode.upper()}... "
        f"(Đã có sẵn {len(processed_asins)}/{len(pool)} mẫu)"
    )

    written = 0
    with open(output_file, "a", encoding="utf-8") as f:
        for idx, item in enumerate(pool):
            asin = item.get("asin", "")
            if asin in processed_asins:
                continue

            title = item.get("title", "")
            bullet_point = item.get("bullet_point", "")
            image_path = item.get("image_path", "")

            print(f"[{idx + 1}/{len(pool)}] Suy luận cục bộ ASIN: {asin}")

            try:
                if mode == "agtd":
                    result = generator.generate_agtd_sample(title, bullet_point, image_path)
                    item["attributes"] = result.get("attributes", {})
                else:
                    attr = item.get("attribute_to_judge", "")
                    result = generator.generate_cttd_sample(title, bullet_point, image_path, attr)
                    item["cot_response"] = result.get("cot_response", "")
                    item["decision"] = result.get("decision", item.get("cttd_label"))

                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                written += 1

            except Exception as e:
                print(f"[Lỗi] Bỏ qua ASIN {asin}: {e}")
                continue

            # Xóa cache GPU định kỳ để tránh tràn VRAM nếu chạy thời gian dài
            if idx % 10 == 0:
                _free_cuda_cache()

    return written


__all__ = ["save_test_set", "load_processed_asins", "generate_and_save_sft_labels"]
