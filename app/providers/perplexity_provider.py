from typing import List
from app.schemas.chat_request import Message
from app.config import settings
import httpx

PERPLEXITY_CHAT_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityProviderError(Exception):
    pass


async def call_perplexity(
    model: str,
    messages: List[Message],
    temperature: float,
    max_tokens: int,
    client: httpx.AsyncClient
) -> dict:
    # Perplexity uses OpenAI-compatible API
    payload = {
        "model": model,
        "messages": [m.model_dump() for m in messages],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {getattr(settings, 'PERPLEXITY_API_KEY', '')}",
        "Content-Type": "application/json"
    }

    try:
        response = await client.post(
            PERPLEXITY_CHAT_URL,
            json=payload,
            headers=headers
        )
    except httpx.RequestError as e:
        raise PerplexityProviderError("Failed to reach Perplexity API") from e

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Perplexity API error")
        except Exception:
            error_msg = response.text

        raise PerplexityProviderError(error_msg)

    return response.json()

