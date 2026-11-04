"""Unit tests for the SFT data build modules (readers, preparator, writers).

Run with:  python -m pytest msit/tests/test_data_build.py -v
       or:  python msit/tests/test_data_build.py        (plain asserts)
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from msit.data.build_sft import SFTBuildConfig, build_sft_dataset, load_or_create_splits
from msit.data.preparator import MSITDataPreparator
from msit.data.readers import OAMineRawReader, WOAMRawReader
from msit.data.sft_labels import generate_and_save_sft_labels, save_test_set

LONG_TEXT = "a product with a reasonably long description used for split tests"


# ------------------------------------------------------------------ fixtures
def _make_oamine(root, categories=("Tea", "Vitamin"), per_category=20, skip_images=0):
    """Create annotations/<Cat>.jsonl and images/<asin>.jpg under `root`."""
    ann_dir = os.path.join(root, "oamine", "annotations")
    img_dir = os.path.join(root, "oamine", "images")
    os.makedirs(ann_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for ci, cat in enumerate(categories):
        with open(os.path.join(ann_dir, f"{cat}.jsonl"), "w", encoding="utf-8") as f:
            for i in range(per_category):
                asin = f"{cat[:2].upper()}{i:04d}"
                f.write(
                    json.dumps(
                        {
                            "asin": asin,
                            "title": f"{cat} product {i}",
                            "bullet_points": LONG_TEXT,
                        }
                    )
                    + "\n"
                )
                if i >= skip_images:
                    with open(os.path.join(img_dir, f"{asin}.jpg"), "wb") as img:
                        img.write(b"\x00")
    return os.path.join(root, "oamine")


class FakeGenerator:
    """Stand-in for QwenLocalDataGenerator (no GPU)."""

    def generate_agtd_sample(self, title, bullet_point, image_path):
        return {"attributes": {"brand": title.split()[0]}}

    def generate_cttd_sample(self, title, bullet_point, image_path, target_attribute):
        return {"cot_response": "Step 5: yes.", "decision": "yes"}


# ------------------------------------------------------------------- readers
def test_oamine_reader_loads_categories():
    with tempfile.TemporaryDirectory() as tmp:
        base = _make_oamine(tmp)
        reader = OAMineRawReader(base)
        assert sorted(reader.list_categories()) == ["Tea", "Vitamin"]

        records = reader.load_annotated_records()
        assert len(records) == 40
        assert {r["category"] for r in records} == {"Tea", "Vitamin"}
        assert records[0]["bullet_point"] == LONG_TEXT


def test_oamine_reader_category_and_limit():
    with tempfile.TemporaryDirectory() as tmp:
        base = _make_oamine(tmp)
        records = OAMineRawReader(base).load_annotated_records(category="Tea", limit=3)
        assert len(records) == 3
        assert all(r["category"] == "Tea" for r in records)


def test_woam_reader_split_and_bullet_points():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "woam.jsonl")
        rows = [
            {"asin": "A1", "pt": "TEA", "title": "t1", "bullet_point": ["b1", "b2"]},
            {"asin": "A2", "pt": "TEA", "title": "t2", "bullet_point": "b3", "is_dev": True},
            {"asin": "A3", "pt": "SOFA", "title": "t3", "bullet_point": ["b4"], "is_test": True},
        ]
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")

        reader = WOAMRawReader(path)
        assert [r["asin"] for r in reader.load_records(category="tea", split="train")] == ["A1"]
        assert [r["asin"] for r in reader.load_records(split="dev")] == ["A2"]
        assert [r["asin"] for r in reader.load_records(category="Sofa")] == ["A3"]
        assert reader.load_records(limit=1)[0]["bullet_point"] == "b1 b2"


# --------------------------------------------------------------- preparator
def test_split_sizes_cttd_even_and_13_percent():
    assert MSITDataPreparator.split_sizes(40) == (17, 17, 6)
    assert MSITDataPreparator.split_sizes(100) == (43, 43, 14)
    # Pool smaller than the CTTD floor still yields the minimum pair.
    assert MSITDataPreparator.split_sizes(2) == (0, 0, 2)


def test_prepare_splits_filters_and_labels():
    with tempfile.TemporaryDirectory() as tmp:
        base = _make_oamine(tmp, per_category=20, skip_images=2)
        records = OAMineRawReader(base).load_annotated_records()
        preparator = MSITDataPreparator(records, os.path.join(base, "images"), seed=7)
        test_pool, agtd_pool, cttd_pool = preparator.prepare_splits()

        assert len(test_pool) + len(agtd_pool) + len(cttd_pool) == 36
        assert len(cttd_pool) % 2 == 0
        assert all("image_path" in r for r in test_pool + agtd_pool + cttd_pool)

        half = len(cttd_pool) // 2
        assert all(r["cttd_label"] == "yes" for r in cttd_pool[:half])
        assert all(r["cttd_label"] == "no" for r in cttd_pool[half:])
        assert all(r["attribute_to_judge"] for r in cttd_pool)


def test_prepare_splits_is_deterministic_per_seed():
    with tempfile.TemporaryDirectory() as tmp:
        base = _make_oamine(tmp)
        records = OAMineRawReader(base).load_annotated_records()

        first = MSITDataPreparator(records, os.path.join(base, "images"), seed=11).prepare_splits()
        second = MSITDataPreparator(records, os.path.join(base, "images"), seed=11).prepare_splits()
        assert [r["asin"] for r in first[2]] == [r["asin"] for r in second[2]]


def test_prepare_splits_rejects_empty_pool():
    with tempfile.TemporaryDirectory() as tmp:
        preparator = MSITDataPreparator([], os.path.join(tmp, "images"))
        try:
            preparator.prepare_splits()
        except ValueError:
            return
        raise AssertionError("expected ValueError for an empty pool")


# ------------------------------------------------------------------- build
def test_checkpoint_roundtrip_and_rebuild():
    with tempfile.TemporaryDirectory() as tmp:
        base = _make_oamine(tmp)
        cfg = SFTBuildConfig.from_dirs(
            input_dir=os.path.join(tmp, "input"),
            working_dir=os.path.join(tmp, "work"),
            seed=3,
        )
        cfg.oamine_dir = base
        cfg.image_dir = os.path.join(base, "images")

        first = load_or_create_splits(cfg)
        assert os.path.exists(cfg.checkpoint_file)

        # Cached read must not touch the annotations again.
        cached = load_or_create_splits(cfg)
        assert [r["asin"] for r in cached[1]] == [r["asin"] for r in first[1]]

        rebuilt = load_or_create_splits(cfg, rebuild=True)
        assert len(rebuilt[0]) + len(rebuilt[1]) + len(rebuilt[2]) == 40


def test_build_sft_dataset_with_fake_generator_and_resume():
    with tempfile.TemporaryDirectory() as tmp:
        base = _make_oamine(tmp, per_category=10)
        cfg = SFTBuildConfig.from_dirs(
            input_dir=os.path.join(tmp, "input"),
            working_dir=os.path.join(tmp, "work"),
        )
        cfg.oamine_dir = base
        cfg.image_dir = os.path.join(base, "images")

        counts = build_sft_dataset(cfg, generator=FakeGenerator())
        assert counts["test"] > 0
        assert os.path.exists(cfg.test_set_file)

        with open(cfg.agtd_out_file, encoding="utf-8") as f:
            agtd_rows = [json.loads(line) for line in f if line.strip()]
        assert len(agtd_rows) == counts["agtd"]
        assert agtd_rows[0]["attributes"] == {"brand": agtd_rows[0]["title"].split()[0]}

        # Second run resumes: nothing new is appended.
        assert generate_and_save_sft_labels(
            [], cfg.agtd_out_file, mode="agtd", generator=FakeGenerator()
        ) == 0
        again = build_sft_dataset(cfg, generator=FakeGenerator())
        assert again["agtd"] == 0 and again["cttd"] == 0


def test_save_test_set_overwrites():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "nested", "test_set.jsonl")
        save_test_set([{"asin": "A"}], path)
        save_test_set([{"asin": "B"}, {"asin": "C"}], path)
        with open(path, encoding="utf-8") as f:
            assert [json.loads(line)["asin"] for line in f] == ["B", "C"]


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
