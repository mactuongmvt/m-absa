# Kết Quả Thí Nghiệm

## Các File Kết Quả

<!-- TODO: Copy các file CSV kết quả vào đây và đổi tên cho rõ ràng -->

| File | Mô tả |
|------|--------|
| gemma_zero_shot.csv | Kết quả Gemma 2 zero-shot (1500 mẫu) |
| gemma_finetuned_5e.csv | Kết quả Gemma 2 sau fine-tune 5 epochs |
| gemma_finetuned_7e.csv | Kết quả Gemma 2 sau fine-tune 7 epochs |
| qwen_zero_shot.csv | Kết quả Qwen 2.5 zero-shot (3000 mẫu) |
| qwen_finetuned.csv | Kết quả Qwen 2.5 sau fine-tune |

## Format File CSV

Mỗi file CSV chứa các cột:
- `Language`: Ngôn ngữ (en/vi/zh)
- `Text`: Câu đánh giá gốc
- `True_Labels`: Nhãn ground truth (JSON)
- `Predicted_Labels`: Nhãn dự đoán của model (JSON)

## Tổng Hợp Kết Quả

<!-- TODO: Điền kết quả thực tế sau khi chạy xong tất cả thí nghiệm -->

### Bảng so sánh F1-Score

| Mô hình | Phương pháp | EN | VI | ZH | Trung bình |
|---------|-------------|-----|-----|-----|-----------|
| Gemma 2 9B | Zero-shot | 0.23 | 0.21 | 0.21 | 0.22 |
| Gemma 2 9B | LoRA 5e | 0.480 | 0.454 | 0.387 | 0.440 |
| Gemma 2 9B | LoRA 7e | 0.487 | 0.482 | 0.379 | 0.449 |
| Qwen 2.5 7B | Zero-shot | 0.16 | 0.12 | 0.15 | 0.14 |
| Qwen 2.5 7B | LoRA 5e | 0.576 | 0.536 | 0.414 | 0.509 |
