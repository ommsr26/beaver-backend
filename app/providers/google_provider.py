from typing import List
from app.schemas.chat_request import Message
from app.config import settings
import httpx

GOOGLE_CHAT_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class GoogleProviderError(Exception):
    pass


async def call_google(
    model: str,
    messages: List[Message],
    temperature: float,
    max_tokens: int,
    client: httpx.AsyncClient
) -> dict:
    if not settings.GOOGLE_API_KEY:
        raise GoogleProviderError("Google API key not configured")
    
    # Convert messages format for Google Gemini API
    contents = []
    system_instruction = None
    
    for msg in messages:
        if msg.role == "system":
            system_instruction = msg.content
        elif msg.role in ["user", "assistant"]:
            contents.append({
                "role": "user" if msg.role == "user" else "model",
                "parts": [{"text": msg.content}]
            })
    
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }
    
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    url = GOOGLE_CHAT_URL.format(model=model)
    params = {"key": settings.GOOGLE_API_KEY}

    try:
        response = await client.post(
            url,
            json=payload,
            params=params
        )
    except httpx.RequestError as e:
        raise GoogleProviderError("Failed to reach Google API") from e

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Google API error")
        except Exception:
            error_msg = response.text

        raise GoogleProviderError(error_msg)

    data = response.json()
    
    # Convert Google response format to OpenAI-like format
    candidates = data.get("candidates", [])
    if candidates and len(candidates) > 0:
        content_parts = candidates[0].get("content", {}).get("parts", [])
        if content_parts and len(content_parts) > 0:
            answer = content_parts[0].get("text", "")
        else:
            answer = ""
    else:
        answer = ""
    
    usage_metadata = data.get("usageMetadata", {})
    
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": answer
            }
        }],
        "usage": {
            "prompt_tokens": usage_metadata.get("promptTokenCount", 0),
            "completion_tokens": usage_metadata.get("candidatesTokenCount", 0),
            "total_tokens": usage_metadata.get("totalTokenCount", 0)
        }
    }

