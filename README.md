# MSIT Open-World Reproduction (`msit-open-world`)

Repository này chứa mã nguồn tái lập thực nghiệm cho bài báo *"Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning"* (ACL 2025).

> **Lưu ý theo quy định báo cáo:** Toàn bộ mô tả lý thuyết về giải pháp và các bảng kết quả thực nghiệm chi tiết được trình bày trong báo cáo khoa học của nhóm (`docs/BAO_CAO_KHOA_HOC.md`). Tài liệu `README.md` này chỉ tập trung hướng dẫn môi trường, phần cứng, cấu trúc tệp và các câu lệnh để chạy lại mã nguồn của nhóm.

---

## 1. Yêu cầu Phần cứng (Hardware Requirements)

Tùy thuộc vào chế độ chạy, hệ thống yêu cầu cấu hình phần cứng như sau:

1. **Chế độ Huấn luyện QLoRA và Suy luận MLLM thực tế (`finetune.ipynb` / GPU):**
   - **GPU:** Tối thiểu 01 GPU NVIDIA có **$\ge 16\text{ GB VRAM}$** (đã kiểm chứng trên **Kaggle NVIDIA Tesla T4 $\times 2$** hoặc **NVIDIA Tesla P100 16GB**, hoặc **NVIDIA A100 40GB/80GB**).
   - **RAM hệ thống:** Tối thiểu $16\text{ GB}$ (khuyến nghị $29\text{ GB}$ trên môi trường Kaggle).
   - **Dung lượng ổ cứng trống:** Tối thiểu $30\text{ GB}$ để lưu trữ checkpoint mô hình gốc từ HuggingFace (`LLaVA-1.5-7B`, `Qwen2-VL-7B-Instruct`, `InternLM-XComposer2-7B`) và bộ dữ liệu ảnh.

2. **Chế độ Kiểm thử Logic Pipeline và Chạy thử nghiệm Cục bộ (`msit/demo.py`, `msit/tests/test_msit.py` / CPU):**
   - **CPU:** Bất kỳ bộ vi xử lý đa nhân tiêu chuẩn (x86_64 / ARM64).
   - **RAM hệ thống:** Tối thiểu $4\text{ GB}$ ($8\text{ GB}$ nếu tải mô hình nhúng từ `word2vec-google-news-300` qua `gensim`).
   - Không yêu cầu GPU.

---

## 2. Môi trường Phần mềm và Cài đặt (Environment Setup)

### 2.1. Phiên bản Python và Hệ điều hành

- **Hệ điều hành:** Linux (Ubuntu 20.04/22.04), Windows 10/11, hoặc macOS.
- **Python:** `>= 3.10` (khuyến nghị `Python 3.10` hoặc `3.11`).

### 2.2. Cài đặt Mã nguồn và Thư viện Phụ thuộc

```bash
# 1. Sao chép repository về máy
git clone https://github.com/linhnnh688/msit-open-world.git
cd msit-open-world

# 2. Tạo và kích hoạt môi trường ảo (khuyến nghị)
python -m venv .venv
# Trên Linux/macOS:
source .venv/bin/activate
# Trên Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 3. Cài đặt các thư viện phục vụ huấn luyện và suy luận MLLM trên GPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install "transformers==4.44.2" "peft==0.13.2" "accelerate==0.34.2" \
            "bitsandbytes==0.43.3" "datasets==3.0.1" \
            safetensors sentencepiece Pillow gensim openai wandb huggingface_hub
```

### 2.3. Thiết lập Biến môi trường (Environment Variables)

Khi chạy huấn luyện mô hình thực tế, sinh dữ liệu với OpenAI API hoặc ghi nhận nhật ký lên Weights & Biases, thiết lập các biến môi trường sau:

```bash
# Trên Linux/macOS:
export HF_TOKEN="<huggingface_access_token_cua_ban>"
export WANDB_API_KEY="<wandb_api_key_cua_ban>"
export OPENAI_API_KEY="<openai_api_key_neu_chay_gpt4_backend>"

# Trên Windows (PowerShell):
$env:HF_TOKEN="<huggingface_access_token_cua_ban>"
$env:WANDB_API_KEY="<wandb_api_key_cua_ban>"
$env:OPENAI_API_KEY="<openai_api_key_neu_chay_gpt4_backend>"
```

---

## 3. Cấu trúc Mã nguồn và Tệp thực thi (Repository Structure)

