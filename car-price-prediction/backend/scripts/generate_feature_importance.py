import pandas as pd
import numpy as np
import joblib
import json

# Load model
pipeline = joblib.load('../models/full_pipeline.pkl')

# Get feature names from preprocessor
preprocessor = pipeline.named_steps['preprocessor']
feature_names = preprocessor.get_feature_names_out()

# Get feature importances
model = pipeline.named_steps['model']
importances = model.feature_importances_

# Convert float32 to Python float (JSON serializable)
importances = importances.astype(float)

# Create mapping
feature_importance = dict(zip(feature_names, importances))

# Sort by importance (optional)
feature_importance = dict(sorted(feature_importance.items(), 
                                 key=lambda x: x[1], reverse=True))

# Save to JSON with proper serialization
with open('../app/data/feature_importance.json', 'w') as f:
    json.dump(feature_importance, f, indent=2)

print("✅ Feature importance saved successfully!")
print(f"📊 Total features: {len(feature_importance)}")
print(f"🔝 Top 5 features:")
for i, (name, imp) in enumerate(list(feature_importance.items())[:5]):
    print(f"   {i+1}. {name}: {imp:.4f}")