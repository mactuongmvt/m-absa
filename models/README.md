# Mô Hình Đã Huấn Luyện

## Checkpoints / Adapters

Các checkpoint và LoRA adapter không được push trực tiếp lên GitHub do kích thước file. Các model nền được tải từ Hugging Face Hub; artifact đã train hiện được lưu theo dataset/output trên Kaggle.

### Gemma 2 9B - ABSA LoRA

- **Link**: https://www.kaggle.com/datasets/tiendq/gemma2-absa-lora
- **Base model**: google/gemma-2-9b-it
- **LoRA config**: r=8, alpha=16, target=[q_proj, v_proj, o_proj]
- **Training**: 5 epochs trên 1,002 mẫu (334/ngôn ngữ)

### Qwen 2.5 7B - ABSA LoRA

- **Link**: https://www.kaggle.com/datasets/tiendq/qwen25-absa-lora
- **Base model**: Qwen/Qwen2.5-7B-Instruct
- **LoRA config**: r=8, alpha=16, target=[q_proj, v_proj, o_proj]
- **Training**: 5 epochs trên 1,002 mẫu (334/ngôn ngữ)

### Llama 3.1 8B - ABSA LoRA

- **Base model**: NousResearch/Meta-Llama-3.1-8B-Instruct
- **Adapter output**: `/kaggle/working/Llama-3.1-absa-final`
- **Training**: continued LoRA fine-tuning, 2 epochs trên split cân bằng
- **Trainable params**: 5,505,024 / 8,035,766,272 (0.0685%)

### mT5 Small - ABSA Seq2Seq

- **Base model**: google/mt5-small
- **Checkpoint output**: `/kaggle/working/uabsa_mt5_clean_all`
- **Training**: 5 epochs trên `clean_all.txt`, split 80/10/10 theo từng ngôn ngữ

## Cách Sử Dụng

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch

# Load base model
model_id = "google/gemma-2-9b-it"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "YOUR_LORA_PATH")
model.eval()
```
