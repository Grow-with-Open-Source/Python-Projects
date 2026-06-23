# 💳 Credit Card Fraud Detection using DBSCAN Clustering

An unsupervised machine learning approach to detect fraudulent credit 
card transactions using DBSCAN clustering algorithm.

## 🎯 Overview
Implements an unsupervised anomaly detection system for identifying 
potentially fraudulent credit card transactions without labeled data.

## 🚀 Installation
```bash
pip install pandas numpy matplotlib scikit-learn
```

## 💻 Usage
Open `DBSCAN_clustering.ipynb` in Jupyter Notebook or Google Colab 
and run all cells sequentially.

## 📊 Dataset
Works with credit card transaction datasets. Recommended:
[Kaggle Credit Card Fraud Detection Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud)

## 🔬 Methodology
1. Data Preprocessing — handles missing values and standardizes features
2. DBSCAN Clustering — density-based anomaly detection
3. Anomaly Detection — points labeled -1 are potential fraud
4. PCA Visualization — 2D projection of clusters

## 📚 References
- Ester, M., et al. (1996). "A density-based algorithm for discovering clusters"
- Scikit-learn DBSCAN Documentation