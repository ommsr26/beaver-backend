"""
Populate database with all LLM models and calculate dynamic pricing
Run this after init_db.py to set up all models with pricing
"""
from app.database.db import SessionLocal, engine, Base
from app.database.models import Model
from app.models.all_models import ALL_MODELS
from app.core.pricing_engine import PricingEngine
from datetime import datetime

def populate_models():
    """Add all models to database"""
    db = SessionLocal()
    
    try:
        print("📦 Adding models to database...")
        
        added_count = 0
        skipped_count = 0
        
        for model_data in ALL_MODELS:
            # Check if model already exists
            existing = db.query(Model).filter(Model.name == model_data["name"]).first()
            
            if existing:
                print(f"⏭️  Skipping {model_data['name']} (already exists)")
                skipped_count += 1
                continue
            
            # Create new model
            model = Model(
                id=Model.generate_id(),
                name=model_data["name"],
                display_name=model_data["display_name"],
                provider=model_data["provider"],
                base_input_price=model_data["base_input_price"],
                base_output_price=model_data["base_output_price"],
                status="active"
            )
            
            db.add(model)
            added_count += 1
            print(f"✅ Added {model_data['display_name']} ({model_data['provider']})")
        
        db.commit()
        print(f"\n✅ Added {added_count} new models")
        print(f"⏭️  Skipped {skipped_count} existing models")
        
        # Now calculate pricing
        print("\n💰 Calculating dynamic pricing...")
        engine = PricingEngine(db)
        result = engine.recalculate_all_pricing()
        
        print(f"\n📊 Pricing Summary:")
        print(f"   Total models: {result['total_models']}")
        print(f"   Percentiles:")
        print(f"     P20: ${result['percentiles']['p20']:.2f}")
        print(f"     P40: ${result['percentiles']['p40']:.2f}")
        print(f"     P60: ${result['percentiles']['p60']:.2f}")
        print(f"     P80: ${result['percentiles']['p80']:.2f}")
        print(f"   Updated at: {result['updated_at']}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    # Populate models
    populate_models()
    
    print("\n🎉 Model population complete!")

