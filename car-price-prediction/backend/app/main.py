from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from typing import List, Optional
import json
from datetime import datetime
import uuid

from app.config import API_TITLE, API_VERSION, API_DESCRIPTION, MODEL_METRICS, BRANDS_PATH, BMODELS_PATH
from app.schemas import (
    CarFeatures, PredictionRequest, PriceResponse, DealAnalysisResponse, ModelMetricsResponse, HealthResponse
)
from app.utils import (
    engineer_features, get_price_category, get_deal_status,
    get_price_range, calculate_confidence
)
from app.models import PricePredictor

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
predictor = PricePredictor()


# ============================================
# Load Brands and Models Data
# ============================================

def load_brands() -> dict:
    """Load brands and models from JSON file or create from model"""
    try:
        with open(BRANDS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback: create from training data if available
        # This should be populated from your training data
        return {
            "brands": [
                "Not Found"
            ]
        }
    
brands_data = load_brands()

def load_models(brand:str) -> dict:
    """Load models for a specific brand from JSON file"""
    try:
        with open(BMODELS_PATH, 'r') as f:
            data = json.load(f)
        
    
        if brand in data:
            return {"models": data[brand]}
        

        for key in data.keys():
            if key.lower() == brand.lower():
                return {"models": data[key]}
        

        return {"models": ["Not Found"]}
        
    except FileNotFoundError:
        return {
            "models": ["Not Found"]
        }


# ============================================
# Health Check Endpoint
# ============================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API and model are healthy"""
    return HealthResponse(
        status="OK",
        model_loaded=predictor.is_loaded,
        api_version=API_VERSION
    )

# ============================================
# Brands and Models Endpoints
# ============================================

@app.get("/brands")
async def get_brands():
    """Get all available brands and their models"""
    return brands_data

@app.get("/brands/{brand}/models")
async def get_models_by_brand(brand: str):
    """Get models for a specific brand"""
    models = load_models(brand)
    return models


# ============================================
# Model Metrics Endpoint
# ============================================

@app.get("/model-metrics", response_model=ModelMetricsResponse)
async def get_model_metrics():
    """Get model performance metrics"""
    return ModelMetricsResponse(**MODEL_METRICS)

# ============================================
# Feature Importance Endpoint - but of no use as fetures are one hot encoded
# ============================================

# @app.get("/feature-importance", response_model=FeatureImportanceResponse)
# async def get_feature_importance():
#     """Get feature importance in original feature names"""
#     try:
#         # Get raw importance from model
#         raw_importance = get_feature_importance_mapping()
        
#         # Define mapping for original feature names
#         # This maps engineered/encoded features back to original names
#         feature_mapping = {
#             'brand_model': 'Brand + Model',
#             'max_power': 'Max Power',
#             'vehicle_age': 'Vehicle Age',
#             'brand': 'Brand',
#             'engine': 'Engine Capacity',
#             'km_driven': 'KM Driven',
#             'mileage': 'Mileage',
#             'seats': 'Seats',
#             'fuel_type': 'Fuel Type',
#             'transmission_type': 'Transmission Type',
#             'seller_type': 'Seller Type',
#             'age_squared': 'Age (squared)',
#             'engine_power_interaction': 'Engine × Power',
#             'km_per_year': 'KM per Year'
#         }
        
#         # Process importance
#         feature_importance = []
#         for feat, imp in raw_importance.items():
#             # Try to get original name
#             original_name = feature_mapping.get(feat, feat)
            
#             # Determine category
#             is_engineered = feat in [
#                 'age_squared', 'km_per_year', 'power_per_cc', 
#                 'mileage_per_hp', 'age_km_interaction', 
#                 'engine_power_interaction'
#             ]
#             category = 'engineered' if is_engineered else 'base'
            
#             feature_importance.append({
#                 "feature": original_name,
#                 "importance": imp,
#                 "category": category
#             })
        
#         # Sort by importance
#         feature_importance.sort(key=lambda x: x['importance'], reverse=True)
        
#         # Get top 15
#         top_features = feature_importance[:15]
        
#         return {
#             "feature_importance": feature_importance,
#             "total_features": len(feature_importance),
#             "top_features": top_features
#         }
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to get feature importance: {str(e)}"
#         )

# ============================================
# Prediction Endpoints
# ============================================

@app.post("/predict", response_model=PriceResponse)
async def predict_price(car: CarFeatures):
    """
    Predict the fair market price of a used car.
    """
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([car.model_dump()])
        
        # Engineer features
        input_df_engineered = engineer_features(input_df)
        
        # Get prediction
        prediction = predictor.predict(input_df_engineered)
        
        # Calculate price range and confidence
        price_range = get_price_range(prediction)
        confidence = calculate_confidence(prediction, input_df_engineered)
        
        # Prepare response
        return PriceResponse(
            predicted_price=round(prediction, 2),
            predicted_price_lakhs=round(prediction / 100000, 2),
            price_category=get_price_category(prediction),
            price_range=price_range,
            confidence_score=round(confidence, 2),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prediction failed: {str(e)}"
        )

@app.post("/predict-with-asking", response_model=DealAnalysisResponse)
async def predict_with_asking(car: PredictionRequest):
    """
    Predict price and analyze the deal based on seller's asking price.
    """
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([car.model_dump()])
        
        # Remove asking_price from features if present
        if 'asking_price' in input_df.columns:
            asking_price = input_df['asking_price'].iloc[0]
            input_df = input_df.drop(columns=['asking_price'])
        else:
            asking_price = None
        
        # Engineer features
        input_df_engineered = engineer_features(input_df)
        
        # Get prediction
        prediction = predictor.predict(input_df_engineered)
        
        # Calculate price range and confidence
        price_range = get_price_range(prediction)
        confidence = calculate_confidence(prediction, input_df_engineered)
        
        # Prepare base response
        response = {
            "predicted_price": round(prediction, 2),
            "predicted_price_lakhs": round(prediction / 100000, 2),
            "price_category": get_price_category(prediction),
            "price_range": price_range,
            "confidence_score": round(confidence, 2),
            "timestamp": datetime.now()
        }
        
        # Add deal analysis if asking price provided
        if asking_price is not None:
            deal_status, deal_message, difference = get_deal_status(prediction, asking_price)
            response.update({
                "asking_price": asking_price,
                "price_difference": round(difference, 2),
                "deal_status": deal_status,
                "deal_message": deal_message,
                "savings": round(max(0, difference), 2)
            })
        
        return DealAnalysisResponse(**response)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prediction failed: {str(e)}"
        )


# ============================================
# Model Info Endpoint
# ============================================

@app.get("/model-info")
async def get_model_info():
    """Get information about the model"""
    return {
        "model_type": "XGBoost Regressor",
        "is_loaded": predictor.is_loaded,
        "features_used": {
            "categorical": [
                "brand", "model", "seller_type", "fuel_type", 
                "transmission_type", "engine_category", "brand_group", "brand_model"
            ],
            "numerical": [
                "vehicle_age", "km_driven", "mileage", "engine", "max_power", "seats",
                "age_squared", "km_per_year", "power_per_cc", "mileage_per_hp",
                "age_km_interaction", "engine_power_interaction"
            ]
        },
        "model_metrics": MODEL_METRICS
    }

# ============================================
# Root Endpoint
# ============================================

@app.get("/")
async def root():
    return {
        "name": "CarCast API",
        "version": API_VERSION,
        "description": "Used Car Price Prediction API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "predict": "/predict",
            "predict_with_asking": "/predict-with-asking",
            "brands": "/brands",
            "brand_models": "/brands/{brand}/models",
            "model_metrics": "/model-metrics",
            "model_info": "/model-info"
        }
    }

# ============================================
# Error Handlers
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An unexpected error occurred",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )