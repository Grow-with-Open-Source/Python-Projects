import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(df):
    # Drop columns that are useless for prediction
    df = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])

    # Fill missing Age with median (more robust than mean)
    df['Age'] = df['Age'].fillna(df['Age'].median())

    # Fill missing Embarked with most common value
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

    # Convert Sex and Embarked from text to numbers
    # Machine learning models only understand numbers, not "male"/"female"
    le = LabelEncoder()
    df['Sex'] = le.fit_transform(df['Sex'])         # male=1, female=0
    df['Embarked'] = le.fit_transform(df['Embarked']) # S=2, C=0, Q=1

    return df

if __name__ == '__main__':
    df = pd.read_csv('data/titanic.csv')
    df = preprocess(df)

    print("Cleaned shape:", df.shape)
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())
    print("\nFirst 5 rows after cleaning:")
    print(df.head())