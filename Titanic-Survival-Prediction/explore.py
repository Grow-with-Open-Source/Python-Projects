import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('data/titanic.csv')

# --- Basic overview ---
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn info:")
print(df.info())
print("\nMissing values:")
print(df.isnull().sum())

# --- Survival rate by key features ---
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

sns.barplot(x='Sex', y='Survived', data=df, ax=axes[0])
axes[0].set_title('Survival by Sex')

sns.barplot(x='Pclass', y='Survived', data=df, ax=axes[1])
axes[1].set_title('Survival by Passenger Class')

sns.histplot(data=df, x='Age', hue='Survived', bins=30, ax=axes[2])
axes[2].set_title('Survival by Age')

plt.tight_layout()
plt.savefig('exploration.png')
plt.show()
print("\nChart saved as exploration.png")