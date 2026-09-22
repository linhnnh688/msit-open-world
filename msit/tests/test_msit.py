"""Unit tests for the MSIT reproduction.

Run with:  python -m pytest msit/tests/test_msit.py -v
       or:  python msit/tests/test_msit.py        (plain asserts, no pytest needed)
"""

import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from msit.config import MSITConfig
from msit.prompts import agtd_prompts, cttd_prompts, inference_prompts
from msit.utils.json_parser import parse_attributes, extract_json_object, format_attributes
from msit.data.seed_dataset import SeedDataset
from msit.data.agtd_builder import AGTDBuilder
from msit.data.cttd_builder import CTTDBuilder
from msit.models.mock_backend import MockMLLMBackend
from msit.inference.stage1_batch_gen import Stage1BatchGenerator
from msit.inference.stage2_dedup import (
    Stage2RepeatedAttributeFilter,
    are_synonyms,
    choose_deletion,
    tokenize_subwords,
)
from msit.inference.stage3_cot_infer import Stage3CoTValidator, parse_conclusion
from msit.inference.pipeline import MSITInferencePipeline
from msit.evaluation.metrics import match_product, aggregate
from msit.evaluation.evaluate import MSITEvaluator


# --------------------------------------------------------------------- utils
def test_json_parser_bare_dict():
    assert parse_attributes('{"brand": "X", "color": "red"}') == {
        "brand": "X",
        "color": "red",
    }


def test_json_parser_wrapped_attributes():
    out = parse_attributes('{"Attributes": {"Tea_Type": "Green"}}')
    assert out == {"Tea_Type": "Green"}


def test_json_parser_markdown_fence_and_trailing_text():
    text = 'Sure! Here you go:\n```json\n{"Attributes": {"a": 1,},}\n```\nHope this helps.'
    assert extract_json_object(text) is not None


def test_json_parser_garbage_returns_empty():
    assert parse_attributes("no json here") == {}


def test_format_attributes_roundtrip():
    attrs = {"brand": "Micro Ingredients"}
    assert parse_attributes(format_attributes(attrs)) == attrs


# -------------------------------------------------------------------- prompts
def test_agtd_prompts_contain_paper_sections():
    p_text = agtd_prompts.build_extraction_prompt("text", "T", "B")
    assert "world-class algorithm" in p_text
    assert "Title: T" in p_text and "Bullet point: B" in p_text
    assert "Sofa" in p_text  # ICL example present
    p_img = agtd_prompts.build_extraction_prompt("image", "T", "B")
    assert "image information" in p_img.lower()
    assert "Title: T" not in p_img  # modality separation (paper Section 3.1)


def test_merge_prompt():
    p = agtd_prompts.build_merge_prompt({"a": 1}, {"b": 2})
    assert "merge them into one" in p.lower()


def test_cttd_prompt_has_5_steps():
    p = cttd_prompts.build_cttd_prompt("t", "b", "color")
    for i in range(1, 6):
        assert f"Step {i}" in p
    assert "yes or no" in p


def test_inference_prompt_counts():
    assert len(inference_prompts.BATCH_GEN_INSTRUCTIONS) == 10  # Table 4
    assert len(inference_prompts.FILTER_INSTRUCTIONS) == 5  # Table 5


# ------------------------------------------------------------------- stage 2
def fake_sim_factory(pairs):
    """Similarity function from an explicit {(w1,w2): score} mapping."""

    def sim(w1, w2):
        if w1 == w2:
            return 1.0
        return pairs.get((w1, w2), pairs.get((w2, w1), 0.0))

    return sim


def test_tokenize_subwords():
    assert tokenize_subwords("Product Type") == ["product", "type"]
    assert tokenize_subwords("Tea__Type!") == ["tea", "type"]


def test_are_synonyms_one_to_one():
    # "type" vs "kind": single subword, high similarity -> synonyms
    sim = fake_sim_factory({("type", "kind"): 0.9})
    assert are_synonyms("type", "kind", sim, threshold=0.7, single_subword_threshold=0.85)
    # Below the single-subword threshold -> not synonyms
    sim2 = fake_sim_factory({("type", "kind"): 0.8})
    assert not are_synonyms("type", "kind", sim2, threshold=0.7, single_subword_threshold=0.85)
    # Different subword counts can never match one-to-one
    assert not are_synonyms("product type", "type", fake_sim_factory({}))
    # Multi-subword: one-to-one correspondence required
    sim3 = fake_sim_factory({("product", "item"): 0.9, ("type", "kind"): 0.9})
    assert are_synonyms("product type", "item kind", sim3, threshold=0.7)
    sim4 = fake_sim_factory({("product", "item"): 0.9, ("type", "kind"): 0.5})
    assert not are_synonyms("product type", "item kind", sim4, threshold=0.7)


def test_deletion_rule1():
    rng = random.Random(0)
    # 1 vs 3 -> delete the 1-subword attribute
    assert choose_deletion("type", "product item kind", rng) == "type"
    # 1 vs 4 -> delete the longer one
    assert choose_deletion("type", "product item kind extra", rng) == "product item kind extra"


def test_deletion_rule2():
    rng = random.Random(0)
    # 2 vs >=3 -> delete the >=3 one
    assert choose_deletion("product type", "product item kind", rng) == "product item kind"


def test_deletion_rule3_random():
    # same subword count -> either can go; must return one of the two
    for _ in range(10):
        loser = choose_deletion("abc def", "ghi jkl", random.Random())
        assert loser in ("abc def", "ghi jkl")