```text
msit-open-world/
├── finetune.ipynb                      # Notebook huấn luyện QLoRA & suy luận trên Kaggle/GPU
├── msit/
│   ├── config.py                       # Cấu hình siêu tham số huấn luyện, suy luận và lọc
│   ├── demo.py                         # Kịch bản chạy thực nghiệm pipeline đầu-cuối (S1 -> S2 -> S3)
│   ├── notebooks/
│   │   ├── msit-open-world-0ea169.ipynb          # Notebook gốc (code dữ liệu viết trực tiếp trong cell)
│   │   └── msit-open-world-data-pipeline.ipynb   # Notebook tái dựng: chỉ gọi package `msit`
│   ├── prompts/
│   │   ├── agtd_prompts.py             # Các hàm tạo prompt trích xuất và hợp nhất AGTD
│   │   ├── cttd_prompts.py             # Các hàm tạo prompt suy luận 5 bước CTTD
│   │   └── inference_prompts.py        # Danh sách instructions cho Stage 1 và Stage 3
│   ├── data/
│   │   ├── seed_dataset.py             # Quản lý tập thuộc tính hạt giống theo ngành hàng
│   │   ├── agtd_builder.py             # Pipeline khởi tạo dữ liệu AGTD
│   │   ├── cttd_builder.py             # Pipeline khởi tạo dữ liệu CTTD đối kháng âm/dương
│   │   ├── jsonl.py                    # Tiện ích đọc/ghi định dạng JSONL
│   │   ├── readers.py                  # Đọc annotation WOAM / OAMine thô
│   │   ├── preparator.py               # Lọc nhiễu, cân bằng danh mục, chia tập động (test/AGTD/CTTD)
│   │   ├── sft_labels.py               # Ghi JSONL nhãn AGTD/CTTD có thể chạy tiếp (resume)
│   │   ├── build_sft.py                # Driver đầu-cuối dựng dữ liệu SFT (Kaggle)
│   │   └── sft_datasets/               # Tập dữ liệu huấn luyện (agtd_train.jsonl, cttd_train.jsonl) và test_set.jsonl
│   ├── models/
│   │   ├── base_mllm.py                # Giao diện chuẩn cho các backend MLLM
│   │   ├── mock_backend.py             # Backend giả lập phục vụ kiểm thử không cần GPU
│   │   ├── gpt4_backend.py             # Backend kết nối OpenAI GPT-4V API
│   │   ├── lora_trainer.py             # Bộ huấn luyện LoRA/QLoRA cho các MLLM
│   │   ├── qwen_local.py               # Generator Qwen2.5-VL 4-bit sinh nhãn AGTD/CTTD tại chỗ
│   │   ├── llava_lora.py               # Wrapper suy luận cho LLaVA-1.5-7B + LoRA
│   │   ├── qwen_lora.py                # Wrapper suy luận cho Qwen-VL / Qwen2-VL + LoRA
│   │   └── internlm_lora.py            # Wrapper suy luận cho InternLM-XComposer2-7B + LoRA
│   ├── inference/
│   │   ├── stage1_batch_gen.py         # Giai đoạn 1: Sinh thuộc tính theo lô
│   │   ├── stage2_dedup.py             # Giai đoạn 2: Lọc thuộc tính trùng lặp với Word2Vec
│   │   ├── stage3_cot_infer.py         # Giai đoạn 3: Kiểm chứng tuần tự bằng CoT 5 bước
│   │   └── pipeline.py                 # Điều phối pipeline suy luận 3 giai đoạn
│   ├── evaluation/
│   │   ├── metrics.py                  # Độ đo Exact Match, Similar Match, Precision, Recall
│   │   └── evaluate.py                 # Chạy đánh giá lặp 5 trials với random seeds độc lập
│   ├── results/
│   │   ├── msit_qwen_lora/             # Các checkpoints quá trình huấn luyện (checkpoint-82, 164, 246)
│   │   └── msit_qwen_lora_final/       # Trọng số LoRA adapter hoàn chỉnh sau huấn luyện
│   ├── data_samples/
│   │   └── sample_products.json        # Dữ liệu mẫu kiểm thử nhanh pipeline
│   ├── tests/
│   │   ├── test_msit.py                # Bộ kiểm thử đơn vị (Unit tests)
│   │   └── test_data_build.py          # Kiểm thử readers, chia tập và ghi nhãn SFT
│   └── utils/
│       ├── image_loader.py             # Tiện ích tải và tiền xử lý ảnh sản phẩm
│       └── json_parser.py              # Bộ phân tích cú pháp JSON đầu ra của MLLM
└── docs/                               # Thư mục chứa bài báo gốc và báo cáo khoa học của nhóm
```

---

## 4. Hướng dẫn Chạy lại Kết quả Thực nghiệm (How to Run)

### 4.1. Chạy Kiểm thử Đơn vị (Unit Tests) và Demo Pipeline 3 Giai đoạn

