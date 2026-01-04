"""
Dynamic Percentile-Based Pricing Engine
Implements the pricing strategy from Document 05
"""
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.models import Model

# Category markups (from PDF)
CATEGORY_MARKUP_MAP = {
    "ULTRA_BUDGET": 10.0,    # 10% markup
    "BUDGET": 12.5,          # 12.5% markup
    "MID_RANGE": 15.0,       # 15% markup
    "PREMIUM": 5.5,          # 5.5% markup
    "ULTRA_PREMIUM": 3.5,    # 3.5% markup
}


class PricingEngine:
    """Core pricing calculation engine"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_percentiles(self) -> Dict[str, float]:
        """
        Calculate P20, P40, P60, P80 from all active models
        
        Returns:
            {
                'p20': float,
                'p40': float,
                'p60': float,
                'p80': float,
                'total_models': int
            }
        """
        # Get all active models
        models = self.db.query(Model).filter(
            Model.status == 'active'
        ).all()
        
        if not models:
            raise ValueError("No active models found")
        
        # Calculate total_cost for each model (input + output)
        total_costs = []
        for model in models:
            total_cost = model.base_input_price + model.base_output_price
            total_costs.append(total_cost)
        
        # Sort costs
        total_costs.sort()
        
        # Calculate percentiles using numpy
        percentiles = {
            'p20': float(np.percentile(total_costs, 20)),
            'p40': float(np.percentile(total_costs, 40)),
            'p60': float(np.percentile(total_costs, 60)),
            'p80': float(np.percentile(total_costs, 80)),
            'total_models': len(total_costs)
        }
        
        return percentiles
    
    def assign_category(self, total_cost: float, percentiles: Dict[str, float]) -> str:
        """
        Assign category based on percentile thresholds
        
        Args:
            total_cost: Sum of input + output price
            percentiles: Dict with p20, p40, p60, p80
            
        Returns:
            Category name
        """
        if total_cost <= percentiles['p20']:
            return 'ULTRA_BUDGET'
        elif total_cost <= percentiles['p40']:
            return 'BUDGET'
        elif total_cost <= percentiles['p60']:
            return 'MID_RANGE'
        elif total_cost <= percentiles['p80']:
            return 'PREMIUM'
        else:
            return 'ULTRA_PREMIUM'
    
    def get_markup_for_category(self, category: str) -> float:
        """Get markup percentage for a category"""
        return CATEGORY_MARKUP_MAP.get(category, 5.5)
    
    def assign_categories_to_all_models(self) -> Dict:
        """Assign categories to all active models"""
        # Calculate current percentiles
        percentiles = self.calculate_percentiles()
        
        # Get all active models
        models = self.db.query(Model).filter(
            Model.status == 'active'
        ).all()
        
        # Assign category to each model
        for model in models:
            total_cost = model.base_input_price + model.base_output_price
            category = self.assign_category(total_cost, percentiles)
            
            # Update model
            model.category = category
            model.pricing_updated_at = datetime.utcnow()
        
        # Commit changes
        self.db.commit()
        
        print(f"✅ Assigned categories to {len(models)} models")
        
        return {
            'total_models': len(models),
            'percentiles': percentiles
        }
    
    def calculate_beaver_ai_prices(self) -> Dict:
        """Calculate Beaver AI prices with markup"""
        # Get all active models
        models = self.db.query(Model).filter(
            Model.status == 'active'
        ).all()
        
        for model in models:
            # Get markup for this model's category
            markup_percent = self.get_markup_for_category(model.category)
            
            # Calculate Beaver AI prices
            beaver_ai_input = model.base_input_price * (1 + markup_percent / 100)
            beaver_ai_output = model.base_output_price * (1 + markup_percent / 100)
            
            # Update model
            model.markup_percent = markup_percent
            model.beaver_ai_input_price = round(beaver_ai_input, 6)
            model.beaver_ai_output_price = round(beaver_ai_output, 6)
            model.pricing_updated_at = datetime.utcnow()
        
        # Commit
        self.db.commit()
        
        print(f"✅ Calculated pricing for {len(models)} models")
        
        return {
            'total_models': len(models),
            'updated_at': datetime.utcnow().isoformat()
        }
    
    def recalculate_all_pricing(self) -> Dict:
        """
        Complete pricing recalculation:
        1. Calculate percentiles
        2. Assign categories
        3. Calculate Beaver AI prices
        """
        print("🔄 Starting pricing recalculation...")
        
        # Step 1: Assign categories
        category_result = self.assign_categories_to_all_models()
        
        # Step 2: Calculate prices
        pricing_result = self.calculate_beaver_ai_prices()
        
        print("✅ Pricing recalculation complete!")
        
        return {
            'percentiles': category_result['percentiles'],
            'total_models': category_result['total_models'],
            'updated_at': pricing_result['updated_at']
        }
    
    def get_model_pricing(self, model_name: str) -> Optional[Dict]:
        """Get pricing information for a specific model"""
        model = self.db.query(Model).filter(
            Model.name == model_name,
            Model.status == 'active'
        ).first()
        
        if not model:
            return None
        
        return {
            'name': model.name,
            'display_name': model.display_name,
            'provider': model.provider,
            'category': model.category,
            'base_input_price': float(model.base_input_price),
            'base_output_price': float(model.base_output_price),
            'markup_percent': float(model.markup_percent) if model.markup_percent else None,
            'beaver_ai_input_price': float(model.beaver_ai_input_price) if model.beaver_ai_input_price else None,
            'beaver_ai_output_price': float(model.beaver_ai_output_price) if model.beaver_ai_output_price else None,
        }
    
    def calculate_cost_for_request(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict:
        """
        Calculate cost for a specific request
        
        Returns:
            {
                'model': str,
                'input_tokens': int,
                'output_tokens': int,
                'beaver_ai_cost': {
                    'input_cost': float,
                    'output_cost': float,
                    'total_cost': float
                }
            }
        """
        pricing = self.get_model_pricing(model_name)
        
        if not pricing:
            raise ValueError(f"Model not found: {model_name}")
        
        if not pricing['beaver_ai_input_price'] or not pricing['beaver_ai_output_price']:
            raise ValueError(f"Pricing not calculated for model: {model_name}")
        
        # Calculate costs
        input_cost = (input_tokens / 1_000_000) * pricing['beaver_ai_input_price']
        output_cost = (output_tokens / 1_000_000) * pricing['beaver_ai_output_price']
        total_cost = input_cost + output_cost
        
        return {
            'model': model_name,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'beaver_ai_cost': {
                'input_cost': round(input_cost, 8),
                'output_cost': round(output_cost, 8),
                'total_cost': round(total_cost, 8)
            },
            'pricing': pricing
        }