def test_stage2_end_to_end():
    cfg = MSITConfig()
    sim = fake_sim_factory({("type", "kind"): 0.95})
    f = Stage2RepeatedAttributeFilter(cfg, sim_fn=sim, rng=random.Random(1))
    attrs = {"type": "Green", "kind": "Green", "brand": "X", "product item kind": "Y"}
    out = f.filter(attrs)
    # 'type'/'kind' are synonyms (single subword, 0.95 >= 0.85) -> one removed
    assert not ("type" in out and "kind" in out)
    assert "brand" in out and "product item kind" in out


# ------------------------------------------------------------------- stage 3
def test_parse_conclusion():
    trace = (
        "Step 1 ...\nStep 5 Final Evaluation...\nConclusion: yes"
    )
    assert parse_conclusion(trace) is True
    assert parse_conclusion("Step 5 ...\nConclusion: no") is False
    assert parse_conclusion("garbage") is None


def test_stage3_with_mock_backend():
    db = {"Tea A": {"Tea_Type": "Green", "brand": "X"}}
    backend = MockMLLMBackend(db)
    v = Stage3CoTValidator(backend, MSITConfig())
    kept, traces = v.run("Tea A", "green tea", {"Tea_Type": "Green", "weight": "1lb"})
    assert kept == {"Tea_Type": "Green"}
    assert len(traces) == 2 and all("Step 1" in t["reasoning"] for t in traces)


# ----------------------------------------------------------------- pipeline
def test_full_pipeline_mock():
    db = {"Tea A": {"Tea_Type": "Green", "brand": "X"}}
    backend = MockMLLMBackend(db)
    pipe = MSITInferencePipeline(backend, MSITConfig())
    out = pipe.run("Tea A", "green tea from Japan")
    assert out["attributes"] == {"Tea_Type": "Green", "brand": "X"}
    assert set(out.keys()) >= {"stage1_raw", "stage2_filtered", "stage3_traces"}


# ------------------------------------------------------------------ metrics
def test_metrics_exact_and_similar():
    gold = {"Tea_Type": "Green", "brand": "X", "Weight": "1lb"}
    pred = {"Tea_Type": "Green", "brand": "Y", "Extra": "z"}
    exact = match_product(pred, gold, mode="exact")
    assert (exact.tp, exact.fp, exact.fn) == (1, 2, 2)
    similar = match_product(pred, gold, mode="similar")
    assert (similar.tp, similar.fp, similar.fn) == (1, 2, 2)
    # Synonym value should count under similar match
    pred2 = {"Tea_Type": "Matcha Green"}
    m = match_product(pred2, {"Tea_Type": "Green"}, mode="similar")
    assert m.tp == 1 and m.fn == 0


def test_aggregate():
    r1 = match_product({"a": 1}, {"a": 1, "b": 2}, mode="exact")
    r2 = match_product({"a": 1, "c": 3}, {"a": 1}, mode="exact")
    agg = aggregate([r1, r2])
    assert agg["tp"] == 2 and agg["fp"] == 1 and agg["fn"] == 1
    assert abs(agg["precision"] - 2 / 3) < 1e-9


# ------------------------------------------------------------- data builders
def test_seed_dataset_default():
    sd = SeedDataset.default()
    assert "Tea" in sd.categories() and "Tea_Type" in sd.attributes_for("Tea")


def test_agtd_builder_mock():
    db = {"Micro Ingredients Organic Matcha": {"brand": "Micro Ingredients", "Tea_Type": "Green"}}
    builder = AGTDBuilder(MockMLLMBackend(db))
    sample = builder.build_sample(
        "Micro Ingredients Organic Matcha", "green tea powder", image=None
    )
    assert "instruction" in sample and "output" in sample
    assert parse_attributes(sample["output"]) == db["Micro Ingredients Organic Matcha"]


def test_agtd_merge_single_modality_passthrough():
    builder = AGTDBuilder(MockMLLMBackend())
    assert builder.merge_modalities(None, {"a": 1}) == {"a": 1}
    assert builder.merge_modalities({"a": 1}, None) == {"a": 1}


def test_cttd_builder_balanced():
    products = [
        {"title": "P1", "bullet_point": "b", "attributes": {"a1": "x", "a2": "y"}},
        {"title": "P2", "bullet_point": "b", "attributes": {"b1": "x", "b2": "y"}},
    ]
    builder = CTTDBuilder(MockMLLMBackend())
    samples = builder.build_batch(products, attributes_per_product=1)
    # 2 products x (1 positive + 1 negative) = 4 samples
    assert len(samples) == 4
    labels = [s["label"] for s in samples]
    assert labels.count("yes") == 2 and labels.count("no") == 2


# ----------------------------------------------------------------- evaluator
def test_evaluator_runs_trials():
    db = {"Tea A": {"Tea_Type": "Green", "brand": "X"}}
    test_set = [
        {
            "title": "Tea A",
            "bullet_point": "green tea",
            "gold": {"Tea_Type": "Green", "brand": "X"},
        }
    ]
    ev = MSITEvaluator(MockMLLMBackend(db), MSITConfig())
    summary = ev.run(test_set, n_trials=2)
    assert "similar" in summary and "exact" in summary
    assert summary["similar"]["precision"]["mean"] == 1.0


# --------------------------------------------------------------------- main
if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} tests passed")
    sys.exit(1 if failed else 0)
