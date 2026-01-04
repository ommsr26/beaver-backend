"""
Model registry - now uses database with dynamic pricing
"""
from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.database.models import Model
from app.core.pricing_engine import PricingEngine


def get_model(model_id: str, db: Session) -> dict:
    """
    Get model from database with pricing information
    
    Args:
        model_id: Model name/ID
        db: Database session
        
    Returns:
        Model configuration dict
    """
    model = db.query(Model).filter(
        Model.name == model_id,
        Model.status == 'active'
    ).first()
    
    if not model:
        raise ValueError(f"Model not found: {model_id}")
    
    # Use Beaver AI prices if available, otherwise use base prices
    input_price = model.beaver_ai_input_price if model.beaver_ai_input_price else model.base_input_price
    output_price = model.beaver_ai_output_price if model.beaver_ai_output_price else model.base_output_price
    
    return {
        "provider": model.provider,
        "active": model.status == "active",
        "category": model.category or "PREMIUM",  # Fallback to PREMIUM if not categorized
        "base_input_price": float(model.base_input_price),
        "base_output_price": float(model.base_output_price),
        "beaver_ai_input_price": float(input_price),
        "beaver_ai_output_price": float(output_price),
        "markup_percent": float(model.markup_percent) if model.markup_percent else None,
        "display_name": model.display_name
    }
