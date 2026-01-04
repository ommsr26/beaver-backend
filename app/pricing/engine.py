from typing import Dict

# Pricing categories & markups (percent)
CATEGORY_MARKUP: Dict[str, float] = {
    "ULTRA_BUDGET": 10.0,
    "BUDGET": 12.5,
    "MID_RANGE": 15.0,
    "PREMIUM": 5.5,
    "ULTRA_PREMIUM": 3.5
}


def apply_markup(base_price: float, markup_percent: float) -> float:
    """
    Apply markup percentage to a base price.
    """
    return round(base_price * (1 + markup_percent / 100), 6)


def calculate_request_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_1m: float,
    output_price_per_1m: float
) -> float:
    """
    Calculate total cost for a request.
    Prices are per 1M tokens.
    """
    input_cost = (input_tokens / 1_000_000) * input_price_per_1m
    output_cost = (output_tokens / 1_000_000) * output_price_per_1m
    return round(input_cost + output_cost, 8)
