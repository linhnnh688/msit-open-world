"""Stage 2: Filtering Repeated Attributes (paper Section 3.4 + Appendix B.2).

"attributes like 'type' and 'product type' are identified as duplicates. A
rule-based system is employed to eliminate these redundancies."

Appendix B.2 algorithm (reproduced faithfully):
  * Two phrases are synonyms iff the subwords of one correspond ONE-TO-ONE
    with the subwords of the other.
  * Subword similarity = cosine similarity of word2vec-google-news-300
    vectors, with a threshold; if one phrase has only ONE subword, a HIGHER
    threshold is used.
  * Deletion rules based on subword counts:
      Rule 1: one attribute (A) has exactly 1 subword; the other (B) has:
                - exactly 3 subwords  -> delete A
                - more than 3        -> delete B
      Rule 2: A has 2 subwords, B has >= 3 subwords -> delete B
      Rule 3: same number of subwords -> randomly delete one

The embedding backend is pluggable: Word2VecBackend uses gensim when the
google-news-300 vectors are available; otherwise a deterministic
heuristic backend keeps the pipeline runnable (and fully unit-testable with
injected fake similarity functions).
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import random
import re

from ..config import MSITConfig


# --------------------------------------------------------------------------
# Subword tokenization
# --------------------------------------------------------------------------
def tokenize_subwords(phrase: str) -> List[str]:
    """Split an attribute phrase into subwords (lowercased alphanumeric runs)."""
    return re.findall(r"[a-z0-9]+", phrase.lower())


# --------------------------------------------------------------------------
# Similarity backends
# --------------------------------------------------------------------------
SimilarityFn = Callable[[str, str], float]  # cosine similarity in [0, 1]


class Word2VecBackend:
    """word2vec-google-news-300 cosine similarity (paper Appendix B.2)."""

    def __init__(self, model_path: Optional[str] = None):
        try:
            import gensim.downloader as api
        except ImportError as e:
            raise ImportError(
                "gensim is required for the word2vec backend: pip install gensim"
            ) from e
        if model_path:
            from gensim.models import KeyedVectors

            self.kv = KeyedVectors.load_word2vec_format(model_path, binary=True)
        else:
            self.kv = api.load("word2vec-google-news-300")

    def similarity(self, w1: str, w2: str) -> float:
        if w1 == w2:
            return 1.0
        try:
            return float(self.kv.similarity(w1, w2))
        except KeyError:
            return 0.0

    def __call__(self, w1: str, w2: str) -> float:
        return self.similarity(w1, w2)


class HeuristicBackend:
    """Deterministic fallback when word2vec is unavailable.

    Exact matches are identical (1.0); everything else scores 0.0. This keeps
    the deletion rules operational (equal-token phrases still deduplicate).
    """

    def __call__(self, w1: str, w2: str) -> float:
        return 1.0 if w1 == w2 else 0.0


# --------------------------------------------------------------------------
# Synonym detection (one-to-one subword correspondence)
# --------------------------------------------------------------------------
def are_synonyms(
    phrase_a: str,
    phrase_b: str,
    sim_fn: SimilarityFn,
    threshold: float = 0.70,
    single_subword_threshold: float = 0.85,
) -> bool:
    """Two phrases are synonyms iff their subwords match one-to-one.

    A single-subword phrase uses the higher threshold (Appendix B.2).
    """
    sa, sb = tokenize_subwords(phrase_a), tokenize_subwords(phrase_b)
    if not sa or not sb:
        return False
    if len(sa) != len(sb):
        return False  # one-to-one requires equal counts

    single_involved = len(sa) == 1 or len(sb) == 1
    thr = single_subword_threshold if single_involved else threshold

    # Greedy bipartite matching: for each subword in A pick the most similar
    # unused subword in B; all picks must clear the threshold.
    used = set()
    for wa in sa:
        best_j, best_s = -1, -1.0
        for j, wb in enumerate(sb):
            if j in used:
                continue
            s = sim_fn(wa, wb)
            if s > best_s:
                best_s, best_j = s, j
        if best_j == -1 or best_s < thr:
            return False
        used.add(best_j)
    return True


# --------------------------------------------------------------------------
# Deletion rules (Appendix B.2)
# --------------------------------------------------------------------------
def choose_deletion(
    attr_a: str, attr_b: str, rng: Optional[random.Random] = None
) -> str:
    """Return the attribute name that should be DELETED.

    Rules (n = number of subwords):
      Rule 1: n_A == 1 and n_B == 3 -> delete A; n_A == 1 and n_B > 3 -> delete B
      Rule 2: n_A == 2 and n_B >= 3 (or symmetric) -> delete the >=3 one
      Rule 3: n_A == n_B -> random choice
    (Rules are symmetric in A/B: counts are sorted first.)
    """
    r = rng or random.Random(0)
    na, nb = len(tokenize_subwords(attr_a)), len(tokenize_subwords(attr_b))
    lo, hi = sorted((attr_a, attr_b), key=lambda x: len(tokenize_subwords(x)))
    n_lo, n_hi = min(na, nb), max(na, nb)

    if n_lo == n_hi:
        return r.choice([attr_a, attr_b])  # Rule 3
    if n_lo == 1:
        # Rule 1
        return lo if n_hi == 3 else hi
    if n_lo == 2 and n_hi >= 3:
        return hi  # Rule 2
    # Fallback (2 vs 1 handled by Rule 1 symmetry; anything else: delete longer)
    return hi


# --------------------------------------------------------------------------
# Stage 2 runner
# --------------------------------------------------------------------------
@dataclass
class Stage2RepeatedAttributeFilter:
    cfg: MSITConfig = field(default_factory=MSITConfig)
    sim_fn: Optional[SimilarityFn] = None
    rng: random.Random = field(default_factory=lambda: random.Random(42))

    def __post_init__(self):
        if self.sim_fn is None:
            try:
                self.sim_fn = Word2VecBackend()
            except ImportError:
                self.sim_fn = HeuristicBackend()

    def filter(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Remove synonymous (repeated-meaning) attributes.

        Keeps deterministic order; the first occurrence of a synonym cluster
        survives unless a deletion rule says otherwise.
        """
        names = list(attributes.keys())
        delete: set = set()
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                if a in delete or b in delete:
                    continue
                if are_synonyms(
                    a,
                    b,
                    self.sim_fn,
                    threshold=self.cfg.similarity_threshold,
                    single_subword_threshold=self.cfg.single_subword_threshold,
                ):
                    loser = choose_deletion(a, b, rng=self.rng)
                    delete.add(loser)
        return {k: v for k, v in attributes.items() if k not in delete}
