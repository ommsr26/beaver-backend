from typing import List
from app.schemas.chat_request import Message
from app.config import settings
import httpx

ANTHROPIC_CHAT_URL = "https://api.anthropic.com/v1/messages"


class AnthropicProviderError(Exception):
    pass


async def call_anthropic(
    model: str,
    messages: List[Message],
    temperature: float,
    max_tokens: int,
    client: httpx.AsyncClient
) -> dict:
    if not settings.ANTHROPIC_API_KEY:
        raise AnthropicProviderError("Anthropic API key not configured")
    
    # Convert messages format (Anthropic uses different format)
    # Anthropic doesn't support system messages in the same way, so we'll prepend it to the first user message
    anthropic_messages = []
    system_message = None
    
    for msg in messages:
        if msg.role == "system":
            system_message = msg.content
        elif msg.role in ["user", "assistant"]:
            anthropic_messages.append({
                "role": msg.role,
                "content": msg.content
            })
    
    payload = {
        "model": model,
        "messages": anthropic_messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    if system_message:
        payload["system"] = system_message

    headers = {
        "x-api-key": settings.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    try:
        response = await client.post(
            ANTHROPIC_CHAT_URL,
            json=payload,
            headers=headers
        )
    except httpx.RequestError as e:
        raise AnthropicProviderError("Failed to reach Anthropic API") from e

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Anthropic error")
        except Exception:
            error_msg = response.text

        raise AnthropicProviderError(error_msg)

    data = response.json()
    
    # Convert Anthropic response format to OpenAI-like format
    content = data.get("content", [])
    if content and len(content) > 0:
        answer = content[0].get("text", "")
    else:
        answer = ""
    
    usage = data.get("usage", {})
    
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": answer
            }
        }],
        "usage": {
            "prompt_tokens": usage.get("input_tokens", 0),
            "completion_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
        }
    }

