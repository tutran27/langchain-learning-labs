from shared.config import settings
import json
import re

def beauty_json_output(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

def extract_response(text):
    """
    Extract the final structured response from model output.

    This helper is intended for cases where the model may emit extra
    reasoning/thinking text before the actual answer. It first looks for a
    fenced ```json block, then falls back to the last JSON object found in the
    text. If no JSON-like content is found, it returns the stripped raw text.
    """
    fenced_matches = re.findall(r"```json\s*([\s\S]*?)\s*```", text, flags=re.IGNORECASE)
    if fenced_matches:
        return fenced_matches[-1].strip()

    object_matches = re.findall(r"(\{[\s\S]*\})", text)
    if object_matches:
        return object_matches[-1].strip()

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
