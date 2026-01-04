"""
Comprehensive model registry with all LLM models
From OpenAI, Google, Anthropic, Deepseek, Perplexity, and Grok (XAI)
Base prices are per 1M tokens (input/output)
"""
from typing import List, Dict

# All models with their base pricing (as of 2024)
ALL_MODELS: List[Dict] = [
    # ==================== OpenAI Models ====================
    {
        "name": "gpt-4o",
        "display_name": "GPT-4o",
        "provider": "openai",
        "base_input_price": 2.50,
        "base_output_price": 10.00
    },
    {
        "name": "gpt-4o-mini",
        "display_name": "GPT-4o Mini",
        "provider": "openai",
        "base_input_price": 0.15,
        "base_output_price": 0.60
    },
    {
        "name": "gpt-4-turbo",
        "display_name": "GPT-4 Turbo",
        "provider": "openai",
        "base_input_price": 10.00,
        "base_output_price": 30.00
    },
    {
        "name": "gpt-4",
        "display_name": "GPT-4",
        "provider": "openai",
        "base_input_price": 30.00,
        "base_output_price": 60.00
    },
    {
        "name": "gpt-3.5-turbo",
        "display_name": "GPT-3.5 Turbo",
        "provider": "openai",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
    {
        "name": "o1-preview",
        "display_name": "O1 Preview",
        "provider": "openai",
        "base_input_price": 15.00,
        "base_output_price": 60.00
    },
    {
        "name": "o1-mini",
        "display_name": "O1 Mini",
        "provider": "openai",
        "base_input_price": 3.00,
        "base_output_price": 12.00
    },
    
    # ==================== Anthropic Models ====================
    {
        "name": "claude-3-5-sonnet-20241022",
        "display_name": "Claude 3.5 Sonnet",
        "provider": "anthropic",
        "base_input_price": 3.00,
        "base_output_price": 15.00
    },
    {
        "name": "claude-3-5-haiku-20241022",
        "display_name": "Claude 3.5 Haiku",
        "provider": "anthropic",
        "base_input_price": 1.00,
        "base_output_price": 5.00
    },
    {
        "name": "claude-3-opus-20240229",
        "display_name": "Claude 3 Opus",
        "provider": "anthropic",
        "base_input_price": 15.00,
        "base_output_price": 75.00
    },
    {
        "name": "claude-3-sonnet-20240229",
        "display_name": "Claude 3 Sonnet",
        "provider": "anthropic",
        "base_input_price": 3.00,
        "base_output_price": 15.00
    },
    {
        "name": "claude-3-haiku-20240307",
        "display_name": "Claude 3 Haiku",
        "provider": "anthropic",
        "base_input_price": 0.25,
        "base_output_price": 1.25
    },
    
    # ==================== Google Models ====================
    {
        "name": "gemini-1.5-pro",
        "display_name": "Gemini 1.5 Pro",
        "provider": "google",
        "base_input_price": 1.25,
        "base_output_price": 5.00
    },
    {
        "name": "gemini-1.5-flash",
        "display_name": "Gemini 1.5 Flash",
        "provider": "google",
        "base_input_price": 0.075,
        "base_output_price": 0.30
    },
    {
        "name": "gemini-pro",
        "display_name": "Gemini Pro",
        "provider": "google",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
    {
        "name": "gemini-pro-vision",
        "display_name": "Gemini Pro Vision",
        "provider": "google",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
    {
        "name": "gemini-1.0-pro",
        "display_name": "Gemini 1.0 Pro",
        "provider": "google",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
    
    # ==================== Deepseek Models ====================
    {
        "name": "deepseek-chat",
        "display_name": "DeepSeek Chat",
        "provider": "deepseek",
        "base_input_price": 0.14,
        "base_output_price": 0.28
    },
    {
        "name": "deepseek-coder",
        "display_name": "DeepSeek Coder",
        "provider": "deepseek",
        "base_input_price": 0.14,
        "base_output_price": 0.28
    },
    {
        "name": "deepseek-reasoner",
        "display_name": "DeepSeek Reasoner",
        "provider": "deepseek",
        "base_input_price": 0.55,
        "base_output_price": 2.19
    },
    {
        "name": "deepseek-v2",
        "display_name": "DeepSeek V2",
        "provider": "deepseek",
        "base_input_price": 0.14,
        "base_output_price": 0.28
    },
    {
        "name": "deepseek-v2.5",
        "display_name": "DeepSeek V2.5",
        "provider": "deepseek",
        "base_input_price": 0.14,
        "base_output_price": 0.28
    },
    
    # ==================== Perplexity Models ====================
    {
        "name": "llama-3.1-sonar-small-128k-online",
        "display_name": "Llama 3.1 Sonar Small (Online)",
        "provider": "perplexity",
        "base_input_price": 0.20,
        "base_output_price": 0.20
    },
    {
        "name": "llama-3.1-sonar-large-128k-online",
        "display_name": "Llama 3.1 Sonar Large (Online)",
        "provider": "perplexity",
        "base_input_price": 1.00,
        "base_output_price": 1.00
    },
    {
        "name": "llama-3.1-sonar-small-128k-chat",
        "display_name": "Llama 3.1 Sonar Small (Chat)",
        "provider": "perplexity",
        "base_input_price": 0.20,
        "base_output_price": 0.20
    },
    {
        "name": "llama-3.1-sonar-large-128k-chat",
        "display_name": "Llama 3.1 Sonar Large (Chat)",
        "provider": "perplexity",
        "base_input_price": 1.00,
        "base_output_price": 1.00
    },
    {
        "name": "llama-3.1-70b-versatile",
        "display_name": "Llama 3.1 70B Versatile",
        "provider": "perplexity",
        "base_input_price": 0.59,
        "base_output_price": 0.79
    },
    {
        "name": "llama-3.1-8b-instant",
        "display_name": "Llama 3.1 8B Instant",
        "provider": "perplexity",
        "base_input_price": 0.05,
        "base_output_price": 0.05
    },
    
    # ==================== Grok (XAI) Models ====================
    {
        "name": "grok-beta",
        "display_name": "Grok Beta",
        "provider": "xai",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
    {
        "name": "grok-2",
        "display_name": "Grok 2",
        "provider": "xai",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
    {
        "name": "grok-2-vision-beta",
        "display_name": "Grok 2 Vision Beta",
        "provider": "xai",
        "base_input_price": 0.50,
        "base_output_price": 1.50
    },
]

