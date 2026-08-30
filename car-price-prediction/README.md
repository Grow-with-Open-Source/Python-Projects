 # CarCast - Used Car Price Prediction

CarCast is an end-to-end data science + web application project that estimates the fair market price of used cars in India using machine learning.

This project starts from real listing data (sourced from CarDekho), goes through data understanding, cleaning, preprocessing, model training, feature engineering, model re-training, and finally serves predictions through a FastAPI backend with a React frontend.

## What this project does

- Predicts used car selling price from core vehicle attributes.
- Provides deal analysis by comparing predicted value vs asking price.
- Exposes a clean API for prediction and model metadata.
- Delivers a user-facing web app where anyone can enter car details and get an instant estimate.

## Data snapshot

- Source dataset: `cardekho_dataset.csv` (CarDekho listings)
- Total raw records: **15,411**
- Raw columns: **14**
- Cleaned dataset: **15,411 x 13**
- Feature-engineered dataset: **15,411 x 22**
- Train/Test split (enhanced processed): **12,328 / 3,083**

## ML journey in short

1. Collected and explored used-car listing data.
2. Cleaned and preprocessed data.
3. Trained multiple baseline regressors.
4. Performed feature engineering to better capture depreciation, usage intensity, and brand/engine interactions.
5. Repeated preprocessing and model selection on enhanced data.
6. Selected **XGBoost Regressor** as final model and saved the full prediction pipeline.

## Final selected model

**Model:** XGBoost Regressor  
**R2:** 0.9459  
**MAE:** 97,149.24  
**RMSE:** 201,768.88

The final model performance report is available in [model_performance_enhanced.csv](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/reports/model_performance_enhanced.csv).

## Tech stack

- **Data Science:** Python, Pandas, NumPy, scikit-learn, XGBoost, Matplotlib, Seaborn, Jupyter
- **Backend/API:** FastAPI, Pydantic, Uvicorn, Joblib
- **Frontend:** React, TypeScript, TanStack Router, TanStack Query, Tailwind CSS

## Important project resources

- Data files: [backend/data/](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/data)
- Notebooks (full DS workflow): [backend/notebooks/](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/notebooks)
- Saved model pipelines: [backend/models/](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/models)
- Full DS write-up: [documentation.md](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/documentation.md)

## Scope note

This is a strong portfolio data science project focused on model development and practical deployment. It is not positioned as a production-grade automotive pricing platform.