Không yêu cầu GPU hay khóa API, dùng để xác minh toàn bộ các mô-đun từ tiền xử lý prompt, lọc trùng lặp Giai đoạn 2, suy luận Giai đoạn 3 đến hàm tính độ đo:

```bash
# Chạy bộ kiểm thử đơn vị
python msit/tests/test_msit.py
python msit/tests/test_data_build.py

# Chạy thực thi pipeline 3 giai đoạn (Stage 1 -> Stage 2 -> Stage 3) và xuất độ đo
python -m msit.demo
```

### 4.2. Dựng lại dữ liệu SFT (AGTD / CTTD / Test) bằng Qwen2.5-VL 4-bit

Toàn bộ logic dựng dữ liệu nằm trong `msit/data` và `msit/models/qwen_local.py`; notebook
`msit/notebooks/msit-open-world-data-pipeline.ipynb` chỉ cấu hình đường dẫn Kaggle và gọi các hàm này.

```bash
# Một lệnh cho toàn bộ pipeline (mặc định theo layout Kaggle)
python -m msit.data.build_sft \
    --input-dir /kaggle/input/datasets/kunzero106/msit-open-world-dataset \
    --working-dir /kaggle/working
```

- Input yêu cầu: `<input-dir>/datasets/oamine/annotations/<Category>.jsonl` và `<input-dir>/datasets/images/oamine/<asin>.jpg`.
- Output: `splits_checkpoint.json`, `test_set.jsonl`, `agtd_train.jsonl`, `cttd_train.jsonl` trong `--working-dir`.
- Chạy lại sẽ đọc `splits_checkpoint.json` và bỏ qua các ASIN đã sinh nhãn; dùng `--rebuild` để chia tập lại từ đầu.

### 4.3. Chạy Huấn luyện QLoRA bằng Notebook `finetune.ipynb` (Trên Kaggle hoặc Máy trạm GPU)

1. Mở tệp **`finetune.ipynb`** trên môi trường **Kaggle Notebook** (hoặc JupyterLab có GPU $\ge 16\text{ GB VRAM}$).
2. Trong phần **Settings** của Kaggle:
   - Chọn **Accelerator**: `GPU T4 x2` hoặc `GPU P100`.
   - Bật **Internet**: `ON`.
   - Trong mục **Add-ons $\rightarrow$ Secrets**, thêm `HF_TOKEN` (và `WANDB_API_KEY` nếu bật đồng bộ trực tiếp lên Weights & Biases).
3. Dữ liệu huấn luyện đã được chuẩn bị sẵn trong `msit/data/sft_datasets/agtd_train.jsonl` (1.000 mẫu) và `msit/data/sft_datasets/cttd_train.jsonl` (300 mẫu) hoặc gắn qua thư mục `/kaggle/input/msit-data/`.
4. Thực thi tuần tự các ô lệnh (Run All) trong `finetune.ipynb` để:
   - Cài đặt thư viện và nạp cấu hình `MSITConfig`.
   - Huấn luyện LoRA adapter thông qua `msit.models.lora_trainer.LoRATrainer` cho các mô hình (`llava-hf/llava-1.5-7b-hf`, `Qwen/Qwen-VL-Chat` / `Qwen/Qwen2-VL-7B-Instruct`, `internlm/internlm-xcomposer2-7b`).
   - Lưu trọng số adapter vào thư mục đích (ví dụ: `msit/results/msit_qwen_lora_final/`) và chạy kiểm thử suy luận.

### 4.4. Chạy Đánh giá 5 Lần Độc lập (5 Independent Trials Evaluation) với Adapter đã Huấn luyện

Để nạp trọng số LoRA đã huấn luyện trong `msit/results/msit_qwen_lora_final/` và chạy đánh giá 5 lần thử nghiệm độc lập (`n_trials = 5`, `temperature = 0.2`, `top_p = 0.7`) trên tập kiểm thử `msit/data/sft_datasets/test_set.jsonl`:

```bash
python -c "
from msit.config import MSITConfig
from msit.data.jsonl import load_jsonl
from msit.models.qwen_lora import QwenVLLoRABackend
from msit.evaluation.evaluate import MSITEvaluator

cfg = MSITConfig()
backend = QwenVLLoRABackend(
    cfg=cfg,
    model_name_or_path='Qwen/Qwen2-VL-7B-Instruct',
    lora_weights='msit/results/msit_qwen_lora_final'
)
backend.load()

test_samples = load_jsonl('msit/data/sft_datasets/test_set.jsonl')
evaluator = MSITEvaluator(backend=backend, cfg=cfg)
print(evaluator.evaluate(test_samples))
"
```
