"""
Pipeline inference theo batch cho ABSA.
"""
import torch
from tqdm import tqdm


def batch_inference(texts, langs, domains, category_list, domain_to_cats,
                    model, tokenizer, batch_size=8, max_new_tokens=256):
    """
    Chạy inference ABSA theo batch.
    
    Args:
        texts: list câu cần phân tích
        langs: list ngôn ngữ tương ứng
        domains: list domain tương ứng
        category_list: danh sách tất cả categories
        domain_to_cats: dict mapping domain -> list categories
        model: model đã load
        tokenizer: tokenizer đã load
        batch_size: kích thước batch
        max_new_tokens: số token tối đa sinh ra
    
    Returns:
        list string responses từ model
    """
    from .prompts import SYSTEM_PROMPT, build_user_prompt

    prompts = []
    for text, lang, domain in zip(texts, langs, domains):
        cats = domain_to_cats.get(domain, category_list)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(text, cats, lang)}
        ]
        prompts.append(
            tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        )

    all_responses = []

    for i in tqdm(range(0, len(prompts), batch_size), desc="ABSA Inference"):
        batch = prompts[i: i + batch_size]

        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1536,
        ).to(model.device)

        with torch.no_grad():
            generated = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                use_cache=True,
            )

        new_tokens = [
            out[len(inp):]
            for inp, out in zip(inputs.input_ids, generated)
        ]
        responses = tokenizer.batch_decode(new_tokens, skip_special_tokens=True)
        all_responses.extend(responses)

        del inputs, generated, new_tokens
        torch.cuda.empty_cache()

    return all_responses
