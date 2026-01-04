"""
Recalculate pricing for all models
Run this daily to update pricing based on current model base prices
"""
from app.database.db import SessionLocal
from app.core.pricing_engine import PricingEngine

def recalculate_pricing():
    """Recalculate all model pricing"""
    db = SessionLocal()
    
    try:
        print("🔄 Recalculating pricing for all models...")
        engine = PricingEngine(db)
        result = engine.recalculate_all_pricing()
        
        print(f"\n✅ Pricing recalculation complete!")
        print(f"\n📊 Summary:")
        print(f"   Total models: {result['total_models']}")
        print(f"   Percentiles:")
        print(f"     P20: ${result['percentiles']['p20']:.2f}")
        print(f"     P40: ${result['percentiles']['p40']:.2f}")
        print(f"     P60: ${result['percentiles']['p60']:.2f}")
        print(f"     P80: ${result['percentiles']['p80']:.2f}")
        print(f"   Updated at: {result['updated_at']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    recalculate_pricing()

