"""
Module đọc và tiền xử lý dữ liệu M-ABSA.
"""
import os
import ast
import pandas as pd


def normalize_category(cat):
    """Chuẩn hóa category về format aspect#attribute."""
    cat = str(cat).lower().strip()
    if '#' in cat:
        return cat
    parts = cat.rsplit(' ', 1)
    if len(parts) == 2:
        asp = parts[0].strip().replace(' ', '_')
        att = parts[1].strip().replace(' ', '_')
        return f"{asp}#{att}"
    return cat


def convert_to_dict_format(true_labels):
    """Chuyển labels từ tuple sang dict format."""
    out = []
    for t in true_labels:
        if len(t) == 3:
            out.append({
                'entity': str(t[0]).strip(),
                'category': normalize_category(t[1]),
                'sentiment': str(t[2]).lower().strip()
            })
    return out


def load_data(input_dir, target_langs=None, target_file='clean_all.txt'):
    """
    Đọc dữ liệu M-ABSA từ thư mục.
    
    Args:
        input_dir: đường dẫn thư mục gốc chứa data
        target_langs: list ngôn ngữ cần đọc (default: ['en', 'vi', 'zh'])
        target_file: tên file dữ liệu (default: 'clean_all.txt')
    
    Returns:
        pandas DataFrame với các cột: language, text, true_labels, domain, formatted_true_labels
    """
    if target_langs is None:
        target_langs = ['en', 'vi', 'zh']

    all_data = []

    for root, dirs, files in os.walk(input_dir):
        folder_name = os.path.basename(root)
        if folder_name in target_langs:
            for file in files:
                if file == target_file:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            clean_line = line.strip()
                            if not clean_line or '####' not in clean_line:
                                continue
                            parts = clean_line.split('####')
                            text_part = parts[0].strip()
                            labels_part = parts[1].strip()
                            try:
                                true_labels = ast.literal_eval(labels_part)
                            except:
                                true_labels = []
                            all_data.append({
                                'language': folder_name,
                                'file_name': file,
                                'text': text_part,
                                'true_labels': true_labels,
                                'domain': os.path.basename(os.path.dirname(root))
                            })

    df = pd.DataFrame(all_data)
    df['formatted_true_labels'] = df['true_labels'].apply(convert_to_dict_format)
    return df


def stratified_sample(df, sample_per_lang, domains=None, random_state=42):
    """
    Lấy mẫu phân tầng theo domain cho mỗi ngôn ngữ.
    
    Args:
        df: DataFrame gốc
        sample_per_lang: số mẫu mỗi ngôn ngữ
        domains: list domain (default: tất cả domain trong data)
        random_state: seed
    
    Returns:
        DataFrame đã sampling
    """
    if domains is None:
        domains = df['domain'].unique().tolist()

    sample_per_domain = sample_per_lang // len(domains)
    frames = []

    for lang in df['language'].unique():
        sub = df[df['language'] == lang]
        parts = []
        for domain in domains:
            domain_rows = sub[sub['domain'] == domain]
            n = min(sample_per_domain, len(domain_rows))
            if n > 0:
                parts.append(domain_rows.sample(n=n, random_state=random_state))

        sampled = pd.concat(parts)
        remaining = sample_per_lang - len(sampled)
        if remaining > 0:
            extra = sub[~sub.index.isin(sampled.index)].sample(
                n=min(remaining, len(sub) - len(sampled)),
                random_state=random_state
            )
            sampled = pd.concat([sampled, extra])

        sampled = sampled.sample(frac=1, random_state=random_state).reset_index(drop=True)
        frames.append(sampled)

    return pd.concat(frames).reset_index(drop=True)
