"""Evaluation metrics (paper Section 4.1).

"1) Precision, the ratio of true positives to total positive predictions, and
2) Recall, the proportion of true positives among all actual positives. We
report ExactMatch and SimilarMatch as in previous work (Roy et al., 2021;
Zheng et al., 2018a). ExactMatch requires strict consistency with the gold
standard, while SimilarMatch allows for synonyms, treating attribute
predictions as correct if they match any synonym of labels."
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import re


def normalize_name(name: str) -> str:
    """Normalize attribute names: lowercase, underscores/spaces unified."""
    return re.sub(r"[_\s]+", " ", name.strip().lower())


def normalize_value(value: Any) -> str:
    """Normalize an attribute value to a comparable string."""
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    s = str(value).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


# A small built-in synonym lexicon for SimilarMatch. In the full reproduction
# this can be extended from WordNet / the synonym sets of Roy et al. (2021).
DEFAULT_SYNONYMS: Dict[str, Set[str]] = {
    "green": {"lime", "matcha green", "jade"},
    "black": {"dark"},
    "couch": {"sofa", "settee"},
    "sofa": {"couch", "settee"},
    "16 tea bags": {"16 count", "16 bags", "box of 16"},
    "caffeine-free": {"decaffeinated", "no caffeine", "caffeine free"},
}


@dataclass
class MatchResult:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 0.0


def _value_matches(pred_v: str, gold_v: str, synonyms: Dict[str, Set[str]]) -> bool:
    if pred_v == gold_v:
        return True
    # Symmetric synonym lookup.
    for key, syns in synonyms.items():
        key_n = normalize_value(key)
        if pred_v == key_n and gold_v in {normalize_value(s) for s in syns}:
            return True
        if gold_v == key_n and pred_v in {normalize_value(s) for s in syns}:
            return True
        if pred_v in {normalize_value(s) for s in syns} and gold_v in {
            normalize_value(s) for s in syns
        }:
            return True
    return False


def match_product(
    predicted: Dict[str, Any],
    gold: Dict[str, Any],
    mode: str = "similar",
    synonyms: Optional[Dict[str, Set[str]]] = None,
) -> MatchResult:
    """Compute TP/FP/FN for one product's attribute-value pairs.

    A prediction is a true positive iff its normalized attribute name exists
    in the gold set AND (exact mode) its normalized value equals the gold
    value, or (similar mode) its value matches a gold value/synonym.
    """
    if synonyms is None:
        synonyms = DEFAULT_SYNONYMS
    res = MatchResult()

    gold_by_name: Dict[str, Any] = {}
    for k, v in gold.items():
        gold_by_name.setdefault(normalize_name(k), v)

    used_gold: Set[str] = set()
    for pk, pv in predicted.items():
        name = normalize_name(pk)
        if name in gold_by_name and name not in used_gold:
            gv_norm = normalize_value(gold_by_name[name])
            pv_norm = normalize_value(pv)
            if mode == "exact":
                hit = pv_norm == gv_norm
            else:
                hit = _value_matches(pv_norm, gv_norm, synonyms)
            if hit:
                res.tp += 1
                used_gold.add(name)
                continue
        res.fp += 1

    res.fn = len(gold) - len(used_gold)
    return res


def aggregate(results: List[MatchResult]) -> Dict[str, float]:
    """Aggregate per-product TP/FP/FN into corpus-level precision/recall."""
    tp = sum(r.tp for r in results)
    fp = sum(r.fp for r in results)
    fn = sum(r.fn for r in results)
    mr = MatchResult(tp=tp, fp=fp, fn=fn)
    return {"precision": mr.precision, "recall": mr.recall, "tp": tp, "fp": fp, "fn": fn}
