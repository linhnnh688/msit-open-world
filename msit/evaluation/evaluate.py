"""Evaluation runner (paper Section 4.1).

"We report the means and standard deviations of 5 independent trials. For
each trial, we utilize a random seed to ensure fairness."
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import random
import statistics

from ..config import MSITConfig
from ..inference.pipeline import MSITInferencePipeline
from .metrics import match_product, aggregate, MatchResult


@dataclass
class MSITEvaluator:
    """Run the full MSIT pipeline on a test set and report metrics.

    test_set: list of {"title", "bullet_point", "gold": {attr: value},
                       "image" (optional)} dicts.
    """

    backend: Any
    cfg: MSITConfig = field(default_factory=MSITConfig)
    sim_fn: Optional[Any] = None

    def run_trial(
        self, test_set: List[Dict[str, Any]], seed: int
    ) -> Dict[str, Dict[str, float]]:
        """One inference trial; returns {match_mode: {precision, recall}}."""
        rng = random.Random(seed)
        pipeline = MSITInferencePipeline(self.backend, self.cfg, sim_fn=self.sim_fn)
        results = {"exact": [], "similar": []}
        for item in test_set:
            out = pipeline.run(
                item["title"],
                item.get("bullet_point", ""),
                image=item.get("image"),
                rng=rng,
            )
            for mode in ("exact", "similar"):
                results[mode].append(
                    match_product(out["attributes"], item["gold"], mode=mode)
                )
        return {mode: aggregate(res) for mode, res in results.items()}

    def run(
        self, test_set: List[Dict[str, Any]], n_trials: Optional[int] = None
    ) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Run n_trials independent trials and report mean +- std."""
        n = n_trials or self.cfg.n_trials
        per_trial = [self.run_trial(test_set, seed=1000 + t) for t in range(n)]

        summary: Dict[str, Dict[str, Dict[str, float]]] = {}
        for mode in ("exact", "similar"):
            for metric in ("precision", "recall"):
                values = [per_trial[t][mode][metric] for t in range(n)]
                summary.setdefault(mode, {})[metric] = {
                    "mean": statistics.mean(values),
                    "std": statistics.stdev(values) if n > 1 else 0.0,
                    "trials": values,
                }
        return summary
