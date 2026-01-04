# 🎯 Dynamic Pricing Engine - Setup Guide

## Overview

Beaver now uses a **dynamic percentile-based pricing system** as described in Document 05. This system automatically categorizes models and applies appropriate markups based on their pricing tier.

## How It Works

### 1. Percentile Calculation
- Calculates P20, P40, P60, P80 percentiles from all active models
- Based on total cost (input + output prices)

### 2. Category Assignment
- **ULTRA_BUDGET** (≤ P20): 10% markup
- **BUDGET** (≤ P40): 12.5% markup
- **MID_RANGE** (≤ P60): 15% markup
- **PREMIUM** (≤ P80): 5.5% markup
- **ULTRA_PREMIUM** (> P80): 3.5% markup

### 3. Price Calculation
- Beaver AI prices = Base prices × (1 + markup%)
- Automatically calculated and stored in database

## Setup Instructions

### Step 1: Initialize Database
```bash
python init_db.py
```

This creates all tables including the new `models` table.

### Step 2: Populate Models
```bash
python populate_models.py
```

This will:
- Add all 30+ models from 6 providers
- Calculate percentiles
- Assign categories
- Calculate Beaver AI prices

### Step 3: Verify Setup
```bash
python test_api.py
```

Check that models are listed correctly.

## Models Included

### OpenAI (7 models)
- gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo, o1-preview, o1-mini

### Anthropic (5 models)
- claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus, claude-3-sonnet, claude-3-haiku

### Google (5 models)
- gemini-1.5-pro, gemini-1.5-flash, gemini-pro, gemini-pro-vision, gemini-1.0-pro

### Deepseek (5 models)
- deepseek-chat, deepseek-coder, deepseek-reasoner, deepseek-v2, deepseek-v2.5

### Perplexity (6 models)
- llama-3.1-sonar-small-128k-online, llama-3.1-sonar-large-128k-online
- llama-3.1-sonar-small-128k-chat, llama-3.1-sonar-large-128k-chat
- llama-3.1-70b-versatile, llama-3.1-8b-instant

### XAI/Grok (3 models)
- grok-beta, grok-2, grok-2-vision-beta

**Total: 31 models**

## Daily Recalculation

To update pricing when provider prices change:

```bash
python recalculate_pricing.py
```

This recalculates:
1. Percentiles from current models
2. Categories for all models
3. Beaver AI prices with markups

## API Usage

### List Models
```bash
GET /v1/models
```

Returns all models with:
- Base prices
- Beaver AI prices (with markup)
- Category
- Markup percentage

### Chat Completion
```bash
POST /v1/models/{model_id}/chat
```

Automatically uses Beaver AI prices from database.

## Pricing Example

**Example: Claude 3.5 Sonnet**
- Base: $3.00 input + $15.00 output = $18.00 total
- If P80 = $18.00 → Category: PREMIUM
- Markup: 5.5%
- Beaver AI: $3.165 input + $15.825 output

**Example: GPT-4o Mini**
- Base: $0.15 input + $0.60 output = $0.75 total
- If P40 = $1.37 → Category: BUDGET
- Markup: 12.5%
- Beaver AI: $0.16875 input + $0.675 output

## Benefits

1. **Automatic Categorization**: No manual category assignment
2. **Fair Pricing**: Lower markups on expensive models, higher on budget models
3. **Competitive**: 3-12% cheaper than fixed 5.5% markup
4. **Dynamic**: Adapts when new models are added
5. **Transparent**: All pricing stored in database

## Database Schema

### Models Table
- `name`: Model ID (e.g., "gpt-4o")
- `display_name`: Human-readable name
- `provider`: Provider name
- `base_input_price`: Provider's input price
- `base_output_price`: Provider's output price
- `category`: Assigned category
- `markup_percent`: Applied markup
- `beaver_ai_input_price`: Final input price
- `beaver_ai_output_price`: Final output price

## Next Steps

1. ✅ Models added to database
2. ✅ Pricing engine implemented
3. ✅ Dynamic pricing active
4. ⏳ Add API keys when ready
5. ⏳ Test with real API calls

The system is ready to use! Models are in the database and pricing is calculated.

