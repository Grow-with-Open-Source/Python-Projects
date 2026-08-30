import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from app.config import LUXURY_BRANDS, ENGINE_BINS, ENGINE_LABELS, MODEL_METRICS

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engineered features to the input dataframe.
    This must match the feature engineering done during training.
    """
    df = df.copy()
    
    # 1. Age squared (non-linear depreciation)
    df['age_squared'] = df['vehicle_age'] ** 2
    
    # 2. KM per year (usage intensity)
    df['km_per_year'] = df['km_driven'] / (df['vehicle_age'] + 1)
    
    # 3. Power per CC (engine efficiency)
    df['power_per_cc'] = df['max_power'] / (df['engine'] + 1)
    
    # 4. Mileage per HP (fuel efficiency context)
    df['mileage_per_hp'] = df['mileage'] / (df['max_power'] + 1)
    
    # 5. Age-KM interaction
    df['age_km_interaction'] = df['vehicle_age'] * df['km_driven']
    
    # 6. Engine-Power interaction
    df['engine_power_interaction'] = df['engine'] * df['max_power']
    
    # 7. Engine category (categorical)
    df['engine_category'] = pd.cut(
        df['engine'],
        bins=ENGINE_BINS,
        labels=ENGINE_LABELS,
        right=False
    )
    
    # 8. Brand group (categorical)
    df['brand_group'] = df['brand'].apply(
        lambda x: 'Luxury' if x in LUXURY_BRANDS else 'Mass Market'
    )
    
    # 9. Brand-Model combination (categorical)
    df['brand_model'] = df['brand'] + '_' + df['model']
    
    return df

def get_price_category(price: float) -> str:
    """Categorize price into meaningful ranges"""
    if price < 300000:
        return "Budget"
    elif price < 800000:
        return "Entry"
    elif price < 1500000:
        return "Mid-Range"
    elif price < 3000000:
        return "Premium"
    elif price < 5000000:
        return "Luxury"
    else:
        return "Ultra-Luxury"

def get_deal_status(predicted_price: float, asking_price: float) -> Tuple[str, str, float]:
    """
    Analyze the deal and return status, message, and difference
    """
    difference = asking_price - predicted_price
    diff_percentage = (difference / predicted_price) * 100
    
    if diff_percentage < -10:
        return (
            "🟢 Excellent Deal!",
            f"This car is priced ₹{abs(difference):,} below market value. Great opportunity!",
            difference
        )
    elif diff_percentage < -5:
        return (
            "🟢 Good Deal",
            f"This car is ₹{abs(difference):,} below market value. Fair price.",
            difference
        )
    elif diff_percentage < 5:
        return (
            "🟡 Fair Price",
            f"This car is priced close to market value (±₹{abs(difference):,}).",
            difference
        )
    elif diff_percentage < 10:
        return (
            "🟡 Slightly Overpriced",
            f"This car is ₹{difference:,} above market value. Consider negotiating.",
            difference
        )
    else:
        return (
            "🔴 Overpriced",
            f"This car appears overpriced by ₹{difference:,}. Negotiate closer to our estimate.",
            difference
        )

def get_price_range(prediction: float, mae: float = 97149) -> Dict[str, float]:
    """Calculate price range with confidence interval"""
    return {
        "low": max(0, prediction - (mae * 0.7)),
        "high": prediction + (mae * 0.7)
    }

def calculate_confidence(prediction: float, features: pd.DataFrame) -> float:
    """
    Calculate confidence score based on feature completeness and model certainty
    """
    # Base confidence
    confidence = 0.90
    
    # Adjust based on feature completeness
    missing_count = features.isnull().sum().sum()
    if missing_count > 0:
        confidence -= 0.05 * missing_count
    
    # Adjust based on price range
    if prediction > 3000000:  # Luxury cars have higher uncertainty
        confidence -= 0.05
    elif prediction > 5000000:
        confidence -= 0.10
    
    # Ensure confidence is within bounds
    return max(0.70, min(0.98, confidence))

def format_price(price: float) -> str:
    """Format price in Indian currency format"""
    return f"₹{price:,.0f}"

# def get_feature_importance_mapping() -> Dict[str, float]:
#     """
#     Get feature importance mapping from trained model.
#     This should match the features from your trained model.
#     """
#     # These values should be extracted from your trained XGBoost model
#     return {
#         "brand_model": 0.25,
#         "max_power": 0.18,
#         "vehicle_age": 0.12,
#         "brand": 0.10,
#         "engine": 0.08,
#         "km_driven": 0.07,
#         "mileage": 0.05,
#         "seats": 0.04,
#         "fuel_type": 0.03,
#         "transmission_type": 0.02,
#         "seller_type": 0.02,
#         "age_squared": 0.02,
#         "engine_power_interaction": 0.01,
#         "km_per_year": 0.01
#     }