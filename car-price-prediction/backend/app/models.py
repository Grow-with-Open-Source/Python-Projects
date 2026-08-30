import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any
from app.config import MODEL_PATH

class PricePredictor:
    """Singleton class for loading and using the prediction model"""
    
    _instance = None
    _pipeline = None
    _model = None
    _preprocessor = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PricePredictor, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load the trained pipeline"""
        try:
            self._pipeline = joblib.load(MODEL_PATH)
            print("✅ Model loaded successfully!")
            
            # Extract components for potential individual use
            if hasattr(self._pipeline, 'named_steps'):
                self._model = self._pipeline.named_steps.get('model')
                self._preprocessor = self._pipeline.named_steps.get('preprocessor')
                
        except FileNotFoundError:
            print(f"❌ Model not found at {MODEL_PATH}")
            raise
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def predict(self, features: pd.DataFrame) -> float:
        """Make a prediction"""
        if self._pipeline is None:
            raise ValueError("Model not loaded")
        
        # Make prediction
        prediction = self._pipeline.predict(features)[0]
        
        # Ensure prediction is not negative
        return max(0, prediction)
    
    # def get_feature_importance(self) -> Dict[str, float]:
    #     """Get feature importance from the model"""
    #     if self._model is None or not hasattr(self._model, 'feature_importances_'):
    #         return {}
        
    #     # Get feature names from preprocessor
    #     if self._preprocessor is None:
    #         return {}
        
    #     # Get all feature names
    #     feature_names = self._preprocessor.get_feature_names_out()
        
    #     # Get importances
    #     importances = self._model.feature_importances_
        
    #     # Create mapping
    #     return dict(zip(feature_names, importances))
    
    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None