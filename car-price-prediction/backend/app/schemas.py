from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

# ============================================
# Enums
# ============================================

class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    CNG = "CNG"
    LPG = "LPG"
    ELECTRIC = "Electric"

class TransmissionType(str, Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"

class SellerType(str, Enum):
    INDIVIDUAL = "Individual"
    DEALER = "Dealer"
    TRUSTMARK_DEALER = "Trustmark Dealer"

# ============================================
# Request Schemas
# ============================================

class CarFeatures(BaseModel):
    """Input features for car price prediction"""
    
    brand: str = Field(..., description="Car brand (e.g., Maruti, Hyundai, Toyota)")
    model: str = Field(..., description="Car model (e.g., Alto, i20, Fortuner)")
    vehicle_age: int = Field(..., ge=0, le=30, description="Vehicle age in years")
    km_driven: int = Field(..., ge=0, le=1000000, description="Total kilometers driven")
    fuel_type: FuelType = Field(..., description="Fuel type")
    transmission_type: TransmissionType = Field(..., description="Transmission type")
    mileage: float = Field(..., ge=0, le=50, description="Mileage in km/l")
    engine: int = Field(..., ge=0, le=8000, description="Engine capacity in CC")
    max_power: float = Field(..., ge=0, le=1000, description="Maximum horsepower")
    seats: int = Field(..., ge=1, le=10, description="Number of seats")
    seller_type: SellerType = Field(..., description="Type of seller")
    
    @validator('vehicle_age')
    def validate_age(cls, v):
        if v < 0 or v > 30:
            raise ValueError('Vehicle age must be between 0 and 30 years')
        return v
    
    @validator('km_driven')
    def validate_km(cls, v):
        if v < 0:
            raise ValueError('KM driven cannot be negative')
        if v > 1000000:
            raise ValueError('KM driven seems unrealistic (max 1,000,000)')
        return v
    
    @validator('mileage')
    def validate_mileage(cls, v):
        if v < 0:
            raise ValueError('Mileage cannot be negative')
        if v > 50:
            raise ValueError('Mileage seems unrealistic (max 50 km/l)')
        return v
    
    @validator('engine')
    def validate_engine(cls, v):
        if v < 0:
            raise ValueError('Engine capacity cannot be negative')
        if v > 8000:
            raise ValueError('Engine capacity seems unrealistic (max 8000 CC)')
        return v
    
    @validator('max_power')
    def validate_power(cls, v):
        if v < 0:
            raise ValueError('Maximum power cannot be negative')
        if v > 1000:
            raise ValueError('Maximum power seems unrealistic (max 1000 HP)')
        return v
    
    @validator('seats')
    def validate_seats(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Seats must be between 1 and 10')
        return v

class PredictionRequest(CarFeatures):
    """Extended request with optional asking price"""
    asking_price: Optional[float] = Field(None, description="Seller's asking price for deal analysis")

# ============================================
# Response Schemas
# ============================================

class PriceResponse(BaseModel):
    """Response schema for price prediction"""
    
    predicted_price: float = Field(..., description="Predicted price in rupees")
    predicted_price_lakhs: float = Field(..., description="Predicted price in lakhs")
    price_category: str = Field(..., description="Price category")
    price_range: Dict[str, float] = Field(..., description="Price range with confidence interval")
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 1875000.0,
                "predicted_price_lakhs": 18.75,
                "price_category": "Premium",
                "price_range": {
                    "low": 1687500,
                    "high": 2062500
                },
                "confidence_score": 0.92,
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class DealAnalysisResponse(PriceResponse):
    """Response schema for deal analysis"""
    
    asking_price: Optional[float] = Field(None, description="Seller's asking price")
    price_difference: Optional[float] = Field(None, description="Difference between asking and predicted price")
    deal_status: Optional[str] = Field(None, description="Deal status emoji and text")
    deal_message: Optional[str] = Field(None, description="Detailed deal analysis message")
    savings: Optional[float] = Field(None, description="Potential savings if buying")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 1875000.0,
                "predicted_price_lakhs": 18.75,
                "price_category": "Premium",
                "price_range": {"low": 1687500, "high": 2062500},
                "confidence_score": 0.92,
                "timestamp": "2024-01-15T10:30:00",
                "asking_price": 2050000.0,
                "price_difference": -175000.0,
                "deal_status": "🔴 Overpriced",
                "deal_message": "This car appears to be overpriced by ₹1,75,000. Consider negotiating closer to our estimated price.",
                "savings": 175000.0
            }
        }


# ============================================
# Model Info Schemas
# ============================================

# class FeatureImportanceItem(BaseModel):
#     """Feature importance item for frontend display"""
    
#     feature: str = Field(..., description="Original feature name (not encoded)")
#     importance: float = Field(..., description="Feature importance score (0-1)")
#     category: str = Field(..., description="Feature category: 'base' or 'engineered'")

# class FeatureImportanceResponse(BaseModel):
#     """Feature importance response"""
    
#     feature_importance: List[FeatureImportanceItem]
#     total_features: int
#     top_features: List[FeatureImportanceItem]



class ModelMetricsResponse(BaseModel):
    """Model performance metrics"""
    
    model_name: str
    r2_score: float
    mae: float
    rmse: float
    training_samples: int
    test_samples: int
    features_count: int
    description: str


# ============================================
# Health Check
# ============================================

class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = "OK"
    model_loaded: bool
    api_version: str
    uptime: Optional[float] = None