# msit-open-world

## Kiến trúc tổng quan

```text
/mnt/agents/output/msit/
├── config.py                  # hyperparams đúng paper (lr 3e-4, 10 epochs, T=0.2, top_p=0.7)
├── prompts/
│   ├── agtd_prompts.py        # Appendix A.1 (text/image tách riêng + 4 ICL examples), A.2 (merge)
│   ├── cttd_prompts.py        # Appendix A.3 — 5-step CoT nguyên văn
│   └── inference_prompts.py   # Table 4 (10 instructions), Table 5 (5 instructions)
├── data/
│   ├── seed_dataset.py        # seed attributes 4 category WOAM
│   ├── agtd_builder.py        # generate text/image riêng → review hook → merge (GPT-4)
│   └── cttd_builder.py        # 5-step CoT + contrastive pos/neg cân bằng
├── models/
│   ├── base_mllm.py           # protocol chung cho mọi backend
│   ├── mock_backend.py        # backend giả lập chạy end-to-end không cần GPU/API
│   ├── gpt4_backend.py        # GPT-4V thật (cắm OPENAI_API_KEY)
│   ├── lora_trainer.py        # LoRA finetune đúng paper (Adam, lr 3e-4, 10 epochs, Eq. 1)
│   └── llava_lora.py / qwen_lora.py / internlm_lora.py   # 3 MLLM của paper
├── inference/
│   ├── stage1_batch_gen.py    # batch generation + parse JSON
│   ├── stage2_dedup.py        # ★ word2vec one-to-one synonym + Rule 1/2/3 (Appendix B.2)
│   ├── stage3_cot_infer.py    # sequential validate, quyết định yes/no ở Step 5
│   └── pipeline.py            # orchestrate S1→S2→S3
├── evaluation/
│   ├── metrics.py             # ExactMatch/SimilarMatch + Precision/Recall
│   └── evaluate.py            # 5 trials, mean±std (đúng paper)
├── utils/ (json_parser, image_loader)
├── data_samples/sample_products.json
├── tests/test_msit.py         # 25 tests
└── demo.py                    # chạy demo end-to-end
```

## Cách chạy

```bash
cd /mnt/agents/output
python msit/tests/test_msit.py    # unit tests (không cần pytest)
python -m msit.demo             # demo S1→S2→S3 + metrics trên 3 sản phẩm mẫu
```

### Độ phủ và hạn chế

| Thành phần paper                    | Trạng thái                                                                                   |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| Prompts A.1/A.2/A.3, Table 4/5      | ✅ nguyên văn                                                                                 |
| AGTD/CTTD construction              | ✅ code đầy đủ, chạy được với GPT-4 backend thật                                              |
| Stage 2 dedup (3 luật + word2vec)   | ✅ logic đầy đủ, có test; word2vec thật cần `pip install gensim` + tải model                  |
| Stage 1 & 3 inference               | ✅ chạy end-to-end với mock                                                                   |
| LoRA training (LLaVA/Qwen/InternLM) | ✅ code đầy đủ nhưng cần GPU + `transformers/peft` để thực thi                                |
| Số liệu Table 1                     | ⚠️ không reproduce được trong môi trường CPU — cần WOAM/OAMine multimodal + 1×A100 như paper |

*Ghi chú*

- Để reproduce kết quả paper thật: (1) áp 2 bản vá trên, (2) cài gensim transformers peft accelerate + tải word2vec-google-news-300, (3) set OPENAI_API_KEY và chạy AGTDBuilder/CTTDBuilder với GPT4Backend trên WOAM/OAMine, (4) train LoRA trên GPU, (5) chạy MSITEvaluator với LLaVALoRABackend. Kiến trúc đã sẵn sàng cho toàn bộ quy trình này.
