from shared.config import settings
import json
import re

def beauty_json_output(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

def _normalize_json_candidate(candidate):
    try:
        parsed = json.loads(candidate)
        return json.dumps(parsed, ensure_ascii=False)
    except json.JSONDecodeError:
        return None

def extract_response(text):
    """
    Extract the final structured response from model output.

    This helper is intended for cases where the model may emit extra
    reasoning/thinking text before the actual answer. It first looks for a
    fenced ```json block, then falls back to the last valid JSON object or
    array found in the text. If no JSON-like content is found, it returns the
    stripped raw text.
    """
    if isinstance(text, (dict, list)):
        return json.dumps(text, ensure_ascii=False)

    if not isinstance(text, str):
        return str(text).strip()

    fenced_matches = re.findall(r"```json\s*([\s\S]*?)\s*```", text, flags=re.IGNORECASE)
    for candidate in reversed(fenced_matches):
        parsed = _normalize_json_candidate(candidate.strip())
        if parsed is not None:
            return parsed

    decoder = json.JSONDecoder()
    valid_candidates = []
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            parsed, end_index = decoder.raw_decode(text[index:])
            normalized = json.dumps(parsed, ensure_ascii=False)
            valid_candidates.append((index + end_index, parsed, normalized))
        except json.JSONDecodeError:
            continue

    for _, parsed, normalized in reversed(valid_candidates):
        if isinstance(parsed, dict):
            return normalized

    if valid_candidates:
        return valid_candidates[-1][2]

    return text.strip()

def _langchain_to_hf_prompt(prompt_messages):
    role_map = {
        "human": "user",
        "ai": "assistant",
    }
    template=[]
    for msg in prompt_messages:
        temp = {
            "role": role_map.get(msg.type, msg.type),
            "content": msg.content,
        }
        template.append(temp)
    return template

def add_tokenize(template, tokenizer):
    tokenized=tokenizer.apply_chat_template(
        template, 
        tokenize=False, 
        add_generation_prompt=True,
        enable_thinking=settings.ENABLE_THINKING,
        )
    return tokenized
