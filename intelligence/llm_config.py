LLM_MODEL = "qwen2.5:7b"

LLM_TEMPERATURE = 0.2
LLM_TIMEOUT = 120

LLM_SYSTEM_PROMPT = (
    "You are a precise financial intelligence assistant. "
    "Follow instructions strictly. "
    "When asked for JSON, respond with valid JSON only. "
    "Do not include explanations unless explicitly requested."
)
