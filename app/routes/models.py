from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database.models import Model

router = APIRouter(prefix="/v1")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/models")
async def list_models(db: Session = Depends(get_db)):
    """List all available models with dynamic pricing"""
    models = db.query(Model).filter(Model.status == 'active').all()
    
    model_list = []
    for model in models:
        # Use Beaver AI prices if available, otherwise base prices
        input_price = model.beaver_ai_input_price if model.beaver_ai_input_price else model.base_input_price
        output_price = model.beaver_ai_output_price if model.beaver_ai_output_price else model.base_output_price
        
        model_list.append({
            "id": model.name,
            "display_name": model.display_name,
            "provider": model.provider,
            "category": model.category or "PREMIUM",
            "pricing": {
                "base_input_price_per_1m": float(model.base_input_price),
                "base_output_price_per_1m": float(model.base_output_price),
                "beaver_ai_input_price_per_1m": float(input_price),
                "beaver_ai_output_price_per_1m": float(output_price),
                "markup_percent": float(model.markup_percent) if model.markup_percent else None
            }
        })
    
    return {
        "models": model_list,
        "total": len(model_list)
    }

