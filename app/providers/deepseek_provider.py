from typing import List
from app.schemas.chat_request import Message
from app.config import settings
import httpx

DEEPSEEK_CHAT_URL = "https://api.deepseek.com/v1/chat/completions"


class DeepseekProviderError(Exception):
    pass


async def call_deepseek(
    model: str,
    messages: List[Message],
    temperature: float,
    max_tokens: int,
    client: httpx.AsyncClient
) -> dict:
    # Deepseek uses OpenAI-compatible API
    payload = {
        "model": model,
        "messages": [m.model_dump() for m in messages],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {getattr(settings, 'DEEPSEEK_API_KEY', '')}",
        "Content-Type": "application/json"
    }

    try:
        response = await client.post(
            DEEPSEEK_CHAT_URL,
            json=payload,
            headers=headers
        )
    except httpx.RequestError as e:
        raise DeepseekProviderError("Failed to reach Deepseek API") from e

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Deepseek API error")
        except Exception:
            error_msg = response.text

        raise DeepseekProviderError(error_msg)

    return response.json()

