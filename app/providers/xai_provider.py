from typing import List
from app.schemas.chat_request import Message
from app.config import settings
import httpx

XAI_CHAT_URL = "https://api.x.ai/v1/chat/completions"


class XAIProviderError(Exception):
    pass


async def call_xai(
    model: str,
    messages: List[Message],
    temperature: float,
    max_tokens: int,
    client: httpx.AsyncClient
) -> dict:
    # XAI (Grok) uses OpenAI-compatible API
    payload = {
        "model": model,
        "messages": [m.model_dump() for m in messages],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {getattr(settings, 'XAI_API_KEY', '')}",
        "Content-Type": "application/json"
    }

    try:
        response = await client.post(
            XAI_CHAT_URL,
            json=payload,
            headers=headers
        )
    except httpx.RequestError as e:
        raise XAIProviderError("Failed to reach XAI API") from e

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "XAI API error")
        except Exception:
            error_msg = response.text

        raise XAIProviderError(error_msg)

    return response.json()

