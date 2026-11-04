# Bước 1 & 2: Review bài báo và xác định modules/functions

## 1.1 Tổng quan bài báo

**Tên:** *Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning* (MSIT) — ACL 2025 Long Paper.

**Bài toán:** Khai thác thuộc tính sản phẩm e-commerce ở **open-world setting** — trích xuất các cặp `attribute: value` từ **title + bullet points + ảnh sản phẩm**, mà **không giới hạn schema có sẵn** (khác với các phương pháp classification truyền thống như OpenTag, CMA-CLIP).

**Hai hạn chế mà bài báo giải quyết:**

1. **Underutilization of multimodal information** — các phương pháp cũ (OA-Mine, Amacer) chỉ dùng text, bỏ qua thuộc tính chỉ có trên ảnh (vd: shape, weight trên bao bì).
2. **Absence of explicit reasoning** — MLLM generate trực tiếp mà không kiểm chứng → sinh ra "Marketing Claims" vô nghĩa, không tự sửa lỗi.

## 1.2 Kiến trúc MSIT (3 thành phần chính)

### Thành phần 1: Xây dựng AGTD (Attribute Generation Tuning Data)

- **Raw data:** mở rộng 2 dataset unimodal (WOAM: Tea/Vitamin/Sofa/Phone Case; OAMine: 100 product types) thành multimodal bằng ảnh Amazon.
- **Seed dataset:** tập nhỏ thuộc tính được gán thủ công theo từng loại sản phẩm (WOAM: ~16.5 loại thuộc tính, 22 giá trị/loại).
- **In-context learning với GPT-4:** extract thuộc tính **riêng từng modality** (ảnh và text tách riêng) vì khi đưa cả hai cùng lúc, GPT-4 bị bias về text (§3.1). Prompt ở Appendix A.1.
- **Manual review** lọc thuộc tính sai, rồi GPT-4 **merge** attributes từ ảnh + text (Appendix A.2).

### Thành phần 2: Xây dựng CTTD (Chain-of-Thought Tuning Data)

- Chuỗi suy luận **5 bước có cấu trúc** (giảm hallucinated rationales so với CoT vanilla):
  1. **Product Type Range Narrowing** — xác định loại sản phẩm từ ảnh+text
  2. **Reasoning with Internal Common-sense** — phân tích nghĩa của attribute, dùng common sense sơ bộ đánh giá có phù hợp loại SP không
  3. **Image-Based Attribute Validation** — dùng ảnh đoán giá trị gần đúng để xác nhận thuộc tính
  4. **Text-Based Attribute Verification** — nếu phù hợp, trích giá trị chính xác từ text
  5. **Final Evaluation and Decision-Making** — tổng hợp, kết luận **yes/no**
- **Contrastive CoT data:** positive = attributes đã review của chính sản phẩm; negative = attributes lấy ngẫu nhiên từ sản phẩm khác; cân bằng 2 loại để chống overfit.

### Thành phần 3: Huấn luyện & 3-Stage Inference

- **Training:** LoRA fine-tune 3 MLLM (LLaVA-7B, Qwen-VL, InternLM), Adam lr=3e-4, 10 epochs, A100, sampling top_p, temperature=0.2, top_p=0.7. Output format phải gồm **attribute-value pairs** (Attri-Value tốt hơn Attri-only đáng kể, Table 3).
- **Inference 3 giai đoạn:**
  - **S1 — Batch Attribute Generation:** model sinh hàng loạt attribute-value pairs (JSON), dùng 10 instruction variant (Table 4).
  - **S2 — Filtering Repeated Attributes:** rule-based dedup dùng **word2vec-google-news-300**, cosine similarity với ngưỡng; 3 luật xóa dựa trên số subwords:
    - Rule 1: một cụm có 1 subword (A), cụm kia (B) — nếu B có đúng 3 subwords → xóa A; nếu B > 3 → xóa B
    - Rule 2: A có 2 subwords, B có ≥3 → xóa B
    - Rule 3: cùng số subwords → xóa ngẫu nhiên 1 cái
  - **S3 — Sequential Attribute Inference:** lần lượt đưa từng attribute qua 5-step CoT, giữ lại nếu kết luận cuối = "yes".

