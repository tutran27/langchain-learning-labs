from shared.config import settings
import json

def beauty_json_output(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

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
