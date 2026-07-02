# Titanic Survival Predictor 🚢

A machine learning model that predicts whether a Titanic passenger would have survived, based on features like age, gender, class, and fare.

## Results
| Model | Accuracy |
|---|---|
| Logistic Regression | 81.01% |
| Random Forest | **82.12%** |

## Project Structure
```
titanic-survival-predictor/
├── data/               # Raw dataset
├── explore.py          # Data exploration & visualization
├── preprocess.py       # Data cleaning & feature engineering
├── train.py            # Model training & evaluation
├── predict.py          # Make predictions on new passengers
└── requirements.txt    # Dependencies
```

## Setup
```bash
pip install -r requirements.txt
```
## Dataset
Download `titanic.csv` from [here](https://github.com/datasciencedojo/datasets/blob/master/Titanic.csv) and place it inside the `data/` folder.

## Usage
```bash
python predict.py
```

## What I learned
- Data cleaning and handling missing values
- Feature engineering and label encoding
- Training and comparing ML models
- Evaluating with confusion matrix and classification report