## 1.3 Kết quả tham chiếu (để so sánh khi reproduce)

| Model | WOAM SimilarMatch P/R | WOAM ExactMatch P/R | OAMine SimilarMatch P/R | OAMine ExactMatch P/R |
| --- | --- | --- | --- | --- |
| GPT-4 | 52.03 / 65.35 | 15.51 / 41.60 | 64.92 / 55.75 | 29.25 / 33.72 |
| **MSIT (LLaVA-7B)** | **66.90 / 66.99** | **35.34 / 52.50** | **74.50 / 63.06** | **54.33 / 51.54** |

Ablation quan trọng (WOAM, SimilarMatch P): baseline LLaVA 40.49 → +AGTD 62.15 → +CTTD 50.15 (riêng lẻ) → AGTD+CTTD 63.89 → +S1,S2 63.72 → **full (S1+S2+S3) 66.90**. S3 (CoT self-correction) là chìa khóa tăng precision.

---

## 2. Các modules/functions cần có (thiết kế ban đầu)

> Cây dưới đây là thiết kế lúc lập kế hoạch. Cấu trúc thực tế sau triển khai (và sau dọn dẹp
> ngày 2026-11-04) được ghi ở **mục 4** — dùng mục 4 khi cần tra cứu file.

```text
msit/
├── config.py                     # hyperparams: lr=3e-4, epochs=10, temp=0.2, top_p=0.7...
│
├── prompts/
│   ├── agtd_prompts.py           # A.1 (text/image extract + ICL examples), A.2 (merge)
│   ├── cttd_prompts.py           # A.3 (5-step CoT template, task description)
│   └── inference_prompts.py      # Table 4 (10 batch-gen instructions), Table 5 (5 filter instructions)
│
├── data/
│   ├── seed_dataset.py           # load/validate seed attribute JSON per category
│   ├── agtd_builder.py           # generate_attributes(image), generate_attributes(text),
│   │                             #   review(), merge_modalities() → AGTD samples
│   ├── cttd_builder.py           # build_cot_sample(), sample_contrastive_negatives(),
│   │                             #   balance_pos_neg()
│   └── dataset.py                # InstructionDataset (image+text+instruction → target)
│
├── models/
│   ├── base_mllm.py              # MLLMBackend interface: generate(image, text, prompt)
│   ├── gpt4_backend.py           # GPT-4 API backend (AGTD/CTTD construction)
│   ├── lora_trainer.py           # LoRA finetune (peft), Adam, cosine sched
│   └── llava_lora.py, qwen_lora.py, internlm_lora.py   # 3 model wrappers
│
├── inference/
│   ├── stage1_batch_gen.py       # batch_generate() → parse attribute JSON
│   ├── stage2_dedup.py           # SubwordTokenizer, cosine_sim(), are_synonyms(),
│   │                             #   apply_deletion_rules() (Rule1/2/3)
│   └── stage3_cot_infer.py       # sequential_validate(attr) → 5-step reasoning → yes/no
│
├── evaluation/
│   ├── metrics.py                # exact_match(), similar_match(synonyms), precision/recall
│   └── evaluate.py               # run 5 trials w/ random seeds, report mean±std
│
└── utils/
    ├── json_parser.py            # robust extraction of {"Attributes": {...}} from output
    └── image_loader.py           # load/resize product images
```

**Các function cốt lõi nhất (theo paper):** `merge_modalities`, `build_cot_sample` (5 bước), `apply_deletion_rules` (3 luật + word2vec), `sequential_validate`, `similar_match` metric.

## 3. Kế hoạch thực thi (đã hiệu chỉnh theo môi trường)

⚠️ **Ràng buộc thực tế:** môi trường này **không có GPU** (torch CPU, 4GB RAM, thiếu transformers/peft/gensim, không có API GPT-4). Vì vậy kế hoạch reproduce chia 2 tầng:

