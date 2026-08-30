import os
from pathlib import Path
from typing import List, Dict

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model paths
MODEL_PATH = BASE_DIR / "models" / "full_pipeline.pkl"

# Data paths
DATA_DIR = BASE_DIR / "app" / "data"
BRANDS_PATH = DATA_DIR / "brands.json"
BMODELS_PATH = DATA_DIR / "models.json"
FEATURE_IMPORTANCE_PATH = DATA_DIR / "feature_importance.json"

# Luxury brands list
LUXURY_BRANDS = [
    'Mercedes-Benz', 'BMW', 'Audi', 'Land Rover',
    'Jaguar', 'Porsche', 'Lexus', 'Volvo', 'Mini',
    'Mercedes-AMG', 'Maserati', 'Bentley', 'Rolls-Royce',
    'Ferrari', 'Lamborghini', 'Mclaren', 'Aston Martin'
]

# Engine category bins
ENGINE_BINS = [0, 1500, 2500, 3500, 6000]
ENGINE_LABELS = ['Small', 'Mid', 'Large', 'Luxury']

# API settings
API_TITLE = "CarCast - Used Car Price Prediction API"
API_VERSION = "2.0.0"
API_DESCRIPTION = """
## CarCast API

A comprehensive API for used car price prediction with advanced features.

### Features:
- **Car Price Prediction**: Predict fair market price
- **Deal Analysis**: Compare predicted vs asking price
- **Model Metrics**: View model performance
- **Feature Importance**: Understand what drives prices
- **Brand/Model Data**: Get available brands and models
- **Prediction History**: Track past predictions
"""

# Model performance metrics (from your training)
MODEL_METRICS = {
    "model_name": "XGBoost Regressor",
    "r2_score": 0.9459,
    "mae": 97149.24,
    "rmse": 201768.88,
    "training_samples": 12328,
    "test_samples": 3083,
    "features_count": 295,
    "description": "XGBoost model trained on 15,240 used car listings with 11 base features and 9 engineered features"
}