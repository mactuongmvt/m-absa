"""
Các template prompt cho bài toán ABSA.
"""
from collections import defaultdict


def group_categories(category_list):
    """Nhóm categories theo aspect để hiển thị gọn trong prompt."""
    groups = defaultdict(list)
    for cat in category_list:
        if '#' not in cat:
            continue
        asp, att = cat.split('#', 1)
        groups[asp].append(att)
    return "\n".join(
        f"  {asp}: [{', '.join(sorted(atts))}]"
        for asp, atts in sorted(groups.items())
    )


def build_user_prompt(text, category_list, lang="en"):
    """
    Tạo prompt cho inference (dùng cho cả zero-shot và fine-tuned).
    
    Args:
        text: câu đánh giá cần phân tích
        category_list: danh sách category hợp lệ
        lang: ngôn ngữ (en/vi/zh)
    
    Returns:
        string prompt
    """
    cat_block = group_categories(category_list)
    lang_rule = {
        "zh": "Extract entity in Chinese. Do NOT translate.",
        "vi": "Extract entity in Vietnamese. Do NOT translate.",
        "en": ""
    }.get(lang, "")

    return (
        f"Extract ABSA tuples from the review. {lang_rule}\n"
        f"Categories: {cat_block}\n"
        "Return ONLY a JSON array. entity=NULL if not explicitly named.\n\n"
        f'Text: "{text}"\nOutput:'
    )


SYSTEM_PROMPT = (
    "You are an expert in multilingual Aspect-Based Sentiment Analysis. "
    "You ALWAYS return a valid JSON array and nothing else. "
    "No explanation, no markdown, no ```json fences."
)
