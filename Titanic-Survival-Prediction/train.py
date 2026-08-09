import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from preprocess import preprocess

# Load and preprocess
df = pd.read_csv('data/titanic.csv')
df = preprocess(df)

# Split features and target
X = df.drop(columns=['Survived'])  # everything except what we're predicting
y = df['Survived']                 # what we're predicting

# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Model 1: Logistic Regression ---
lr = LogisticRegression(max_iter=200)
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
lr_acc = accuracy_score(y_test, lr_preds)

# --- Model 2: Random Forest ---
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_preds)

# --- Compare ---
print(f"Logistic Regression Accuracy: {lr_acc:.2%}")
print(f"Random Forest Accuracy:       {rf_acc:.2%}")

# Pick the better model
best_model = rf if rf_acc >= lr_acc else lr
best_name = "Random Forest" if rf_acc >= lr_acc else "Logistic Regression"
print(f"\nBest model: {best_name}")

# --- Detailed report for best model ---
best_preds = rf_preds if rf_acc >= lr_acc else lr_preds
print("\nClassification Report:")
print(classification_report(y_test, best_preds))
print("Confusion Matrix:")
print(confusion_matrix(y_test, best_preds))

# --- Save the best model ---
os.makedirs('models', exist_ok=True)
joblib.dump(best_model, 'models/titanic_model.pkl')
print("\nModel saved to models/titanic_model.pkl")