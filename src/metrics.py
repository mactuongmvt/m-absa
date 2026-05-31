"""
Hàm tính toán metrics đánh giá cho bài toán ABSA.
Sử dụng exact match trên bộ ba (entity, category, sentiment).
"""


def calculate_metrics(true_list, pred_list):
    """
    Tính TP, FP, FN cho một câu dựa trên exact match.
    
    Args:
        true_list: list of dict, mỗi dict có keys: entity, category, sentiment
        pred_list: list of dict, mỗi dict có keys: entity, category, sentiment
    
    Returns:
        tuple (tp, fp, fn)
    """
    true_set = set()
    for t in true_list:
        ent = str(t.get('entity', '')).lower().strip()
        cat = str(t.get('category', '')).lower().strip()
        sent = str(t.get('sentiment', '')).lower().strip()
        if ent or cat or sent:
            true_set.add((ent, cat, sent))

    pred_set = set()
    if isinstance(pred_list, list):
        for p in pred_list:
            if isinstance(p, dict):
                ent = str(p.get('entity', '')).lower().strip()
                cat = str(p.get('category', '')).lower().strip()
                sent = str(p.get('sentiment', '')).lower().strip()
                if ent or cat or sent:
                    pred_set.add((ent, cat, sent))

    tp = len(true_set.intersection(pred_set))
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    return tp, fp, fn


def compute_f1(tp, fp, fn):
    """
    Tính Precision, Recall, F1 từ TP, FP, FN.
    
    Returns:
        tuple (precision, recall, f1)
    """
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1