| Phase | Nội dung | Cách kiểm chứng |
| --- | --- | --- |
| **P1 — Core pipeline (logic thuần)** | Toàn bộ prompts (A.1–A.3, Table 4/5), stage1 parsing, stage2 dedup rules, stage3 CoT orchestration, metrics exact/similar match | Unit tests + end-to-end với **mock LLM backend** (trả về JSON mẫu) → chạy được ngay |
| **P2 — Data construction** | `agtd_builder`, `cttd_builder` với GPT-4 backend thật (code sẵn, cắm API key là chạy); seed dataset mẫu | Smoke test với mock |
| **P3 — Training** | Script LoRA finetune LLaVA/Qwen/InternLM đúng hyperparams paper (lr 3e-4, 10 epochs, Adam) | Code review + dry-run shape check (không train được do thiếu GPU) |
| **P4 — Eval** | `evaluate.py` chạy 5 trials, mean±std; demo nhỏ trên mock data | Chạy được, so sánh trend với Table 2 |

---

## 4. Cập nhật trạng thái triển khai (2026-11-04)

### 4.1. Cấu trúc thực tế (sau dọn dẹp)

Chú thích: **[I]** = cần cho inference/đánh giá, **[T]** = huấn luyện, **[D]** = dựng dữ liệu.

```text
msit/
├── config.py                    [I/T] hyperparams (lr, epochs, temp, top_p, ngưỡng dedup, ...)
├── demo.py                      [I]   demo 3 giai đoạn với MockMLLMBackend, không cần GPU
├── notebooks/
│   ├── msit-open-world-0ea169.ipynb          [D] notebook gốc (giữ làm tham chiếu)
│   └── msit-open-world-data-pipeline.ipynb   [D] notebook tái dựng, chỉ gọi package msit
├── prompts/                     [I]   agtd_prompts, cttd_prompts, inference_prompts
├── data/
│   ├── jsonl.py                 [I/T] load_jsonl dùng khi nạp test_set/train
│   ├── readers.py               [D]   WOAMRawReader, OAMineRawReader
│   ├── preparator.py            [D]   lọc nhiễu, cân bằng danh mục, chia tập động 13% CTTD
│   ├── sft_labels.py            [D]   ghi JSONL nhãn có resume theo ASIN
│   ├── build_sft.py             [D]   driver `python -m msit.data.build_sft`
│   ├── agtd_builder.py          [D]   dựng AGTD qua backend (finetune.ipynb fallback + tests)
│   ├── cttd_builder.py          [D]   dựng CTTD đối lập (finetune.ipynb fallback + tests)
│   ├── seed_dataset.py          [D]   seed attributes, dùng bởi agtd_builder + tests
│   └── sft_datasets/            [T/I] agtd_train.jsonl, cttd_train.jsonl, test_set.jsonl
├── models/
│   ├── base_mllm.py             [I]   protocol MLLMBackend
│   ├── mock_backend.py          [I]   backend giả lập cho demo/test
│   ├── gpt4_backend.py          [D]   backend OpenAI tuỳ chọn (không được import ở đâu)
│   ├── qwen_local.py            [D]   Qwen2.5-VL 4-bit sinh nhãn AGTD/CTTD tại chỗ
│   ├── lora_trainer.py          [T]   LoRATrainer + build_prompt (3 wrapper bên dưới import)
│   ├── llava_lora.py            [I]   LLaVA-1.5-7B + LoRA
│   ├── qwen_lora.py             [I]   Qwen-VL/Qwen2-VL + LoRA
│   └── internlm_lora.py         [I]   InternLM-XComposer2 + LoRA
├── inference/                   [I]   stage1_batch_gen, stage2_dedup, stage3_cot_infer, pipeline
├── evaluation/                  [I]   metrics (EM/SM, P/R), evaluate (5 trials, mean±std)
├── results/msit_qwen_lora_final [I]   LoRA adapter hoàn chỉnh (base Qwen2-VL-7B)
├── data_samples/                [I]   sample_products.json cho demo
├── tests/                             test_msit.py, test_data_build.py
└── utils/json_parser.py         [I]   parse attributes/JSON từ output MLLM
```

Khác biệt so với thiết kế ban đầu (mục 2):

- `data/dataset.py` không cần: dữ liệu là `list[dict]` + collate bên trong `LoRATrainer`.
- `utils/image_loader.py` từng được viết nhưng **không ai import** → đã xóa.
- Bổ sung 5 module dựng dữ liệu: `readers.py`, `preparator.py`, `sft_labels.py`, `build_sft.py`, `models/qwen_local.py`
  (thay đường GPT-4 API bằng Qwen2.5-VL 4-bit chạy local trên Kaggle).
