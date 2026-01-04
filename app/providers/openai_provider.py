from typing import List
from app.schemas.chat_request import Message
from app.config import settings
import httpx

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"

class OpenAIProviderError(Exception):
    pass

async def call_openai(
    model: str,
    messages: List[Message],
    temperature: float,
    max_tokens: int,
    client: httpx.AsyncClient
) -> dict:
    payload = {
        "model": model,
        "messages": [m.model_dump() for m in messages],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = await client.post(
            OPENAI_CHAT_URL,
            json=payload,
            headers=headers
        )
    except httpx.RequestError as e:
        raise OpenAIProviderError("Failed to reach OpenAI") from e

    if response.status_code != 200:
        # Forward OpenAI's error message safely
        try:
            error_msg = response.json().get("error", {}).get("message", "OpenAI error")
        except Exception:
            error_msg = response.text

        raise OpenAIProviderError(error_msg)

    return response.json()
