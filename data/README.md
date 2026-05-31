# Dữ Liệu

## Mô Tả Dataset

Nghiên cứu sử dụng tập dữ liệu **M-ABSA** (Multilingual Aspect-Based Sentiment Analysis) gồm các đánh giá (review) đa ngôn ngữ đã được gán nhãn.

### Thông tin chung
- **Tổng số mẫu**: 38,135 câu
- **Ngôn ngữ**: English (EN), Vietnamese (VI), Chinese (ZH)
- **Miền (Domain)**: coursera, food, hotel, laptop, phone, restaurant, sight
- **Số lượng category**: 241 categories (format: aspect#attribute)

### Format dữ liệu

Mỗi dòng có format:

```
text####[(entity, category, sentiment), (entity, category, sentiment), ...]
```

Ví dụ:
```
The staff was very friendly but the price was too high.####[('staff', 'SERVICE#GENERAL', 'positive'), ('price', 'RESTAURANT#PRICES', 'negative')]
```

### Cấu trúc thư mục dữ liệu gốc

```
data/
├── coursera/
│   ├── en/clean_all.txt
│   ├── vi/clean_all.txt
│   └── zh/clean_all.txt
├── food/
│   ├── en/clean_all.txt
│   ├── vi/clean_all.txt
│   └── zh/clean_all.txt
├── hotel/
│   └── ...
├── laptop/
│   └── ...
├── phone/
│   └── ...
├── restaurant/
│   └── ...
└── sight/
    └── ...
```

## Hướng Dẫn Tải Dataset

Dataset có thể tải từ: https://www.kaggle.com/datasets/tuongmacvan/m-absb-for-ppnckh

1. Tải dataset từ nguồn gốc (link ở trên)
2. Giải nén vào thư mục `data/`
3. Đảm bảo cấu trúc thư mục đúng như mô tả

## Thống Kê Theo Domain

| Domain | Số categories |
|--------|--------------|
| coursera | 28 |
| food | 10 |
| hotel | 34 |
| laptop | 75 |
| phone | 83 |
| restaurant | 13 |
| sight | 5 |

## Lưu Ý

- File dữ liệu gốc **không được push lên GitHub** do vấn đề bản quyền
- Chỉ push file README này với hướng dẫn tải