- `finetune.ipynb` và `msit/demo.py` vẫn dùng `agtd_builder`/`cttd_builder`/`mock_backend` nên các file này được giữ.

### 4.2. Nhật ký dọn dẹp (2026-11-04)

| Đã xóa | Kích thước | Lý do |
| --- | ---: | --- |
| `msit/utils/image_loader.py` | nhỏ | 0 tham chiếu trong toàn repo |
| `msit/results/__huggingface_repos__.json` | nhỏ | metadata cache HuggingFace |
| `msit/data/sft_datasets/__huggingface_repos__.json` | nhỏ | metadata cache HuggingFace |
| `msit/data/sft_datasets/splits_checkpoint.json` | 7,7 MB | cache chia tập, tái tạo bằng `build_sft`; các `.jsonl` đã chứa đủ ASIN |
| `msit/results/msit_qwen_lora/checkpoint-{82,164,246}` | 92 MB | checkpoint trung gian; inference chỉ dùng `msit_qwen_lora_final/` |

Giữ nguyên vì đang được dùng: toàn bộ `inference/`, `evaluation/`, `prompts/`, 3 wrapper LoRA, `mock_backend`,
`lora_trainer`, `demo.py`, `data_samples/`, tests, `results/msit_qwen_lora_final/`, cả 2 notebook.

`msit/` giảm từ ~138 MB xuống ~40 MB.

### 4.3. Bằng chứng huấn luyện (trích trước khi xóa checkpoint)

Từ `trainer_state.json` của các checkpoint đã xóa; mỗi epoch = 82 step.

| Checkpoint | Epoch | Global step | Loss |
| --- | ---: | ---: | --- |
| checkpoint-82 | 1.0 | 82 | 2.0925 (step 10) → 1.2728 (step 70) |
| checkpoint-164 | 2.0 | 164 | → 1.2500 (step 150) |
| checkpoint-246 | 3.0 | 246 | → 1.1976 (step 230) |

Adapter còn lại: base `Qwen/Qwen2-VL-7B-Instruct`, LoRA `r=16`, `alpha=32`, `dropout=0.05`,
`target_modules=[q_proj, v_proj]`, `task_type=CAUSAL_LM`.

### 4.4. Bug registry (lỗi đã biết, chưa sửa)

Hai test fail có sẵn từ commit `f2d64ce`, không liên quan dọn dẹp:

| Triệu chứng | Nguyên nhân gốc | Cách phát hiện | Trạng thái |
| --- | --- | --- | --- |
| `test_parse_conclusion` fail: `parse_conclusion("...\nConclusion: no")` trả `None`, không phải `False` | Sau `split("conclusion", 1)`, chuỗi còn `": no"`; `.strip(".!")` không bỏ dấu `:`, nên nhánh `startswith("no")` không khớp. Nhánh "yes" vẫn đúng nhờ fallback `" yes" in last_par` | `python -c "from msit.inference.stage3_cot_infer import parse_conclusion; print(parse_conclusion('Conclusion: no'))"` → `None` | Chưa sửa (Stage 3 coi `None` là loại bỏ nên ảnh hưởng hạn chế) |
| `test_cttd_builder_balanced` fail: cả 4 mẫu đều nhãn `no` | Test tạo `MockMLLMBackend()` **không có `attributes_db`**, nên `_answer_cot` luôn kết luận "no" kể cả với mẫu dương | Chạy lại test với `MockMLLMBackend({"P1": {"a1": "x"}, ...})` → nhãn cân bằng `['yes','no','yes','no']` | Chưa sửa (lỗi ở test setup, không phải builder) |

### 4.5. Kiểm chứng sau dọn dẹp

- `python msit/tests/test_data_build.py` → 10/10 pass.
- `python msit/tests/test_msit.py` → 23/25 (đúng như trước dọn dẹp, 2 lỗi ở 4.4).
- `python -m msit.demo` → Pre/Recall = 1.0000 trên dữ liệu mock.
- Import toàn bộ package (`msit.data`, `msit.models`, `msit.inference.pipeline`, `msit.evaluation.evaluate`) OK.
