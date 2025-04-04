import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

# Load trained models
print("Loading trained models...")
scaler = joblib.load("models/scaler.pkl")
pca = joblib.load("models/pca.pkl")
kmeans = joblib.load("models/kmeans.pkl")
nn_model = joblib.load("models/nearest_neighbors.pkl")

# Load the processed dataset
print("Loading processed dataset...")
df = pd.read_csv("models/processed_tracks.csv")

# Select feature columns
audio_features = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 
                  'speechiness', 'acousticness', 'liveness', 'instrumentalness']

features_scaled = df[audio_features].values

# ==============================
# 1. PCA Evaluation
# ==============================
print("\n--- PCA Explained Variance Ratio ---")
explained_variance = pca.explained_variance_ratio_
print("Explained Variance per Component:", explained_variance)
print("Total Explained Variance:", sum(explained_variance))

plt.figure(figsize=(8, 5))
plt.bar(range(1, len(explained_variance) + 1), explained_variance, color='skyblue')
plt.xlabel("Principal Components")
plt.ylabel("Explained Variance Ratio")
plt.title("Variance Explained by PCA Components")
plt.show()

# ==============================
# 2. K-Means Evaluation
# ==============================
print("\n--- K-Means Clustering Evaluation ---")
print("Inertia (Lower is better):", kmeans.inertia_)

labels = kmeans.labels_
silhouette = silhouette_score(features_scaled, labels)
print("Silhouette Score (Closer to 1 is better):", silhouette)

# ==============================
# 3. Nearest Neighbors Evaluation
# ==============================
print("\n--- Evaluating Nearest Neighbors Recommendations ---")
sample_index = 5  # Change index to test different songs
song_features = features_scaled[sample_index].reshape(1, -1)

distances, indices = nn_model.kneighbors(song_features)

# Display original song
print("\nOriginal Song:")
print(df.iloc[sample_index][['track_name', 'artist', 'genres', 'mood', 'activity']])

# Display recommended songs
print("\nRecommended Songs:")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {df.iloc[idx]['track_name']} by {df.iloc[idx]['artist']} - {df.iloc[idx]['genres']} - Mood: {df.iloc[idx]['mood']}")

# ==============================
# 4. Scaler Evaluation
# ==============================
print("\n--- Standard Scaler Evaluation ---")
print("Mean of features:", scaler.mean_)
print("Variance of features:", scaler.var_)