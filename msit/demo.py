"""End-to-end demo of the MSIT reproduction on sample products.

Runs the full 3-stage inference pipeline with the mock backend (no GPU/API
needed) on the sample products from data_samples/sample_products.json, then
prints per-stage results and evaluation metrics.

Usage:  python -m msit.demo
"""

import json
import os
import random

from msit.config import MSITConfig
from msit.inference.pipeline import MSITInferencePipeline
from msit.evaluation.metrics import match_product, aggregate
from msit.models.mock_backend import MockMLLMBackend


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data_samples", "sample_products.json"), encoding="utf-8") as f:
        products = json.load(f)["products"]

    # Mock backend seeded with gold attributes (stands in for the fine-tuned
    # MLLM). In the real reproduction this is MSIT(LLaVA-7B) etc.
    backend = MockMLLMBackend({p["title"]: p["gold"] for p in products})
    cfg = MSITConfig()
    rng = random.Random(cfg.random_seed)
    pipe = MSITInferencePipeline(backend, cfg)

    exact_results, similar_results = [], []
    for p in products:
        out = pipe.run(p["title"], p["bullet_point"], rng=rng)
        print("=" * 72)
        print(f"PRODUCT: {p['title']}")
        print(f"  Stage 1 (batch gen)     : {out['stage1_raw']}")
        print(f"  Stage 2 (dedup)         : {out['stage2_filtered']}")
        print(f"  Stage 3 (validated)     : {out['attributes']}")
        kept = sum(1 for t in out["stage3_traces"] if t["kept"])
        print(f"  Stage 3 traces          : {kept}/{len(out['stage3_traces'])} attributes kept")
        print(f"  Gold                    : {p['gold']}")
        exact_results.append(match_product(out["attributes"], p["gold"], mode="exact"))
        similar_results.append(match_product(out["attributes"], p["gold"], mode="similar"))

    print("=" * 72)
    for mode, res in (("ExactMatch", exact_results), ("SimilarMatch", similar_results)):
        agg = aggregate(res)
        print(
            f"{mode:12s}  Precision = {agg['precision']:.4f}   "
            f"Recall = {agg['recall']:.4f}   (tp={agg['tp']}, fp={agg['fp']}, fn={agg['fn']})"
        )


if __name__ == "__main__":
    main()
