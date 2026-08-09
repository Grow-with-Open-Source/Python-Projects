import pandas as pd
import joblib

# Load the saved model
model = joblib.load('models/titanic_model.pkl')

# Example passenger (you can change these values)
passenger = pd.DataFrame([{
    'Pclass':   3,      # 1=First, 2=Second, 3=Third class
    'Sex':      1,      # 1=Male, 0=Female
    'Age':      22,
    'SibSp':    1,      # siblings/spouses aboard
    'Parch':    0,      # parents/children aboard
    'Fare':     7.25,
    'Embarked': 2       # 0=Cherbourg, 1=Queenstown, 2=Southampton
}])

result = model.predict(passenger)[0]
probability = model.predict_proba(passenger)[0]

print(f"Prediction: {'Survived' if result == 1 else 'Did not survive'}")
print(f"Survival probability:  {probability[1]:.2%}")
print(f"Death probability:     {probability[0]:.2%}")