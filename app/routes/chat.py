from fastapi import APIRouter, Depends, HTTPException, Request
import uuid
from sqlalchemy.orm import Session

from app.auth.api_key import verify_api_key
from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import (
    ChatResponse,
    ChatChoice,
    ChatMessage,
    ChatUsage
)
from app.models.registry import get_model
from app.providers.openai_provider import (
    call_openai,
    OpenAIProviderError
)
from app.providers.anthropic_provider import (
    call_anthropic,
    AnthropicProviderError
)
from app.providers.google_provider import (
    call_google,
    GoogleProviderError
)
from app.providers.deepseek_provider import (
    call_deepseek,
    DeepseekProviderError
)
from app.providers.perplexity_provider import (
    call_perplexity,
    PerplexityProviderError
)
from app.providers.xai_provider import (
    call_xai,
    XAIProviderError
)
from app.database.db import SessionLocal
from app.database.models import Transaction, Account
from app.usage.logger import log_usage
from app.core.pricing_engine import PricingEngine

router = APIRouter(prefix="/v1/models")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{model_id}/chat", response_model=ChatResponse)
async def chat(
    model_id: str,
    request: ChatRequest,
    req: Request,
    api_key = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    # 1️⃣ Validate model and get pricing
    try:
        model_config = get_model(model_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    provider = model_config["provider"]
    
    # Initialize pricing engine
    pricing_engine = PricingEngine(db)

    input_tokens = 0
    output_tokens = 0
    answer = ""

    try:
        # 🔹 OpenAI
        if provider == "openai":
            result = await call_openai(
                model=model_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                client=req.app.state.http_client
            )

            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        # 🔹 Anthropic (Claude)
        elif provider == "anthropic":
            result = await call_anthropic(
                model=model_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                client=req.app.state.http_client
            )

            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        # 🔹 Google (Gemini)
        elif provider == "google":
            result = await call_google(
                model=model_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                client=req.app.state.http_client
            )

            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        # 🔹 Deepseek
        elif provider == "deepseek":
            result = await call_deepseek(
                model=model_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                client=req.app.state.http_client
            )

            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        # 🔹 Perplexity
        elif provider == "perplexity":
            result = await call_perplexity(
                model=model_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                client=req.app.state.http_client
            )

            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        # 🔹 XAI (Grok)
        elif provider == "xai":
            result = await call_xai(
                model=model_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                client=req.app.state.http_client
            )

            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        # 🔹 Other providers (fallback)
        else:
            user_message = request.messages[-1].content
            answer = f"(mock {provider} response from {model_id}) You said: {user_message}"
            input_tokens = 20
            output_tokens = 30

    except (OpenAIProviderError, AnthropicProviderError, GoogleProviderError, 
            DeepseekProviderError, PerplexityProviderError, XAIProviderError) as e:
        # 🔥 LOG FAILED REQUEST WITH ZERO COST
        try:
            log_usage(
                db=db,
                api_key_id=api_key.id,
                account_id=api_key.account.id,
                model_id=model_id,
                provider=provider,
                input_tokens=0,
                output_tokens=0,
                total_cost=0.0
            )
        except Exception:
            pass  # logging must never break API

        provider_name = provider.upper()
        raise HTTPException(
            status_code=402,
            detail=f"{provider_name} error: {str(e)}"
        )

    # ============================
    # 💰 PRICING CALCULATION (Dynamic)
    # ============================
    
    # Use Beaver AI prices from database (already includes markup)
    try:
        cost_result = pricing_engine.calculate_cost_for_request(
            model_name=model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        total_cost = cost_result['beaver_ai_cost']['total_cost']
    except Exception as e:
        # Fallback to manual calculation if pricing engine fails
        input_price = model_config.get("beaver_ai_input_price", model_config["base_input_price"])
        output_price = model_config.get("beaver_ai_output_price", model_config["base_output_price"])
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price
        total_cost = round(input_cost + output_cost, 8)

    # ============================
    # 💳 DEDUCT BALANCE
    # ============================
    
    account = api_key.account
    
    # Check if account has sufficient balance (with small buffer for rounding)
    if account.balance < total_cost - 0.0001:
        # Log failed request with zero cost
        try:
            log_usage(
                db=db,
                api_key_id=api_key.id,
                account_id=account.id,
                model_id=model_id,
                provider=provider,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_cost=0.0
            )
        except Exception:
            pass
        
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient balance. Required: ${total_cost:.6f}, Available: ${account.balance:.6f}"
        )
    
    # Deduct balance
    account.balance -= total_cost
    
    # Create transaction record
    transaction = Transaction(
        id=f"txn_{Account.generate_id()}",
        account_id=account.id,
        amount=-total_cost,
        transaction_type="deduction",
        description=f"API usage: {model_id} ({input_tokens} input + {output_tokens} output tokens)"
    )
    db.add(transaction)

    # ============================
    # 📊 LOG USAGE + COST
    # ============================

    try:
        log_usage(
            db=db,
            api_key_id=api_key.id,
            account_id=account.id,
            model_id=model_id,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_cost=total_cost
        )
        db.commit()  # Commit balance deduction and transaction
    except Exception:
        db.rollback()  # Rollback on error
        pass  # never fail response due to logging

    # ============================
    # 📦 RESPONSE
    # ============================

    return ChatResponse(
        id=f"beaver-{uuid.uuid4()}",
        model=model_id,
        choices=[
            ChatChoice(
                message=ChatMessage(
                    role="assistant",
                    content=answer
                )
            )
        ],
        usage=ChatUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
    )
