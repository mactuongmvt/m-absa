# Notebooks

## Danh sách notebook

| File | Mô tả | Model | Phương pháp |
|------|--------|-------|-------------|
| gemma_zero_shot.ipynb | Đánh giá zero-shot Gemma 2 | google/gemma-2-9b-it | Zero-shot với few-shot prompt |
| gemma_finetune_5e.ipynb | Fine-tune Gemma 2 (5 epochs) | google/gemma-2-9b-it | LoRA + SFTTrainer |
| gemma_finetune_7e.ipynb | Tiếp tục fine-tune (7 epochs) | google/gemma-2-9b-it | LoRA (load checkpoint từ 5e) |
| qwen_zero_shot.ipynb | Đánh giá zero-shot Qwen 2.5 | Qwen/Qwen2.5-7B-Instruct | Zero-shot với few-shot prompt |
| qwen_finetune.ipynb | Fine-tune Qwen 2.5 (5 epochs) | Qwen/Qwen2.5-7B-Instruct | LoRA + SFTTrainer |
| llama-3-1_zeroshot.ipynb | Đánh giá zero-shot Llama 3.1 | NousResearch/Meta-Llama-3.1-8B-Instruct | Zero-shot với prompt ABSA |
| llama-3-1_finetune.ipynb | Tiếp tục fine-tune và đánh giá Llama 3.1 | NousResearch/Meta-Llama-3.1-8B-Instruct | Continued LoRA + SFTTrainer |
| mt5_baseline.ipynb | Baseline mT5 theo từng ngôn ngữ trên clean_all | google/mt5-small | Seq2SeqTrainer |

## Hướng dẫn chạy trên Kaggle

1. Tạo notebook mới trên Kaggle
2. Upload file `.ipynb` hoặc copy code vào
3. **Settings**:
   - Accelerator: **GPU T4 x2** (hoặc T4 x1)
   - Internet: **On**
4. **Attach dataset**: Thêm dataset `tuongmacvan/m-absb-for-ppnckh`
5. Tạo file `.env` với HuggingFace token (hoặc sửa code login trực tiếp)
6. Chạy tuần tự từ trên xuống (Run All)

## Thứ tự chạy khuyến nghị

```
1. mt5_baseline.ipynb         → Train mT5 baseline trên clean_all split
2. gemma_zero_shot.ipynb      → Zero-shot Gemma (không cần train)
3. qwen_zero_shot.ipynb       → Zero-shot Qwen (không cần train)
4. llama-3-1_zeroshot.ipynb   → Zero-shot Llama 3.1 (không cần train)
5. gemma_finetune_5e.ipynb    → Train Gemma LoRA 5 epochs
6. gemma_finetune_7e.ipynb    → Tiếp tục train từ checkpoint 5e (cần output của bước 5)
7. qwen_finetune.ipynb        → Train Qwen LoRA 5 epochs
8. llama-3-1_finetune.ipynb   → Tiếp tục train/evaluate Llama 3.1 LoRA
```

## Lưu ý

- Tất cả notebook được thiết kế để chạy trên **Kaggle** với GPU T4
- Zero-shot: khoảng 2-4 giờ (tùy số mẫu)
- Fine-tuning: khoảng 1-2 giờ cho 5 epochs
- `gemma_finetune_7e.ipynb` cần LoRA checkpoint từ `gemma_finetune_5e.ipynb` (upload lên Kaggle Dataset trước)
- `llama-3-1_finetune.ipynb` cần LoRA checkpoint đầu vào đã upload lên Kaggle Dataset
- Nhớ tạo file `.env` hoặc set biến môi trường `HF_TOKEN` trước khi chạy
