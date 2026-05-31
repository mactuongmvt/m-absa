# Multilingual Aspect-Based Sentiment Analysis

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/docs/transformers)
[![PEFT](https://img.shields.io/badge/Hugging%20Face-PEFT-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/docs/peft)
[![Datasets](https://img.shields.io/badge/Hugging%20Face-Datasets-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/docs/datasets)
[![Kaggle](https://img.shields.io/badge/Kaggle-Notebook-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Nghiên cứu này xây dựng baseline cho bài toán **Multilingual Aspect-Based Sentiment Analysis (M-ABSA)** bằng `google/mt5-small`, sau đó so sánh với các mô hình ngôn ngữ lớn ở hai thiết lập: **zero-shot prompting** và **LoRA fine-tuning** trên ba ngôn ngữ English (`en`), Vietnamese (`vi`) và Chinese (`zh`).

Mục tiêu của bài toán là trích xuất các bộ ba:

```text
(entity, category, sentiment)
```

từ mỗi câu đánh giá. Ví dụ:

```text
The screen is beautiful but the battery is poor.
=> (screen, LAPTOP#DISPLAY, positive), (battery, LAPTOP#BATTERY, negative)
```

## Highlights

- Dùng `google/mt5-small` làm **baseline encoder-decoder** cho ABSA dạng text-to-text.
- So sánh baseline với các decoder-only LLM: Gemma 2, Qwen 2.5, Llama 3.1.
- Đánh giá các LLM ở cả **zero-shot prompting** và **LoRA fine-tuning**.
- Pipeline chạy chủ yếu trên Kaggle/Colab với GPU T4.
- Dataset M-ABSA gồm 38,135 mẫu từ 7 domain.

## Models

| Vai trò | Model | Hugging Face | Thiết lập |
|---------|-------|--------------|-----------|
| Baseline | mT5 Small | [`google/mt5-small`](https://huggingface.co/google/mt5-small) | Seq2Seq fine-tuning |
| Comparison LLM | Gemma 2 9B IT | [`google/gemma-2-9b-it`](https://huggingface.co/google/gemma-2-9b-it) | Zero-shot, LoRA |
| Comparison LLM | Qwen 2.5 7B Instruct | [`Qwen/Qwen2.5-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | Zero-shot, LoRA |
| Comparison LLM | Llama 3.1 8B Instruct | [`NousResearch/Meta-Llama-3.1-8B-Instruct`](https://huggingface.co/NousResearch/Meta-Llama-3.1-8B-Instruct) | Zero-shot, continued LoRA |

Các adapter/checkpoint dung lượng lớn không được commit trực tiếp vào GitHub. Xem thêm tại [models/README.md](models/README.md).

## Results

### Baseline: mT5 Clean-All Split

Notebook [mt5_baseline.ipynb](notebooks/mt5_baseline.ipynb) fine-tune `google/mt5-small` theo từng ngôn ngữ trên toàn bộ `clean_all.txt`, chia lại 80/10/10. Đây là baseline chính của repo.

| Language | Train | Validation | Test | Precision | Recall | F1 |
|----------|------:|-----------:|-----:|----------:|-------:|---:|
| EN | 10,189 | 1,274 | 1,274 | 0.3806 | 0.3389 | 0.3585 |
| VI | 10,157 | 1,270 | 1,270 | 0.3242 | 0.2670 | 0.2928 |
| ZH | 10,160 | 1,270 | 1,271 | 0.4113 | 0.3463 | 0.3760 |
| **Macro Avg** | - | - | - | **0.3720** | **0.3174** | **0.3424** |

Notebook mT5 cũng có các lần chạy nhỏ trước đó trên tập con/domain hẹp hơn; bảng trên lấy các kết quả cuối cùng trên `clean_all`.

### LLM Comparison Split

Kết quả dưới đây dùng split cân bằng theo 3 ngôn ngữ:

- Train: 1,002 mẫu, 334 mẫu/ngôn ngữ
- Validation: 501 mẫu, 167 mẫu/ngôn ngữ
- Test: 2,001 mẫu, 667 mẫu/ngôn ngữ

| Model | Setting | EN F1 | VI F1 | ZH F1 | Avg F1 |
|-------|---------|------:|------:|------:|-------:|
| Gemma 2 9B IT | Zero-shot | 0.230 | 0.210 | 0.210 | 0.217 |
| Qwen 2.5 7B Instruct | Zero-shot | 0.160 | 0.120 | 0.150 | 0.143 |
| Gemma 2 9B IT | LoRA, 5 epochs | 0.480 | 0.454 | 0.387 | 0.440 |
| Gemma 2 9B IT | LoRA, 7 epochs | 0.487 | 0.482 | 0.379 | 0.449 |
| Qwen 2.5 7B Instruct | LoRA, 5 epochs | **0.576** | **0.536** | **0.414** | **0.509** |
| Llama 3.1 8B Instruct | Continued LoRA, 2 epochs | 0.446 | 0.417 | 0.372 | 0.412 |

Do mT5 baseline và các LLM dùng split khác nhau, hai bảng kết quả không nên so sánh trực tiếp tuyệt đối. Bảng LLM dùng để so sánh tác động của zero-shot và LoRA fine-tuning giữa các mô hình lớn.

## Dataset

- **Nguồn**: M-ABSA Dataset
- **Tổng số mẫu dùng trong repo**: 38,135 câu
- **Ngôn ngữ**: English, Vietnamese, Chinese
- **Domain**: coursera, food, hotel, laptop, phone, restaurant, sight
- **Số category**: 241
- **Format**:

```text
text####[(entity, category, sentiment), ...]
```

Dataset không được lưu trực tiếp trong repo. Tải dữ liệu theo hướng dẫn tại [data/README.md](data/README.md).

## Repository Structure

```text
multilingual-absa/
├── README.md
├── requirements.txt
├── LICENSE
├── data/
│   └── README.md
├── models/
│   └── README.md
├── notebooks/
│   ├── gemma_zero_shot.ipynb
│   ├── gemma_finetune_5e.ipynb
│   ├── gemma_finetune_7e.ipynb
│   ├── qwen_zero_shot.ipynb
│   ├── qwen_finetune.ipynb
│   ├── llama-3-1_zeroshot.ipynb
│   ├── llama-3-1_finetune.ipynb
│   └── mt5_baseline.ipynb
├── src/
│   ├── data_loader.py
│   ├── inference.py
│   ├── metrics.py
│   └── prompts.py
├── results/
│   └── README.md
└── paper/
    └── README.md
```

## Setup

### Requirements

- Python 3.10+
- NVIDIA GPU khuyến nghị: T4 16GB VRAM trở lên
- Kaggle Notebook hoặc Google Colab
- Hugging Face token nếu model yêu cầu quyền truy cập hoặc cần tải nhanh hơn từ Hub

### Install

```bash
pip install -r requirements.txt
```

### Run Experiments

1. Tải dataset theo [data/README.md](data/README.md).
2. Cấu hình `HF_TOKEN` nếu cần:

```bash
export HF_TOKEN=your_huggingface_token
```

3. Chạy notebook theo thứ tự khuyến nghị:

```text
1. notebooks/mt5_baseline.ipynb
2. notebooks/gemma_zero_shot.ipynb
3. notebooks/qwen_zero_shot.ipynb
4. notebooks/llama-3-1_zeroshot.ipynb
5. notebooks/gemma_finetune_5e.ipynb
6. notebooks/gemma_finetune_7e.ipynb
7. notebooks/qwen_finetune.ipynb
8. notebooks/llama-3-1_finetune.ipynb
```

## Training Details

### mT5 Baseline

| Parameter | Value |
|-----------|-------|
| Base model | `google/mt5-small` |
| Objective | text-to-text generation |
| Split | 80% train, 10% validation, 10% test |
| Epochs | 5 on final clean-all runs |
| Learning rate | 3e-4 |
| Max input length | 128 |
| Max target length | 64 |

### LLM Zero-Shot / LoRA

Các mô hình Gemma, Qwen và Llama được dùng để so sánh với baseline theo hai hướng: prompt trực tiếp không huấn luyện lại và fine-tune bằng LoRA.

| Parameter | Value |
|-----------|-------|
| Quantization | 4-bit NF4, bitsandbytes |
| Optimizer | `paged_adamw_8bit` |
| Scheduler | cosine |
| Effective batch size | 16 |
| Max sequence length | 1536 tokens |

Gemma/Qwen experiments use LoRA adapters with low trainable-parameter ratio. Llama 3.1 continues training from an existing LoRA adapter and reports 5,505,024 trainable parameters, about 0.0685% of all parameters.

## Citation

Nếu sử dụng repo này, vui lòng trích dẫn dataset gốc:

```bibtex
@inproceedings{mabsa2025,
  title = {M-ABSA: A Multilingual Dataset for Aspect-Based Sentiment Analysis},
  booktitle = {Proceedings of EMNLP 2025},
  pages = {2530--2557},
  year = {2025},
  publisher = {Association for Computational Linguistics}
}
```

## License

Dự án được phát hành theo giấy phép MIT. Xem [LICENSE](LICENSE) để biết thêm chi tiết.
